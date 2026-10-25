# Notes: berth

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

## Contributing and support

Report bugs at https://github.com/openpak/berth/issues, not with the xemu
project. To report a security problem, contact the OpenPak maintainers privately
through the contact on https://openpak.org and do not open a public issue.
See [CONTRIBUTING.md](../CONTRIBUTING.md), inherited from xemu, for its design
philosophy: faithful hardware emulation and no per-game hacks. Most useful:
captures of what a real console and the 5960 dashboard send on the wire, and help
tracking down the Vulkan assertion.

## License and acknowledgements

Berth keeps xemu's and QEMU's licences. QEMU is released under the GNU General
Public License version 2, and individual files carry their own licence headers,
which are preserved. See [LICENSE](../LICENSE), [COPYING](../COPYING) and
[COPYING.LIB](../COPYING.LIB). Berth is not relicensed. The Berth icon in
`packaging/berth.svg` is separate artwork, AGPL-3.0-only as declared in the SVG.
Internal xemu names and credits are retained on purpose. Thanks to the xemu
and QEMU developers.

The original xemu README is kept in [README.upstream.md](../README.upstream.md); the
QEMU README is [README.rst](../README.rst).
