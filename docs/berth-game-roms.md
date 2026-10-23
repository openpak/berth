# Game backups on the Berth HDD

The UIX Lite dashboard (C:\UIX Configs\config.ini, `Path2=Games`) lists folders
that contain `default.xbe` under `<partition>:\Games\`. `tools/sync-xbox-roms.sh`
installs XISO files (or already extracted game folders) from a ROM directory
into a Berth raw HDD image as `E:\Games\<Title>\`.

    export TMPDIR=<scratch dir, not /tmp>   # holds one extracted game at a time
    export PYTHON=<python with pyfatx>      # see below
    export EXTRACT_XISO=<path to extract-xiso>
    tools/sync-xbox-roms.sh ROM_DIR DISK.RAW [--partition e] [--verify] [--dry-run] [--no-backup]

Behaviour: refuses while any process has the image open (Berth does); makes a
sparse backup `DISK.RAW.bak-<time>`; writes only inside the FATX volume and
checks a hash of every byte outside it (account sectors, EEPROM-adjacent data)
before and after; skips titles whose installed file tree already matches.
After running, open the dashboard Launcher and rescan (cache.ini is rebuilt).

Limits: E: is about 4.8 GiB, so one 3.5 GB game fits and a second will not
(the script stops with a write error and tells you to restore the backup).
For more titles, use Machine > Load Disc with the ISO instead.

Tools: pyfatx / libfatx (mborgerson/fatx, GPL-2.0) and extract-xiso (XboxDev,
BSD-style). Upstream libfatx rejects 42-character names (`>=` instead of `>`),
which breaks titles such as Fable; build pyfatx from a copy with that check
changed in `libfatx/fatx_dir.c` and `fatx_file.c`. Game data is never committed.
