"""Critic. Checks citations and whether the case result matches the rules."""

from __future__ import annotations

from tp_copilot.agents.far_agent import profile_map


def critique_retrieval(citations: list[dict], hits: list[dict]) -> dict:
    retrieved = {hit["paragraph"] for hit in hits}
    missing = [item["paragraph"] for item in citations if item["paragraph"] not in retrieved]
    if missing:
        joined = ", ".join(missing)
        notes = [f"Zitat ohne abgerufene Textstelle: {joined}"]
        notes_en = [f"Citation with no retrieved passage: {joined}"]
    else:
        notes = ["Jedes genannte Zitat stammt aus dem abgerufenen Kontext."]
        notes_en = ["Every citation comes from a retrieved passage."]
    return {"ok": not missing, "notes": notes, "notes_en": notes_en}


def _pair(notes: list[str], notes_en: list[str], de: str, en: str) -> None:
    notes.append(de)
    notes_en.append(en)


def critique_case(assessment: dict, matrix_gaps: list[dict]) -> dict:
    notes: list[str] = []
    notes_en: list[str] = []
    ok = True
    profiles = profile_map()
    pl_method = profiles["HTPL"]["method_key"]
    if pl_method == "profit_split":
        ok = False
        _pair(notes, notes_en, "Gewinnaufteilung passt nicht zum Lohnfertiger (Rn. 2.119).", "A profit split does not fit a contract manufacturer (para. 2.119).")
    elif pl_method == "TNMM":
        _pair(notes, notes_en, "Methodenwahl HTPL ist TNMM / Net Cost Plus, passend zur Routinefunktion.", "The HTPL method is TNMM / net cost plus, which matches the routine function.")
    else:
        ok = False
        _pair(notes, notes_en, "HTPL hat keine passende einseitige Methode.", "HTPL has no fitting one-sided method.")

    if assessment["htpl_position"] != "inside":
        adjustment = assessment["htpl_adjustment"]
        if not adjustment or adjustment["rule"] != "§ 1 Abs. 3a AStG":
            ok = False
            _pair(
                notes, notes_en,
                "Außerhalb der Bandbreite muss der Median nach § 1 Abs. 3a AStG geprüft werden.",
                "Outside the range, the median under § 1 Abs. 3a AStG has to be considered.",
            )
        else:
            _pair(
                notes, notes_en,
                "HTPL liegt außerhalb der eingeengten Bandbreite. Korrekturpunkt ist der Median, sofern kein anderer Wert in der Bandbreite glaubhaft besser passt.",
                "HTPL is outside the narrowed range. The adjustment point is the median, unless another point inside the range is credibly better.",
            )
    else:
        _pair(
            notes, notes_en,
            "HTPL liegt in der Bandbreite. OECD-VPL Rn. 3.60: keine Berichtigung allein deshalb.",
            "HTPL is inside the range. OECD TPG para. 3.60: no adjustment merely because a median exists.",
        )

    if assessment["htus_position"] != "inside":
        _pair(
            notes, notes_en,
            "HTUS liegt außerhalb der Vertriebsbandbreite. Restgewinn gehört nicht in den Routinevertrieb.",
            "HTUS is outside the distributor range. Residual profit does not belong in the routine distributor.",
        )
    else:
        _pair(notes, notes_en, "HTUS liegt in der Vertriebsbandbreite.", "HTUS is inside the distributor range.")

    if assessment["htpl"]["royalty"] > 0 and "Lohnfertiger" in profiles["HTPL"]["characterization"]:
        _pair(
            notes, notes_en,
            "HTPL zahlt eine Lizenz und ist zugleich Lohnfertiger. Die Lizenz ist ein eigener Geschäftsvorfall (§ 1 Abs. 3c AStG) und darf die Routinevergütung nicht aushöhlen.",
            "HTPL pays a royalty and is also a contract manufacturer. The royalty is a separate transaction (§ 1 Abs. 3c AStG) and must not hollow out the routine return.",
        )

    if matrix_gaps:
        count = len(matrix_gaps)
        _pair(
            notes, notes_en,
            f"{count} Buchungsart ohne benannten Vertrag. Die Transaktionsmatrix nach § 90 Abs. 3 AO verlangt die vertragliche Grundlage.",
            f"{count} transaction type has no named contract. The matrix under § 90 Abs. 3 AO requires the contractual basis.",
        )
    else:
        _pair(notes, notes_en, "Jede aggregierte Buchungsart nennt einen Vertrag.", "Every aggregated transaction type names a contract.")

    if assessment["htpl_position"] != "inside":
        _pair(
            notes, notes_en,
            "§ 1 Abs. 3b AStG lässt die Transferpaketbewertung nur beiseite, wenn die Funktion ausschließlich für den Prinzipal ausgeübt wird und das Entgelt einem Kostenaufschlag entspricht. Die Ausschließlichkeit liegt vor, der Aufschlag in diesem Jahr nicht.",
            "§ 1 Abs. 3b AStG sets a transfer-package valuation aside only if the function is performed exclusively for the principal and the remuneration is an arm's length cost plus. Exclusivity is met. This year's mark-up is not.",
        )

    return {"ok": ok, "notes": notes, "notes_en": notes_en}
