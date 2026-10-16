"""Synthetic Härtetechnik AG ledger.

The group is fictional. Bookings are generated, not taken from a client.
Numbers are exact so the margin test is reproducible:

- 2023 and 2024: Polish net cost plus is 5.0 percent, inside the peer range.
- 2025: energy costs jump and the transfer price does not follow. Net cost
  plus falls to 2.0 percent, outside the narrowed range.
- The US distributor's 2025 operating margin is about 10 percent, above the
  peer range.
- Management charges are booked with an empty contract id.
"""

from __future__ import annotations

import pandas as pd

ENTITIES = {
    "HTDE": {"name": "Härtetechnik AG", "country": "Deutschland", "role": "Prinzipal"},
    "HTPL": {"name": "Härtetechnik Polska sp. z o.o.", "country": "Polen", "role": "Lohnfertiger"},
    "HTUS": {"name": "Härtetechnik North America Inc.", "country": "USA", "role": "Routinevertrieb"},
}

# Manufacturing cost accounts used for the Polish net cost plus.
MFG_ACCOUNTS = {"COST_MATERIAL", "COST_ENERGY", "COST_LABOR", "COST_OVERHEAD"}

# Annual amounts in euro. Last month absorbs the remainder so sums are exact.
PL_YEARS = {
    2023: {
        "REV_GOODS": 7_350_000,
        "COST_MATERIAL": 4_200_000,
        "COST_ENERGY": 380_000,
        "COST_LABOR": 1_700_000,
        "COST_OVERHEAD": 720_000,
        "COST_ROYALTY": 80_000,
    },
    2024: {
        "REV_GOODS": 7_875_000,
        "COST_MATERIAL": 4_500_000,
        "COST_ENERGY": 400_000,
        "COST_LABOR": 1_800_000,
        "COST_OVERHEAD": 800_000,
        "COST_ROYALTY": 80_000,
    },
    2025: {
        "REV_GOODS": 8_160_000,
        "COST_MATERIAL": 4_400_000,
        "COST_ENERGY": 1_200_000,
        "COST_LABOR": 1_900_000,
        "COST_OVERHEAD": 500_000,
        "COST_ROYALTY": 80_000,
    },
}

# US third-party sales, purchases from Germany, opex, management fee.
US_YEARS = {
    2023: {"REV_THIRD": 9_500_000, "COST_GOODS": 8_700_000, "COST_OPEX": 380_000, "COST_MGMT": 135_000},
    2024: {"REV_THIRD": 10_000_000, "COST_GOODS": 9_120_000, "COST_OPEX": 400_000, "COST_MGMT": 180_000},
    2025: {"REV_THIRD": 12_000_000, "COST_GOODS": 10_200_000, "COST_OPEX": 400_000, "COST_MGMT": 180_000},
}

DE_HQ = {2023: 900_000, 2024: 900_000, 2025: 900_000}
LOAN_PRINCIPAL = 2_000_000
LOAN_INTEREST = {2023: 20_000, 2024: 20_000, 2025: 20_000}

ACCOUNT_META = {
    "REV_GOODS": ("revenue", "goods", "IC-GOODS-PL-DE", "Warenlieferung gehärteter Teile"),
    "COST_MATERIAL": ("cost", "operating_cost", "IC-GOODS-PL-DE", "Materialeinsatz"),
    "COST_ENERGY": ("cost", "operating_cost", "IC-GOODS-PL-DE", "Energie Induktionsofen"),
    "COST_LABOR": ("cost", "operating_cost", "IC-GOODS-PL-DE", "Fertigungslohn"),
    "COST_OVERHEAD": ("cost", "operating_cost", "IC-GOODS-PL-DE", "Fertigungsabweichungen"),
    "COST_ROYALTY": ("cost", "royalty", "IC-LIC-DE-PL", "Lizenz Prozess-Know-how"),
    "REV_ROYALTY": ("revenue", "royalty", "IC-LIC-DE-PL", "Lizenzertrag Prozess-Know-how"),
    "COST_GOODS_PL": ("cost", "goods", "IC-GOODS-PL-DE", "Wareneinkauf von HTPL"),
    "REV_GOODS_US": ("revenue", "goods", "IC-GOODS-DE-US", "Warenlieferung an HTUS"),
    "COST_GOODS": ("cost", "goods", "IC-GOODS-DE-US", "Wareneinkauf von HTDE"),
    "REV_THIRD": ("revenue", "third_party_sale", "THIRD-OEM", "OEM-Umsatz Detroit"),
    "COST_OPEX": ("cost", "operating_cost", "THIRD-OEM", "Vertriebsbetriebskosten"),
    "REV_MGMT": ("revenue", "management_fee", "", "Konzernumlage Management"),
    "COST_MGMT": ("cost", "management_fee", "", "Konzernumlage Management"),
    "COST_HQ": ("cost", "hq_cost", "HQ-DE", "Holdingkosten Stuttgart"),
    "COST_INTEREST": ("cost", "loan_interest", "IC-LOAN-DE-PL", "Zins Gesellschafterdarlehen"),
    "REV_INTEREST": ("revenue", "loan_interest", "IC-LOAN-DE-PL", "Zinsertrag Gesellschafterdarlehen"),
}


def _months(total: int, periods: int = 12) -> list[int]:
    base = total // periods
    amounts = [base] * (periods - 1)
    amounts.append(total - base * (periods - 1))
    return amounts


def _row(entity: str, year: int, period: int, account: str, amount: int, doc: str) -> dict:
    side, tx_type, contract, description = ACCOUNT_META[account]
    partner = {
        "HTPL": "HTDE" if account != "COST_INTEREST" else "HTDE",
        "HTDE": "HTPL" if account in {"COST_GOODS_PL", "REV_ROYALTY", "REV_INTEREST"} else "HTUS" if account == "REV_GOODS_US" else "HTUS" if account == "REV_MGMT" else "",
        "HTUS": "HTDE",
    }[entity]
    if account in {"REV_THIRD", "COST_OPEX"}:
        partner = "OEM"
    return {
        "entity": entity,
        "entity_name": ENTITIES[entity]["name"],
        "country": ENTITIES[entity]["country"],
        "year": year,
        "period": period,
        "posting_date": f"{year}-{period:02d}-28",
        "document_no": doc,
        "partner": partner,
        "account": account,
        "side": side,
        "amount_eur": int(amount),
        "transaction_type": tx_type,
        "contract_id": contract,
        "description": description,
    }


def build_ledger() -> pd.DataFrame:
    rows: list[dict] = []
    doc_no = 1
    for year, accounts in PL_YEARS.items():
        for account, total in accounts.items():
            for period, amount in enumerate(_months(total), start=1):
                rows.append(_row("HTPL", year, period, account, amount, f"PL{doc_no:05d}"))
                doc_no += 1
        for period, amount in enumerate(_months(LOAN_INTEREST[year]), start=1):
            rows.append(_row("HTPL", year, period, "COST_INTEREST", amount, f"PL{doc_no:05d}"))
            doc_no += 1
    for year, accounts in US_YEARS.items():
        for account, total in accounts.items():
            for period, amount in enumerate(_months(total), start=1):
                rows.append(_row("HTUS", year, period, account, amount, f"US{doc_no:05d}"))
                doc_no += 1
    for year in (2023, 2024, 2025):
        de_accounts = {
            "COST_GOODS_PL": PL_YEARS[year]["REV_GOODS"],
            "REV_GOODS_US": US_YEARS[year]["COST_GOODS"],
            "REV_ROYALTY": PL_YEARS[year]["COST_ROYALTY"],
            "REV_MGMT": US_YEARS[year]["COST_MGMT"],
            "REV_INTEREST": LOAN_INTEREST[year],
            "COST_HQ": DE_HQ[year],
        }
        for account, total in de_accounts.items():
            for period, amount in enumerate(_months(total), start=1):
                rows.append(_row("HTDE", year, period, account, amount, f"DE{doc_no:05d}"))
                doc_no += 1
    return pd.DataFrame(rows)


def entity_amounts(ledger: pd.DataFrame, entity: str, year: int) -> dict[str, int]:
    part = ledger[(ledger["entity"] == entity) & (ledger["year"] == year)]
    grouped = part.groupby("account")["amount_eur"].sum()
    return {account: int(grouped.get(account, 0)) for account in grouped.index}
