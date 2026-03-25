# NextDNS Skill for Zo Computer

[![Skill Version](https://img.shields.io/badge/Skill%20Version-1.0.0-blue.svg)](Skills/nextdns/skills/nextdns-api)
[![Platform](https://img.shields.io/badge/Platform-Zo%20Computer-6366f1.svg)](https://zo.computer)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-orange.svg)](https://python.org)

Query NextDNS DNS logs and analytics directly from your Zo Computer terminal.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Command Reference](#command-reference)
- [Examples](#examples)
- [Output Samples](#output-samples)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

This skill provides a command-line interface to the [NextDNS API](https://api.nextdns.io), allowing you to:

- 🔍 **Query DNS logs** — See exactly what DNS queries are being made on your network
- 📊 **View analytics** — Understand traffic patterns, top domains, and device usage
- 🚫 **Audit blocked queries** — Review what NextDNS has blocked and why
- 📱 **Filter by device** — Track activity per device on your network
- 🔎 **Search domains** — Find specific domain lookups in real-time

---

## Features

- **Multiple analytics endpoints** — status, domains, devices, reasons, protocols, query types, IPs, destinations
- **Flexible filtering** — By status, domain, device, time range
- **Profile support** — Work with multiple NextDNS profiles
- **Pagination** — Handle large result sets with cursor-based pagination
- **Error handling** — Clear, actionable error messages with API error details
- **No dependencies** — Uses only Python standard library + `requests`

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Python | 3.12 or higher |
| NextDNS Account | [Sign up free](https://nextdns.io) |
| NextDNS API Key | Generate in your NextDNS dashboard |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ShadowsDistant/nextdns-skill.git
cd nextdns-skill
```

### 2. Set Up API Key

1. Log into [my.nextdns.io](https://my.nextdns.io)
2. Go to **Settings → API**
3. Generate a new API key
4. Add it to Zo Computer:
   - Navigate to **Settings → Advanced → Secrets**
   - Add a new secret: `NEXTDNS_API_KEY` = `<your-api-key>`

---

## Configuration

The tool reads your API key from the `NEXTDNS_API_KEY` environment variable.

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXTDNS_API_KEY` | ✅ Yes | Your NextDNS API key |

---

## Usage

```bash
python nextdns.py <command> [options]
```

### Quick Start

```bash
# View all profiles
python nextdns.py profiles

# Get recent DNS logs (last 50 queries)
python nextdns.py logs --limit 50

# See blocked queries only
python nextdns.py logs --status blocked --limit 50

# View top domains by query volume
python nextdns.py analytics domains --limit 20

# See what's being blocked and why
python nextdns.py analytics reasons

# View device breakdown
python nextdns.py analytics devices
```

---

## Command Reference

### `profiles`

List all NextDNS profiles associated with your account.

```bash
python nextdns.py profiles
```

**Output columns:** `ID` | `Name`

---

### `logs`

Fetch DNS query logs.

```bash
python nextdns.py logs [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--profile <id>` | string | first profile | Profile ID to query |
| `--status` | enum | — | Filter: `blocked`, `allowed`, `default`, `error` |
| `--domain <name>` | string | — | Filter by domain name |
| `--device <name>` | string | — | Filter by device name |
| `--from <time>` | string | — | Start time (`-1h`, `-1d`, `-7d`, `2024-01-01`) |
| `--to <time>` | string | — | End time |
| `--limit` | int | 100 | Results count (10–1000) |
| `--sort` | enum | `desc` | Sort: `asc`, `desc` |
| `--raw` | flag | false | Show all queries including noise |

**Output columns:** `Timestamp` | `Domain` | `Status` | `Device`

---

### `analytics`

Fetch analytics data for an endpoint.

```bash
python nextdns.py analytics <endpoint> [options]
```

#### Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `status` | Allowed vs blocked query breakdown |
| `domains` | Top domains by query volume |
| `devices` | Queries grouped by device |
| `reasons` | Block reasons (parental, security, etc.) |
| `protocols` | DNS protocol distribution (DoH, DoT, etc.) |
| `queryTypes` | Query types (A, AAAA, TXT, etc.) |
| `ips` | Client IP addresses |
| `destinations` | Upstream DNS servers used |

#### Analytics Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--profile <id>` | string | first profile | Profile ID to query |
| `--status` | enum | — | Filter: `blocked`, `allowed` |
| `--limit` | int | 10 | Number of results |

---

## Examples

### View All Blocked Queries

```bash
python nextdns.py logs --status blocked --limit 100
```

### Search Logs for a Specific Domain

```bash
python nextdns.py logs --domain google.com --limit 50
```

### Filter Logs by Device

```bash
python nextdns.py logs --device "iPhone" --limit 50
```

### Get Top 25 Domains

```bash
python nextdns.py analytics domains --limit 25
```

### View Block Reasons

```bash
python nextdns.py analytics reasons
```

### Get Last Hour's Activity

```bash
python nextdns.py logs --from -1h --limit 100
```

### See Device Breakdown

```bash
python nextdns.py analytics devices
```

### Query Specific Profile

```bash
python nextdns.py logs --profile "abc123" --limit 50
```

---

## Output Samples

### `profiles`

```
ID                  Name
-------------------------------------------------------
x9z2a8              Home Network
y7w1b6              Work Setup
```

### `logs`

```
Timestamp                     Domain                                       Status    Device
--------------------------------------------------------------------------------------------------------------
2024-03-25 10:45:23          doubleclick.net                              allowed   iPhone
2024-03-25 10:45:22          googleadservices.com                        blocked   MacBook-Pro
2024-03-25 10:45:21          api.example.com                             allowed   Desktop
```

### `analytics status`

```
Status           Queries
-----------------------------------
allowed          12450
blocked          834
```

### `analytics domains`

```
Domain                                           Queries     Root
-----------------------------------------------------------------------------------------------------------------
google.com                                       2340        google.com
facebook.com                                    1892        facebook.com
api.twitter.com                                  456         twitter.com
```

---

## Troubleshooting

### "NEXTDNS_API_KEY not found"

Your API key isn't set in Zo secrets. Go to **Settings → Advanced → Secrets** and add `NEXTDNS_API_KEY`.

### "No logs found matching your criteria"

- Try widening your time range (`--from -7d`)
- Use `--status allowed` to see all non-blocked queries
- Check that your profile ID is correct

### "API request failed"

- Verify your API key is valid at [my.nextdns.io](https://my.nextdns.io)
- Check your internet connection
- NextDNS API may be temporarily unavailable — retry later

### "No NextDNS profiles found"

- Confirm your API key has access to profiles
- You may need to create a NextDNS profile first

---

## License

MIT License — feel free to use, modify, and distribute.

---

## Links

- [NextDNS API Documentation](https://api.nextdns.io)
- [NextDNS Dashboard](https://my.nextdns.io)
- [Zo Computer](https://zo.computer)
- [Report Issue](https://github.com/ShadowsDistant/nextdns-skill/issues)
