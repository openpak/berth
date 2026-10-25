# Deploy: berth

## Requirements

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

- Do not share one EEPROM or MAC address between a running emulator and a real
  console on the same network.
- Linux only so far. Other platforms inherit xemu's build but are untested here.
