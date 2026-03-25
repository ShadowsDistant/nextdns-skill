# NextDNS Skill for Zo Computer

[![Skill Version](https://img.shields.io/badge/Skill%20Version-2.0.0-blue.svg)](https://github.com/ShadowsDistant/nextdns-skill)
[![Platform](https://img.shields.io/badge/Platform-Zo%20Computer-6366f1.svg)](https://zo.computer)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-orange.svg)](https://python.org)
[![API](https://img.shields.io/badge/API-NextDNS-ff6b6b.svg)](https://nextdns.github.io/api/)

Full-featured NextDNS API integration for Zo Computer. Query logs, analyze DNS traffic, manage profiles, blocklists, and settings — all from the command line.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
  - [Profile Management](#profile-management)
  - [Settings](#settings)
  - [Denylist & Allowlist](#denylist--allowlist)
  - [Blocklists & Native Trackers](#blocklists--native-trackers)
  - [Logs](#logs)
  - [Analytics](#analytics)
- [Examples](#examples)
- [Time Series Analytics](#time-series-analytics)
- [Streaming Logs](#streaming-logs)
- [Troubleshooting](#troubleshooting)
- [API Documentation](#api-documentation)

---

## Overview

This skill provides complete access to the [NextDNS API](https://nextdns.github.io/api/), allowing you to:

- 📊 Query and analyze DNS traffic
- 🔴 Manage blocklists and deny/allow lists
- 👤 Create and manage profiles
- ⚙️ Configure security, privacy, and parental control settings
- 📈 Stream logs in real-time
- ⬇️ Download logs for offline analysis

---

## Features

### Profile Management
- ✅ List all profiles
- ✅ Get full profile details
- ✅ Create new profiles
- ✅ Delete profiles

### Settings Control
- ✅ Security settings (threat feeds, AI detection, etc.)
- ✅ Privacy settings (blocklists, native tracking protection)
- ✅ Parental controls (services, categories, safe search)
- ✅ Log settings (retention, location, IP/domain dropping)
- ✅ Performance settings (ECS, cache boost, CNAME flattening)

### List Management
- ✅ Denylist/Allowlist CRUD operations
- ✅ Blocklist enable/disable
- ✅ Native tracker protection (Apple, Samsung, Huawei, etc.)
- ✅ Toggle active status

### Logs & Analytics
- ✅ Query logs with filters (status, device, domain, time range)
- ✅ Real-time log streaming via SSE
- ✅ Download logs as files
- ✅ Clear logs
- ✅ 11 analytics endpoints with formatted output
- ✅ Time series data for charting
- ✅ GeoIP data for client IPs

---

## Prerequisites

1. **NextDNS Account** with API access
2. **API Key** from [my.nextdns.io/account](https://my.nextdns.io/account)
3. **Zo Computer** with the skill configured

---

## Installation

1. Add your API key to Zo:
   - Go to **Settings → Advanced → Secrets**
   - Add `NEXTDNS_API_KEY` with your key

2. The skill is located at:
   ```
   Skills/nextdns/skills/nextdns-api/scripts/nextdns.py
   ```

---

## Quick Start

```bash
# List your profiles
python nextdns.py profiles

# Get recent blocked queries
python nextdns.py logs --status blocked --limit 20

# Stream logs in real-time
python nextdns.py logs-stream

# Check analytics
python nextdns.py analytics status
python nextdns.py analytics devices
```

---

## Command Reference

### Profile Management

```bash
# List all profiles
python nextdns.py profiles

# Get full profile configuration
python nextdns.py profile-get --profile <id>

# Create a new profile
python nextdns.py profile-create --name "My New Profile"
python nextdns.py profile-create --name "Full Profile" --json-file profile.json

# Delete a profile
python nextdns.py profile-delete --profile <id>
python nextdns.py profile-delete --profile <id> --yes  # Skip confirmation
```

### Settings

```bash
# Get settings sections
python nextdns.py settings-get security
python nextdns.py settings-get privacy
python nextdns.py settings-get parentalControl
python nextdns.py settings-get settings/logs
python nextdns.py settings-get settings/performance
python nextdns.py settings-get settings/blockPage

# Update settings via JSON file
python nextdns.py settings-update security --json-file security.json

# Update single setting
python nextdns.py settings-update privacy --key disguisedTrackers --value true
```

### Denylist & Allowlist

```bash
# View lists
python nextdns.py list-get denylist
python nextdns.py list-get allowlist

# Add domains
python nextdns.py list-add denylist tracking-site.com
python nextdns.py list-add allowlist trusted-site.com
python nextdns.py list-add denylist temp-block.com --inactive  # Add disabled

# Remove domains
python nextdns.py list-remove denylist tracking-site.com

# Toggle active status
python nextdns.py list-toggle denylist tracking-site.com --active false
```

### Blocklists & Native Trackers

```bash
# View enabled blocklists/natives
python nextdns.py blocklists-get blocklists
python nextdns.py blocklists-get natives

# Add blocklist
python nextdns.py blocklists-add blocklists nextdns-recommended
python nextdns.py blocklists-add blocklists oisd

# Enable native tracking protection
python nextdns.py blocklists-add natives apple
python nextdns.py blocklists-add natives samsung
python nextdns.py blocklists-add natives huawei

# Remove blocklist/native
python nextdns.py blocklists-remove blocklists oisd
python nextdns.py blocklists-remove natives samsung
```

### Logs

```bash
# Basic log query
python nextdns.py logs
python nextdns.py logs --limit 500

# Filter by status
python nextdns.py logs --status blocked
python nextdns.py logs --status allowed
python nextdns.py logs --status error

# Filter by domain
python nextdns.py logs --domain facebook.com
python nextdns.py logs --domain google.com --status blocked

# Filter by device
python nextdns.py logs --device "John's iPhone"
python nextdns.py logs --device "__UNIDENTIFIED__"

# Time range filtering
python nextdns.py logs --from -1h          # Last hour
python nextdns.py logs --from -1d --to now  # Last 24 hours
python nextdns.py logs --from -7d        # Last week

# Show all query types (not just navigational)
python nextdns.py logs --raw

# Pagination
python nextdns.py logs --cursor <cursor_value>
```

### Log Streaming & Management

```bash
# Stream logs in real-time (SSE)
python nextdns.py logs-stream
python nextdns.py logs-stream --status blocked  # Only blocked
python nextdns.py logs-stream --device "iPhone"

# Resume streaming from specific ID
python nextdns.py logs-stream --stream-id <id>

# Download logs
python nextdns.py logs-download
python nextdns.py logs-download --output logs.json
python nextdns.py logs-download --no-redirect  # Get URL only

# Clear all logs
python nextdns.py logs-clear --yes
```

### Analytics

#### Basic Analytics

```bash
# Query status breakdown
python nextdns.py analytics status

# Top domains
python nextdns.py analytics domains
python nextdns.py analytics domains --limit 50
python nextdns.py analytics domains --root  # Root domains only

# Block reasons
python nextdns.py analytics reasons
python nextdns.py analytics reasons --limit 20

# Protocol usage
python nextdns.py analytics protocols

# Query types
python nextdns.py analytics queryTypes

# Client IPs (with GeoIP)
python nextdns.py analytics ips
python nextdns.py analytics ips --limit 20

# IP versions
python nextdns.py analytics ipVersions

# DNSSEC validation
python nextdns.py analytics dnssec

# Encryption status
python nextdns.py analytics encryption

# Per-device stats
python nextdns.py analytics devices
python nextdns.py analytics devices --limit 20

# Destination countries
python nextdns.py analytics destinations --dest-type countries

# Big Tech (GAFAM) queries
python nextdns.py analytics destinations --dest-type gafam
```

#### Time Range Filtering

```bash
# Filter by time range
python nextdns.py analytics domains --from -1d
python nextdns.py analytics status --from -7d --to now
python nextdns.py analytics devices --from -24h --device "iPhone"
```

---

## Time Series Analytics

Get time-series data for charting by adding `--series`:

```bash
# Status over time
python nextdns.py analytics status --series

# Hourly domain stats for last 24 hours
python nextdns.py analytics domains --series --from -1d --interval 1h

# Daily protocol usage for last week
python nextdns.py analytics protocols --series --from -7d --interval 1d

# Clock-aligned with timezone
python nextdns.py analytics devices --series \
  --alignment clock \
  --timezone America/New_York \
  --from -1d \
  --interval 1h
```

### Time Series Options

| Option | Description |
|--------|-------------|
| `--series` | Enable time series mode |
| `--interval` | Window size (e.g., `1h`, `1d`, `86400`) |
| `--alignment` | `start`, `end`, or `clock` |
| `--timezone` | IANA timezone name (e.g., `America/New_York`) |
| `--partials` | Include partial windows: `none`, `start`, `end`, `all` |

---

## Examples

### Monitor Blocked Ads in Real-Time

```bash
python nextdns.py logs-stream --status blocked
```

### Check What's Being Blocked

```bash
# Top blocked domains
python nextdns.py analytics domains --status blocked --limit 20

# Which blocklists are active
python nextdns.py analytics reasons --limit 10
```

### Device-Specific Analysis

```bash
# Get device ID from logs
python nextdns.py logs --limit 1

# Analytics for specific device
python nextdns.py analytics domains --device <device_id>
python nextdns.py analytics status --device <device_id>
```

### Export Logs for Analysis

```bash
# Download logs
python nextdns.py logs-download --output nextdns-logs.json

# Then analyze with jq or other tools
jq '.[] | select(.status == "blocked") | .domain' nextdns-logs.json
```

### Enable New Blocklist

```bash
python nextdns.py blocklists-add blocklists oisd
```

### Check DNS Security

```bash
# DNSSEC validation rates
python nextdns.py analytics dnssec

# Encryption usage
python nextdns.py analytics encryption

# Protocol distribution
python nextdns.py analytics protocols
```

---

## Troubleshooting

### API Key Issues

**Error:** `NEXTDNS_API_KEY not found`
- Add your API key in **Settings → Advanced → Secrets**
- Ensure it's named exactly `NEXTDNS_API_KEY`

### No Data Returned

- Check that your profile ID is correct
- Verify time range parameters use valid formats (`-1h`, `-1d`, ISO 8601)
- Use `profiles` command to see available profiles

### Rate Limiting

- The API has rate limits. If you hit them, wait a few minutes
- Use streaming for real-time data instead of polling

### Device Filtering

- Use `__UNIDENTIFIED__` for unidentified devices
- Device names are case-sensitive

---

## API Documentation

For full API reference, see:
- [NextDNS API Docs](https://nextdns.github.io/api/)
- [NextDNS Help Center](https://help.nextdns.io/)

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

**Made for [Zo Computer](https://zo.computer)**
