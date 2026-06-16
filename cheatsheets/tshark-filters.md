# TShark Display Filters (Cheatsheet)

## Capture parsing
| Filter                                    | What you get                         |
|-------------------------------------------|--------------------------------------|
| `wlan.fc.type_subtype == 0x08`            | Beacons                              |
| `wlan.fc.type_subtype == 0x04`            | Probe requests (active scanning)     |
| `wlan.fc.type_subtype == 0x05`            | Probe responses                      |
| `eapol`                                   | All EAPOL (handshake) frames         |
| `eapol.type == 3`                         | EAPOL-Key msg 1/4 (ANonce)           |
| `eapol.type == 2`                         | EAPOL-Key msg 2/4 (SNonce + MIC)     |
| `eapol.type == 0`                         | EAPOL-Key msg 3/4                    |
| `eapol.type == 1`                         | EAPOL-Key msg 4/4                    |
| `wlan.bssid == aa:bb:cc:dd:ee:ff`         | All frames to/from one AP            |
| `wlan.fc.type == 2`                       | Data frames                          |
| `wlan.fc.type == 1 && wlan.fc.subtype == 0x0c` | Deauth frame                    |

## Useful combos
- `eapol || wlan.fc.type_subtype == 0x0c` - handshake + deauth
- `wlan.ssid == "Hotel-Guest"` - one SSID
- `wlan.fc.type_subtype == 0x08 && wlan.rsn.capabilities` - WPA2 beacons only
- `eapol && frame.time_delta > 1` - long delays = suspicious

## Conversion commands
```bash
# Just EAPOL frames to a new file
tshark -r in.pcapng -Y "eapol" -w eapol.pcapng

# Per-BSSID
tshark -r in.pcapng -Y "wlan.bssid == aa:bb:cc:dd:ee:ff" -w one_ap.pcapng

# Beacons to text
tshark -r in.pcapng -Y "wlan.fc.type_subtype == 0x08" -T fields \
  -e wlan.bssid -e wlan.ssid -e wlan.channel
```

## Decryption hint
If you have the PSK and want to decrypt a WPA capture:
```
tshark -r in.pcapng -o "wlan.enable_decryption:TRUE" \
       -o "uat:80211_keys:\"wpa-pwd\",\"psk:ssid\""
```
