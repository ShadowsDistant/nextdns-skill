---
name: nextdns-api
description: Query and review NextDNS DNS query logs via the official API. Use when asked about DNS queries, blocked domains, allowed domains, device activity, or any NextDNS log analysis.
compatibility: Created for Zo Computer
metadata:
  author: shadowsdistant.zo.computer
---

# NextDNS API Skill

Integrates with the NextDNS API to pull DNS query logs and analytics.

## Setup

1. Get your API key from https://my.nextdns.io/account
2. Save it as `NEXTDNS_API_KEY` in [Settings > Advanced](/?t=settings&s=advanced) → Secrets

## Usage

The skill provides a Python CLI tool for querying logs and analytics.

### Commands

```bash
# Get recent logs (last 100 queries)
nextdns logs

# Get logs with filters
nextdns logs --status blocked --limit 50
nextdns logs --domain facebook.com
nextdns logs --device "iPhone" --from "-1h"

# Get analytics summary
nextdns analytics status
nextdns analytics domains --status blocked
nextdns analytics devices
nextdns analytics reasons

# List your profiles
nextdns profiles

# Get logs from a specific profile
nextdns logs --profile <profile_id>
```

### Filter Options

- `--status`: `default`, `blocked`, `allowed`, `error`
- `--domain`: Filter by domain name (partial match)
- `--device`: Filter by device name
- `--from`: Start time (e.g., `-1h`, `-1d`, `-7d`, `2024-01-01`)
- `--to`: End time
- `--limit`: Number of results (10-1000, default 100)
- `--raw`: Show all DNS queries including noise (default: filtered)
- `--profile`: Specify profile ID (default: first profile)

### Status Codes

- `default`: Normal query with no blocking
- `blocked`: Query was blocked
- `allowed`: Query was explicitly allowed
- `error`: DNS resolution error

## Script Location

`scripts/nextdns.py` - Main CLI tool

## References

- API Docs: https://nextdns.github.io/api/
- Account: https://my.nextdns.io/account
