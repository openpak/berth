# Berth architecture and bring-up

Cross-repository service architecture is maintained in
[Original Xbox on OpenPak](https://github.com/openpak/docs/blob/main/xbox/native-service-architecture.md).
That plan is authoritative for core integration, service boundaries and routing;
the notes below describe emulator bring-up.

## Invariants

- Original Xbox guest kernel, dashboard and title code own protocol behavior.
- Emulate CPU, memory, NV2A, MCPX devices, storage, EEPROM, input and NIC.
- Serve physical Xbox and Berth through the same native service endpoints.
- DNS/routing configuration belongs at the network boundary. Do not replace
  guest account, authentication, friends or matchmaking calls with host APIs.
- Retain console identity and storage semantics. Do not share an EEPROM/MAC
  between concurrently connected devices. Never commit firmware or credentials.
- Keep account-core integration server-side. Do not copy AGPL server code into
  the upstream emulator tree without checking license compatibility.

## Server deployment boundary

User requirement, 2026-10-16: Xbox network services live in their own services
and container images on the OpenPak server, following the existing console
adapter deployment model. They do not run inside Berth.

The Xbox account adapter talks to the existing account core for account linking,
identity and shared account state. Xbox protocol and credential translation
remain in the Xbox adapter; account core stays console-neutral. Other Xbox
services must be independently deployable, each with its own runtime container
image and process, configuration, credentials and health checks. Do not ship
an all-services image or supervise the whole network in one container. Shared
protocol libraries are fine; separate runtime images remain mandatory. Exact
repository names, ports and protocols to be established from observed traffic.
Berth and physical Xbox consoles use the same native Xbox endpoints. No new
backend is implemented or deployed by the emulator bring-up work.

## Gates

1. Build the fork; verify executable startup and separate configuration.
2. Provision owner-supplied MCPX boot ROM, compatible BIOS/kernel, EEPROM and
   a writable HDD image with the official dashboard. Record hashes and versions
   locally, never raw identity material in committed reports. Determine and
   verify the final original-Xbox dashboard revision before calling it latest.
3. Boot the official dashboard; record video output, input, disk and clock
   behavior. Do not claim all system modules work from a successful boot alone.
4. Capture DHCP, DNS and service traffic from guest NIC. Compare against a
   physical Xbox running the same dashboard/title and equivalent setup.
5. Point both clients at one native service backend; verify sign-in, friends,
   presence, matchmaking and cross-device play individually. Record failures.

## Network starting point

`ui/xemu-net.c` connects the emulated `nvnet.0` NIC to a hub and NAT/libslirp,
UDP Ethernet tunnel or pcap backend. Preserve the guest packets. Use NAT for
initial bring-up; check the actual transport requirements before assuming NAT
supports the complete Xbox Live protocol. DNS changes alone cannot implement
an account service or substitute console credentials.

Upstream PR #3107 (NVNet queued-packet flushing) is open at initial inspection:
https://github.com/xemu-project/xemu/pull/3107 . Track it during networking
validation; it has not been imported into Berth.

## Hotkeys

F8 returns the guest to the Xbox dashboard from anywhere, including a running
game and with the UI hidden. It ejects any inserted disc (the kernel would boot
it ahead of the dashboard) and then resets the machine, which boots the
dashboard from the HDD again. Machine > Return to Dashboard does the same.
Shift+F8 still saves the fourth bound snapshot; plain F8 no longer loads it.

## Base selection

xemu is a full-system hardware emulator and already supports the official
Xbox dashboard when supplied by the owner. Cxbx-Reloaded includes its own
kernel/HLE implementation and targets Windows/Wine; it is less aligned with
preserving the real system software on this Linux workstation.

Sources: https://xemu.app/docs/about/ , https://xemu.app/docs/networking/ ,
https://xemu.app/docs/dashboard/ ,
https://github.com/Cxbx-Reloaded/Cxbx-Reloaded .
