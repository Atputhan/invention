#!/usr/bin/env python3
"""
pcapng_split.py - split a big .pcapng into per-BSSID .pcapng files
Useful when one porkchop capture has handshakes from dozens of APs.
Pure Python, uses tshark.

Usage:
  python pcapng_split.py input.pcapng out_dir/
  python pcapng_split.py input.pcapng out_dir/ --only "bssid eq aa:bb:cc:dd:ee:ff"
"""
import argparse, os, subprocess, sys
from collections import defaultdict

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap")
    ap.add_argument("out")
    ap.add_argument("--only", default=None)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    cmd = ["tshark","-r",args.pcap,"-T","fields","-e","wlan.bssid","-Y","wlan.bssid"]
    try:
        rows = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.splitlines()
    except FileNotFoundError:
        print("tshark not in PATH"); sys.exit(1)
    bssids = sorted({b.strip().lower() for b in rows if b.strip()})
    print(f"# {len(bsids)} unique BSSIDs in capture")
    written = 0
    for b in bssids:
        if args.only and b != args.only.lower(): continue
        safe = b.replace(":","-")
        out = os.path.join(args.out, f"{safe}.pcapng")
        cmd2 = ["tshark","-r",args.pcap,"-Y",f"wlan.bssid == {b}","-w",out]
        subprocess.run(cmd2, capture_output=True, check=False)
        if os.path.exists(out) and os.path.getsize(out) > 0:
            written += 1
            print(f"  {b} -> {out}")
    print(f"# wrote {written} files")

if __name__ == "__main__":
    main()
