# hashcat Mode 22000 Cheatsheet (WPA/WPA2)

## Mode
- `-m 22000` : WPA-PBKDF2-PMKID+EAPOL (the new universal format since v6.2)

## Attack modes
| Flag  | Type                  | Example                                                |
|-------|-----------------------|--------------------------------------------------------|
| `-a 0`| Straight dictionary   | `hashcat -m 22000 h.22000 wordlist.txt`                |
| `-a 1`| Combinator            | `hashcat -m 22000 h.22000 w1.txt w2.txt`               |
| `-a 3`| Brute-force mask      | `hashcat -m 22000 h.22000 ?u?l?l?l?d?d?d?d`           |
| `-a 6`| Hybrid word + mask    | `hashcat -m 22000 h.22000 word.txt ?d?d?d?d`           |
| `-a 7`| Hybrid mask + word    | `hashcat -m 22000 h.22000 ?d?d?d?d word.txt`           |

## Mask charsets
| Code | Charset         |
|------|-----------------|
| `?l` | abcdefghijklmnopqrstuvwxyz |
| `?u` | ABCDEFGHIJKLMNOPQRSTUVWXYZ |
| `?d` | 0123456789      |
| `?s` | special chars   |
| `?a` | ?l?u?d?s        |
| `?b` | 0x00-0xff       |
| `-1 ?d?l` | custom 1   |

## Useful rules in `hashcat/rules/`
- `best64.rule`     - top 64 transforms
- `rockyou-30000.rule` - aggressive
- `dive.rule`       - deep ruleset
- `InsidePro-PasswordsPro.rule`

## Common flags
```
--status            - periodic status
--status-timer=10   - update every 10s
--restore-disable   - don't save resume
--session=name      - named session
--potfile-path=X    - custom potfile location
-O                  - optimized kernel (limited password length)
-w 4                - workload profile (1=low, 4=highest)
--force             - skip warning prompts
```

## WPA-PBKDF2 performance (rough, GTX 1660)
- Mode 22000: ~420 kH/s
- 8-char lower+digits (2.2e12 combos): ~90 days single-GPU
- Hotel-WiFi rockyou subset (top 1M): seconds to minutes

## Resume after crash
```
hashcat -m 22000 h.22000 wordlist.txt --restore
```
