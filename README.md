# Berth

Berth is OpenPak's original Xbox emulator, forked from
[xemu](https://github.com/xemu-project/xemu), built on QEMU.

The goal is to run the console's own kernel, dashboard and title software over
emulated Xbox hardware. Network services must speak the native Xbox protocols
so the same backend can serve Berth and physical Xbox consoles. There is no
Berth-specific login or replacement guest networking API. Xbox backend services
run in their own container images on the OpenPak server; the Xbox account
adapter talks to the existing console-neutral account core.

This targets the original Xbox, not Xbox 360, Xbox One or Xbox Series firmware.
Hardware-dependent guest components run against emulated devices; they are not
removed simply because they touch hardware.

## Current state

The Linux emulator builds and runs supplied guest software to the HDD's
placeholder dashboard. The supplied HDD does not contain the official Microsoft
dashboard. Native service parity and retail dashboard boot remain unverified.
Upstream emulation behavior is retained.

Berth uses `berth.toml` and SDL's `OpenPak/Berth` preferences directory, separate
from xemu. Upstream update checks default to off. Internal xemu names and credits
are retained to keep upstream changes straightforward to integrate.

## Build on Linux

Run `./build-berth.sh -j8`. Build output, temporary files and logs live next to
the checkout in `../build-linux`, `../tmp` and `../logs`. The shared OpenPak build
lock prevents overlapping builds. The packaged executable is
`../build-linux/dist/berth`.

The build downloads pinned dependencies declared in `subprojects/`; see
`build.sh` for upstream options. No Xbox firmware, keys or HDD contents are
included. Obtain the required files from your own console and configure their
paths in Settings > System. See [xemu's required-files guide](https://xemu.app/docs/required-files/).

## Architecture and next steps

See [docs/berth-plan.md](docs/berth-plan.md) and
[docs/berth-next-session.md](docs/berth-next-session.md).

## Attribution and licensing

Preserve upstream copyright notices and the per-file licenses described in
[LICENSE](LICENSE). This fork is not relicensed to OpenPak's AGPL code license.
The separate Berth icon in `packaging/berth.svg` is user-supplied artwork,
Copyright 2026 tobagin, AGPL-3.0-only as declared in that SVG. It is packaged as
a separate asset, not embedded into the emulator binary.
