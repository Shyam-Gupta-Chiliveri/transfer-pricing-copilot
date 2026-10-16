"""Original study notes for the portfolio RAG.

These notes are not the OECD Transfer Pricing Guidelines and not a BMF letter.
They paraphrase the public structure of those sources so the demo can cite
paragraph numbers without redistributing copyrighted text. Official files
dropped into data/regelwerke/ are chunked separately at runtime.
"""

from __future__ import annotations


def note(
    note_id: str,
    source: str,
    source_id: str,
    paragraph: str,
    title: str,
    keywords: list[str],
    text_en: str,
    text_de: str,
) -> dict:
    return {
        "id": note_id,
        "source": source,
        "source_id": source_id,
        "paragraph": paragraph,
        "title": title,
        "keywords": keywords,
        "text_en": text_en.strip(),
        "text_de": text_de.strip(),
    }


NOTES: list[dict] = [
    note(
        "oecd-1.6",
        "OECD TPG 2022",
        "oecd",
        "1.6",
        "Arm's length principle",
        ["arm's length", "article 9", "fremdvergleichsgrundsatz", "independent enterprises", "1.6"],
        """
        Study note on OECD TPG 2022 paragraph 1.6. The arm's length principle,
        as stated in Article 9 of the OECD Model Tax Convention, asks whether
        the conditions of a transaction between associated enterprises differ
        from the conditions that independent enterprises would have agreed.
        If they differ, profit that would have accrued to one of them may be
        included in its profit and taxed. This is the starting point for every
        later method, range and documentation rule in this project.
        """,
        """
        Studiennotiz zu OECD-VPL 2022, Randnummer 1.6. Der Fremdvergleichsgrundsatz
        folgt aus Artikel 9 des OECD-Musterabkommens. Geprüft wird, ob die
        Bedingungen einer Geschäftsbeziehung zwischen verbundenen Unternehmen
        von den Bedingungen abweichen, die voneinander unabhängige Unternehmen
        vereinbart hätten. Weichen sie ab, können die entgangenen Gewinne
        hinzugerechnet und besteuert werden. Alle Methoden, Bandbreiten und
        Aufzeichnungspflichten in diesem Projekt bauen darauf auf.
        """,
    ),
    note(
        "oecd-1.33",
        "OECD TPG 2022",
        "oecd",
        "1.33",
        "Comparability analysis",
        ["comparability analysis", "accurately delineate", "controlled transaction", "vergleichbarkeitsanalyse", "1.33"],
        """
        Study note on paragraph 1.33. A comparability analysis has two steps.
        First, identify the commercial relations and accurately delineate the
        controlled transaction, including the economically relevant
        circumstances. Second, compare that delineated transaction with
        comparable transactions between independent enterprises. Chapters II
        and III deal with the pricing step. The delineation step is not yet
        the choice of CUP, cost plus or TNMM.
        """,
        """
        Studiennotiz zu Randnummer 1.33. Eine Vergleichbarkeitsanalyse hat zwei
        Schritte. Zuerst werden die Geschäftsbeziehungen identifiziert und der
        kontrollierte Geschäftsvorfall wird genau abgegrenzt, einschließlich
        der wirtschaftlich relevanten Umstände. Danach wird dieser abgegrenzte
        Vorgang mit vergleichbaren Geschäften unabhängiger Unternehmen
        verglichen. Die Kapitel II und III betreffen die Bepreisung. Die
        Abgrenzung ist noch nicht die Wahl von Preisvergleich, Kostenaufschlag
        oder TNMM.
        """,
    ),
    note(
        "oecd-1.36",
        "OECD TPG 2022",
        "oecd",
        "1.36",
        "Comparability factors",
        ["comparability factors", "contractual terms", "economic circumstances", "business strategies", "1.36"],
        """
        Study note on paragraph 1.36. To delineate the transaction, the
        Guidelines group the economically relevant characteristics into five
        comparability factors: the contractual terms; the functions performed,
        assets used and risks assumed; the characteristics of the property or
        services; the economic circumstances and the market; and the business
        strategies. A benchmark that ignores one of these factors is incomplete.
        """,
        """
        Studiennotiz zu Randnummer 1.36. Für die Abgrenzung fassen die Leitlinien
        die wirtschaftlich relevanten Merkmale in fünf Vergleichbarkeitsfaktoren:
        Vertragsbedingungen; ausgeübte Funktionen, eingesetzte Wirtschaftsgüter
        und übernommene Risiken; Merkmale der übertragenen Güter oder
        Dienstleistungen; wirtschaftliche Umstände und Markt; Geschäftsstrategien.
        Ein Benchmark, der einen dieser Faktoren auslässt, ist unvollständig.
        """,
    ),
    note(
        "oecd-1.51",
        "OECD TPG 2022",
        "oecd",
        "1.51",
        "Functional analysis",
        ["functional analysis", "functions assets risks", "FAR", "funktionsanalyse", "1.51"],
        """
        Study note on paragraph 1.51. Between independents, the price usually
        reflects the functions each party performs, the assets it uses and the
        risks it actually assumes. A functional analysis (functions, assets,
        risks) is therefore required before a method is chosen. Contractual
        risk allocation is the starting point, but it has to match the conduct
        of the parties. A plant that only processes to the principal's recipe
        does not become an entrepreneur because the contract uses that word.
        """,
        """
        Studiennotiz zu Randnummer 1.51. Zwischen unabhängigen Unternehmen bildet
        der Preis in der Regel die Funktionen, die eingesetzten Wirtschaftsgüter
        und die tatsächlich übernommenen Risiken ab. Eine Funktions- und
        Risikoanalyse ist deshalb vor der Methodenwahl nötig. Die vertragliche
        Risikozuordnung ist der Ausgangspunkt, muss aber zum tatsächlichen
        Verhalten passen. Ein Werk, das nur nach Rezeptur des Prinzipals
        fertigt, wird nicht dadurch zum Entrepreneur, dass der Vertrag dieses
        Wort verwendet.
        """,
    ),
    note(
        "oecd-2.1",
        "OECD TPG 2022",
        "oecd",
        "2.1",
        "Recognised methods",
        ["traditional transaction methods", "transactional profit methods", "CUP", "resale price", "cost plus", "TNMM", "profit split", "2.1"],
        """
        Study note on paragraph 2.1. The Guidelines recognise five methods.
        Traditional transaction methods are the comparable uncontrolled price
        method (CUP), the resale price method and the cost plus method.
        Transactional profit methods are the transactional net margin method
        (TNMM) and the transactional profit split method. Other approaches are
        used only if they produce an outcome consistent with the arm's length
        principle.
        """,
        """
        Studiennotiz zu Randnummer 2.1. Die Leitlinien kennen fünf Methoden.
        Standardmethoden sind die Preisvergleichsmethode (CUP), die
        Wiederverkaufspreismethode und die Kostenaufschlagsmethode.
        Gewinnorientierte Methoden sind die geschäftsvorfallbezogene
        Nettomargenmethode (TNMM) und die Gewinnaufteilungsmethode. Andere
        Ansätze kommen nur in Betracht, wenn sie zu einem fremdvergleichskonformen
        Ergebnis führen.
        """,
    ),
    note(
        "oecd-2.2",
        "OECD TPG 2022",
        "oecd",
        "2.2",
        "Most appropriate method",
        ["most appropriate method", "strengths and weaknesses", "reliable information", "geeignetste methode", "2.2"],
        """
        Study note on paragraph 2.2. The selection always aims at the most
        appropriate method for the case. Consider the strengths and weaknesses
        of each recognised method, the nature of the controlled transaction as
        shown by the functional analysis, the availability of reliable
        information on uncontrolled comparables, and the degree of comparability
        including any adjustments. It is not necessary to prove that every
        other method is unusable.
        """,
        """
        Studiennotiz zu Randnummer 2.2. Gesucht wird die für den Fall geeignetste
        Methode. Einzubeziehen sind Stärken und Schwächen der anerkannten
        Methoden, die Art des Geschäftsvorfalls laut Funktionsanalyse, die
        Verfügbarkeit verlässlicher Vergleichsdaten und der Grad der
        Vergleichbarkeit einschließlich etwaiger Anpassungen. Es ist nicht
        nötig nachzuweisen, dass jede andere Methode unbrauchbar ist.
        """,
    ),
    note(
        "oecd-2.3",
        "OECD TPG 2022",
        "oecd",
        "2.3",
        "Preference when equally reliable",
        ["most direct means", "equally reliable", "traditional over profit", "2.3"],
        """
        Study note on paragraph 2.3. Traditional transaction methods are the
        most direct means of testing a price, because a price difference can
        be traced to the commercial relations. Where a traditional method and
        a transactional profit method can be applied in an equally reliable
        manner, the traditional method is preferred. If the gross-margin data
        are not equally reliable, this preference does not force cost plus or
        resale price ahead of TNMM.
        """,
        """
        Studiennotiz zu Randnummer 2.3. Standardmethoden sind das direkteste
        Mittel, einen Preis zu prüfen, weil eine Preisabweichung auf die
        Geschäftsbeziehung zurückgeführt werden kann. Sind eine Standardmethode
        und eine gewinnorientierte Methode gleich zuverlässig anwendbar, hat
        die Standardmethode Vorrang. Sind Bruttomargen nicht gleich zuverlässig,
        erzwingt dieser Vorrang weder Kostenaufschlag noch Wiederverkaufspreis
        vor der TNMM.
        """,
    ),
    note(
        "oecd-2.14",
        "OECD TPG 2022",
        "oecd",
        "2.14",
        "CUP method",
        ["comparable uncontrolled price", "CUP method", "preisvergleichsmethode", "internal comparable", "2.14"],
        """
        Study note on paragraph 2.14. The CUP method compares the price in the
        controlled transaction with the price in a comparable uncontrolled
        transaction. The comparison may be internal (the same taxpayer deals
        with a third party) or external (two independents). CUP is strong when
        the product and the circumstances are very close. It is weak for
        specialised manufacturing where no independent price for the same
        process exists.
        """,
        """
        Studiennotiz zu Randnummer 2.14. Die Preisvergleichsmethode vergleicht
        den Preis des kontrollierten Geschäfts mit dem Preis eines vergleichbaren
        unkontrollierten Geschäfts. Der Vergleich kann intern sein (derselbe
        Steuerpflichtige handelt mit einem Dritten) oder extern. CUP ist stark,
        wenn Produkt und Umstände sehr nah beieinanderliegen. Sie ist schwach
        bei spezialisierter Fertigung, für die es keinen unabhängigen Preis
        desselben Prozesses gibt.
        """,
    ),
    note(
        "oecd-2.27",
        "OECD TPG 2022",
        "oecd",
        "2.27",
        "Resale price method",
        ["resale price method", "resale price margin", "gross margin", "wiederverkaufspreismethode", "2.27"],
        """
        Study note on paragraph 2.27. The resale price method starts from the
        price at which a product bought from an associated enterprise is resold
        to an independent customer. That resale price is reduced by an
        appropriate gross margin, the resale price margin, which covers the
        reseller's selling costs and a profit appropriate to its functions.
        What remains is the arm's length purchase price. The method suits
        distributors who do not add substantial value to the goods.
        """,
        """
        Studiennotiz zu Randnummer 2.27. Die Wiederverkaufspreismethode geht vom
        Preis aus, zu dem ein von einem verbundenen Unternehmen gekauftes
        Produkt an einen unabhängigen Kunden weiterverkauft wird. Von diesem
        Wiederverkaufspreis wird eine angemessene Bruttomarge abgezogen. Sie
        deckt die Vertriebskosten und einen funktionsgerechten Gewinn. Der
        Rest ist der fremdübliche Einkaufspreis. Die Methode passt zu
        Vertriebsgesellschaften, die der Ware keinen erheblichen Wert hinzufügen.
        """,
    ),
    note(
        "oecd-2.45",
        "OECD TPG 2022",
        "oecd",
        "2.45",
        "Cost plus method",
        ["cost plus method", "cost plus mark-up", "gross mark-up", "kostenaufschlagsmethode", "2.45"],
        """
        Study note on paragraph 2.45. The cost plus method starts from the
        costs incurred by the supplier of property or services in the controlled
        transaction. An appropriate gross mark-up is added. The mark-up should
        reflect the functions, assets and risks of that supplier. The method
        is often considered for contract manufacturers and service providers.
        It needs a reliable gross mark-up and a consistent definition of the
        cost base. Differences in how energy, scrap or overhead are classified
        can make gross mark-ups incomparable.
        """,
        """
        Studiennotiz zu Randnummer 2.45. Die Kostenaufschlagsmethode geht von
        den Kosten aus, die der Lieferant von Gütern oder Dienstleistungen im
        kontrollierten Geschäft trägt. Darauf wird ein angemessener
        Bruttoaufschlag gesetzt. Der Aufschlag soll Funktionen, Wirtschaftsgüter
        und Risiken dieses Lieferanten abbilden. Die Methode wird oft für
        Lohnfertiger und Dienstleister geprüft. Sie braucht einen verlässlichen
        Bruttoaufschlag und eine einheitliche Kostenbasis. Unterschiede bei
        Energie, Ausschuss oder Gemeinkosten können Bruttoaufschläge
        unvergleichbar machen.
        """,
    ),
    note(
        "oecd-2.64",
        "OECD TPG 2022",
        "oecd",
        "2.64",
        "Transactional net margin method",
        ["transactional net margin", "TNMM", "net profit indicator", "appropriate base", "nettomargenmethode", "2.64"],
        """
        Study note on paragraph 2.64. The transactional net margin method
        examines the net profit relative to an appropriate base such as costs,
        sales or assets that the tested party earns from the controlled
        transaction. It is applied consistently with the way cost plus or the
        resale price method would be applied. Internal comparables are
        preferred. If none exist, the net margin of an independent enterprise
        in a comparable transaction may be used as an external comparable.
        A functional analysis is required, together with the comparability
        points in paragraphs 2.74 to 2.81.
        """,
        """
        Studiennotiz zu Randnummer 2.64. Die geschäftsvorfallbezogene
        Nettomargenmethode prüft den Nettogewinn im Verhältnis zu einer
        geeigneten Bezugsgröße wie Kosten, Umsatz oder Vermögen, den das
        untersuchte Unternehmen aus dem kontrollierten Geschäft erzielt. Sie
        ist so anzuwenden wie Kostenaufschlag oder Wiederverkaufspreis.
        Interne Vergleichswerte haben Vorrang. Fehlen sie, kann die Nettomarge
        eines unabhängigen Unternehmens als externer Vergleich dienen. Eine
        Funktionsanalyse ist erforderlich, ebenso die Vergleichbarkeitsregeln
        in den Randnummern 2.74 bis 2.81.
        """,
    ),
    note(
        "oecd-tnmm-vs-costplus",
        "OECD TPG 2022",
        "oecd",
        "2.64",
        "When TNMM is used instead of cost plus",
        ["tnmm instead of cost plus", "cost classification", "net cost plus", "energy overhead", "lohnfertiger", "2.64"],
        """
        Study note linking paragraphs 2.2, 2.3, 2.45 and 2.64. Cost plus needs
        comparable gross mark-ups on a similarly defined cost base. Hardening
        and machining plants often classify energy, tooling and overhead
        differently, so gross mark-ups are not equally reliable. TNMM with a
        net cost plus indicator (operating profit over total relevant costs)
        is then the more appropriate method under paragraph 2.2, because the
        net indicator is less sensitive to that classification. Paragraph 2.3
        does not override this when the traditional method is less reliable.
        The tested party should be the routine entity, not the entrepreneur
        who owns the process know-how.
        """,
        """
        Studiennotiz zu den Randnummern 2.2, 2.3, 2.45 und 2.64. Die
        Kostenaufschlagsmethode braucht vergleichbare Bruttoaufschläge auf
        einer gleich abgegrenzten Kostenbasis. Härtereien und Zerspaner
        ordnen Energie, Werkzeuge und Gemeinkosten oft unterschiedlich zu,
        sodass Bruttoaufschläge nicht gleich zuverlässig sind. Die TNMM mit
        Net Cost Plus (operatives Ergebnis im Verhältnis zu den relevanten
        Gesamtkosten) ist dann nach Randnummer 2.2 die geeignetere Methode,
        weil die Nettokennzahl weniger empfindlich auf diese Zuordnung
        reagiert. Randnummer 2.3 verdrängt das nicht, wenn die Standardmethode
        weniger zuverlässig ist. Untersuchtes Unternehmen ist das
        Routineunternehmen, nicht der Prinzipal, der die Prozesskenntnis hält.
        """,
    ),
    note(
        "oecd-2.106",
        "OECD TPG 2022",
        "oecd",
        "2.106",
        "Berry ratio",
        ["berry ratio", "gross profit to operating expenses", "distributor", "2.106"],
        """
        Study note on paragraph 2.106. Berry ratios are ratios of gross profit
        to operating expenses. Interest and extraneous income are generally
        left out of the gross profit. The ratio is sometimes used as a net
        profit indicator for distributors or intermediaries whose value lies
        in the operating expenses they incur, not in the goods they happen to
        take title to. It is a cross-check, not a reason to skip the
        functional analysis.
        """,
        """
        Studiennotiz zu Randnummer 2.106. Berry Ratios setzen den Bruttogewinn
        ins Verhältnis zu den Betriebskosten. Zinsen und betriebsfremder Ertrag
        bleiben beim Bruttogewinn in der Regel außen vor. Die Kennzahl dient
        mitunter als Nettogewinnindikator für Vertriebsgesellschaften, deren
        Wert in den Betriebskosten liegt und nicht in der Ware, an der sie
        zufällig Eigentum halten. Sie ist eine Gegenprobe, kein Ersatz für
        die Funktionsanalyse.
        """,
    ),
    note(
        "oecd-2.114",
        "OECD TPG 2022",
        "oecd",
        "2.114",
        "Profit split method",
        ["profit split method", "gewinnaufteilung", "combined profits", "2.114"],
        """
        Study note on paragraph 2.114. The transactional profit split method
        seeks an arm's length outcome by looking at how independent parties
        would have split the combined profits, or losses, of the controlled
        transaction. It is a two-sided method. It becomes relevant when both
        parties make unique and valuable contributions or the activities are
        highly integrated, not when one party is a routine manufacturer or a
        limited-risk distributor.
        """,
        """
        Studiennotiz zu Randnummer 2.114. Die Gewinnaufteilungsmethode sucht
        ein fremdübliches Ergebnis, indem sie fragt, wie unabhängige Parteien
        den zusammengefassten Gewinn oder Verlust des Geschäftsvorfalls geteilt
        hätten. Sie ist zweiseitig. Sie wird relevant, wenn beide Seiten
        einzigartige und wertvolle Beiträge leisten oder die Tätigkeiten stark
        integriert sind, nicht wenn eine Seite Lohnfertiger oder
        Routinevertrieb ist.
        """,
    ),
    note(
        "oecd-2.119",
        "OECD TPG 2022",
        "oecd",
        "2.119",
        "Strength of the profit split",
        ["unique and valuable contributions", "highly integrated", "both parties", "2.119"],
        """
        Study note on paragraph 2.119. The main strength of the transactional
        profit split is that it can deal with cases in which both parties make
        unique and valuable contributions, or in which the operations are so
        integrated that a one-sided method cannot isolate a reliable margin.
        If only one party contributes the intangibles and the other performs
        routine production to that party's specifications, a one-sided method
        on the routine party is usually the better fit.
        """,
        """
        Studiennotiz zu Randnummer 2.119. Die Stärke der Gewinnaufteilung liegt
        darin, Fälle abzubilden, in denen beide Seiten einzigartige und
        wertvolle Beiträge leisten oder die Abläufe so integriert sind, dass
        eine einseitige Methode keine verlässliche Marge isolieren kann.
        Wenn nur eine Seite die immateriellen Werte beisteuert und die andere
        nach deren Vorgaben routinehaft fertigt, passt in der Regel eine
        einseitige Methode auf das Routineunternehmen.
        """,
    ),
    note(
        "oecd-3.55",
        "OECD TPG 2022",
        "oecd",
        "3.55",
        "Arm's length range",
        ["arm's length range", "single figure", "bandbreite", "3.55"],
        """
        Study note on paragraph 3.55. Sometimes the arm's length principle
        produces a single figure. Often, because comparables are imperfect,
        it produces a range of figures that are all relatively equally
        reliable. That range is the arm's length range. A tested result is
        judged against the range, not against the average of an unfiltered
        list of companies.
        """,
        """
        Studiennotiz zu Randnummer 3.55. Manchmal führt der Fremdvergleich zu
        einem einzelnen Wert. Häufig entsteht wegen unvollkommener Vergleichswerte
        eine Bandbreite von Werten, die alle relativ gleich zuverlässig sind.
        Das ist die Fremdvergleichsbandbreite. Das Ergebnis des untersuchten
        Unternehmens wird an der Bandbreite gemessen, nicht am Durchschnitt
        einer ungefilterten Unternehmensliste.
        """,
    ),
    note(
        "oecd-3.60",
        "OECD TPG 2022",
        "oecd",
        "3.60",
        "Result inside the range",
        ["no adjustment", "inside the range", "within the arm's length range", "3.60"],
        """
        Study note on paragraph 3.60. If the relevant condition of the
        controlled transaction, such as the price or the margin, is within
        the arm's length range, no adjustment should be made. Being inside
        the range is enough. The taxpayer does not have to sit on the median
        merely because a statistical centre exists.
        """,
        """
        Studiennotiz zu Randnummer 3.60. Liegt die maßgebliche Bedingung des
        kontrollierten Geschäfts, etwa Preis oder Marge, innerhalb der
        Fremdvergleichsbandbreite, ist keine Berichtigung vorzunehmen. Innerhalb
        der Bandbreite zu liegen genügt. Das Unternehmen muss nicht auf dem
        Median sitzen, nur weil es einen statistischen Mittelpunkt gibt.
        """,
    ),
    note(
        "oecd-3.62",
        "OECD TPG 2022",
        "oecd",
        "3.62",
        "Point in the range",
        ["central tendency", "any point in the range", "comparability defects", "median mean", "3.62"],
        """
        Study note on paragraph 3.62. Where the range consists of results of
        relatively equal and high reliability, any point in the range can
        satisfy the arm's length principle. Where comparability defects
        remain, a measure of central tendency such as the median, the mean or
        a weighted average may be used to pick the point. This OECD approach
        is not identical to the German statutory rule in section 1(3a) AStG,
        which points to the median once the taxpayer's figure is outside the
        narrowed range.
        """,
        """
        Studiennotiz zu Randnummer 3.62. Besteht die Bandbreite aus relativ
        gleich zuverlässigen Werten, kann jeder Punkt in der Bandbreite dem
        Fremdvergleich genügen. Bleiben Vergleichbarkeitsmängel, kann ein
        Lagemaß wie Median, Mittelwert oder gewichteter Durchschnitt den
        Korrekturpunkt bestimmen. Dieser OECD-Ansatz ist nicht identisch mit
        § 1 Absatz 3a AStG. Dort ist der Median maßgeblich, wenn der angesetzte
        Wert außerhalb der eingeengten Bandbreite liegt.
        """,
    ),
    note(
        "oecd-6.32",
        "OECD TPG 2022",
        "oecd",
        "6.32",
        "Who keeps intangible returns",
        ["intangibles", "exploiting intangibles", "DEMPE", "process know-how", "6.32"],
        """
        Study note on paragraph 6.32. In cases involving intangibles, the
        question is which entity is entitled to the returns from exploiting
        those intangibles, and which entity should bear the related costs and
        risks. Legal ownership is only the starting point. Development,
        enhancement, maintenance, protection and exploitation (DEMPE) show who
        actually controls the asset. Process recipes, hardening parameters and
        customer-approval know-how are intangibles even when they are not
        registered as patents.
        """,
        """
        Studiennotiz zu Randnummer 6.32. Bei immateriellen Werten ist zu
        bestimmen, welche Gesellschaft die Erträge aus ihrer Nutzung beanspruchen
        kann und welche die zugehörigen Kosten und Risiken trägt. Rechtliches
        Eigentum ist nur der Ausgangspunkt. Entwicklung, Verbesserung, Erhaltung,
        Schutz und Nutzung (DEMPE) zeigen, wer den Wert tatsächlich steuert.
        Prozessrezepturen, Härteparameter und Freigabe-Know-how sind immaterielle
        Werte, auch wenn sie nicht als Patent eingetragen sind.
        """,
    ),
    note(
        "astg-1-1",
        "§ 1 AStG",
        "astg",
        "§1 Abs. 1",
        "German arm's length correction",
        ["§ 1 AStG", "einkünftekorrektur", "auslandsbeziehung", "fremdvergleichsgrundsatz", "absatz 1"],
        """
        Study note on section 1(1) of the Außensteuergesetz. Where a
        taxpayer's income from a cross-border business relationship with a
        related party is reduced because the conditions differ from those
        independent parties would have agreed, the income is corrected. The
        German statute applies the arm's length principle as a correction
        rule. The official text is published at gesetze-im-internet.de.
        """,
        """
        Studiennotiz zu § 1 Absatz 1 AStG. Werden die Einkünfte eines
        Steuerpflichtigen aus einer grenzüberschreitenden Geschäftsbeziehung
        zu einer nahestehenden Person dadurch gemindert, dass die Bedingungen
        von denen unabhängiger Dritter abweichen, sind die Einkünfte zu
        berichtigen. Das deutsche Gesetz formuliert den Fremdvergleich als
        Korrekturnorm. Der amtliche Wortlaut steht auf gesetze-im-internet.de.
        """,
    ),
    note(
        "astg-1-3a",
        "§ 1 AStG",
        "astg",
        "§1 Abs. 3a",
        "Interquartile range and median",
        ["interquartile", "median", "eingeengte bandbreite", "viertel der kleinsten", "absatz 3a", "§1 abs. 3a"],
        """
        Study note on section 1(3a) AStG. Applying the arm's length principle
        regularly produces a range. If differences in comparability remain,
        the range is narrowed. Where the values themselves do not show a
        better way to narrow it, the quarter of the smallest values and the
        quarter of the largest values are left out. This is the statutory
        interquartile approach. If the value used by the taxpayer lies outside
        the full range or outside that narrowed range, the median is decisive,
        unless the taxpayer credibly shows that another point inside the range
        better satisfies the arm's length principle.
        """,
        """
        Studiennotiz zu § 1 Absatz 3a AStG. Der Fremdvergleich führt regelmäßig
        zu einer Bandbreite. Bleiben Unterschiede in der Vergleichbarkeit, ist
        die Bandbreite einzuengen. Bieten die Werte selbst keinen Anhalt für
        eine bestimmte Einengung, bleiben das Viertel der kleinsten und das
        Viertel der größten Werte unberücksichtigt. Das ist die gesetzliche
        Interquartilsbetrachtung. Liegt der vom Steuerpflichtigen verwendete
        Wert außerhalb der Bandbreite oder der eingeengten Bandbreite, ist der
        Median maßgeblich, sofern er nicht glaubhaft macht, dass ein anderer
        Wert innerhalb der Bandbreite dem Fremdvergleich besser entspricht.
        """,
    ),
    note(
        "astg-1-3b",
        "§ 1 AStG",
        "astg",
        "§1 Abs. 3b",
        "Transfer of a function",
        ["funktionsverlagerung", "transferpaket", "kostenaufschlagsmethode", "ausschließlich", "absatz 3b"],
        """
        Study note on section 1(3b) AStG. If a function is transferred together
        with the related chances, risks and assets, and no comparables exist
        for the transfer package as a whole, the bargaining range is
        determined on that package. The taxpayer can set the package valuation
        aside by showing that no significant intangibles or other advantages
        were transferred. The statute treats that showing as made where the
        receiving company exercises the function exclusively for the
        transferring company and the remuneration is to be determined under
        the cost plus method. A routine plant that sells only to its principal
        may fall under this sentence, but only if the remuneration itself is
        an arm's length cost-plus return. A margin below the range does not
        meet that condition.
        """,
        """
        Studiennotiz zu § 1 Absatz 3b AStG. Wird eine Funktion einschließlich
        der Chancen, Risiken und Wirtschaftsgüter verlagert und fehlen
        Vergleichsdaten für das Transferpaket als Ganzes, ist der Einigungsbereich
        auf Grundlage des Transferpakets zu bestimmen. Davon kann abgesehen
        werden, wenn keine wesentlichen immateriellen Werte oder sonstigen
        Vorteile mitübertragen wurden. Das Gesetz sieht diesen Nachweis als
        geführt an, wenn das übernehmende Unternehmen die Funktion ausschließlich
        gegenüber dem verlagernden Unternehmen ausübt und das Entgelt nach der
        Kostenaufschlagsmethode zu bestimmen ist. Ein Routinewerk, das nur an
        den Prinzipal liefert, kann unter diesen Satz fallen, aber nur wenn
        die Vergütung selbst ein fremdüblicher Kostenaufschlag ist. Eine Marge
        unter der Bandbreite erfüllt das nicht.
        """,
    ),
    note(
        "astg-1-3c",
        "§ 1 AStG",
        "astg",
        "§1 Abs. 3c",
        "Remuneration of intangibles",
        ["immaterieller wert", "überlassung zur nutzung", "absatz 3c", "lizenz"],
        """
        Study note on section 1(3c) AStG. The transfer of an intangible, or
        the permission to use it, is to be remunerated where the relationship
        is a business relationship under section 1(4) and there is a financial
        effect. An intangible for this purpose is an asset that is not a
        tangible, a participation or a financial asset, that can be the object
        of a transaction even if it is not separately transferable, and that
        can give a person a factual or legal position. A royalty on top of a
        routine manufacturing return has to be tested on its own. It should
        not be used to push the manufacturer's operating result below the
        arm's length range.
        """,
        """
        Studiennotiz zu § 1 Absatz 3c AStG. Die Übertragung eines immateriellen
        Werts oder die Überlassung zur Nutzung ist zu vergüten, wenn eine
        Geschäftsbeziehung im Sinne von § 1 Absatz 4 vorliegt und eine
        finanzielle Auswirkung eintritt. Ein immaterieller Wert ist danach ein
        Vermögenswert, der kein Sachgut, keine Beteiligung und keine Finanzanlage
        ist, der Gegenstand eines Geschäftsvorfalls sein kann, ohne einzeln
        übertragbar sein zu müssen, und der eine tatsächliche oder rechtliche
        Position vermitteln kann. Eine Lizenz zusätzlich zu einer Routinefertigung
        ist eigenständig zu prüfen. Sie darf das operative Ergebnis des
        Fertigers nicht unter die Fremdvergleichsbandbreite drücken.
        """,
    ),
    note(
        "ao-90-matrix",
        "§ 90 AO / BMF-Merkblatt 2. April 2025",
        "ao",
        "§90 Abs. 3",
        "Transaction matrix",
        ["transaktionsmatrix", "§ 90", "vertragliche grundlage", "steuerhoheitsgebiet", "leistungserbringer"],
        """
        Study note on the transaction matrix under section 90(3) sentence 2
        number 1 of the Abgabenordnung, as explained in the BMF leaflet of
        2 April 2025. The matrix states, for the controlled transactions, the
        subject and type, the parties marking provider and recipient, the
        volume and the consideration in euro, the contractual basis by name,
        the transfer pricing method used, the tax jurisdictions, and whether
        the transaction is outside ordinary taxation. Contracts are named,
        not attached. A booking without a named contract is a documentation
        gap even if the cash movement is real.
        """,
        """
        Studiennotiz zur Transaktionsmatrix nach § 90 Absatz 3 Satz 2 Nummer 1
        AO, erläutert im BMF-Merkblatt vom 2. April 2025. Anzugeben sind
        Gegenstand und Art der Geschäftsvorfälle, die Beteiligten mit Kennzeichnung
        von Leistungserbringer und Leistungsempfänger, Volumen und Entgelt in
        Euro, die vertragliche Grundlage namentlich, die angewandte
        Verrechnungspreismethode, die betroffenen Steuerhoheitsgebiete und ob
        der Vorgang nicht der Regelbesteuerung unterliegt. Verträge werden
        benannt, nicht beigelegt. Eine Buchung ohne benannten Vertrag ist eine
        Dokumentationslücke, auch wenn die Zahlung real ist.
        """,
    ),
    note(
        "vwg-2023",
        "BMF-Schreiben 6. Juni 2023",
        "vwg",
        "VWG VP 2023",
        "Administrative principles 2023",
        ["verwaltungsgrundsätze", "6. juni 2023", "IV B 5", "vwg vp 2023", "bmf"],
        """
        Study note on the Verwaltungsgrundsätze Verrechnungspreise of 6 June
        2023 (IV B 5 - S 1341/19/10017 :003). The letter explains how the tax
        administration applies the arm's length principle after the reform of
        section 1 AStG, in light of the 2022 OECD Guidelines. It covers the
        range and the interquartile narrowing, function transfers, financing
        relationships and documentation. It is administrative guidance, not
        a statute. Where the letter and section 1 AStG speak to the same
        point, the statute remains the rule this project implements in code.
        """,
        """
        Studiennotiz zu den Verwaltungsgrundsätzen Verrechnungspreise vom
        6. Juni 2023 (IV B 5 - S 1341/19/10017 :003). Das Schreiben legt dar,
        wie die Finanzverwaltung den Fremdvergleich nach der Reform des § 1
        AStG und im Licht der OECD-Leitlinien 2022 anwendet. Es behandelt
        Bandbreite und Interquartilseinengung, Funktionsverlagerungen,
        Finanzierungsbeziehungen und Aufzeichnungen. Es ist Verwaltungshilfe,
        kein Gesetz. Wo Schreiben und § 1 AStG denselben Punkt regeln, setzt
        dieses Projekt die gesetzliche Regel im Code um.
        """,
    ),
    note(
        "case-hardening",
        "Fallstudie Härtetechnik AG",
        "case",
        "Fall HT",
        "Why a hardening plant is a transfer pricing case",
        ["induction hardening", "härten", "ppap", "8d", "energy pass-through", "lohnfertiger"],
        """
        Project note, not a legal source. Induction hardening is
        energy-intensive. The economically relevant question in a contract
        manufacturing setup is who carries the energy-price risk and who owns
        the process parameters, the PPAP approval and the 8D quality
        responsibility. If the German principal owns the recipe and the
        customer contract, and the Polish plant only executes it, the plant
        is a routine manufacturer. A fixed transfer price that does not pass
        through an energy shock leaves the routine plant outside the net cost
        plus range. That is a pricing failure, not a change in who owns the
        know-how.
        """,
        """
        Projektnotiz, keine Rechtsquelle. Induktionshärten ist energieintensiv.
        Bei einem Lohnfertiger ist wirtschaftlich entscheidend, wer das
        Energiepreisrisiko trägt und wem Prozessparameter, PPAP-Freigabe und
        8D-Qualitätsverantwortung gehören. Hält der deutsche Prinzipal Rezeptur
        und Kundenvertrag und führt das polnische Werk sie nur aus, ist das
        Werk ein Routinefertiger. Ein fester Verrechnungspreis, der einen
        Energieschock nicht weitergibt, schiebt das Routinewerk aus der
        Net-Cost-Plus-Bandbreite. Das ist ein Preisfehler, keine Änderung
        daran, wem das Know-how gehört.
        """,
    ),
]
