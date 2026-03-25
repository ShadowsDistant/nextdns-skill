#!/usr/bin/env python3
"""NextDNS API CLI tool for querying logs and analytics."""

import os
import sys
import argparse
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("NEXTDNS_API_KEY")
BASE_URL = "https://api.nextdns.io"


def get_headers():
    if not API_KEY:
        raise SystemExit("Error: NEXTDNS_API_KEY not found. Add it in Settings > Advanced → Secrets.")
    return {"X-Api-Key": API_KEY, "Accept": "application/json"}


def get_profiles():
    """List all NextDNS profiles."""
    resp = requests.get(f"{BASE_URL}/profiles", headers=get_headers())
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", [])


def get_profile_id(profile_id=None):
    """Get profile ID, using first profile if not specified."""
    if profile_id:
        return profile_id
    profiles = get_profiles()
    if not profiles:
        raise SystemExit("Error: No NextDNS profiles found.")
    return profiles[0]["id"]


def cmd_logs(args):
    """Fetch DNS query logs."""
    profile_id = get_profile_id(args.profile)
    params = {"limit": args.limit, "sort": args.sort}

    if args.status:
        params["status"] = args.status
    if args.domain:
        params["search"] = args.domain
    if args.device:
        params["device"] = args.device
    if args.from_time:
        params["from"] = args.from_time
    if args.to_time:
        params["to"] = args.to_time
    if args.raw:
        params["raw"] = "1"

    url = f"{BASE_URL}/profiles/{profile_id}/logs"
    resp = requests.get(url, headers=get_headers(), params=params)
    resp.raise_for_status()
    data = resp.json()

    logs = data.get("data", [])
    if not logs:
        print("No logs found matching your criteria.")
        return

    print(f"\n{'Timestamp':<30} {'Domain':<45} {'Status':<10} {'Device':<20}")
    print("-" * 110)
    for log in logs:
        ts = log.get("timestamp", "")
        domain = log.get("domain", "")
        status = log.get("status", "")
        device_name = log.get("device", {}).get("name", "") if log.get("device") else ""
        print(f"{ts:<30} {domain:<45} {status:<10} {device_name:<20}")

    meta = data.get("meta", {})
    if meta.get("pagination", {}).get("cursor"):
        print(f"\n... more results available (cursor: {meta['pagination']['cursor']})")
    print(f"\nTotal shown: {len(logs)}")


def cmd_analytics(args):
    """Fetch analytics data."""
    profile_id = get_profile_id(args.profile)
    endpoint = args.endpoint
    params = {"limit": args.limit}

    if args.status:
        params["status"] = args.status

    url = f"{BASE_URL}/profiles/{profile_id}/analytics/{endpoint}"
    resp = requests.get(url, headers=get_headers(), params=params)
    resp.raise_for_status()
    data = resp.json()

    items = data.get("data", [])
    if not items:
        print("No analytics data found.")
        return

    if endpoint == "status":
        print(f"\n{'Status':<15} {'Queries':<15}")
        print("-" * 35)
        for item in items:
            print(f"{item.get('status', ''):<15} {item.get('queries', 0):<15}")
    elif endpoint == "domains":
        print(f"\n{'Domain':<50} {'Queries':<10} {'Root':<30}")
        print("-" * 95)
        for item in items:
            root = item.get("root", "")
            print(f"{item.get('domain', ''):<50} {item.get('queries', 0):<10} {root:<30}")
    elif endpoint == "devices":
        print(f"\n{'Device Name':<30} {'Model':<25} {'Queries':<10}")
        print("-" * 70)
        for item in items:
            print(f"{item.get('name', ''):<30} {item.get('model', ''):<25} {item.get('queries', 0):<10}")
    elif endpoint == "reasons":
        print(f"\n{'Reason ID':<45} {'Name':<40} {'Queries':<10}")
        print("-" * 100)
        for item in items:
            print(f"{item.get('id', ''):<45} {item.get('name', ''):<40} {item.get('queries', 0):<10}")
    elif endpoint == "protocols":
        print(f"\n{'Protocol':<25} {'Queries':<15}")
        print("-" * 45)
        for item in items:
            print(f"{item.get('protocol', ''):<25} {item.get('queries', 0):<15}")
    else:
        # Generic output
        print(json.dumps(items, indent=2))

    print(f"\nTotal: {len(items)}")


def cmd_profiles(args):
    """List all profiles."""
    profiles = get_profiles()
    if not profiles:
        print("No profiles found.")
        return

    print(f"\n{'ID':<20} {'Name':<30}")
    print("-" * 55)
    for p in profiles:
        pid = p.get("id", "")
        name = p.get("name", "")
        print(f"{pid:<20} {name:<30}")


def main():
    parser = argparse.ArgumentParser(description="NextDNS API CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Profiles command
    subparsers.add_parser("profiles", help="List all NextDNS profiles")

    # Logs command
    logs_parser = subparsers.add_parser("logs", help="Get DNS query logs")
    logs_parser.add_argument("--profile", help="Profile ID (default: first profile)")
    logs_parser.add_argument("--status", choices=["default", "blocked", "allowed", "error"], help="Filter by status")
    logs_parser.add_argument("--domain", help="Filter by domain name")
    logs_parser.add_argument("--device", help="Filter by device name")
    logs_parser.add_argument("--from", dest="from_time", help="Start time (e.g., -1h, -1d, -7d)")
    logs_parser.add_argument("--to", dest="to_time", help="End time")
    logs_parser.add_argument("--limit", type=int, default=100, help="Number of results (10-1000)")
    logs_parser.add_argument("--sort", choices=["asc", "desc"], default="desc", help="Sort order")
    logs_parser.add_argument("--raw", action="store_true", help="Show all DNS queries (including noise)")

    # Analytics command
    analytics_parser = subparsers.add_parser("analytics", help="Get analytics")
    analytics_parser.add_argument("endpoint", choices=["status", "domains", "devices", "reasons", "protocols", "queryTypes", "ips", "destinations"])
    analytics_parser.add_argument("--profile", help="Profile ID (default: first profile)")
    analytics_parser.add_argument("--status", choices=["default", "blocked", "allowed"], help="Filter by status")
    analytics_parser.add_argument("--limit", type=int, default=10, help="Number of results")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "logs":
            cmd_logs(args)
        elif args.command == "analytics":
            cmd_analytics(args)
        elif args.command == "profiles":
            cmd_profiles(args)
    except requests.exceptions.HTTPError as e:
        err_msg = "API request failed"
        try:
            err_data = e.response.json()
            errors = err_data.get("errors", [])
            if errors:
                err_msg = errors[0].get("detail", str(errors))
        except:
            pass
        raise SystemExit(f"Error: {err_msg}")
    except Exception as e:
        raise SystemExit(f"Error: {e}")


if __name__ == "__main__":
    main()
