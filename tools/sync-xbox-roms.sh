#!/usr/bin/env bash
# Sync Xbox ROM backups (XISO / extracted folders) into a Berth raw HDD image.
# Usage: tools/sync-xbox-roms.sh ROM_DIR DISK.RAW [extra sync_xbox_roms.py args]
# Env: TMPDIR (required, not /tmp), PYTHON (needs pyfatx), EXTRACT_XISO.
set -euo pipefail
[ $# -ge 2 ] || { sed -n 2,5p "$0"; exit 2; }
here=$(cd "$(dirname "$0")" && pwd)
roms=$1 image=$2; shift 2
exec "${PYTHON:-python3}" -I "$here/sync_xbox_roms.py" --roms "$roms" --image "$image" "$@"
