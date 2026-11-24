# ThinkPad T480s · macOS Sequoia

OpenCore 1.0.8 configuration for the ThinkPad T480s with an i5-8350U, Intel UHD 620 (5917), 1080p internal display, Intel AC 8265, Realtek ALC257 audio and G2Touch USB touchscreen. Tested on Sequoia build **24H241**. Compare your hardware before using the port map or firmware patches.

## Hardware results

| Snapshot | Status | Observed on this T480s |
| --- | --- | --- |
| Audio11 | 本机实测通过 | One cold boot from internal storage without a USB stick. Speakers and headphone playback, jack switching and internal microphone level response. Recording playback and wake recovery remain untested. |
| Wi-Fi test | 本机实测通过 | itlwm 2.3.0 and HeliPort 1.5.0 connected to a hotspot and fetched a web page over Wi-Fi. Login reconnect and wake reconnect remain untested. |
| Touch HID test | 本机实测通过 | G2Touch finger taps and window dragging. Edge accuracy and multitouch remain untested. |
| Brightness (published configuration) | 本机实测通过 | F5/F6 adjust panel brightness. Metal 3 reported and a GPU command-buffer fill completed. |
| Brightness | 已观察 | Wireless and touchscreen drivers loaded. |
| Brightness | 静态检查通过 | Installed EFI files read back correctly. A subsequent internal cold boot with this revision remains unverified. |

Bluetooth, full trackpad and TrackPoint operation, physical port mapping, camera, card reader and extended sleep remain pending. The ELAN SMBus touchpad and G2Touch USB touchscreen are separate devices.

## Reproduce the brightness configuration

1. With Python 3.9 or newer, run `python assemble.py ../T480s-build` from this repository. Use a new output directory. The script downloads the pinned upstream releases and checks each archive and each selected file against its SHA-256 digest. For offline use, supply `--cache PATH` containing the exact files named in [assets.json](assets.json).
2. Personalize the output copy of `EFI/OC/config.plist`. Under `PlatformInfo → Generic`, keep the MacBookPro15,2 model. Generate your own SystemSerialNumber and MLB with OpenCore macserial or GenSMBIOS, generate a fresh SystemUUID, and set ROM to your own six-byte network hardware address as plist Data. The published template has empty identity strings and a zero ROM. Keep the personalized copy private.
3. Run the OpenCore 1.0.8 checker against the personalized file, for example `ocvalidate.exe ../T480s-build/EFI/OC/config.plist`. The checker ships under Utilities/ocvalidate in the pinned OpenCore archive.
4. Test on a separate, identified USB boot device using the firmware F12 menu. Preserve a working boot and recovery path. Obtain Sequoia installation media separately from Apple. For the Intel wireless interface install [HeliPort 1.5.0](https://github.com/OpenIntelWireless/HeliPort/releases/tag/v1.5.0) in macOS.

## Configuration details

The compiled PLUG, PNLF and USBX tables and custom USB map are included. The asset manifest records the exact upstream members for OpenCore, drivers and kernel extensions. The Kaby Lake graphics injection and ALC257 layout 11 follow the tested configuration. The snapshot uses verbose/debug boot arguments and disables OpenCore SecureBootModel. Full port and sleep validation depends on the target machine.
