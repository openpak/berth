# Evidence: berth

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

## Known limitations

- A Vulkan GPU-command assertion (`pfifo_run_pusher` in `hw/xbox/nv2a/pfifo.c`)
  aborts the dashboard under the Vulkan renderer. Root cause is unknown; use
  OpenGL for now. A similar PFIFO DMA-range assertion (`pfifo.c:299`) ended one
  networking test run.
