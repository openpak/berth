# Evidence: berth

## What works today

- Builds on Linux and starts with its own configuration, kept separate from
  xemu: `berth.toml` in the `OpenPak/Berth` preferences directory. Upstream
  update checks default to off.
- Boots a user-supplied Microsoft 5960 dashboard from a prepared test disk to
  the first-run notice, the main menu and the native Xbox Live connection test.
  System Info reports K:1.00.4627.01 / D:1.00.5960.01. Memory, Music and the
  full Settings list were driven and screenshotted; the clock follows the
  host and guest audio reaches the host mixer. Rendering confirmed with both
  the OpenGL and Vulkan renderers (8/8 soak boots clean on 2026-10-27).
- A `net.nat.dns` option lets the guest use an explicit DNS address outside the
  NAT network, added as groundwork for reaching OpenPak. It has not been used
  against a live service.

Verified on production, 2026-10-17/18: Berth running the 5960 dashboard signed
in to OpenPak's native Xbox services. DNS resolved through xb-dns, Kerberos AS
and TGS through xb-auth, SG init on UDP 3074 through xb-gateway, service 1
(presence, friends) through xb-social, service 5 (signup, account management)
through xb-account, service 11 (terms, motd) through xb-tou and service 6
(dashboard voice-chat sessions) through xb-voice. The friends list, account
signup and voice chat sessions were exercised from the dashboard.

Not yet verified: any game title online, a physical console, and provisioning
without manual server-side setup.

## Known limitations

- An intermittent PFIFO pusher abort (`pfifo_run_pusher` DMA-range assertion
  in `hw/xbox/nv2a/pfifo.c`) fired on both renderers. It no longer aborts:
  out-of-range DMA state now logs get/put/len and suspends the pusher on the
  hardware's own error path until the guest clears it. A whole-process abort
  on guest-driven FIFO state cannot recur from these sites; if the GPU ever
  stalls instead, the stderr lines name the stuck state.
- The HDD `-drive` line now passes `format=` explicitly (qcow2 magic probe,
  else raw), so raw images no longer get block-0 writes restricted.
