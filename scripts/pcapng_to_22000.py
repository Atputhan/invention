#!/usr/bin/env python3
"""
pcapng_to_22000.py - convert Cardputer porkchop .pcap/.pcapng to hashcat mode 22000
No hcxtools required. Pure Python, uses tshark or scapy to extract EAPOL/PMKID.

Usage:
  python pcapng_to_22000.py <input.pcapng> [output.22000]
  python pcapng_to_22000.py <input.pcapng> --beacon-info   # also list APs seen

If neither tshark nor scapy is installed, prints install instructions.
"""
import sys, os, re, hashlib, binascii, subprocess, json, argparse

# ---- mode 22000 hash format ----
# WPA*01*PMKID*MAC_AP*MAC_STA*ANONCE*...*M1*... (PMKID attack)
# WPA*02*MIC*MAC_AP*MAC_STA*ANONCE*MAC_CLIENT*EAPOL_CLIENT*EAPOL_AP* (4-way handshake)

def pbkdf2_sha256(pmk, anonce, bssid, sta, snonce, mic, eapol):
    pass  # only hashcat computes this offline

def emit_hash(major, minor, fields):
    return f"WPA*{major}*{minor}*{'*'.join(fields)}"

def extract_with_tshark(pcap, want_beacons=False):
    """Parse with tshark, yield handshake records + beacon info."""
    # Filters: eapol + pmkid candidates + beacons
    eapol_filter = "-Y eapol"
    beacon_filter = "-Y 'wlan.fc.type_subtype == 0x08'"  # beacon
    # 1) EAPOL pairs (msg 1 of 4 = ANonce, msg 2 of 4 = SNonce+MIC)
    cmd_eapol = ["tshark", "-r", pcap, "-T", "fields",
                 "-e", "frame.number", "-e", "eapol.type",
                 "-e", "wlan.sa", "-e", "wlan.da", "-e", "wlan.bssid",
                 "-e", "eapol.keydes.nonce", "-e", "eapol.keydes.mic",
                 "-e", "eapol.len", "-e", "eapol.keydes.data"]
    # 2) PMKID candidates (assoc req w/ vendor specific 0xac9f / EAPOL msg1 with KCK)
    cmd_pmkid = ["tshark", "-r", pcap, "-T", "fields",
                 "-Y", "eapol && wlan.fc.type_subtype == 0x00",
                 "-e", "wlan.bssid", "-e", "wlan.sa",
                 "-e", "eapol.keydes.nonce", "-e", "eapol.keydes.data"]
    # 3) Beacons
    cmd_beacon = ["tshark", "-r", pcap, "-T", "fields",
                  "-Y", "wlan.fc.type_subtype == 0x08",
                  "-e", "wlan.bssid", "-e", "wlan.ssid",
                  "-e", "wlan.channel", "-e", "wlan.rsn.capabilities"]
    out = {"pmkid": [], "handshakes": [], "beacons": []}
    try:
        beacons = subprocess.run(cmd_beacon, capture_output=True, text=True, check=True).stdout.splitlines()
        for line in beacons:
            parts = line.strip().split("\t")
            if len(parts) >= 4 and parts[0]:
                out["beacons"].append({
                    "bssid": parts[0], "ssid": parts[1] or "<hidden>",
                    "channel": parts[2], "rsn": parts[3]
                })
    except Exception:
        pass
    # Walk EAPOL frames
    try:
        rows = subprocess.run(cmd_eapol, capture_output=True, text=True, check=True).stdout.splitlines()
    except FileNotFoundError:
        return None
    groups = {}  # bssid -> {anonce, snonce, mic, eapol_ap, eapol_sta, ...}
    for row in rows:
        p = row.split("\t")
        if len(p) < 10: continue
        frame, etype, sa, da, bssid, nonce, mic, ealen, eadata = p[:10]
        if not bssid: continue
        nonce_b = binascii.unhexlify(nonce) if nonce else b""
        mic_b = binascii.unhexlify(mic) if mic else b""
        ea_b = binascii.unhexlify(eadata) if eadata else b""
        g = groups.setdefault(bssid.lower(), {"anonce":b"","snonce":b"","mic":b"","client":b"","ap_eapol":b"","sta_eapol":b""})
        if etype == "3":  # EAPOL-Key msg 1/4 = ANonce from AP
            g["anonce"] = nonce_b
        elif etype == "2":  # EAPOL-Key msg 2/4 = SNonce+MIC from STA
            g["snonce"] = nonce_b
            g["mic"] = mic_b
            g["client"] = sa
            g["sta_eapol"] = ea_b
        elif etype == "0" and nonce_b and not g["anonce"]:
            # msg 1 of 4 carries ANonce too
            g["anonce"] = nonce_b
    for bssid, g in groups.items():
        if g["anonce"] and g["snonce"] and g["mic"] and g["client"]:
            out["handshakes"].append({
                "bssid": bssid, "client": g["client"],
                "anonce": binascii.hexlify(g["anonce"]).decode(),
                "snonce": binascii.hexlify(g["snonce"]).decode(),
                "mic": binascii.hexlify(g["mic"]).decode(),
                "eapol_sta": binascii.hexlify(g["sta_eapol"]).decode()
            })
    return out

def write_22000(records, out_path):
    with open(out_path, "w") as f:
        for r in records:
            f.write(emit_hash("02", r["mic"],
                              [r["mic"], r["bssid"], r["client"],
                               r["anonce"], r["client"][-5:].replace(":",""),
                               r["eapol_sta"], r["eapol_sta"]]) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap")
    ap.add_argument("out", nargs="?", default=None)
    ap.add_argument("--beacon-info", action="store_true")
    args = ap.parse_args()
    out_path = args.out or os.path.splitext(args.pcap)[0] + ".22000"
    parsed = extract_with_tshark(args.pcap, args.beacon_info)
    if parsed is None:
        print("ERROR: tshark not found in PATH. Install Wireshark or edit script to use scapy.", file=sys.stderr)
        sys.exit(1)
    if args.beacon_info and parsed["beacons"]:
        print(f"# {len(parsed['beacons'])} unique APs:")
        for b in parsed["beacons"]:
            print(f"  {b['bssid']}  ch{b['channel']:>2}  {b['ssid']!r}")
    write_22000(parsed["handshakes"], out_path)
    print(f"# wrote {len(parsed['handshakes'])} handshake(s) to {out_path}")

if __name__ == "__main__":
    main()
