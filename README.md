# Berth

OpenPak's Berth Emulator.

| | |
| --- | --- |
| Console | Xbox |
| Kind | Emulator |
| Based on | [xemu](https://github.com/xemu-project/xemu) (GPL-2.0) |
| Licence | GPL-2.0 for QEMU as a whole, per-file licences kept; see [LICENSE](LICENSE) |

## What it does

- Emulates the original Xbox, as a fork of xemu, which is built on QEMU.
- Targets the original Xbox only, not Xbox 360, Xbox One or Xbox Series.
- Keeps its own configuration, `berth.toml`, in the `OpenPak/Berth` preferences directory, separate from xemu.

## Build

```sh
./build.sh
```

Builds on Linux, wrapping QEMU's `configure` for the `i386-softmmu` target. The long form is in [deploy](docs/deploy.md).

## Docs

- [Protocol](docs/protocol.md)
- [Evidence](docs/evidence.md)
- [Deploy](docs/deploy.md)
- [Notes](docs/notes.md)

Other files already in `docs/`:

| | | |
| --- | --- | --- |
| [about/](docs/about/) | [berth-game-roms.md](docs/berth-game-roms.md) | [berth-next-session.md](docs/berth-next-session.md) |
| [berth-plan.md](docs/berth-plan.md) | [block-replication.txt](docs/block-replication.txt) | [bypass-iommu.txt](docs/bypass-iommu.txt) |
| [COLO-FT.txt](docs/COLO-FT.txt) | [colo-proxy.txt](docs/colo-proxy.txt) | [config/](docs/config/) |
| [conf.py](docs/conf.py) | [defs.rst.inc](docs/defs.rst.inc) | [devel/](docs/devel/) |
| [glossary.rst](docs/glossary.rst) | [igd-assign.txt](docs/igd-assign.txt) | [image-fuzzer.txt](docs/image-fuzzer.txt) |
| [index.rst](docs/index.rst) | [interop/](docs/interop/) | [memory-hotplug.txt](docs/memory-hotplug.txt) |
| [meson.build](docs/meson.build) | [multiseat.txt](docs/multiseat.txt) | [multi-thread-compression.txt](docs/multi-thread-compression.txt) |
| [nvdimm.txt](docs/nvdimm.txt) | [pcie_pci_bridge.txt](docs/pcie_pci_bridge.txt) | [pcie_sriov.txt](docs/pcie_sriov.txt) |
| [pcie.txt](docs/pcie.txt) | [pci_expander_bridge.txt](docs/pci_expander_bridge.txt) | [qcow2-cache.txt](docs/qcow2-cache.txt) |
| [qdev-device-use.txt](docs/qdev-device-use.txt) | [qemu-option-trace.rst.inc](docs/qemu-option-trace.rst.inc) | [qemupciserial.inf](docs/qemupciserial.inf) |
| [rdma.txt](docs/rdma.txt) | [requirements.txt](docs/requirements.txt) | [specs/](docs/specs/) |
| [sphinx/](docs/sphinx/) | [sphinx-static/](docs/sphinx-static/) | [spice-port-fqdn.txt](docs/spice-port-fqdn.txt) |
| [spin/](docs/spin/) | [system/](docs/system/) | [_templates/](docs/_templates/) |
| [throttle.txt](docs/throttle.txt) | [tools/](docs/tools/) | [user/](docs/user/) |
| [xbzrle.txt](docs/xbzrle.txt) | [xen-save-devices-state.txt](docs/xen-save-devices-state.txt) |  |

## Licence

Berth keeps xemu's and QEMU's licences and is not relicensed. See [LICENSE](LICENSE), [COPYING](COPYING) and [COPYING.LIB](COPYING.LIB).
