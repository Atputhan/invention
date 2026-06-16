# Cardputer ADV Trip Checklist

## On the device
- [ ] SD card (>=32GB) formatted FAT32
- [ ] Cardputer ADV charged (USB-C)
- [ ] Firmware flashed: Marauder OR Bruce OR Porkchop (one primary)
- [ ] Test boot: scan AP, see at least 5 networks
- [ ] Test capture: handshakes file appears on SD
- [ ] Test deauth: with explicit permission on YOUR OWN AP only

## On the Mac
- [ ] `git clone https://github.com/Atputhan/invention.git ~/tools`
- [ ] `brew install hashcat wireshark python`
- [ ] `pip3 install scapy` (fallback when tshark unavailable)
- [ ] `~/tools/bin/crack.sh <file.pcapng>` smoke test on sample

## Wordlists on Mac
- [ ] rockyou.txt
- [ ] `python scripts/hotel_wardict.py --top 50000 > wordlists/hotel.txt`
- [ ] any local-language wordlist relevant to region

## Daily routine
1. Morning: check Cardputer battery, SD space
2. During day: capture, note location/SSID/BSSID in logbook
3. Evening on Mac: pull SD, convert with `pcap2hash.sh`, run hashcat
4. End of day: `git commit` + push to `Atputhan/invention`

## Off-grid workflow (no WiFi)
- Cardputer standalone: scan, deauth, capture to SD
- Process on phone with Termux + aircrack-ng if Mac unavailable:
  ```
  apt install aircrack-ng tshark
  ```
