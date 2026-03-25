# NextDNS Skill for Zo Computer

<div align="center">

[![Skill Version](https://img.shields.io/badge/Skill%20Version-1.1.0-blue.svg)](https://github.com/ShadowsDistant/nextdns-skill)
[![Platform](https://img.shields.io/badge/Platform-Zo%20Computer-6366f1.svg)](https://zo.computer)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-orange.svg)](https://python.org)
[![NextDNS API](https://img.shields.io/badge/NextDNS%20API-v2-Badge?logo=nextdns)](https://nextdns.github.io/api/)

**Query DNS logs and analytics, manage profiles, blocklists, allowlists, and settings via CLI.**

</div>

---

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Command Reference](#command-reference)
- [Output Examples](#output-examples)
- [Profile Management](#profile-management)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)

---

## Features

- 📊 **Analytics** — Query status, domains, devices, protocols, query types, IPs, DNSSEC, encryption, and destinations
- 📜 **Logs** — Browse, filter, stream live, download, and clear DNS query logs
- 👥 **Profile Management** — Create, view, update, and delete NextDNS profiles
- 🚫 **Blocklist/Denylist** — Add/remove domains from your blocklist
- ✅ **Allowlist** — Manage domains that should never be blocked
- ⚙️ **Settings** — Configure logging, performance, security, privacy, and parental controls
- 🔒 **Security** — Threat intelligence feeds, AI threat detection, safe browsing
- 🛡️ **Parental Controls** — Service blocking, content categories, safe search

---

## Setup

### 1. Get Your NextDNS API Key

1. Log in to your NextDNS account at [my.nextdns.io](https://my.nextdns.io/account)
2. Scroll to the bottom of the page
3. Copy your API key

### 2. Add API Key to Zo

Navigate to **Settings → Advanced → Secrets** and add:

| Key | Value |
|-----|-------|
| `NEXTDNS_API_KEY` | Your NextDNS API key |

### 3. Usage

```bash
python scripts/nextdns.py <command> [options]
```

---

## Usage

### Quick Examples

```bash
# List all profiles
python scripts/nextdns.py profiles

# Get recent DNS logs
python scripts/nextdns.py logs --limit 50

# Get blocked queries only
python scripts/nextdns.py logs --status blocked --limit 20

# Search logs for specific domain
python scripts/nextdns.py logs --domain example.com

# Get analytics by status
python scripts/nextdns.py analytics status

# Get top domains by queries
python scripts/nextdns.py analytics domains --limit 10

# Get device breakdown
python scripts/nextdns.py analytics devices

# Get query type distribution
python scripts/nextdns.py analytics queryTypes

# Check DNSSEC validation status
python scripts/nextdns.py analytics dnssec

# Get encryption stats
python scripts/nextdns.py analytics encryption

# Get IP/geo analytics
python scripts/nextdns.py analytics ips --limit 10

# Get destination countries
python scripts/nextdns.py analytics destinations

# Get GAFAM company tracking
python scripts/nextdns.py analytics destinations --type gafam

# Get top blocking reasons
python scripts/nextdns.py analytics reasons --limit 10

# Stream live logs (Ctrl+C to stop)
python scripts/nextdns.py logs --stream

# Download logs as JSONL
python scripts/nextdns.py logs --download

# Clear all logs
python scripts/nextdns.py logs --clear

# View profile settings
python scripts/nextdns.py settings

# Update specific settings
python scripts/nextdns.py settings --patch-logs '{"enabled": true, "retention": 7776000}'

# View security settings
python scripts/nextdns.py security

# Update security settings
python scripts/nextdns.py security --patch '{"threatIntelligenceFeeds": true, "googleSafeBrowsing": false}'

# View privacy settings
python scripts/nextdns.py privacy

# Update privacy settings
python scripts/nextdns.py privacy --patch '{"disguisedTrackers": true}'

# View parental controls
python scripts/nextdns.py parental

# Update parental controls
python scripts/nextdns.py parental --patch '{"safeSearch": true, "youtubeRestrictedMode": true}'

# Manage denylist
python scripts/nextdns.py denylist
python scripts/nextdns.py denylist --add badsite.com
python scripts/nextdns.py denylist --remove badsite.com

# Manage allowlist
python scripts/nextdns.py allowlist
python scripts/nextdns.py allowlist --add goodsite.com
python scripts/nextdns.py allowlist --remove goodsite.com

# Create/delete profiles
python scripts/nextdns.py create-profile --name "My New Profile"
python scripts/nextdns.py delete-profile --profile <profile_id>
```

---

## Command Reference

### Global Options

| Option | Description |
|--------|-------------|
| `--profile <id>` | Use specific profile ID (default: first profile) |
| `--help`, `-h` | Show help for command |

---

### Profiles

```bash
python scripts/nextdns.py profiles
```

List all NextDNS profiles.

**Output:**
```
ID                   Name
-----------------------------------------------------
abc123def            My Profile
456xyz789            Work Profile
```

---

### Logs

```bash
python scripts/nextdns.py logs [options]
```

Fetch DNS query logs.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--status` | string | | Filter: `default`, `blocked`, `allowed`, `error` |
| `--domain` | string | | Filter by domain name |
| `--device` | string | | Filter by device name |
| `--from` | string | | Start time (`-1h`, `-1d`, `-7d`, `now`) |
| `--to` | string | | End time |
| `--limit` | int | 100 | Results (10-1000) |
| `--sort` | string | desc | Sort: `asc`, `desc` |
| `--raw` | flag | false | Show all DNS queries (including noise) |
| `--stream` | flag | false | Stream live logs |
| `--download` | flag | false | Download logs as JSONL |
| `--clear` | flag | false | Clear all logs |
| `--cursor` | string | | Pagination cursor |

---

### Analytics

```bash
python scripts/nextdns.py analytics <endpoint> [options]
```

Fetch analytics data.

| Endpoint | Description |
|----------|-------------|
| `status` | Query status breakdown (default, blocked, allowed) |
| `domains` | Top domains by query volume |
| `devices` | Device breakdown |
| `protocols` | DNS protocol breakdown (DoH, DoT, UDP) |
| `queryTypes` | DNS query type distribution (A, AAAA, HTTPS, etc.) |
| `ips` | Top IP addresses by queries |
| `reasons` | Top blocking reasons |
| `destinations` | Top destination countries |
| `ipVersions` | IPv4 vs IPv6 breakdown |
| `dnssec` | DNSSEC validation status |
| `encryption` | Encrypted vs unencrypted queries |

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--status` | string | | Filter: `default`, `blocked`, `allowed` |
| `--root` | flag | false | Show root domains only |
| `--type` | string | | For `destinations`: `countries` or `gafam` |
| `--limit` | int | 10 | Number of results (1-500) |
| `--from` | string | | Start time |
| `--to` | string | | End time |
| `--series` | flag | false | Return time series data |

---

### Settings

```bash
python scripts/nextdns.py settings [options]
```

View and update profile settings.

| Option | Description |
|--------|-------------|
| `--view` | View current settings (default) |
| `--patch` | Update settings (JSON) |
| `--logs` | Target logs settings |
| `--performance` | Target performance settings |
| `--blockPage` | Target block page settings |

**Settings Structure:**
```json
{
  "logs": {
    "enabled": true,
    "drop": { "ip": false, "domain": false },
    "retention": 7776000,
    "location": "eu"
  },
  "blockPage": { "enabled": true },
  "performance": {
    "ecs": true,
    "cacheBoost": false,
    "cnameFlattening": true
  },
  "web3": true
}
```

---

### Security

```bash
python scripts/nextdns.py security [options]
```

Manage security settings.

| Option | Description |
|--------|-------------|
| `--view` | View current security settings (default) |
| `--patch` | Update security settings (JSON) |

**Available Security Options:**
| Setting | Description |
|---------|-------------|
| `threatIntelligenceFeeds` | Block malicious domains via threat intel feeds |
| `aiThreatDetection` | AI-powered threat detection |
| `googleSafeBrowsing` | Google Safe Browsing |
| `cryptojacking` | Block cryptojacking domains |
| `dnsRebinding` | Block DNS rebinding attacks |
| `idnHomographs` | Block IDN homograph attacks |
| `typosquatting` | Block typosquatting domains |
| `dga` | Block DGA (domain generation algorithm) |
| `nrd` | Block newly registered domains |
| `ddns` | Block dynamic DNS domains |
| `parking` | Block parked domains |
| `csam` | Block CSAM content |
| `tlds` | Block specific TLDs |

---

### Privacy

```bash
python scripts/nextdns.py privacy [options]
```

Manage privacy settings.

| Option | Description |
|--------|-------------|
| `--view` | View current privacy settings (default) |
| `--patch` | Update privacy settings (JSON) |
| `--blocklist` | Manage blocklists |
| `--add-blocklist` | Add a blocklist |
| `--remove-blocklist` | Remove a blocklist |
| `--natives` | Manage native trackers to block |
| `--add-native` | Add native tracker |
| `--remove-native` | Remove native tracker |

**Privacy Options:**
| Setting | Description |
|---------|-------------|
| `disguisedTrackers` | Block disguised third-party trackers |
| `allowAffiliate` | Allow affiliate tracking |

---

### Parental Controls

```bash
python scripts/nextdns.py parental [options]
```

Manage parental controls.

| Option | Description |
|--------|-------------|
| `--view` | View current parental settings (default) |
| `--patch` | Update parental settings (JSON) |
| `--service` | Manage blocked services |
| `--add-service` | Add blocked service |
| `--remove-service` | Remove blocked service |
| `--category` | Manage content categories |
| `--add-category` | Add content category |
| `--remove-category` | Remove content category |

**Parental Control Options:**
| Setting | Description |
|---------|-------------|
| `safeSearch` | Force safe search on search engines |
| `youtubeRestrictedMode` | Enable YouTube restricted mode |
| `blockBypass` | Block bypass methods |

**Services:** `tiktok`, `facebook`, `instagram`, `twitter`, `youtube`, `netflix`, `gaming` (and more)

**Categories:** `porn`, `social-networks`, `gambling`, `torrents`, `gaming`, `dating`, `violent`

---

### Denylist

```bash
python scripts/nextdns.py denylist [options]
```

Manage blocked domains.

| Option | Description |
|--------|-------------|
| `--view` | View denylist (default) |
| `--add <domain>` | Add domain to denylist |
| `--remove <domain>` | Remove domain from denylist |
| `--activate <domain>` | Activate a previously deactivated domain |
| `--deactivate <domain>` | Deactivate without removing |

---

### Allowlist

```bash
python scripts/nextdns.py allowlist [options]
```

Manage always-allowed domains.

| Option | Description |
|--------|-------------|
| `--view` | View allowlist (default) |
| `--add <domain>` | Add domain to allowlist |
| `--remove <domain>` | Remove domain from allowlist |
| `--activate <domain>` | Activate a previously deactivated domain |
| `--deactivate <domain>` | Deactivate without removing |

---

### Profile Management

```bash
python scripts/nextdns.py create-profile --name "My Profile"
python scripts/nextdns.py delete-profile --profile <id>
```

---

## Output Examples

### Analytics Status
```
Status          Queries
---------------------------------
default         819491
blocked         132513
allowed         6923
```

### Analytics Domains
```
Domain                                  Queries    Root
-------------------------------------------------------------------------------------
app-measurement.com                     29801
gateway.icloud.com                      18468      icloud.com
app.smartmailcloud.com                  16414      smartmailcloud.com
```

### Analytics Devices
```
Device Name                     Model                   Queries
----------------------------------------------------------------------
Romain's iPhone                 iPhone 12 Pro Max       489885
MBP                             Macbook Pro             215663
```

### Analytics Query Types
```
Type     Name     Queries
---------------------------
28       AAAA     356230
1        A        341812
65       HTTPS    260478
```

### DNS Logs
```
Timestamp                       Domain                                       Status     Device
--------------------------------------------------------------------------------------------------------------
2024-01-15T10:30:15.123Z       api.example.com                              default    John's iPhone
2024-01-15T10:29:45.456Z       tracker.ads.com                              blocked    John's iPhone
2024-01-15T10:29:30.789Z       dns.google                                  default    MacBook-Pro
```

---

## Profile Management

### Create Profile
```bash
python scripts/nextdns.py create-profile --name "Work Profile"
```

### Delete Profile
```bash
python scripts/nextdns.py delete-profile --profile abc123
```

### Get Full Profile
```bash
python scripts/nextdns.py get-profile --profile abc123
```

---

## Configuration Options

### Logs Settings

```json
{
  "logs": {
    "enabled": true,
    "drop": {
      "ip": false,
      "domain": false
    },
    "retention": 7776000,
    "location": "eu"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Enable query logging |
| `drop.ip` | boolean | Don't log IP addresses |
| `drop.domain` | boolean | Don't log domain queries |
| `retention` | integer | Retention in seconds (default: 7776000 = 90 days) |
| `location` | string | Data region: `eu`, `us`, or leave null for auto |

### Performance Settings

```json
{
  "performance": {
    "ecs": true,
    "cacheBoost": false,
    "cnameFlattening": true
  }
}
```

| Field | Description |
|-------|-------------|
| `ecs` | EDNS Client Subnet (preserve client location for CDN) |
| `cacheBoost` | Increase cache hit rate |
| `cnameFlattening` | Flatten CNAME chains for faster resolution |

### Web3 Settings

```json
{
  "web3": true
}
```

| Value | Description |
|-------|-------------|
| `true` | Enable Web3 features |
| `false` | Standard DNS resolution |

---

## Troubleshooting

### API Key Not Found

```
Error: NEXTDNS_API_KEY not found. Add it in Settings → Advanced → Secrets.
```

**Fix:** Add `NEXTDNS_API_KEY` to your Zo secrets.

---

### No Profiles Found

```
Error: No NextDNS profiles found.
```

**Fix:** Make sure your API key is valid and you have at least one profile.

---

### Rate Limiting

The API may rate limit requests. If you hit limits:
- Wait a few seconds between requests
- Use `--limit` to reduce result sets

---

### Invalid Date Format

Use relative dates or ISO 8601:
- `-1h` (1 hour ago)
- `-1d` (1 day ago)
- `-7d` (7 days ago)
- `2024-01-15T16:34:05.203Z` (ISO 8601)

---

## API Reference

For full API documentation, visit: [https://nextdns.github.io/api/](https://nextdns.github.io/api/)

---

## License

MIT License - feel free to use and modify.
