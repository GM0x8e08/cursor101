#!/usr/bin/env python3
"""Resilient cached Firecrawl scraper for DataCenterMap crawl.

Wraps the `firecrawl scrape` CLI. Caches every page to disk so re-runs never
re-fetch. Retries on rate-limit / transient errors with exponential backoff.
"""
import os
import re
import subprocess
import sys
import time
import hashlib

BASE_DELAY = float(os.environ.get("FC_BASE_DELAY", "4"))
MAX_RETRIES = int(os.environ.get("FC_MAX_RETRIES", "6"))
MIN_BYTES = 400  # a valid DCM page markdown is always larger than this

RATE_LIMIT_MARKERS = (
    "rate limit",
    "429",
    "too many requests",
    "keyless free tier",
)


def is_valid_cache(path: str) -> bool:
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
    except OSError:
        return False
    if len(txt) < MIN_BYTES:
        return False
    # A real DCM page always contains the site chrome + a breadcrumb.
    if "datacentermap.com" not in txt:
        return False
    # Reject Vercel bot-challenge captures.
    if "Vercel Security Checkpoint" in txt:
        return False
    return True


def scrape(url: str, out_path: str, force: bool = False) -> bool:
    """Scrape `url` into `out_path`. Returns True on success (fresh or cached)."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if not force and is_valid_cache(out_path):
        return True

    delay = BASE_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            proc = subprocess.run(
                ["firecrawl", "scrape", url, "-o", out_path],
                capture_output=True,
                text=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            print(f"    [timeout] attempt {attempt} for {url}", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 90)
            continue

        combined = (proc.stdout + "\n" + proc.stderr).lower()
        rate_limited = any(m in combined for m in RATE_LIMIT_MARKERS)

        if is_valid_cache(out_path) and not rate_limited:
            # small politeness delay between successful requests
            time.sleep(BASE_DELAY)
            return True

        # Failed: remove any partial/invalid file
        if os.path.exists(out_path) and not is_valid_cache(out_path):
            try:
                os.remove(out_path)
            except OSError:
                pass

        reason = "rate-limited" if rate_limited else "invalid/empty"
        print(
            f"    [{reason}] attempt {attempt}/{MAX_RETRIES} for {url}; "
            f"backing off {delay:.0f}s",
            flush=True,
        )
        time.sleep(delay)
        delay = min(delay * 2, 90)

    print(f"    [FAILED] {url}", flush=True)
    return False


def slug_for(url: str) -> str:
    path = url.replace("https://www.datacentermap.com/", "").strip("/")
    return path.replace("/", "__")


if __name__ == "__main__":
    # CLI: python scraper.py <url> <out_path>
    ok = scrape(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
