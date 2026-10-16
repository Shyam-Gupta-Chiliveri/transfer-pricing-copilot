"""Route a question to the specialists that should answer it."""

from __future__ import annotations

ROUTES: dict[str, tuple[str, ...]] = {
    "guideline": (
        "oecd", "astg", "fremdvergleich", "arm's length", "arms length", "tnmm",
        "cup", "cost plus", "kostenaufschlag", "preisvergleich", "paragraph",
        "randnummer", "leitlinie", "guideline", "methode", "method", "dempe",
        "verwaltungsgrund", "transaktionsmatrix", "§", "abs.", "berry",
        "gewinnaufteilung", "profit split", "bandbreite", "median",
    ),
    "benchmarking": (
        "benchmark", "comparable", "vergleichsunternehmen", "screening",
        "classifier", "peer", "orbis",
    ),
    "margin": (
        "margin", "marge", "interquartil", "net cost", "operating margin",
        "betriebsmarge", "pli", "iqr", "quartile",
    ),
    "far": (
        "function", "funktion", "risiko", "risk", "value chain", "wertschöpfung",
        "wertschoepfung", "lohnfertiger", "charakter", "härte", "haerte",
        "härtetechnik", "haertetechnik", "far", "dempe",
    ),
    "matrix": (
        "matrix", "buchung", "ledger", "vertrag", "contract", "sap",
        "transaktion", "booking",
    ),
}


def route_question(question: str) -> list[str]:
    text = question.lower()
    chosen = [name for name, words in ROUTES.items() if any(word in text for word in words)]
    if not chosen:
        return ["guideline"]
    if "guideline" not in chosen and any(word in text for word in ("why", "warum", "which method", "welche methode")):
        chosen.insert(0, "guideline")
    return chosen
