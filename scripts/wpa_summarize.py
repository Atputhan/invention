#!/usr/bin/env python3
"""
wpa_summarize.py - summarize a hashcat .potfile or .22000 file into
markdown table: BSSID, ESSID, password, handshake type.

Usage:
  python wpa_summarize.py hashcat.potfile > cracked.md
  python wpa_summarize.py hashes.22000
"""
import sys, re, os, subprocess, json

def load_pmkid_dict(hashfile):
    """Read 22000 hash and extract BSSID + ESSID by parsing pcapng sibling."""
    pmk = {}
    for line in open(hashfile):
        line = line.strip()
        if not line.startswith("WPA*"): continue
        p = line.split("*")
        if len(p) < 5: continue
        bssid = p[3]
        pmk[bssid] = pmk.get(bssid, 0) + 1
    return pmk

def load_potfile(potfile):
    cracks = {}
    if not os.path.exists(potfile): return cracks
    for line in open(potfile):
        line = line.strip()
        if not line: continue
        # 22000 potfile: hash:password  where hash is the hash string
        if ":" in line:
            h, pw = line.rsplit(":", 1)
            # extract bssid from h (WPA*02*mic*bssid*...)
            if h.startswith("WPA*"):
                p = h.split("*")
                if len(p) >= 4:
                    cracks.setdefault(p[3].lower(), []).append(pw)
    return cracks

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "hashcat.potfile"
    pot = target if target.endswith(".potfile") else os.path.splitext(target)[0] + ".potfile"
    # If user passed .22000, derive sibling .potfile path
    if target.endswith(".22000") and not os.path.exists(pot):
        pot = "hashcat.potfile"
    pmk = load_pmkid_dict(target) if target.endswith(".22000") else {}
    cracks = load_potfile(pot)
    print("| BSSID | Password | # hits |")
    print("|-------|----------|-------|")
    for b, pws in sorted(cracks.items()):
        for pw in pws:
            print(f"| {b} | `{pw}` | {pmk.get(b,'-')} |")
    if not cracks:
        print(f"| (no cracks yet in {pot}) | | |")

if __name__ == "__main__":
    main()
