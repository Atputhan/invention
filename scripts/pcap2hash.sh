#!/usr/bin/env bash
# pcap2hash.sh - one-shot: .pcapng -> 22000 hash, ready for hashcat
# Deps: tshark
set -euo pipefail
PCAP="${1:-}"
OUT="${2:-}"
if [[ -z "$PCAP" || ! -r "$PCAP" ]]; then
  echo "usage: $0 input.pcapng [output.22000]" >&2
  exit 1
fi
OUT="${OUT:-${PCAP%.pcapng}.22000}"
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/pcapng_to_22000.py" --beacon-info "$PCAP" "$OUT"
