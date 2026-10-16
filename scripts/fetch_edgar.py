"""Optional SEC EDGAR pull for a few public manufacturers.

The demo does not need this. Real intercompany ledgers are not public.
Company facts are. Set a contact address in the user agent before calling SEC.
"""

from __future__ import annotations

import json
import sys
import urllib.request

# CIKs are public SEC identifiers, zero-padded to 10 digits.
SAMPLE = {
    "0000051143": "IBM",
    "0000320193": "Apple",
}


def company_facts(cik: str, contact: str) -> dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    request = urllib.request.Request(url, headers={"User-Agent": contact})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/fetch_edgar.py 'Your Name you@example.com'")
        print("Prints whether Revenues and OperatingIncomeLoss exist for two sample CIKs.")
        return
    contact = sys.argv[1]
    for cik, name in SAMPLE.items():
        facts = company_facts(cik, contact)
        us_gaap = facts.get("facts", {}).get("us-gaap", {})
        keys = [key for key in ("Revenues", "OperatingIncomeLoss") if key in us_gaap]
        print(f"{name} {cik}: {', '.join(keys) or 'no operating facts under those tags'}")


if __name__ == "__main__":
    main()
