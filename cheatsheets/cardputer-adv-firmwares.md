# Cardputer ADV Quick Reference

## Hardware
- M5Stack Cardputer ADV (ESP32-S3)
- Built-in: WiFi 2.4GHz, BLE, IR TX, mic, keyboard, 1.14" TFT, microSD
- 8MB PSRAM, 16MB flash

## Useful firmwares (no extras required)

### Marauder (esp32-marauder fork for Cardputer)
- GitHub: `SpacehuhnTech/esp32_marauder` (and the `toblum/m5stickc-marauder` style forks for Cardputer)
- Why: WiFi deauth, beacon spam, probe capture, packet monitor, PMKID capture
- Install: via M5Burner (m5burner.com) or `esptool.py` flash

### Bruce
- GitHub: `pr3y/Bruce` 
- Why: multi-tool firmware - WiFi, BLE, IR, Sub-GHz (with module), BadUSB-lite, RFID prep
- Install: M5Burner "Cardputer" firmware slot

### Nemo
- GitHub: `SpacehuhnTech/Nemo`
- Why: BLE/IR focused, quieter than Bruce, faster boot

### Cardputer specific
- `saint-loup/esp32-marauder-cardputer` or `0xZ0F/Cardputer-Adv-Marauder`
- Pick the one that has the right pinout for the ADV (the ADV has different GPIO than the original Cardputer)

## On-device commands (Marauder-style)
```
scan ap          - list nearby APs
select -a <idx>  - target an AP
attack -t deauth - send deauth flood
attack -t beacon - spam random SSIDs
capture -eapol   - record handshake
sniff -beacon    - record beacon frames
```

## Storage
- SD card root expected by most firmwares
- Captures usually in `/capture/` or `/Bruce/` directory

## Quick data exfil
- USB-C to phone: many firmwares expose as USB mass storage
- SD swap to Mac: fastest, full-speed
- WiFi HTTP server: some firmwares serve `/cap/` over a local AP
