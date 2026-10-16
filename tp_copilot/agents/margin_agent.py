"""Arm's length range under § 1 Abs. 3a AStG, applied to the synthetic ledger."""

from __future__ import annotations

import statistics

import pandas as pd

from tp_copilot.agents.screening_agent import accepted_peers
from tp_copilot.data.comparables import LRD_MARGINS
from tp_copilot.data.group import MFG_ACCOUNTS, build_ledger, entity_amounts


def german_range(values: list[float]) -> dict:
    """Drop the bottom and top quarter of observations, then take the median.

    Section 1(3a) AStG leaves out the quarter of the smallest values and the
    quarter of the largest values when the remaining points do not themselves
    indicate a tighter narrowing. The median of the full observed set is the
    adjustment point if the tested result sits outside that narrowed range.
    """
    ordered = sorted(float(value) for value in values)
    count = len(ordered)
    drop = count // 4 if count >= 4 else 0
    narrowed = ordered[drop : count - drop] if drop else list(ordered)
    return {
        "n": count,
        "dropped_each_tail": drop,
        "low": narrowed[0],
        "high": narrowed[-1],
        "median": float(statistics.median(ordered)),
        "values": ordered,
    }


def locate(value: float, rng: dict) -> str:
    if rng["low"] - 1e-9 <= value <= rng["high"] + 1e-9:
        return "inside"
    return "below" if value < rng["low"] else "above"


def _percent(value: float) -> float:
    return round(value * 100, 2)


def polish_pli(ledger: pd.DataFrame, year: int) -> dict:
    amounts = entity_amounts(ledger, "HTPL", year)
    revenue = amounts.get("REV_GOODS", 0)
    manufacturing = sum(amounts.get(account, 0) for account in MFG_ACCOUNTS)
    royalty = amounts.get("COST_ROYALTY", 0)
    operating_profit = revenue - manufacturing
    net_cost_plus = operating_profit / manufacturing if manufacturing else 0.0
    return {
        "entity": "HTPL",
        "year": year,
        "revenue": revenue,
        "manufacturing_costs": manufacturing,
        "royalty": royalty,
        "operating_profit_before_royalty": operating_profit,
        "net_cost_plus": net_cost_plus,
        "energy": amounts.get("COST_ENERGY", 0),
    }


def us_pli(ledger: pd.DataFrame, year: int) -> dict:
    amounts = entity_amounts(ledger, "HTUS", year)
    revenue = amounts.get("REV_THIRD", 0)
    costs = amounts.get("COST_GOODS", 0) + amounts.get("COST_OPEX", 0) + amounts.get("COST_MGMT", 0)
    operating_profit = revenue - costs
    gross_profit = revenue - amounts.get("COST_GOODS", 0)
    opex = amounts.get("COST_OPEX", 0) + amounts.get("COST_MGMT", 0)
    return {
        "entity": "HTUS",
        "year": year,
        "revenue": revenue,
        "operating_profit": operating_profit,
        "operating_margin": operating_profit / revenue if revenue else 0.0,
        "berry_ratio": gross_profit / opex if opex else None,
        "management_fee": amounts.get("COST_MGMT", 0),
    }


def assess(year: int = 2025, ledger: pd.DataFrame | None = None) -> dict:
    ledger = build_ledger() if ledger is None else ledger
    peers = accepted_peers()
    cm_range = german_range([peer["net_cost_plus"] for peer in peers])
    lrd_range = german_range([rate for _, rate in LRD_MARGINS])
    tested_pl = polish_pli(ledger, year)
    tested_us = us_pli(ledger, year)
    pl_position = locate(tested_pl["net_cost_plus"], cm_range)
    us_position = locate(tested_us["operating_margin"], lrd_range)

    def adjustment(actual: float, base: int, rng: dict, position: str) -> dict | None:
        if position == "inside":
            return None
        gap = rng["median"] - actual
        return {
            "target": rng["median"],
            "gap": gap,
            "profit_eur": int(round(gap * base)),
            "rule": "§ 1 Abs. 3a AStG",
        }

    return {
        "year": year,
        "cm_range": cm_range,
        "lrd_range": lrd_range,
        "peers": peers,
        "lrd_peers": [{"name": name, "operating_margin": rate} for name, rate in LRD_MARGINS],
        "htpl": tested_pl,
        "htus": tested_us,
        "htpl_position": pl_position,
        "htus_position": us_position,
        "htpl_adjustment": adjustment(
            tested_pl["net_cost_plus"],
            tested_pl["manufacturing_costs"],
            cm_range,
            pl_position,
        ),
        "htus_adjustment": adjustment(
            tested_us["operating_margin"],
            tested_us["revenue"],
            lrd_range,
            us_position,
        ),
        "history": {
            "HTPL": [polish_pli(ledger, y) for y in (2023, 2024, 2025)],
            "HTUS": [us_pli(ledger, y) for y in (2023, 2024, 2025)],
        },
    }


def format_pct(value: float) -> str:
    return f"{_percent(value):.2f} %"
