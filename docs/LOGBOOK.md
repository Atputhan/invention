# Field Trip Logbook (2-week template)

| Date | Time | Lat,Lon | BSSID | SSID | Sec | Channel | Action | Outcome | Notes |
|------|------|---------|-------|------|-----|---------|--------|---------|-------|

Fill in as you go. When you crack, add the password column too.

## Daily housekeeping
- Backup `caps/` and `potfile/` to cloud daily
- Check `wordlists/` space
- Format SD card at start of week 2 to clear old captures
- Export cracked results as CSV from `wpa_summarize.py`

## Sync to Mac
- End of day: `git add . && git commit -m "day X captures" && git push`
- Mac pulls: `git pull origin master`

## Hard rules
- Only audit networks you own or have written authorization to test
- Hotel/cruise/airport WiFi: it's the property's network - do not attack
- Public hotspots: airodump OK for inventory, deauth NO
- Keep this logbook for legal proof of authorization when required
