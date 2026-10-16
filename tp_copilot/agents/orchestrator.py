"""Supervisor: guideline RAG, benchmarking, margins, FAR and the critic."""

from __future__ import annotations

import pandas as pd

from tp_copilot.agents.critic_agent import critique_case, critique_retrieval
from tp_copilot.agents.far_agent import run_far
from tp_copilot.agents.kg_agent import run_kg
from tp_copilot.agents.margin_agent import assess, format_pct, locate
from tp_copilot.agents.rag_agent import answer_question
from tp_copilot.agents.router import route_question
from tp_copilot.agents.screening_agent import evaluate, screen_text
from tp_copilot.data.group import LOAN_PRINCIPAL, build_ledger


def _sum(ledger: pd.DataFrame, entity: str, year: int, account: str) -> int:
    part = ledger[(ledger["entity"] == entity) & (ledger["year"] == year) & (ledger["account"] == account)]
    return int(part["amount_eur"].sum())


def transaction_matrix(year: int = 2025, ledger: pd.DataFrame | None = None) -> pd.DataFrame:
    ledger = build_ledger() if ledger is None else ledger
    goods_pl = _sum(ledger, "HTPL", year, "REV_GOODS")
    goods_us = _sum(ledger, "HTDE", year, "REV_GOODS_US")
    royalty = _sum(ledger, "HTPL", year, "COST_ROYALTY")
    management = _sum(ledger, "HTUS", year, "COST_MGMT")
    interest = _sum(ledger, "HTPL", year, "COST_INTEREST")
    records = [
        _matrix_row("Warenlieferung gehärteter Teile", "Supply of hardened parts", "Lieferung", "Supply", "HTPL", "HTDE", goods_pl, goods_pl, "IC-GOODS-PL-DE", "TNMM (Net Cost Plus)", "TNMM (net cost plus)", "Polen / Deutschland", "Poland / Germany"),
        _matrix_row("Weiterverkauf an OEM", "Resale to OEMs", "Lieferung", "Supply", "HTDE", "HTUS", goods_us, goods_us, "IC-GOODS-DE-US", "TNMM (Betriebsmarge)", "TNMM (operating margin)", "Deutschland / USA", "Germany / United States"),
        _matrix_row("Prozess-Know-how", "Process know-how", "Lizenz", "Licence", "HTDE", "HTPL", royalty, royalty, "IC-LIC-DE-PL", "CUP (behauptet)", "CUP (claimed)", "Deutschland / Polen", "Germany / Poland"),
        _matrix_row("Managementumlage", "Management charge", "Dienstleistung", "Service", "HTDE", "HTUS", management, management, "", "Kostenaufschlagsmethode", "Cost plus", "Deutschland / USA", "Germany / United States"),
        _matrix_row("Gesellschafterdarlehen", "Intercompany loan", "Darlehen", "Loan", "HTDE", "HTPL", LOAN_PRINCIPAL, interest, "IC-LOAN-DE-PL", "CUP", "CUP", "Deutschland / Polen", "Germany / Poland"),
    ]
    return pd.DataFrame(records)


def _matrix_row(
    subject, subject_en, kind, kind_en, provider, recipient,
    volume, consideration, contract, method, method_en, territories, territories_en,
) -> dict:
    return {
        "gegenstand": subject,
        "gegenstand_en": subject_en,
        "art": kind,
        "art_en": kind_en,
        "leistungserbringer": provider,
        "leistungsempfaenger": recipient,
        "volumen_eur": volume,
        "entgelt_eur": consideration,
        "vertrag": contract,
        "methode": method,
        "methode_en": method_en,
        "steuerhoheitsgebiete": territories,
        "steuerhoheitsgebiete_en": territories_en,
        "ausserhalb_regelbesteuerung": "nein",
        "ausserhalb_regelbesteuerung_en": "no",
    }


def matrix_gaps(matrix: pd.DataFrame) -> list[dict]:
    missing = matrix[matrix["vertrag"].astype(str).str.strip() == ""]
    return missing.to_dict(orient="records")


def _eur(amount: int) -> str:
    return f"{abs(amount):,}".replace(",", ".")


def _eur_en(amount: int) -> str:
    return f"€{abs(amount):,}"


def _pct_de(value: float) -> str:
    return format_pct(value).replace(".", ",")


_POSITION = {"inside": "in", "below": "unter", "above": "über"}


def findings_for(assessment: dict, gaps: list[dict]) -> list[dict]:
    findings = []
    pl = assessment["htpl"]
    if assessment["htpl_position"] != "inside":
        adjustment = assessment["htpl_adjustment"]
        direction = "zusätzliches" if adjustment["profit_eur"] > 0 else "geringeres"
        findings.append(
            {
                "id": "pl_margin",
                "severity": "high",
                "title": f"HTPL Net Cost Plus {format_pct(pl['net_cost_plus'])} liegt {_POSITION[assessment['htpl_position']]} der Bandbreite",
                "title_en": f"HTPL net cost plus {format_pct(pl['net_cost_plus'])} is {assessment['htpl_position']} the range",
                "detail": (
                    f"Fertigungskosten {_eur(pl['manufacturing_costs'])} EUR, operatives Ergebnis vor Lizenz "
                    f"{_eur(pl['operating_profit_before_royalty'])} EUR. Eingeengte Bandbreite "
                    f"{format_pct(assessment['cm_range']['low'])} bis {format_pct(assessment['cm_range']['high'])}, "
                    f"Median {format_pct(assessment['cm_range']['median'])}. "
                    f"Energiekosten in diesem Jahr: {_eur(pl['energy'])} EUR. "
                    f"Richtung: {_eur(adjustment['profit_eur'])} EUR {direction} operatives Ergebnis (§ 1 Abs. 3a AStG)."
                ),
                "detail_en": (
                    f"Manufacturing costs {_eur_en(pl['manufacturing_costs'])}, operating profit before royalty "
                    f"{_eur_en(pl['operating_profit_before_royalty'])}. Narrowed range "
                    f"{format_pct(assessment['cm_range']['low'])} to {format_pct(assessment['cm_range']['high'])}, "
                    f"median {format_pct(assessment['cm_range']['median'])}. "
                    f"Energy cost this year: {_eur_en(pl['energy'])}. "
                    f"Direction: {_eur_en(adjustment['profit_eur'])} "
                    f"{'more' if adjustment['profit_eur'] > 0 else 'less'} operating profit (§ 1 Abs. 3a AStG)."
                ),
                "citation": "§ 1 Abs. 3a AStG; OECD TPG Rn. 2.64 und 3.60",
                "citation_en": "§ 1 (3a) AStG; OECD TPG paras. 2.64 and 3.60",
                "rows": [
                    ("Geprüft", "HTPL"),
                    ("Kennzahl", "Net Cost Plus"),
                    ("Ergebnis", _pct_de(pl["net_cost_plus"])),
                    ("Fertigungskosten", f"{_eur(pl['manufacturing_costs'])} EUR"),
                    ("Operatives Ergebnis vor Lizenz", f"{_eur(pl['operating_profit_before_royalty'])} EUR"),
                    ("Bandbreite", f"{_pct_de(assessment['cm_range']['low'])} – {_pct_de(assessment['cm_range']['high'])}"),
                    ("Median", _pct_de(assessment["cm_range"]["median"])),
                    ("Lage", _POSITION[assessment["htpl_position"]]),
                    ("Energie", f"{_eur(pl['energy'])} EUR"),
                    ("Berichtigung", f"{_eur(adjustment['profit_eur'])} EUR {direction} operatives Ergebnis"),
                    ("Quelle", "§ 1 Abs. 3a AStG; OECD-VPL Rn. 2.64 und 3.60"),
                ],
                "rows_en": [
                    ("Tested party", "HTPL"),
                    ("Indicator", "Net cost plus"),
                    ("Result", format_pct(pl["net_cost_plus"])),
                    ("Manufacturing costs", _eur_en(pl["manufacturing_costs"])),
                    ("Operating profit before royalty", _eur_en(pl["operating_profit_before_royalty"])),
                    ("Range", f"{format_pct(assessment['cm_range']['low'])} – {format_pct(assessment['cm_range']['high'])}"),
                    ("Median", format_pct(assessment["cm_range"]["median"])),
                    ("Position", assessment["htpl_position"]),
                    ("Energy", _eur_en(pl["energy"])),
                    ("Adjustment", f"{_eur_en(adjustment['profit_eur'])} {'more' if adjustment['profit_eur'] > 0 else 'less'} operating profit"),
                    ("Source", "§ 1 (3a) AStG; OECD TPG paras. 2.64 and 3.60"),
                ],
            }
        )
    else:
        findings.append(
            {
                "id": "pl_margin",
                "severity": "ok",
                "title": f"HTPL Net Cost Plus {format_pct(pl['net_cost_plus'])} liegt in der Bandbreite",
                "title_en": f"HTPL net cost plus {format_pct(pl['net_cost_plus'])} is inside the range",
                "detail": "Rn. 3.60: keine Berichtigung, nur weil ein Median existiert.",
                "detail_en": "Para. 3.60: no adjustment merely because a median exists.",
                "citation": "OECD TPG Rn. 3.60",
                "citation_en": "OECD TPG para. 3.60",
                "rows": [
                    ("Geprüft", "HTPL"),
                    ("Kennzahl", "Net Cost Plus"),
                    ("Ergebnis", _pct_de(pl["net_cost_plus"])),
                    ("Lage", "in der Bandbreite"),
                    ("Berichtigung", "keine"),
                    ("Quelle", "OECD-VPL Rn. 3.60"),
                ],
                "rows_en": [
                    ("Tested party", "HTPL"),
                    ("Indicator", "Net cost plus"),
                    ("Result", format_pct(pl["net_cost_plus"])),
                    ("Position", "inside"),
                    ("Adjustment", "none"),
                    ("Source", "OECD TPG para. 3.60"),
                ],
            }
        )

    us = assessment["htus"]
    if assessment["htus_position"] != "inside":
        findings.append(
            {
                "id": "us_margin",
                "severity": "high",
                "title": f"HTUS Betriebsmarge {format_pct(us['operating_margin'])} liegt über der Bandbreite",
                "title_en": f"HTUS operating margin {format_pct(us['operating_margin'])} is above the range",
                "detail": (
                    f"Vergleichsbandbreite {format_pct(assessment['lrd_range']['low'])} bis "
                    f"{format_pct(assessment['lrd_range']['high'])}, Median {format_pct(assessment['lrd_range']['median'])}. "
                    "Der Routinevertrieb behält einen Restgewinn, der zum Prinzipal gehört."
                ),
                "detail_en": (
                    f"Peer range {format_pct(assessment['lrd_range']['low'])} to "
                    f"{format_pct(assessment['lrd_range']['high'])}, median {format_pct(assessment['lrd_range']['median'])}. "
                    "The routine distributor is keeping a residual that belongs to the principal."
                ),
                "citation": "OECD TPG Rn. 2.64 und 3.62; § 1 Abs. 3a AStG",
                "citation_en": "OECD TPG paras. 2.64 and 3.62; § 1 (3a) AStG",
                "rows": [
                    ("Geprüft", "HTUS"),
                    ("Kennzahl", "Betriebsmarge"),
                    ("Ergebnis", _pct_de(us["operating_margin"])),
                    ("Bandbreite", f"{_pct_de(assessment['lrd_range']['low'])} – {_pct_de(assessment['lrd_range']['high'])}"),
                    ("Median", _pct_de(assessment["lrd_range"]["median"])),
                    ("Lage", "über"),
                    ("Punkt", "Restgewinn gehört zum Prinzipal"),
                    ("Quelle", "OECD-VPL Rn. 2.64 und 3.62; § 1 Abs. 3a AStG"),
                ],
                "rows_en": [
                    ("Tested party", "HTUS"),
                    ("Indicator", "Operating margin"),
                    ("Result", format_pct(us["operating_margin"])),
                    ("Range", f"{format_pct(assessment['lrd_range']['low'])} – {format_pct(assessment['lrd_range']['high'])}"),
                    ("Median", format_pct(assessment["lrd_range"]["median"])),
                    ("Position", "above"),
                    ("Point", "Residual profit belongs to the principal"),
                    ("Source", "OECD TPG paras. 2.64 and 3.62; § 1 (3a) AStG"),
                ],
            }
        )

    if pl["royalty"] > 0:
        findings.append(
            {
                "id": "royalty_characterization",
                "severity": "medium",
                "title": "Lizenz und Lohnfertiger-Charakterisierung passen nicht zusammen",
                "title_en": "A royalty does not sit with the contract-manufacturer profile",
                "detail": (
                    f"HTPL zahlt {_eur(pl['royalty'])} EUR Lizenz an HTDE und fertigt nur für HTDE. "
                    "Die Lizenz ist gesondert zu vergüten, darf die Routinevergütung aber nicht unter die Bandbreite drücken."
                ),
                "detail_en": (
                    f"HTPL pays {_eur_en(pl['royalty'])} of royalty to HTDE and manufactures only for HTDE. "
                    "The royalty is remunerated on its own and must not push the routine return below the range."
                ),
                "citation": "§ 1 Abs. 3c AStG; OECD TPG Rn. 6.32",
                "citation_en": "§ 1 (3c) AStG; OECD TPG para. 6.32",
                "rows": [
                    ("Zahler", "HTPL"),
                    ("Empfänger", "HTDE"),
                    ("Lizenz", f"{_eur(pl['royalty'])} EUR"),
                    ("Profil", "Lohnfertiger, nur für HTDE"),
                    ("Punkt", "Eigener Geschäftsvorfall, Routinevergütung bleibt"),
                    ("Quelle", "§ 1 Abs. 3c AStG; OECD-VPL Rn. 6.32"),
                ],
                "rows_en": [
                    ("Payer", "HTPL"),
                    ("Recipient", "HTDE"),
                    ("Royalty", _eur_en(pl["royalty"])),
                    ("Profile", "Contract manufacturer, only for HTDE"),
                    ("Point", "Separate transaction; routine return stays"),
                    ("Source", "§ 1 (3c) AStG; OECD TPG para. 6.32"),
                ],
            }
        )

    if gaps:
        findings.append(
            {
                "id": "missing_contract",
                "severity": "medium",
                "title": "Managementumlage ohne benannten Vertrag",
                "title_en": "Management charge with no named contract",
                "detail": "Die Transaktionsmatrix verlangt die vertragliche Grundlage. Die Umlage ist gebucht, der Vertrag ist leer.",
                "detail_en": "The transaction matrix requires the contractual basis. The charge is booked. The contract field is empty.",
                "citation": "§ 90 Abs. 3 AO; BMF-Merkblatt 2. April 2025",
                "citation_en": "§ 90 (3) AO; BMF leaflet of 2 April 2025",
                "rows": [
                    ("Geschäftsvorfall", "Managementumlage"),
                    ("Gebucht", "ja"),
                    ("Vertrag", "leer"),
                    ("Quelle", "§ 90 Abs. 3 AO; BMF-Merkblatt 2. April 2025"),
                ],
                "rows_en": [
                    ("Transaction", "Management charge"),
                    ("Booked", "yes"),
                    ("Contract", "blank"),
                    ("Source", "§ 90 (3) AO; BMF leaflet of 2 April 2025"),
                ],
            }
        )

    prior = assessment["history"]["HTPL"]
    prior_positions = []
    for item in prior:
        if item["year"] == assessment["year"]:
            continue
        prior_positions.append(locate(item["net_cost_plus"], assessment["cm_range"]))
    if assessment["htpl_position"] != "inside" and prior_positions and all(item == "inside" for item in prior_positions):
        findings.append(
            {
                "id": "energy_passthrough",
                "severity": "high",
                "title": "Der Verrechnungspreis gibt den Energieschock nicht weiter",
                "title_en": "The transfer price does not pass the energy shock through",
                "detail": (
                    "2023 und 2024 lag die Nettokostenaufschlagsmarge bei 5,00 % und damit in der Bandbreite. "
                    "2025 steigen die Energiekosten der Induktionsöfen, der Preis an HTDE nicht im gleichen Maß. "
                    "Das ist ein Preisfehler beim Lohnfertiger, keine Verlagerung des Know-hows."
                ),
                "detail_en": (
                    "In 2023 and 2024 the net cost plus was 5.00% and inside the range. "
                    "In 2025 the induction furnaces' energy cost rises and the price to HTDE does not keep up. "
                    "That is a pricing failure at the contract manufacturer, not a transfer of the know-how."
                ),
                "citation": "OECD TPG Rn. 1.51; Fallnotiz Härtereiprozess",
                "citation_en": "OECD TPG para. 1.51; case note on the hardening process",
                "rows": [
                    ("2023 und 2024", "5,00 %, in der Bandbreite"),
                    ("2025", "unter der Bandbreite"),
                    ("Energie", "steigt"),
                    ("Preis an HTDE", "folgt nicht"),
                    ("Einordnung", "Preisfehler, keine Know-how-Verlagerung"),
                    ("Quelle", "OECD-VPL Rn. 1.51"),
                ],
                "rows_en": [
                    ("2023 and 2024", "5.00%, inside the range"),
                    ("2025", "below the range"),
                    ("Energy", "up"),
                    ("Price to HTDE", "does not follow"),
                    ("Reading", "Pricing failure, not a know-how transfer"),
                    ("Source", "OECD TPG para. 1.51"),
                ],
            }
        )

    if assessment["htpl_position"] != "inside":
        findings.append(
            {
                "id": "function_transfer_escape",
                "severity": "medium",
                "title": "Die Ausnahme zur Funktionsverlagerung ist so nicht erfüllt",
                "title_en": "The function-transfer escape is not met",
                "detail": (
                    "HTPL arbeitet ausschließlich für HTDE. § 1 Abs. 3b AStG stellt die Transferpaketbewertung "
                    "nur zurück, wenn das Entgelt außerdem nach der Kostenaufschlagsmethode fremdüblich ist. "
                    "Die Marge 2025 liegt außerhalb der Bandbreite."
                ),
                "detail_en": (
                    "HTPL works exclusively for HTDE. § 1 Abs. 3b AStG sets the transfer-package valuation "
                    "aside only if the remuneration is also an arm's length cost plus. "
                    "The 2025 margin is outside the range."
                ),
                "citation": "§ 1 Abs. 3b AStG",
                "citation_en": "§ 1 (3b) AStG",
                "rows": [
                    ("Ausschließlich für HTDE", "ja"),
                    ("Fremdüblicher Kostenaufschlag", "nein"),
                    ("Ausnahme", "nicht erfüllt"),
                    ("Quelle", "§ 1 Abs. 3b AStG"),
                ],
                "rows_en": [
                    ("Exclusively for HTDE", "yes"),
                    ("Arm's length cost plus", "no"),
                    ("Escape", "not met"),
                    ("Source", "§ 1 (3b) AStG"),
                ],
            }
        )
    return findings


def run_case(year: int = 2025) -> dict:
    ledger = build_ledger()
    far = run_far()
    assessment = assess(year, ledger)
    matrix = transaction_matrix(year, ledger)
    gaps = matrix_gaps(matrix)
    found = findings_for(assessment, gaps)
    critic = critique_case(assessment, gaps)
    return {
        "year": year,
        "far": far,
        "assessment": assessment,
        "matrix": matrix,
        "gaps": gaps,
        "findings": found,
        "critic": critic,
        "ledger_rows": int(len(ledger)),
    }


def ask(question: str) -> dict:
    routes = route_question(question)
    rag = answer_question(question) if "guideline" in routes or "far" in routes else None
    graph = run_kg(question) if "guideline" in routes or "far" in routes else None
    screen = None
    margins = None
    case = None
    if "benchmarking" in routes:
        screen = evaluate()
    if "margin" in routes or "matrix" in routes or "far" in routes:
        case = run_case()
        margins = case["assessment"]
    critic = None
    if rag is not None:
        critic = critique_retrieval(rag["citations"], rag["hits"])
    return {
        "routes": routes,
        "rag": rag,
        "graph": graph,
        "screening": screen,
        "assessment": margins,
        "case": case,
        "critic": critic,
    }
