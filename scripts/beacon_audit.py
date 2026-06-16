#!/usr/bin/env python3
"""
beacon_audit.py - quick AP inventory from a .pcapng/.pcap
Uses tshark to pull beacon frames. Flags WEP / Open / WPA1.

Usage:
  python beacon_audit.py input.pcapng
  python beacon_audit.py input.pcapng --json
"""
import argparse, subprocess, sys, json

def parse(pcap):
    cmd = ["tshark","-r",pcap,"-T","fields",
           "-e","wlan.bssid","-e","wlan.ssid",
           "-e","wlan.channel","-e","wlan.rsn.capabilities",
           "-e","wlan.capabilities","-Y","wlan.fc.type_subtype == 0x08"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        print("tshark not in PATH"); sys.exit(1)
    seen = {}
    for line in out.splitlines():
        p = line.split("\t")
        if len(p) < 4 or not p[0]: continue
        bssid = p[0].lower()
        if bssid in seen: continue
        ssid = p[1] or "<hidden>"
        chan = p[2]
        rsn = int(p[3], 16) if p[3] else 0
        cap = int(p[4], 16) if len(p) > 4 and p[4] else 0
        sec = "OPEN"
        if rsn & 0x0c: sec = "WPA2"
        elif rsn & 0x04: sec = "WPA2"
        if not (rsn & 0x0c) and not (rsn & 0x04):
            if (cap >> 4) & 0x01: sec = "WEP"
        seen[bssid] = (ssid, chan, sec, hex(rsn), hex(cap))
    return seen

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    aps = parse(args.pcap)
    if args.json:
        print(json.dumps([{"bssid":k,"ssid":v[0],"ch":v[1],"sec":v[2],"rsn":v[3],"cap":v[4]} for k,v in aps.items()], indent=2))
        return
    print(f"# {len(aps)} unique APs")
    print(f"{'BSSID':<18} {'CH':>3}  {'SEC':<5}  SSID")
    print("-"*60)
    for k in sorted(aps):
        ssid, chan, sec, rsn, cap = aps[k]
        print(f"{k:<18} {chan:>3}  {sec:<5}  {ssid}")
    sec_count = {}
    for v in aps.values(): sec_count[v[2]] = sec_count.get(v[2],0)+1
    print(f"\n# summary: {sec_count}")

if __name__ == "__main__":
    main()
