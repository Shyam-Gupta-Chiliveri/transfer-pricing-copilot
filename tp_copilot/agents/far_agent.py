"""Functional analysis for the fictional Härtetechnik group."""

from __future__ import annotations

PROFILES = [
    {
        "entity": "HTDE",
        "name": "Härtetechnik AG",
        "country": "Deutschland",
        "country_en": "Germany",
        "functions": [
            "Entwicklung der Härteparameter und der Prozessfenster",
            "PPAP-Freigabe und 8D-Verantwortung gegenüber dem OEM",
            "Strategischer Einkauf des Stahls und Kundenverträge",
            "Steuerung von DEMPE am Prozess-Know-how",
        ],
        "functions_en": [
            "Develops the hardening parameters and the process window",
            "PPAP approval and 8D responsibility toward the OEM",
            "Strategic steel purchasing and customer contracts",
            "Controls DEMPE of the process know-how",
        ],
        "assets": [
            "Nicht eingetragenes Prozess-Know-how",
            "OEM-Rahmenverträge",
            "Qualitätsmanagementsystem",
        ],
        "assets_en": [
            "Unregistered process know-how",
            "OEM framework contracts",
            "Quality-management system",
        ],
        "risks": [
            "Marktrisiko und Auslastung der Gruppe",
            "Gewährleistung und Produkthaftung",
            "Energiepreisrisiko, soweit der Verrechnungspreis es nicht weitergibt",
        ],
        "risks_en": [
            "Market risk and group capacity",
            "Warranty and product liability",
            "Energy-price risk, unless the transfer price passes it on",
        ],
        "characterization": "Prinzipal (Entrepreneur)",
        "characterization_en": "Principal (entrepreneur)",
        "method": "Einseitige Routinevergütung der anderen Gesellschaften, Restgewinn verbleibt bei HTDE",
        "method_en": "One-sided routine returns for the other entities. The residual stays with HTDE",
        "method_key": "residual",
        "why": (
            "HTDE kontrolliert Rezeptur, Freigabe und Kundenbeziehung. "
            "Die Rendite aus dem immateriellen Wert steht nach OECD-VPL Rn. 6.32 "
            "bei der Gesellschaft, die DEMPE steuert."
        ),
        "why_en": (
            "HTDE controls the recipe, the approval and the customer relationship. "
            "Under OECD TPG para. 6.32 the return on the intangible belongs to the "
            "entity that controls DEMPE."
        ),
    },
    {
        "entity": "HTPL",
        "name": "Härtetechnik Polska sp. z o.o.",
        "country": "Polen",
        "country_en": "Poland",
        "functions": [
            "Induktionshärten und Zerspanen nach Vorgabe von HTDE",
            "Lokale Fertigungsplanung innerhalb des Abrufs",
            "Wareneingangs- und Prozessprüfung vor Ort",
        ],
        "functions_en": [
            "Induction hardening and machining to HTDE's specification",
            "Local production planning inside the customer's call-off",
            "Incoming and in-process inspection on site",
        ],
        "assets": [
            "Öfen und Maschinen",
            "Keine eigenen OEM-Verträge",
            "Kein wirtschaftliches Eigentum an der Rezeptur",
        ],
        "assets_en": [
            "Furnaces and machines",
            "No OEM contracts of its own",
            "No economic ownership of the recipe",
        ],
        "risks": [
            "Begrenztes Auslastungsrisiko wegen Abrufverpflichtung von HTDE",
            "Kein Marktrisiko",
            "Lokales Personalrisiko",
        ],
        "risks_en": [
            "Limited capacity risk because HTDE has a take-or-pay call-off",
            "No market risk",
            "Local staff risk",
        ],
        "characterization": "Lohnfertiger (contract manufacturer)",
        "characterization_en": "Contract manufacturer",
        "method": "TNMM mit Net Cost Plus",
        "method_en": "TNMM with net cost plus",
        "method_key": "TNMM",
        "why": (
            "Bruttoaufschläge sind bei Energie, Ausschuss und Gemeinkosten "
            "zwischen Härtereien schlecht vergleichbar. Die TNMM auf die "
            "Fertigungskosten ist nach Rn. 2.2 und 2.64 die geeignetere Methode. "
            "Eine Gewinnaufteilung scheidet aus, weil nur HTDE einen einzigartigen "
            "Beitrag leistet (Rn. 2.119)."
        ),
        "why_en": (
            "Gross mark-ups are hard to compare across hardening plants because "
            "energy, scrap and overhead are classified differently. TNMM on "
            "manufacturing costs is the more appropriate method under paras. 2.2 "
            "and 2.64. A profit split does not fit, because only HTDE makes a "
            "unique contribution (para. 2.119)."
        ),
    },
    {
        "entity": "HTUS",
        "name": "Härtetechnik North America Inc.",
        "country": "USA",
        "country_en": "United States",
        "functions": [
            "Ansprache der OEM-Werke in den USA",
            "Lokale Logistik ohne eigenes Fertigungs-Know-how",
            "Keine eigene Produktentwicklung",
        ],
        "functions_en": [
            "Calls on OEM plants in the United States",
            "Local logistics without its own manufacturing know-how",
            "No product development of its own",
        ],
        "assets": ["Vertriebsteam", "Keine Marke und keine Patente"],
        "assets_en": ["Sales team", "No brand and no patents"],
        "risks": [
            "Begrenztes Kreditrisiko",
            "Kein Garantierisiko über eine Bagatellgrenze hinaus",
        ],
        "risks_en": [
            "Limited credit risk",
            "No warranty risk above a small threshold",
        ],
        "characterization": "Routinevertrieb (limited-risk distributor)",
        "characterization_en": "Limited-risk distributor",
        "method": "TNMM mit Betriebsmarge, Berry Ratio als Gegenprobe",
        "method_en": "TNMM with operating margin, Berry ratio as a cross-check",
        "method_key": "TNMM",
        "why": (
            "HTUS kauft und verkauft, ohne der Ware einen technischen Wert "
            "hinzuzufügen. Die Betriebsmarge auf den Umsatz ist der passende "
            "Indikator (Rn. 2.64). Der Berry Ratio (Rn. 2.106) prüft, ob der "
            "Bruttogewinn nur die Betriebskosten deckt."
        ),
        "why_en": (
            "HTUS buys and resells without adding technical value to the goods. "
            "The operating margin on sales is the fitting indicator (para. 2.64). "
            "The Berry ratio (para. 2.106) checks whether gross profit only covers "
            "operating expenses."
        ),
    },
]


def run_far() -> dict:
    return {
        "group": "Härtetechnik AG",
        "case": (
            "Fiktiver Automobilzulieferer. Mutter in Stuttgart, Härterei in Polen, "
            "Vertriebsgesellschaft in Detroit. Kein Mandant, keine echten Buchungen."
        ),
        "case_en": (
            "Fictional automotive supplier. Parent in Stuttgart, hardening plant "
            "in Poland, sales company in Detroit. No client and no real bookings."
        ),
        "profiles": PROFILES,
    }


def profile_map() -> dict[str, dict]:
    return {profile["entity"]: profile for profile in PROFILES}
