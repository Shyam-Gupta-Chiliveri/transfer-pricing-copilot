"""Transaction-type, method and documentation graph.

Same idea as the materials knowledge graph: labeled edges, queried by the
words in the question. The nodes are transfer-pricing concepts, not alloys.
"""

from __future__ import annotations

from collections import defaultdict

# src, relation, dst, {en, de}
TRIPLES: list[tuple[str, str, str, dict[str, str]]] = [
    ("controlled_transaction", "priced_under", "arms_length", {"en": "OECD TPG para. 1.6 / § 1 Abs. 1 AStG.", "de": "OECD-VPL Rn. 1.6 / § 1 Abs. 1 AStG."}),
    ("arms_length", "tested_by", "comparability_analysis", {"en": "Delineate, then compare. Para. 1.33.", "de": "Zuerst abgrenzen, dann vergleichen. Rn. 1.33."}),
    ("comparability_analysis", "uses", "five_factors", {"en": "Contract, FAR, characteristics, market, strategy. Para. 1.36.", "de": "Vertrag, FAR, Merkmale, Markt, Strategie. Rn. 1.36."}),
    ("five_factors", "includes", "functional_analysis", {"en": "Functions, assets, risks. Para. 1.51.", "de": "Funktionen, Wirtschaftsgüter, Risiken. Rn. 1.51."}),
    ("CUP", "type", "traditional_method", {"en": "Comparable uncontrolled price. Para. 2.14.", "de": "Preisvergleichsmethode. Rn. 2.14."}),
    ("resale_price", "type", "traditional_method", {"en": "Gross margin of a distributor. Para. 2.27.", "de": "Bruttomarge eines Vertriebs. Rn. 2.27."}),
    ("cost_plus", "type", "traditional_method", {"en": "Gross mark-up on the supplier's costs. Para. 2.45.", "de": "Bruttoaufschlag auf die Kosten des Lieferanten. Rn. 2.45."}),
    ("TNMM", "type", "profit_method", {"en": "Net profit indicator on costs, sales or assets. Para. 2.64.", "de": "Nettogewinnindikator auf Kosten, Umsatz oder Vermögen. Rn. 2.64."}),
    ("profit_split", "type", "profit_method", {"en": "Two-sided split. Para. 2.114.", "de": "Zweiseitige Aufteilung. Rn. 2.114."}),
    ("method_choice", "follows", "most_appropriate", {"en": "Para. 2.2. No duty to disprove every other method.", "de": "Rn. 2.2. Keine Pflicht, jede andere Methode zu widerlegen."}),
    ("traditional_method", "preferred_if", "equally_reliable", {"en": "Para. 2.3 only if reliability is equal.", "de": "Rn. 2.3 nur bei gleicher Zuverlässigkeit."}),
    ("contract_manufacturer", "tested_with", "TNMM", {"en": "Net cost plus when gross mark-ups are unreliable.", "de": "Net Cost Plus, wenn Bruttoaufschläge unzuverlässig sind."}),
    ("contract_manufacturer", "pli", "net_cost_plus", {"en": "Operating profit / relevant manufacturing costs.", "de": "Operatives Ergebnis / relevante Fertigungskosten."}),
    ("contract_manufacturer", "not_tested_with", "profit_split", {"en": "No unique contribution on the plant side. Para. 2.119.", "de": "Kein einzigartiger Beitrag des Werks. Rn. 2.119."}),
    ("limited_risk_distributor", "tested_with", "TNMM", {"en": "Operating margin on sales.", "de": "Betriebsmarge auf den Umsatz."}),
    ("limited_risk_distributor", "cross_check", "berry_ratio", {"en": "Gross profit / operating expenses. Para. 2.106.", "de": "Bruttogewinn / Betriebskosten. Rn. 2.106."}),
    ("entrepreneur", "retains", "residual_profit", {"en": "After routine entities earn an arm's length return.", "de": "Nachdem die Routinegesellschaften eine fremdübliche Vergütung haben."}),
    ("process_know_how", "analysed_under", "DEMPE", {"en": "Para. 6.32. Control of the intangible, not the logo on the furnace.", "de": "Rn. 6.32. Kontrolle über den immateriellen Wert, nicht das Schild am Ofen."}),
    ("HT_DE", "owns", "process_know_how", {"en": "Recipes, PPAP, customer contracts.", "de": "Rezeptur, PPAP, Kundenverträge."}),
    ("HT_PL", "characterized_as", "contract_manufacturer", {"en": "Hardens only to HT-DE specifications.", "de": "Härtet nur nach Vorgabe von HTDE."}),
    ("HT_US", "characterized_as", "limited_risk_distributor", {"en": "Sells to OEMs without owning the technology.", "de": "Verkauft an OEMs, ohne die Technik zu besitzen."}),
    ("range", "narrowed_by", "interquartile", {"en": "§ 1 Abs. 3a AStG: drop the outer quarters.", "de": "§ 1 Abs. 3a AStG: die äußeren Viertel bleiben außen vor."}),
    ("outside_range", "adjusted_to", "median", {"en": "Unless another in-range point is credibly better.", "de": "Es sei denn, ein anderer Wert in der Bandbreite ist glaubhaft besser."}),
    ("inside_range", "requires", "no_adjustment", {"en": "OECD TPG para. 3.60.", "de": "OECD-VPL Rn. 3.60."}),
    ("function_transfer", "may_require", "transfer_package", {"en": "§ 1 Abs. 3b AStG, unless the cost-plus escape applies.", "de": "§ 1 Abs. 3b AStG, sofern die Kostenaufschlags-Ausnahme nicht greift."}),
    ("cost_plus_escape", "requires", "exclusive_and_cost_plus", {"en": "Function only for the principal, and an arm's length cost plus.", "de": "Funktion nur für den Prinzipal und ein fremdüblicher Kostenaufschlag."}),
    ("transaction_matrix", "required_by", "AO_90", {"en": "Subject, parties, volume, consideration, contract, method, territory.", "de": "Gegenstand, Beteiligte, Volumen, Entgelt, Vertrag, Methode, Gebiet."}),
    ("royalty", "tested_separately", "intangible_transaction", {"en": "§ 1 Abs. 3c AStG. Do not bury it in the manufacturing PLI.", "de": "§ 1 Abs. 3c AStG. Nicht in der Fertigungskennzahl verstecken."}),
    ("documentation", "includes", "master_file", {"en": "OECD Chapter V group overview.", "de": "Überblick der Gruppe nach OECD-Kapitel V."}),
    ("documentation", "includes", "local_file", {"en": "Local entity analysis and benchmarks.", "de": "Lokale Analyse und Benchmarks."}),
    ("documentation", "includes", "transaction_matrix", {"en": "German addition under § 90 Abs. 3 AO.", "de": "Deutsche Ergänzung nach § 90 Abs. 3 AO."}),
]

RELATIONS = {
    "en": {
        "priced_under": "priced under",
        "tested_by": "tested by",
        "uses": "uses",
        "includes": "includes",
        "type": "is a",
        "follows": "follows",
        "preferred_if": "preferred if",
        "tested_with": "tested with",
        "pli": "indicator",
        "not_tested_with": "not tested with",
        "cross_check": "cross-check",
        "retains": "retains",
        "analysed_under": "analysed under",
        "owns": "owns",
        "characterized_as": "characterized as",
        "narrowed_by": "narrowed by",
        "adjusted_to": "adjusted to",
        "requires": "requires",
        "may_require": "may require",
        "required_by": "required by",
        "tested_separately": "tested separately as",
    },
    "de": {
        "priced_under": "bepreist nach",
        "tested_by": "geprüft durch",
        "uses": "nutzt",
        "includes": "umfasst",
        "type": "ist eine",
        "follows": "folgt",
        "preferred_if": "vorrangig wenn",
        "tested_with": "geprüft mit",
        "pli": "Kennzahl",
        "not_tested_with": "nicht geprüft mit",
        "cross_check": "Gegenprobe",
        "retains": "behält",
        "analysed_under": "analysiert nach",
        "owns": "hält",
        "characterized_as": "charakterisiert als",
        "narrowed_by": "eingeengt durch",
        "adjusted_to": "berichtigt auf",
        "requires": "verlangt",
        "may_require": "kann verlangen",
        "required_by": "verlangt von",
        "tested_separately": "gesondert geprüft als",
    },
}

ALIASES = {
    "fremdvergleich": "arms_length",
    "arm's length": "arms_length",
    "arms length": "arms_length",
    "comparability": "comparability_analysis",
    "vergleichbarkeit": "comparability_analysis",
    "functional": "functional_analysis",
    "funktions": "functional_analysis",
    "far": "functional_analysis",
    "cup": "CUP",
    "preisvergleich": "CUP",
    "resale": "resale_price",
    "wiederverkauf": "resale_price",
    "cost plus": "cost_plus",
    "kostenaufschlag": "cost_plus",
    "tnmm": "TNMM",
    "nettomarge": "TNMM",
    "profit split": "profit_split",
    "gewinnaufteilung": "profit_split",
    "lohnfertiger": "contract_manufacturer",
    "contract manufacturer": "contract_manufacturer",
    "vertrieb": "limited_risk_distributor",
    "distributor": "limited_risk_distributor",
    "entrepreneur": "entrepreneur",
    "prinzipal": "entrepreneur",
    "dempe": "DEMPE",
    "know-how": "process_know_how",
    "knowhow": "process_know_how",
    "immateriell": "process_know_how",
    "intangible": "process_know_how",
    "median": "median",
    "interquartil": "interquartile",
    "iqr": "interquartile",
    "bandbreite": "range",
    "funktionsverlagerung": "function_transfer",
    "transferpaket": "transfer_package",
    "transaktionsmatrix": "transaction_matrix",
    "matrix": "transaction_matrix",
    "lizenz": "royalty",
    "royalty": "royalty",
    "härte": "HT_PL",
    "polen": "HT_PL",
    "poland": "HT_PL",
    "härtetechnik": "HT_DE",
    "haertetechnik": "HT_DE",
    "berry": "berry_ratio",
    "master file": "master_file",
    "local file": "local_file",
}


def _index():
    out: dict[str, list[tuple[str, str, str, str]]] = defaultdict(list)
    for src, rel, dst, note in TRIPLES:
        out[src.lower()].append((src, rel, dst, note))
        out[dst.lower()].append((src, rel, dst, note))
        out[rel.lower()].append((src, rel, dst, note))
    return out


_INDEX = _index()


def resolve_entities(query: str) -> list[str]:
    text = query.lower()
    found: list[str] = []
    for alias, node in sorted(ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in text and node not in found:
            found.append(node)
    return found


def query_graph(query: str, max_edges: int = 8) -> dict:
    nodes = resolve_entities(query)
    edges: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    for node in nodes:
        for src, rel, dst, note in _INDEX.get(node.lower(), []):
            key = (src, rel, dst)
            if key in seen:
                continue
            seen.add(key)
            note_en = note["en"] if isinstance(note, dict) else note
            note_de = note["de"] if isinstance(note, dict) else note_en
            edges.append(
                {
                    "src": src,
                    "relation": rel,
                    "dst": dst,
                    "note": note_en,
                    "note_en": note_en,
                    "note_de": note_de,
                }
            )
            if len(edges) >= max_edges:
                break
        if len(edges) >= max_edges:
            break
    return {"nodes": nodes, "edges": edges}


def relation_label(relation: str, lang: str) -> str:
    return RELATIONS.get(lang, RELATIONS["en"]).get(relation, relation.replace("_", " "))
