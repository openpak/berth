# Berth handoff — 2026-10-16

## Workspace

- GitHub: https://github.com/openpak/berth (public fork of xemu-project/xemu).
- Branch: `berth`; upstream base `36334d95b86f9c3c6ae34efb9af06785273f8e1a`.
- Checkout: `scratch/berth/src`, exposed as `emulators/berth`.
- Upstream remote has push disabled. Do not replace this checkout or symlink.
- Read `README.md`, `docs/berth-plan.md`, `AGENTS.md` and `CONTRIBUTING.md`.

## Initial work

Berth SDL name/application ID/window title, isolated `berth.toml` preferences,
upstream update checks disabled by default, a Linux build wrapper, architecture
and parity gates, and user-supplied icon packaged as separate SVG/PNG assets.
The window loads the PNG next to the executable. Upstream credits and per-file
licenses remain intact. Hardware emulation and guest protocols are unchanged.

## Build

`./build-berth.sh -j8` creates `../build-linux/dist/berth`.
All temporary files stay in `../tmp`, logs in `../logs/build.log`.
Uses `/tmp/openpak-build.lock`, the sole allowed temporary path outside scratch.

The first configure attempt incorrectly used the source parent as the build
folder. Meson rejected it. The working build directory is `../build-linux`.

## Firmware and service gate

The user supplied `~/Downloads/Xbox-Emulator-Files`:
512-byte `mcpx/mcpx_1.0.bin`, 1 MiB `bios/Complex_4627.bin`, and
`hdd/xbox_hdd.qcow2` (8 GiB virtual). Copies are in `../firmware` and `../runtime`;
the originals remain intact. No supplied EEPROM; upstream generates one for
this emulator. This does not establish a retail console identity.

Boot with `-config_path ../runtime/berth.toml` (use absolute path). Networking
is disabled for the initial boot. Guest code runs and renders the message
"Please insert an Xbox disc". Read-only QCOW2/FATX inspection found only
`C:/xboxdash.xbe` (172032 bytes), XBE certificate title `hello`, containing that
message. This is a placeholder, not the official Microsoft dashboard. Need the
owner's official dashboard files for the next boot gate. Final firmware revision
and native service behavior remain unverified.

QMP `query-status` reports running. QMP `screendump` is not available in this
xemu build. A scoped window capture is `../runtime/boot-window.png`.

Xbox services run in separate container images on OpenPak; the Xbox account
adapter integrates with account core. Initial AGPL candidate fork:
https://github.com/openpak/xbox-live (from XombieOnline/xombie), exposed in the
workspace as `servers/xbox-live`. See its `docs/openpak-plan.md` for boundaries
and status. No backend was deployed or service parity demonstrated.

## Validation results

- Linux build and package completed through `./build-berth.sh -j8`.
- Pinned libslirp is linked statically so the copied executable does not need
  the build tree's shared libslirp. `ldd dist/berth` reports no missing libraries.
- Final package launches with QMP status `running`; SDL window/app ID is Berth /
  `org.openpak.berth`. strace confirms the separate Berth PNG was opened.
- Initial scoped capture `../runtime/boot-window.png` shows the placeholder.
  Initial `-help` smoke check completed, and a fresh preferences
  path was `OpenPak/Berth/berth.toml`, separate from xemu.
- `bash -n build-berth.sh` and `git diff --check` pass. Upstream third-party code
  emits warnings in the full build; no compiler errors or warnings were observed
  for the modified UI/settings files.
- Additional user paths checked: Downloads/boot-rom-image and
  Downloads/hard-disk-image. The former contains the same MCPX ROM; the latter's
  39714816-byte HDD image also has only the same 172032-byte `hello` placeholder
  on C:, with no xodash/xboxdashdata resources. E: has TDATA and UDATA. It does
  not supply the official dashboard required for gate 2.
- Firmware boot configuration keeps networking disabled. Native service and
  real-console parity remain untested. No Xbox backend container was started.
