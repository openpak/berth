# Berth

Berth is OpenPak's original Xbox emulator, built on [xemu](https://github.com/xemu-project/xemu),
which is itself built on QEMU. The goal is to run the console's own kernel,
dashboard and titles over emulated Xbox hardware, and to speak the same native
protocols as a physical console so one OpenPak backend can serve both.

Berth is an independent project. xemu remains our upstream base and is not
replaced by this fork. It is not an official xemu release. It targets the
original Xbox only, not Xbox 360, Xbox One or Xbox Series.

**Status:** Experimental (boots, online not started)

## Not affiliated

Berth is independent and is not endorsed by the xemu project or by QEMU. It is
not affiliated with Microsoft. Xbox and related names are trademarks of their
respective owners.

## What works today

- Builds on Linux and starts with its own configuration, kept separate from
  xemu: `berth.toml` in the `OpenPak/Berth` preferences directory. Upstream
  update checks default to off.
- Boots a user-supplied Microsoft 5960 dashboard from a prepared test disk to
  the first-run notice, the main menu and the native Xbox Live connection test.
  Rendering was confirmed with the OpenGL renderer.
- A `net.nat.dns` option lets the guest use an explicit DNS address outside the
  NAT network, added as groundwork for reaching OpenPak. It has not been used
  against a live service.

Not verified: any OpenPak service. Networking was disabled in the dashboard
runs, so the connection test fails as expected; that is not an OpenPak result. Sign-in, friends, presence and matchmaking are untested, and no game has
been run against OpenPak. A packet capture of a clean client reached DHCP only.

## Connecting to OpenPak

There is no Berth-specific login and no replacement guest API. The intent is
for the guest's own account and Xbox Live calls to reach OpenPak's Xbox services
through DNS and routing at the network boundary. That integration is not yet
implemented or validated, so Berth cannot sign in to OpenPak today.

You must supply your own MCPX boot ROM, BIOS, EEPROM and hard disk image with
a dashboard, from a console you own. OpenPak provides none and never will. See
[xemu's required-files guide](https://xemu.app/docs/required-files/) for what the
emulator expects. Create an OpenPak account at https://openpak.org.

## Downloads

No public build yet. The version tags in this repository come from xemu and are
not Berth releases. Releases will appear at https://github.com/openpak/berth/releases.

## Building from source

Berth builds like xemu. On Linux use the upstream `./build.sh`, which wraps
QEMU's `configure` for the `i386-softmmu` target. Dependencies are pinned in
`subprojects/` and `get_deps.py`. `build-berth.sh` is the maintainers' wrapper: it
expects the checkout inside a larger work directory and takes a shared build
lock, so most people should use `build.sh`. The packaged executable is renamed
`berth`, with its own icon and application ID `org.openpak.berth`.

## Known limitations

- A Vulkan GPU-command assertion (`pfifo_run_pusher` in `hw/xbox/nv2a/pfifo.c`)
  aborts the dashboard under the Vulkan renderer. Root cause is unknown; use
  OpenGL for now. A similar PFIFO DMA-range assertion (`pfifo.c:299`) ended one
  networking test run.
- No OpenPak service compatibility yet. The Xbox services run as separate
  containers on the OpenPak server and are still being built.
- The original Xbox sends its Xbox Live gateway traffic to fixed UDP port 3074,
  which another OpenPak service family also uses; how to route both is unresolved.
- Do not share one EEPROM or MAC address between a running emulator and a real
  console on the same network.
- Linux only so far. Other platforms inherit xemu's build but are untested here.

## Contributing and support

Report bugs at https://github.com/openpak/berth/issues, not with the xemu
project. To report a security problem, contact the OpenPak maintainers privately
through the contact on https://openpak.org and do not open a public issue.
See [CONTRIBUTING.md](CONTRIBUTING.md), inherited from xemu, for its design
philosophy: faithful hardware emulation and no per-game hacks. Most useful:
captures of what a real console and the 5960 dashboard send on the wire, and help
tracking down the Vulkan assertion.

## License and acknowledgements

Berth keeps xemu's and QEMU's licences. QEMU is released under the GNU General
Public License version 2, and individual files carry their own licence headers,
which are preserved. See [LICENSE](LICENSE), [COPYING](COPYING) and
[COPYING.LIB](COPYING.LIB). Berth is not relicensed. The Berth icon in
`packaging/berth.svg` is separate artwork, AGPL-3.0-only as declared in the SVG.
Internal xemu names and credits are retained on purpose. Thanks to the xemu
and QEMU developers.

The original xemu README is kept in [README.upstream.md](README.upstream.md); the
QEMU README is [README.rst](README.rst).
