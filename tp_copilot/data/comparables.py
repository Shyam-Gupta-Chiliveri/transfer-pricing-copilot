"""Synthetic peer descriptions for the contract-manufacturer screen.

Labels were written for this portfolio case. They are not a download from
SEC EDGAR and they are not client comparables. A production screen would use
Orbis or TP Catalyst. scripts/fetch_edgar.py shows the public-data alternative.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    name: str
    label: int
    description: str
    net_cost_plus: float | None = None


def _peer(name: str, rate: float, description: str) -> Company:
    return Company(name, 1, description, rate)


COMPANIES: list[Company] = [
    _peer(
        "Nordform Metall GmbH",
        0.031,
        "Contract manufacturer machining steel automotive parts to customer drawings. The customer owns the design. The plant has no brand of its own.",
    ),
    _peer(
        "Gliwice Heat Treat Sp. z o.o.",
        0.034,
        "Contract manufacturer for induction hardening of steel components. The customer owns the process recipe and the inventory risk.",
    ),
    _peer(
        "SaarPress Umformtechnik",
        0.038,
        "Contract manufacturer stamping and machining steel brackets to customer drawings. Tooling design stays with the customer.",
    ),
    _peer(
        "Baltic Furnace Works",
        0.042,
        "Contract manufacturer and heat-treatment shop for forged steel. One customer reserves capacity. The customer owns the recipe.",
    ),
    _peer(
        "RheinHard Components",
        0.045,
        "Contract manufacturer of hardened steel shafts. Induction hardening follows the customer specification. The customer issues the PPAP.",
    ),
    _peer(
        "Oder Machining S.A.",
        0.049,
        "Contract manufacturer machining steel castings supplied by the customer. Rework above a threshold is charged back to the customer.",
    ),
    _peer(
        "Elbe Surface Tech",
        0.052,
        "Contract manufacturer for induction hardening and surface treatment of steel truck parts. The customer owns the trademarks.",
    ),
    _peer(
        "Vistula Precision Parts",
        0.056,
        "Contract manufacturer turning steel parts to customer specification. The plant does not carry market or warranty risk.",
    ),
    _peer(
        "Donau Heat Treat",
        0.061,
        "Contract manufacturer for induction hardening of steel gearbox parts. The customer owns the recipe and the OEM contract.",
    ),
    _peer(
        "Morava Toolroom",
        0.064,
        "Contract manufacturer doing batch induction hardening of steel fasteners. The process window belongs to the customer.",
    ),
    _peer(
        "Neckar Metal Processing",
        0.068,
        "Contract manufacturer welding and heat-treating steel assemblies. Invoices cover conversion of customer-owned material.",
    ),
    _peer(
        "Silesia Axle Works",
        0.072,
        "Contract manufacturer of steel axle components. Induction hardening follows the customer hardness specification.",
    ),
    _peer(
        "Mainkai Fabrication",
        0.079,
        "Contract manufacturer for steel fabrication and induction hardening. The only customer is one automotive group that owns the design.",
    ),
    _peer(
        "Bugra Processing Plant",
        0.084,
        "Contract manufacturer heat-treating customer-owned steel blanks. The process know-how stays with the customer.",
    ),
    Company(
        "CloudPayroll Labs",
        0,
        "We develop and market cloud software for payroll. We have no manufacturing operations and no metal processing.",
    ),
    Company(
        "Nordbank Treasury",
        0,
        "Retail and corporate bank. Activities are lending, deposits and payment services. No factory and no automotive parts.",
    ),
    Company(
        "Alpen Pharma AG",
        0,
        "Research-based pharmaceutical company. We own drug patents and sell branded medicine through our own marketing teams.",
    ),
    Company(
        "Stadtmarkt Retail",
        0,
        "Grocery retail chain operating supermarkets. We buy finished consumer goods and sell them to households.",
    ),
    Company(
        "Helios Energy Utility",
        0,
        "Regulated electricity utility. We generate and distribute power. We do not machine or harden metal parts for OEMs.",
    ),
    Company(
        "BrandWerk Consumer",
        0,
        "Full-fledged consumer brand owner. We design products, own the trademark and carry warranty and market risk worldwide.",
    ),
    Company(
        "Atlantic Software Platforms",
        0,
        "Enterprise software vendor for airlines. Revenue comes from licences and subscriptions, not from contract manufacturing.",
    ),
    Company(
        "Rhein Insurance Group",
        0,
        "Life and property insurer. The business is underwriting risk, not producing hardened steel components.",
    ),
    Company(
        "Pacific Social Media",
        0,
        "Advertising-funded social network. Users create content. We do not operate a heat-treatment plant.",
    ),
    Company(
        "LuxMode Apparel",
        0,
        "Fashion house selling branded clothing. Design and brand are the core assets. No automotive machining.",
    ),
    Company(
        "Greenfield Mining",
        0,
        "Copper mining company. We extract ore and sell concentrate. We are not a contract manufacturer of parts.",
    ),
    Company(
        "Hotelkette Süden",
        0,
        "Hotel operator. Revenue is rooms and restaurants. No induction hardening and no OEM supply.",
    ),
    Company(
        "Quantum Biotech",
        0,
        "Biotechnology company developing antibodies. Laboratories, not machine shops. We own the science.",
    ),
    Company(
        "Metro Logistics Only",
        0,
        "Freight forwarder moving third-party cargo. We do not transform metal and we do not own process recipes.",
    ),
    Company(
        "SolarRoof Installers",
        0,
        "Installation of rooftop solar panels for homeowners. Field service business, not a hardening plant.",
    ),
    Company(
        "DataCenter North",
        0,
        "Colocation data centres. We sell power and rack space to software companies.",
    ),
    Company(
        "OEM Motors Entrepreneur",
        0,
        "Full-fledged automotive OEM. We design vehicles, own the brand, set the process, and carry warranty and market risk.",
    ),
    Company(
        "Global Consulting Partners",
        0,
        "Management consulting firm. People-based advisory. No furnaces and no series production.",
    ),
]


LRD_MARGINS: list[tuple[str, float]] = [
    ("Detroit Parts Sales", 0.015),
    ("Lakeshore Distribution", 0.018),
    ("Great Lakes Auto Sales", 0.021),
    ("Ohio Routine Distributor", 0.024),
    ("Midwest Component Sales", 0.027),
    ("Prairie OEM Desk", 0.030),
    ("River City Resale", 0.033),
    ("Lincoln Limited Risk", 0.036),
    ("Erie Buy-Sell Co", 0.039),
    ("Toledo Flash Title", 0.042),
    ("Cleveland Agency Sales", 0.045),
]
