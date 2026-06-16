#!/usr/bin/env python3
"""
hotel_wardict.py - generate a candidate wordlist tuned for hotel/airport/cruise WiFi.
Pure stdlib. No external deps.

Usage:
  python hotel_wardict.py > wordlist.txt
  python hotel_wardict.py --min 4 --max 12 --top 5000 > top.txt
"""
import argparse, itertools, string, random, sys

HOTEL_WORDS = [
    "room","rooms","suite","guest","hotel","lobby","wifi","wireless",
    "stay","welcome","frontdesk","concierge","resort","spa","pool",
    "guestroom","housekeeping","reservation","checkin","checkout"
]
BRAND_WORDS = [
    "marriott","hilton","hyatt","sheraton","westin","ritz","ritzcarlton",
    "ihg","ihgrewards","holidayinn","hiexpress","doubletree","hampton",
    "radisson","bestwestern","bwi","wyndham","laquinta","comfortinn",
    "fairfield","courtyard","residenceinn","springhill","aloft","moxy",
    "ritz","conrad","waldorf","omni","loews","kimpton","fourpoints",
    "embassysuites","home2","homewood","candlewood","staybridge"
]
AIRLINE_WORDS = [
    "delta","united","american","southwest","jetblue","alaska","spirit",
    "frontier","aircanada","british","lufthansa","klm","emirates",
    "qatar","etihad","cathay","ana","jal","singa","aeroflot"
]
AIRPORT_WORDS = [
    "lax","sfo","jfk","ord","dfw","atl","den","mco","las","phx",
    "sea","bwi","iad","mia","mco","ewr","boston","logan","heathrow",
    "gatwick","cdg","frankfurt","munich","narita","haneda","changi"
]
CRUISE_WORDS = [
    "carnival","royal","ncl","princess","celebrity","disney","holland",
    "msc","virginvoyages","cunard","port","deck","cabin","stateroom",
    "lifeboat","captain","mast","bridge","shorex","excursion","atrium"
]
SHAPES_NUM = [str(n) for n in range(0, 10)] + [str(n) for n in range(100)]
SHAPES_YEAR = [str(y) for y in range(2018, 2028)]
SHAPES_MONTH = [f"{m:02d}" for m in range(1,13)]
SEPS = ["","!","#","@","$","*",".","-","_"]

def gen(parts_list, min_len, max_len, top, cap, leet):
    seen, out = set(), []
    for parts in parts_list:
        for combo in itertools.product(parts, [0,1,2,3,4]):
            base = "".join(combo)
            if leet:
                base = base.translate(str.maketrans("aeiosAEIOS","43105S",""))
            for w in [base, base.lower(), base.upper(), base.capitalize()]:
                for s in SEPS:
                    for tail in [""] + SHAPES_NUM[:20]:
                        cand = w + s + tail
                        if min_len <= len(cand) <= max_len and cand not in seen:
                            seen.add(cand)
                            out.append(cand)
                            if len(out) >= top: return out
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=6)
    ap.add_argument("--max", type=int, default=14)
    ap.add_argument("--top", type=int, default=20000)
    ap.add_argument("--cap", type=int, default=4, help="max parts to combine")
    ap.add_argument("--leet", action="store_true")
    args = ap.parse_args()
    parts = [HOTEL_WORDS, BRAND_WORDS, AIRLINE_WORDS, AIRPORT_WORDS, CRUISE_WORDS]
    for w in gen(parts, args.min, args.max, args.top, args.cap, args.leet):
        print(w)

if __name__ == "__main__":
    main()
