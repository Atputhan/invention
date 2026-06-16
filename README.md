# invention

GHOST - WiFi Handshake Cracking Toolkit + Cardputer ADV field kit

## Trip-ready. 2-week self-contained workflow.

Everything in this repo is cross-platform Python or shell scripts. Mac clone + brew and you're running.

```
invention/
  bin/                  hashcat + git + helper launchers
  hashcat/hashcat-7.1.2/  full Win64 hashcat tree
  scripts/              pcapng_to_22000.py, hotel_wardict.py,
                        pcapng_split.py, wpa_summarize.py,
                        beacon_audit.py, crack.sh
  cheatsheets/          tshark-filters.md, hashcat-22000.md,
                        cardputer-adv-firmwares.md,
                        porkchop-to-hashcat.md
  docs/                 CHECKLIST.md (pre-trip), LOGBOOK.md (daily)
  caps/                 drop Cardputer porkchop .pcapng here
  hashes/               converted .22000 handshakes
  potfile/              hashcat recovered passwords
  out/                  cracked results
  logs/                 session logs
```

Authorized WPA/WPA2-PSK recovery pipeline. Cardputer ADV porkchop captures
through hashcat on the host GPU. **Only run on networks you own or have
explicit written authorization to test.**

## Hardware Baseline (this machine)

- CPU: Intel i5-9400F (6c/6t)
- GPU: NVIDIA GeForce GTX 1660 (OpenCL 3.0 via CUDA 12.6.41)
- OS:   Windows 10 19045

## Layout

```
tools/
  bin/                  staged runtime on PATH
    hashcat.exe         v7.1.2
    git.exe             v2.47.1 (portable)
    7zr.exe             7-Zip CLI (extraction)
  hashcat/hashcat-7.1.2/  full hashcat tree (run from here, needs OpenCL/ siblings)
  git/                    full portable-git tree
  hcxtools/7zr.exe        archive helper
  wordlists/rockyou.txt   134 MB classic wordlist
  caps/                   drop Cardputer porkchop .pcapng here
  hashes/                 converted .22000 handshakes
  potfile/                hashcat recovered passwords
  out/                    cracked results
  logs/                   session logs
```

## Workflow (end-to-end)

### 1. Capture on Cardputer ADV with porkchop

Capture WPA2 4-way handshake to SD card. Transfer `.pcap` / `.pcapng` from
the SD to `tools/caps/`. File naming suggestion: `<bssid>_<channel>_<date>.pcapng`.

### 2. Convert to hashcat format (mode 22000)

Modern hashcat (>= 6.2) reads pcapng **directly**. No hcxtools required on
Windows since upstream dropped the binary. If you ever need PMKID-only
filtering or mass batch ops, use `hcxhashtool` from WSL/Linux.

```powershell
cd C:\tools\hashcat\hashcat-7.1.2
.\hashcat.exe -m 22000 C:\tools\caps\<file>.pcapng C:\tools\wordlists\rockyou.txt
```

Hashcat writes the auto-converted hash to `hashcat.potfile` and shows the
first cracks inline. No manual conversion step.

### 3. Cracking modes

| Goal                        | Command                                                                |
|-----------------------------|------------------------------------------------------------------------|
| Dictionary (rockyou)        | `.\hashcat.exe -m 22000 -a 0 hash.22000 wordlists\rockyou.txt`         |
| Rules + dictionary          | `.\hashcat.exe -m 22000 -a 0 hash.22000 wordlists\rockyou.txt -r rules\best64.rule` |
| Brute-force 8-10 char       | `.\hashcat.exe -m 22000 -a 3 hash.22000 ?1?1?1?1?1?1?1?1 -1 ?l?d`      |
| Mask top 20k password shape | `.\hashcat.exe -m 22000 -a 3 hash.22000 masks\top-20k.hcmask`          |
| Hybrid (word + 4 digits)    | `.\hashcat.exe -m 22000 -a 6 hash.22000 wordlists\rockyou.txt ?d?d?d?d` |

### 4. Inspect / show cracked

```powershell
type C:\tools\hashcat\hashcat-7.1.2\hashcat.potfile
```

## Sync to Mac

This repo is pushed to `github.com/IceMan6ix/GHOST`. On the Mac:

```bash
git clone https://github.com/IceMan6ix/GHOST.git ~/tools
# Windows toolchain binaries are .exe-only; for cracking on Mac:
brew install hashcat john
# caps/ hashes/ wordlists/ scripts/ are cross-platform
```

## Legal

WPA password recovery on networks you do not own or have written
authorization to test is a crime in most jurisdictions. The author
assumes no liability for misuse.

## Trip workflow (Cardputer ADV + Mac)

1. **Day prep:** see `docs/CHECKLIST.md`
2. **Capture:** run Marauder/Bruce/Porkchop on device, SD stores `.pcapng`
3. **Pull:** swap SD to Mac, `cp /Volumes/SD/cap.pcapng caps/`
4. **Convert:** `scripts/pcap2hash.sh caps/cap.pcapng`
5. **Crack:** `scripts/crack.sh caps/cap.22000 wordlists/hotel.txt`
6. **Summarize:** `python scripts/wpa_summarize.py caps/cap.22000`
7. **Log:** append row to `docs/LOGBOOK.md`
8. **Sync:** `git commit -am "day N" && git push`
>>>>>>> 7d96bab (init: GHOST WiFi handshake cracking toolkit)
