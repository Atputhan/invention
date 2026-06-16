#!/usr/bin/env bash
# crack.sh - smart hashcat runner for the trip
# Usage: crack.sh path/to/file.22000 [wordlist]
#        crack.sh path/to/file.pcapng rockyou.txt  # auto-converts
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WL="${2:-$ROOT/wordlists/rockyou.txt}"
TARGET="$1"
case "$TARGET" in
  *.pcap|*.pcapng)
    HASH="${TARGET%.*}.22000"
    "$ROOT/scripts/pcap2hash.sh" "$TARGET" "$HASH"
    TARGET="$HASH"
    ;;
esac
hashcat -m 22000 -a 0 "$TARGET" "$WL" \
  --potfile-path "$ROOT/potfile/hashcat.potfile" \
  --session "$ROOT/logs/session-$(date +%Y%m%d-%H%M%S)" \
  "$@"
