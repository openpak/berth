#!/usr/bin/env bash
set -euo pipefail
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
work_dir="$(dirname -- "$source_dir")"
if [[ "$(uname -s)" != Linux ]]; then
    echo 'This wrapper currently supports Linux only; see build.sh for other platforms.' >&2
    exit 1
fi
jobs=8
if [[ "${1:-}" == -j* ]]; then
    jobs="${1#-j}"
    shift
fi
[[ "$jobs" =~ ^[1-9][0-9]*$ ]] || { echo 'Use -jN with a positive job count.' >&2; exit 1; }
mkdir -p "$work_dir/build-linux" "$work_dir/tmp" "$work_dir/logs"
export TMPDIR="$work_dir/tmp"
exec 9>/tmp/openpak-build.lock
flock -w 60 9 || { echo 'Another OpenPak build holds the build lock.' >&2; exit 1; }
cd "$work_dir/build-linux"
{
    "$source_dir/configure" --extra-cflags='-DXBOX=1 -Wno-error=redundant-decls' \
        --target-list=i386-softmmu --disable-werror "$@"
    pyvenv/bin/meson configure -Dforce_fallback_for=slirp -Dslirp:default_library=static
    make -j"$jobs" qemu-system-i386
    mkdir -p dist
    cp qemu-system-i386 dist/berth
    cp "$source_dir/packaging/berth.svg" dist/org.openpak.berth.svg
    cp "$source_dir/packaging/berth.png" dist/org.openpak.berth.png
    cp "$source_dir/packaging/org.openpak.berth.desktop" dist/
    cp "$source_dir/LICENSE" dist/LICENSE
    cp "$source_dir/COPYING" dist/COPYING
    cp "$source_dir/COPYING.LIB" dist/COPYING.LIB
} 2>&1 | tee "$work_dir/logs/build.log"
