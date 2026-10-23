#!/usr/bin/env python3
"""Sync Xbox game backups (XISO files or extracted folders) into a Berth raw
HDD image, as <partition>:\\Games\\<Title>\\ for the UIX Lite launcher.

Only bytes inside the target FATX volume are written. Everything outside the
volume (including the account sectors in the first 512 KiB) is hashed before
and after and must stay byte-identical. Refuses while any process has the image
open (Berth keeps its HDD image open while it runs). Idempotent: titles whose installed file
tree matches the source are skipped.

Needs pyfatx (mborgerson/fatx, GPL-2.0) and extract-xiso (XboxDev, BSD-style).
"""
import argparse, hashlib, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

PARTS = {'x': (0x00080000, 0x2ee00000), 'y': (0x2ee80000, 0x2ee00000),
         'z': (0x5dc80000, 0x2ee00000), 'c': (0x8ca80000, 0x1f400000),
         'e': (0xabe80000, 0x1312d6000)}
CHUNK = 4 << 20
RCHUNK = 64 << 20


def die(msg):
    print('sync-xbox-roms: ' + msg, file=sys.stderr)
    sys.exit(1)


def running_berth(image):
    real = os.path.realpath(image)
    for p in Path('/proc').iterdir():
        if not p.name.isdigit() or int(p.name) == os.getpid():
            continue
        try:
            comm = (p / 'comm').read_text().strip()
            for fd in (p / 'fd').iterdir():
                if os.path.realpath(fd) == real:
                    return f'pid {p.name} ({comm}) has the image open'
        except OSError:
            pass
    return None


def outside_hash(image, off, size):
    h = hashlib.sha256()
    with open(image, 'rb') as f:
        pos, end = 0, os.path.getsize(image)
        for a, b in ((0, off), (off + size, end)):
            f.seek(a)
            left = b - a
            while left > 0:
                d = f.read(min(CHUNK, left))
                if not d:
                    break
                h.update(d)
                left -= len(d)
    return h.hexdigest()


def title_of(name):
    t = re.sub(r'\s*[\(\[].*$', '', name).strip() or name
    t = re.sub(r'[^A-Za-z0-9 ._+&!\-]', '', t).strip()[:42]
    if not t:
        die(f'cannot derive a FATX title from {name!r}')
    return t


def local_tree(root):
    out = {}
    for p in sorted(root.rglob('*')):
        out[p.relative_to(root).as_posix()] = (-1 if p.is_dir() else p.stat().st_size)
    return out


def fatx_tree(fs, base):
    out = {}
    def rec(path, rel):
        for a in fs.listdir(path):
            r = f'{rel}/{a.filename}' if rel else a.filename
            if a.is_directory:
                out[r] = -1
                rec(f'{path}/{a.filename}', r)
            else:
                out[r] = a.file_size
    rec(base, '')
    return out


def rmtree(fs, path):
    for a in list(fs.listdir(path)):
        p = f'{path}/{a.filename}'
        rmtree(fs, p) if a.is_directory else fs.unlink(p)
    fs.rmdir(path)


def install(fs, src, dest):
    fs.mkdir(dest)
    for p in sorted(src.rglob('*'), key=lambda x: (len(x.parts), str(x))):
        t = f"{dest}/{p.relative_to(src).as_posix()}"
        if p.is_dir():
            fs.mkdir(t)
            continue
        with open(p, 'rb') as f:
            off = 0
            first = True
            while True:
                d = f.read(CHUNK)
                if not d and not first:
                    break
                try:
                    fs.write(t, d, offset=off)
                except AssertionError:
                    die(f'FATX write failed at {t} offset {off} (volume full or bad name?)')
                off += len(d)
                first = False
                if not d:
                    break


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(fs, tree_root, dest, want, full, title):
    files = [r for r, s in want.items() if s >= 0] if full else ['Default.xbe', 'default.xbe']
    for r in files:
        lp = tree_root / r
        if lp.is_file():
            h = hashlib.sha256()
            with open(lp, 'rb') as f:
                while (d := f.read(CHUNK)):
                    h.update(d)
            g = hashlib.sha256()
            o = 0
            sz = want[r]
            while o < sz:
                n = min(RCHUNK, sz - o)
                # pyfatx returns a buffer of the whole file size; data is at the front
                d = bytes(fs.read(f'{dest}/{r}', offset=o, size=n))[:n]
                g.update(d); o += len(d)
            if g.digest() != h.digest():
                die(f'[{title}] hash mismatch on {r}')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--roms', required=True, help='folder with *.iso and/or extracted game folders')
    ap.add_argument('--image', required=True, help='Berth raw HDD image')
    ap.add_argument('--partition', default='e', choices=sorted(PARTS))
    ap.add_argument('--games-dir', default='Games')
    ap.add_argument('--extract-xiso', default=os.environ.get('EXTRACT_XISO', 'extract-xiso'))
    ap.add_argument('--no-backup', action='store_true')
    ap.add_argument('--verify', action='store_true', help='hash-compare every file after install')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    try:
        from pyfatx import Fatx
    except ImportError:
        die('pyfatx not importable (pip install pyfatx, or use the venv python)')
    tmp = os.environ.get('TMPDIR', '')
    if not tmp or tmp.startswith('/tmp'):
        die('set TMPDIR to a scratch folder with room for one extracted game (not /tmp)')
    image = Path(a.image)
    if not image.is_file():
        die(f'no such image: {image}')
    why = running_berth(image)
    if why:
        die(f'refusing: {why}. Close Berth first.')
    off, size = PARTS[a.partition]
    if image.stat().st_size < off + size:
        die('image too small for that partition')

    roms = Path(a.roms)
    items = [(title_of(p.stem), p) for p in sorted(roms.glob('*.iso')) + sorted(roms.glob('*.ISO'))]
    items += [(title_of(p.name), p) for p in sorted(roms.iterdir())
              if p.is_dir() and any(c.name.lower() == 'default.xbe' for c in p.iterdir())]
    if not items:
        die(f'no *.iso or game folders in {roms}')
    names = [t for t, _ in items]
    if len(set(n.lower() for n in names)) != len(names):
        die(f'title name clash: {names}')

    before = outside_hash(image, off, size)
    if not a.dry_run and not a.no_backup:
        bak = f'{image}.bak-{time.strftime("%Y%m%d-%H%M%S")}'
        subprocess.run(['cp', '--sparse=always', '--', str(image), bak], check=True)
        print('backup:', bak)

    fs = Fatx(str(image), drive=a.partition)
    gdir = '/' + a.games_dir
    if not a.dry_run:
        if a.games_dir not in [x.filename for x in fs.listdir('/')]:
            fs.mkdir(gdir)
    for title, src in items:
        dest = f'{gdir}/{title}'
        work = None
        try:
            if src.is_file():
                work = Path(tempfile.mkdtemp(prefix='xiso-', dir=tmp))
                print(f'[{title}] extracting {src.name}')
                r = subprocess.run([a.extract_xiso, '-d', str(work), str(src)], capture_output=True, text=True)
                if r.returncode:
                    die(f'extract-xiso failed on {src}: {r.stderr.strip()}')
                tree_root = work
            else:
                tree_root = src
            if not any(p.name.lower() == 'default.xbe' for p in tree_root.iterdir()):
                print(f'[{title}] skipped: no default.xbe'); continue
            want = local_tree(tree_root)
            try:
                have = fatx_tree(fs, dest)
            except AssertionError:
                have = None
            if have == want:
                if a.verify:
                    verify(fs, tree_root, dest, want, True, title)
                print(f'[{title}] up to date'); continue
            need = sum(v for v in want.values() if v > 0)
            print(f'[{title}] install {len(want)} entries, {need/1e6:.0f} MB -> {a.partition.upper()}:{dest.replace("/", chr(92))}')
            if a.dry_run:
                continue
            if have is not None:
                rmtree(fs, dest)
            install(fs, tree_root, dest)
            got = fatx_tree(fs, dest)
            if got != want:
                die(f'[{title}] post-install tree mismatch; restore from the backup')
            verify(fs, tree_root, dest, want, a.verify, title)
            print(f'[{title}] installed and verified')
        finally:
            if work:
                shutil.rmtree(work, ignore_errors=True)
    del fs
    if outside_hash(image, off, size) != before:
        die('BUG: bytes outside the FATX volume changed; restore from the backup')
    print('bytes outside the volume unchanged (accounts/EEPROM area preserved)')

    # launcher config: report only
    cfs = Fatx(str(image), drive='c')
    try:
        ini = bytes(cfs.read('/UIX Configs/config.ini')).decode('latin1')
        ok = re.search(r'^Path\d+=.*\b' + re.escape(a.games_dir) + r'\b', ini, re.M)
        print('UIX launcher config: ' + ('has a Games path' if ok else
              f'NO launcher path for {a.games_dir}; add one in Settings > UIX Settings > Launcher'))
    except AssertionError:
        print('UIX launcher config: C:\\UIX Configs\\config.ini not found (not a UIX dashboard disk?)')


if __name__ == '__main__':
    main()
