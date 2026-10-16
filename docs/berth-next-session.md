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

## 5960 dashboard bring-up and network planning — 2026-10-16

Supersedes the earlier missing-dashboard blocker. User supplied `5960.zip`
(74079781 bytes) and `XboxDash1.00.5659.03V1.4.zip` (older release) in Downloads.
5960 contains a 1961984-byte XBE titled Xbox Dashboard, fonts, xboxdashdata and
xodash. Extracted under `../dashboard-5960`; guest bytes remain outside git.

Installed 137 files into a separate sparse raw disk `../runtime/dashboard-5960.raw`
using pyfatx 0.0.8. Every installed file was read back and SHA-256 compared to
its source. The original HDDs and ZIPs were untouched. Preparation helpers are
in scratch, not emulator source. `qemu-img` was also built with --enable-tools
for future offline disk conversion; do not convert a disk actively in use.

Official dashboard reaches its first-run notice, main menu and native Xbox Live
connection test. Captures: `../runtime/dashboard-5960-window.png` (notice),
`../runtime/xemu-2026-10-16-10-28-45.png` (main menu),
`../runtime/xemu-2026-10-16-10-29-55.png` (connection test, cable unavailable).
Version is supplied as 5960; exact System Info version remains to be checked.

Vulkan run aborted: SIGABRT PID 2677574, assertion at
hw/xbox/nv2a/pfifo.c:426 in pfifo_run_pusher (reserved/invalid GPU command).
coredumpctl confirms that stack; no OOM evidence. Root cause remains unknown.
Retried with separate `../runtime/dashboard-5960-opengl.toml` selecting OpenGL;
main menu and connection test render, and user confirmed it was working.
Both renderers initialize early contexts, so Vulkan device logs alone do not
mean the selected renderer is Vulkan. No hardware-code workaround was added.

Leave the user's current session running; stop automated input. Networking is
still disabled, so the native connection-test failure is expected and is not
an OpenPak service result. Keyboard bindings were edited by the user; preserve
them. Do not share this EEPROM/MAC with concurrent emulators or real hardware.

Next objective is planning how native Xbox services fit OpenPak. Canonical plan:
https://github.com/openpak/docs/blob/main/xbox/native-service-architecture.md .
Separate service images, core-backed identity/social state, original-Xbox
namespace distinct from Xbox 360, and a fixed-port conflict with Demonware UDP
3074 must be resolved. No Xbox service was deployed or guest networking enabled.

## Gateway port audit — 2026-10-16

Isolated test artifacts are in `../network-audit`: fresh client disk and EEPROM,
loopback Ethernet harness, private native.pcap, source-section disassembly and
read-back installer log. Earlier user disk/EEPROM were not reused for this test.
The supplied xonlinedash module's native SG-init builder writes UDP destination
3074 literally at VA 0x135f49, separate from its configured source port. Tag
0x5802 identifies that packet as XB-to-SG init. No SNI routing applies.

Wire capture reached DHCP only. First audit process (2718779) aborted on a
PFIFO DMA-range assertion at pfifo.c:299. Diagnostic restart with boot-animation
skip/software FPU reached the first-run notice then ended on SIGTERM; no claim
that these settings cure the crash. Full authentication/physical-console trace
is still pending. Local KDC build waits timed out behind another workspace build;
no KDC service/database was started. Canonical evidence and scope:
https://github.com/openpak/docs/blob/main/xbox/gateway-port-audit-2026-10-16.md .
