# NextDNS Skill for Zo Computer

Query NextDNS DNS logs and analytics via CLI.

## Setup

1. Get your NextDNS API key from [nextdns.io](https://nextdns.io)
2. Add it to Zo: **Settings → Advanced → Secrets** as `NEXTDNS_API_KEY`

## Usage

```bash
python scripts/nextdns.py profiles
python scripts/nextdns.py logs --limit 50
python scripts/nextdns.py logs --status blocked --limit 20
python scripts/nextdns.py logs --domain example.com
python scripts/nextdns.py analytics status
python scripts/nextdns.py analytics domains --limit 10
python scripts/nextdns.py analytics devices
```

## Commands

| Command | Description |
|---------|-------------|
| `profiles` | List all NextDNS profiles |
| `logs` | Fetch DNS query logs |
| `analytics <endpoint>` | Fetch analytics data |

### Log Filters

- `--profile <id>` — Use specific profile (default: first profile)
- `--status` — Filter by `blocked`, `allowed`, `default`, `error`
- `--domain` — Filter by domain name
- `--device` — Filter by device name
- `--from` / `--to` — Time range (`-1h`, `-1d`, `-7d`)
- `--limit` — Number of results (10–1000)
- `--raw` — Show all DNS queries (including noise)

### Analytics Endpoints

- `status` — Allowed vs blocked queries
- `domains` — Top domains by query volume
- `devices` — Queries by device
- `reasons` — Block reasons
- `protocols` — DNS protocol distribution
- `queryTypes` — Query type distribution
- `ips` — Client IP addresses
- `destinations` — Upstream DNS servers

## Files

- `SKILL.md` — Zo skill specification
- `nextdns.py` — CLI script
