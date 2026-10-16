"""TP Copilot desk. English and German, switched from the top of the page."""

from __future__ import annotations

import html
from pathlib import Path

import pandas as pd
import streamlit as st

from tp_copilot.agents.critic_agent import critique_retrieval
from tp_copilot.agents.kg_agent import run_kg
from tp_copilot.agents.margin_agent import format_pct
from tp_copilot.agents.orchestrator import run_case
from tp_copilot.agents.rag_agent import answer_question
from tp_copilot.agents.screening_agent import evaluate, screen_text
from tp_copilot.eval.run_eval import run_eval
from tp_copilot.ingest.chunker import chunks_from_bytes
from tp_copilot.knowledge.graph import relation_label

st.set_page_config(
    page_title="Transfer Pricing Copilot",
    page_icon="§",
    layout="wide",
    initial_sidebar_state="expanded",
)

TEXT = {
    "de": {
        "kicker": "Portfolio · kein Mandat · keine Steuerberatung",
        "banner": "Eine Prüfung von der Funktion bis zur Akte. Vergleichsunternehmen werden gescreent, bevor die Bandbreite getestet wird. Eine Randnummer erscheint nur, wenn sie gefunden wurde.",
        "side_title": "Fall",
        "year": "Prüfungsjahr",
        "reused_h": "Was eine Prüfung benutzt",
        "reused": "Funktion, Methode, gescreente Vergleichsunternehmen, eingeengte Bandbreite, Transaktionsmatrix. Der Kritiker hält eine Randnummer von der Seite, die nicht gefunden wurde.",
        "new_h": "Was neu ist",
        "new": "OECD-Randnummern, § 1 AStG, Transaktionsmatrix, synthetische Buchungen.",
        "missing_h": "Was bewusst fehlt",
        "missing": "Der OECD-Volltext. Er ist urheberrechtlich geschützt und liegt nicht im Repo. Eine eigene Datei können Sie im Reiter Regelwerke hochladen. Sie bleibt in dieser Sitzung.",
        "caption": "Härtetechnik AG ist erfunden. Die Vergleichsunternehmen auch.",
        "bookings": "Buchungen",
        "pl_metric": "HTPL Net Cost Plus",
        "us_metric": "HTUS Betriebsmarge",
        "high": "Befunde mit Gewicht",
        "tabs": ["Fallakte", "Regelwerke", "Screening", "Margentest", "Transaktionsmatrix", "Evaluation"],
        "chain": "Wertschöpfung",
        "pl_card": "Lohnfertiger. Härtet nach Rezeptur. Trägt das Energiepreisrisiko nur, wenn der Preis es nicht weitergibt.",
        "de_card": "Prinzipal. Prozess-Know-how, PPAP, 8D, OEM-Verträge. Restgewinn nach Routinevergütung.",
        "us_card": "Routinevertrieb. Kein Fertigungs-Know-how. Betriebsmarge, nicht der Markengewinn.",
        "arrows": "Lizenz HTPL → HTDE · Managementumlage HTUS → HTDE · Darlehen HTDE → HTPL",
        "findings": "Befunde",
        "critic": "Kritiker",
        "far": "Funktions- und Risikoanalyse",
        "functions": "Funktionen",
        "assets": "Wirtschaftsgüter",
        "risks": "Risiken",
        "ask_title": "Frage an die Regelwerke",
        "examples_label": "Beispielfragen",
        "examples": [
            "Warum TNMM statt Kostenaufschlag bei einem Lohnfertiger, wenn Energie und Gemeinkosten unterschiedlich zugeordnet werden?",
            "Wie funktioniert das Viertel der kleinsten Werte und der Median nach §1 Abs. 3a AStG?",
            "Wann entfällt das Transferpaket bei einer Funktionsverlagerung?",
            "Was steht in Randnummer 1.6 zum Fremdvergleichsgrundsatz?",
        ],
        "question": "Frage",
        "answer": "Antworten",
        "empty_q": "Bitte eine Frage eingeben.",
        "graph": "Wissensgraph",
        "upload": "Dokument hinzufügen",
        "upload_help": "PDF, TXT, MD oder XML mit echtem Text. Die Datei bleibt in diesem Browser und wird nicht gespeichert. Ein Foto oder ein Scan ohne Textebene kann nicht zitiert werden, weil das System die Wörter braucht.",
        "upload_empty": "In {name} steht kein lesbarer Text. Ein Foto oder ein bildbasierter Scan hat keine Absätze, die man zitieren kann.",
        "upload_big": "{name} ist größer als 8 MB. Bitte einen kürzeren Auszug verwenden.",
        "upload_ok": "{name}: {n} Abschnitte im Index dieser Sitzung.",
        "upload_clear": "Hochgeladene Dateien entfernen",
        "screen_title": "Vergleichbar mit dem polnischen Lohnfertiger?",
        "screen_lead": "Fünf-Falten-F1 auf den Portfolio-Labels: **{f1}**. Die Tabelle zeigt Out-of-fold-Vorhersagen, nicht die Trainingsmenge als Beweis.",
        "description": "Unternehmensbeschreibung",
        "classify": "Einordnen",
        "empty_desc": "Bitte eine Beschreibung eingeben.",
        "yes": "vergleichbar",
        "no": "nicht vergleichbar",
        "prob": "Wahrscheinlichkeit",
        "for": "Wörter in Richtung vergleichbar",
        "against": "Wörter in Richtung nicht vergleichbar",
        "company": "Unternehmen",
        "label": "Label",
        "fold": "Out-of-fold",
        "sales": "Umsatz mit HTDE",
        "mfg": "Fertigungskosten",
        "op": "Operatives Ergebnis vor Lizenz",
        "indicator": "Kennzahl",
        "position": "Lage",
        "range": "Bandbreite",
        "median": "Median",
        "gap": "Median-Lücke",
        "oem_sales": "OEM-Umsatz",
        "op_us": "Operatives Ergebnis",
        "history": "Verlauf HTPL",
        "chart": "Balken in Prozent. 5,00 liegt in der Bandbreite. 2,00 im Jahr 2025 nicht.",
        "year_col": "Jahr",
        "energy_col": "Energie EUR",
        "matrix_help": "Spalten nach dem BMF-Merkblatt vom 2. April 2025 zu § 90 Abs. 3 AO. Beim Darlehen unterscheiden sich Volumen und Entgelt. Die Managementumlage hat keinen Vertragsnamen.",
        "eval_title": "Zitiergenauigkeit",
        "q_col": "Frage",
        "hit_col": "Treffer",
        "exp_col": "Erwartet",
        "top_col": "Top 3",
        "yes_short": "ja",
        "no_short": "nein",
        "eval_note": "Getroffen heißt: eine akzeptierte Randnummer steht unter den drei besten Treffern. Die Fragen liegen im Repository.",
        "inside": "in der Bandbreite",
        "below": "unter der Bandbreite",
        "above": "über der Bandbreite",
        "method": "Methode",
        "steps": [
            ("01", "Charakterisieren", "Wer die Rezeptur besitzt und wer dem Kunden gegenübersteht."),
            ("02", "Methode wählen", "TNMM, wenn Bruttoaufschläge zwischen Härtereien nicht vergleichbar sind."),
            ("03", "Peers screenen", "Dieselbe Funktion bleibt im Set. Eine Marke oder ein Prinzipal fällt heraus."),
            ("04", "Bandbreite testen", "Interquartil und Median nach § 1 Abs. 3a AStG."),
            ("05", "Dokumentieren", "Matrix: Vertrag, Volumen und Entgelt, auch wenn sie auseinanderfallen."),
            ("06", "Zitat prüfen", "Der Kritiker lässt nur eine Randnummer stehen, die abgerufen wurde."),
        ],
    },
    "en": {
        "kicker": "Portfolio · no engagement · not tax advice",
        "banner": "One review, from the function to the file. Peers are screened before the range is tested. A paragraph appears only if it was retrieved.",
        "side_title": "Case",
        "year": "Year under review",
        "reused_h": "What a review uses",
        "reused": "Function, method, screened peers, the narrowed range, and the transaction matrix. The critic keeps a paragraph that was not retrieved off the page.",
        "new_h": "What is new",
        "new": "OECD paragraph numbers, § 1 AStG, the transaction matrix, synthetic bookings.",
        "missing_h": "What is left out on purpose",
        "missing": "The full OECD text. It is copyrighted and is not in the repo. You can upload your own file on the Guidelines tab. It stays in this session.",
        "caption": "Härtetechnik AG is fictional. So are the peer companies.",
        "bookings": "Bookings",
        "pl_metric": "HTPL net cost plus",
        "us_metric": "HTUS operating margin",
        "high": "Material findings",
        "tabs": ["Case file", "Guidelines", "Screening", "Margin test", "Transaction matrix", "Evaluation"],
        "chain": "Value chain",
        "pl_card": "Contract manufacturer. Hardens to the recipe. Carries energy-price risk only when the price does not pass it on.",
        "de_card": "Principal. Process know-how, PPAP, 8D, OEM contracts. Residual profit after routine returns.",
        "us_card": "Limited-risk distributor. No manufacturing know-how. An operating margin, not the brand profit.",
        "arrows": "Royalty HTPL → HTDE · Management charge HTUS → HTDE · Loan HTDE → HTPL",
        "findings": "Findings",
        "critic": "Critic",
        "far": "Functional analysis",
        "functions": "Functions",
        "assets": "Assets",
        "risks": "Risks",
        "ask_title": "Ask the guidelines",
        "examples_label": "Example questions",
        "examples": [
            "When should I use TNMM rather than the cost plus method for a contract manufacturer?",
            "What happens under German law if my margin is outside the interquartile range?",
            "Does the Polish plant have to value a transfer package if it only produces for the parent?",
            "What is the arm's length principle in Article 9?",
        ],
        "question": "Question",
        "answer": "Answer",
        "empty_q": "Enter a question first.",
        "graph": "Knowledge graph",
        "upload": "Add a document",
        "upload_help": "PDF, TXT, MD or XML that contains real text. The file stays in this browser and is not saved. A photo or a scan without a text layer cannot be cited, because the desk needs the words.",
        "upload_empty": "{name} has no readable text. A photo or an image-only scan has no paragraphs to cite.",
        "upload_big": "{name} is larger than 8 MB. Use a shorter extract.",
        "upload_ok": "{name}: {n} sections in this session's index.",
        "upload_clear": "Remove uploaded files",
        "screen_title": "Comparable to the Polish contract manufacturer?",
        "screen_lead": "Five-fold F1 on the portfolio labels: **{f1}**. The table shows out-of-fold predictions, not the training set treated as proof.",
        "description": "Company description",
        "classify": "Classify",
        "empty_desc": "Enter a description first.",
        "yes": "comparable",
        "no": "not comparable",
        "prob": "Probability",
        "for": "Words pulling toward a match",
        "against": "Words pulling away",
        "company": "Company",
        "label": "Label",
        "fold": "Out-of-fold",
        "sales": "Sales to HTDE",
        "mfg": "Manufacturing costs",
        "op": "Operating profit before royalty",
        "indicator": "Indicator",
        "position": "Position",
        "range": "Range",
        "median": "Median",
        "gap": "Gap to the median",
        "oem_sales": "OEM sales",
        "op_us": "Operating profit",
        "history": "HTPL over time",
        "chart": "Bars are percent. 5.00 is inside the range. 2.00 in 2025 is not.",
        "year_col": "Year",
        "energy_col": "Energy EUR",
        "matrix_help": "Columns follow the BMF leaflet of 2 April 2025 on § 90 Abs. 3 AO. For the loan, volume and consideration differ. The management charge has no contract name.",
        "eval_title": "Citation accuracy",
        "q_col": "Question",
        "hit_col": "Hit",
        "exp_col": "Expected",
        "top_col": "Top 3",
        "yes_short": "yes",
        "no_short": "no",
        "eval_note": "A hit means an accepted paragraph is among the top 3. The questions are in the repository.",
        "inside": "inside the range",
        "below": "below the range",
        "above": "above the range",
        "method": "Method",
        "steps": [
            ("01", "Characterize", "Who owns the recipe, and who faces the customer."),
            ("02", "Choose the method", "TNMM when gross mark-ups across hardening plants are not comparable."),
            ("03", "Screen peers", "The same function stays in the set. A brand or a principal drops out."),
            ("04", "Test the range", "Interquartile narrowing and the median under § 1 (3a) AStG."),
            ("05", "Document", "The matrix records the contract, the volume, and the consideration, including when they differ."),
            ("06", "Check the citation", "The critic leaves a paragraph on the page only if it was retrieved."),
        ],
    },
}

SEVERITY = {"high": "warn", "medium": "mid", "ok": "ok"}
MAX_UPLOAD = 8_000_000


def tr(lang: str, key: str) -> str:
    return TEXT[lang][key]


def money(value: int, lang: str) -> str:
    grouped = f"{abs(int(value)):,.0f}"
    if lang == "de":
        return grouped.replace(",", ".") + " €"
    return "€" + grouped


def pct(value: float, lang: str) -> str:
    text = format_pct(value)
    if lang == "de":
        text = text.replace(".", ",")
    return text


def card(title: str, body: str, kind: str = "") -> str:
    klass = f"card {kind}".strip()
    return (
        f"<div class='{klass}'><strong>{html.escape(title)}</strong>"
        f"{html.escape(body)}</div>"
    )


@st.cache_data(show_spinner=False)
def cached_case(year: int) -> dict:
    case = run_case(year)
    case["matrix"] = case["matrix"].to_dict(orient="records")
    return case


@st.cache_data(show_spinner=False)
def cached_eval() -> dict:
    return run_eval()


@st.cache_data(show_spinner=False)
def cached_screen() -> dict:
    return evaluate()


def _suffix(name: str) -> str:
    return Path(name).suffix.lower()


def index_uploads(files) -> list[dict]:
    """Parse the current picker contents. Earlier files drop out when removed."""
    cache = st.session_state.setdefault("upload_cache", {})
    chunks: list[dict] = []
    notes: list[tuple[str, str]] = []
    for file in files or []:
        if _suffix(file.name) not in {".pdf", ".txt", ".md", ".xml"}:
            notes.append(("empty", file.name))
            continue
        if file.size > MAX_UPLOAD:
            notes.append(("big", file.name))
            continue
        signature = (file.name, file.size)
        if signature not in cache:
            cache[signature] = chunks_from_bytes(file.name, file.getvalue())
        parsed = cache[signature]
        if not parsed:
            notes.append(("empty", file.name))
            continue
        chunks.extend(parsed)
        notes.append(("ok", f"{file.name}|{len(parsed)}"))
    st.session_state["upload_chunks"] = chunks
    return notes


st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 1.15rem; max-width: 1180px;}
    h1, h2, h3 {letter-spacing: -0.02em;}
    .banner {
        background: #1f1a17; color: #f4f1ea;
        padding: 1.3rem 1.4rem 1.1rem; border-radius: 14px; margin: 0.2rem 0 0.8rem;
    }
    .banner p {color: #e7d7c4; margin: 0.35rem 0 0;}
    .kicker {color: #e7b08a; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase;}
    .card {
        background: white; border: 1px solid #e4d9c8; border-radius: 12px;
        padding: 0.9rem 1rem; min-height: 148px;
    }
    .card strong {display: block; margin-bottom: 0.25rem;}
    .warn {border-left: 4px solid #9a3412;}
    .ok {border-left: 4px solid #3f6212;}
    .mid {border-left: 4px solid #a16207;}
    .arrow {text-align: center; font-size: 1.4rem; padding-top: 2.2rem; color: #9a3412;}
    .steps {display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.55rem; margin: 0 0 0.95rem;}
    .step {background: white; border: 1px solid #e4d9c8; border-radius: 12px; padding: 0.7rem 0.75rem;}
    .step b {display: block; color: #9a3412; font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.2rem;}
    @media (max-width: 700px) { .steps {grid-template-columns: 1fr;} }
    div[data-testid="stSegmentedControl"] {margin-top: 0.15rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

switch_left, switch_right = st.columns([4.4, 1.7])
with switch_left:
    st.markdown(
        "<div class='kicker' style='padding-top:0.55rem'>Sprache · Language</div>",
        unsafe_allow_html=True,
    )
with switch_right:
    lang = st.segmented_control(
        "Sprache · Language",
        options=["de", "en"],
        default="de",
        format_func=lambda code: "Deutsch" if code == "de" else "English",
        label_visibility="collapsed",
        key="lang",
    )
if lang not in ("de", "en"):
    lang = "de"
S = TEXT[lang]

st.markdown(
    f"""
    <div class="banner">
      <div class="kicker">{html.escape(S['kicker'])}</div>
      <h1 style="margin:0.2rem 0 0; color:#f4f1ea;">Transfer Pricing Copilot</h1>
      <p>{html.escape(S['banner'])}</p>
    </div>
    """,
    unsafe_allow_html=True,
)
steps_html = "".join(
    f"<div class='step'><b>{html.escape(number)} {html.escape(title)}</b>{html.escape(body)}</div>"
    for number, title, body in S["steps"]
)
st.markdown(f"<div class='steps'>{steps_html}</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header(S["side_title"])
    year = st.selectbox(S["year"], [2025, 2024, 2023], index=0, key="review_year")
    st.markdown(f"**{S['reused_h']}**\n\n{S['reused']}")
    st.markdown(f"**{S['new_h']}**\n\n{S['new']}")
    st.markdown(f"**{S['missing_h']}**\n\n{S['missing']}")
    st.caption(S["caption"])

case = cached_case(year)
assessment = case["assessment"]
high = sum(1 for item in case["findings"] if item["severity"] == "high")
lage = {"inside": S["inside"], "below": S["below"], "above": S["above"]}

metric_cols = st.columns(4)
metric_cols[0].metric(S["bookings"], f"{case['ledger_rows']}")
metric_cols[1].metric(S["pl_metric"], pct(assessment["htpl"]["net_cost_plus"], lang))
metric_cols[2].metric(S["us_metric"], pct(assessment["htus"]["operating_margin"], lang))
metric_cols[3].metric(S["high"], high)

tabs = st.tabs(S["tabs"])
tab_case, tab_rag, tab_screen, tab_margin, tab_matrix, tab_eval = tabs

with tab_case:
    st.subheader(S["chain"])
    left, arrow_1, mid, arrow_2, right = st.columns([3, 0.4, 3, 0.4, 3])
    with left:
        st.markdown(card("HTPL · Polen" if lang == "de" else "HTPL · Poland", S["pl_card"]), unsafe_allow_html=True)
    with arrow_1:
        st.markdown("<div class='arrow'>→</div>", unsafe_allow_html=True)
    with mid:
        st.markdown(card("HTDE · Stuttgart", S["de_card"]), unsafe_allow_html=True)
    with arrow_2:
        st.markdown("<div class='arrow'>→</div>", unsafe_allow_html=True)
    with right:
        st.markdown(card("HTUS · Detroit", S["us_card"]), unsafe_allow_html=True)
    st.caption(S["arrows"])
    if lang == "en":
        st.caption(case["far"]["case_en"])
    else:
        st.caption(case["far"]["case"])

    st.subheader(f"{S['findings']} {year}")
    for finding in case["findings"]:
        title = finding["title_en"] if lang == "en" else finding["title"]
        detail = finding["detail_en"] if lang == "en" else finding["detail"]
        citation = finding.get("citation_en", finding["citation"]) if lang == "en" else finding["citation"]
        st.markdown(card(title, detail + "  " + citation, SEVERITY.get(finding["severity"], "mid")), unsafe_allow_html=True)
        st.write("")

    st.subheader(S["critic"])
    critic_notes = case["critic"]["notes_en"] if lang == "en" else case["critic"]["notes"]
    for note in critic_notes:
        st.write("· " + note)

    with st.expander(S["far"]):
        for profile in case["far"]["profiles"]:
            suffix = "_en" if lang == "en" else ""
            characterization = profile.get(f"characterization{suffix}", profile["characterization"])
            why = profile.get(f"why{suffix}", profile["why"])
            method = profile.get(f"method{suffix}", profile["method"])
            st.markdown(f"**{profile['name']} — {characterization}**")
            st.write(why)
            st.caption(f"{S['method']}: {method}")
            cols = st.columns(3)
            cols[0].write(S["functions"])
            cols[0].write(profile.get(f"functions{suffix}", profile["functions"]))
            cols[1].write(S["assets"])
            cols[1].write(profile.get(f"assets{suffix}", profile["assets"]))
            cols[2].write(S["risks"])
            cols[2].write(profile.get(f"risks{suffix}", profile["risks"]))

with tab_rag:
    st.subheader(S["ask_title"])
    if "upload_key" not in st.session_state:
        st.session_state.upload_key = 0
    uploads = st.file_uploader(
        S["upload"],
        type=["pdf", "txt", "md", "xml"],
        accept_multiple_files=True,
        help=S["upload_help"],
        key=f"uploads-{st.session_state.upload_key}",
    )
    for kind, payload in index_uploads(uploads):
        if kind == "ok":
            name, count = payload.split("|", 1)
            st.caption(S["upload_ok"].format(name=name, n=count))
        elif kind == "big":
            st.warning(S["upload_big"].format(name=payload))
        else:
            st.warning(S["upload_empty"].format(name=payload))
    if st.session_state.get("upload_chunks") and st.button(S["upload_clear"]):
        st.session_state.upload_key += 1
        st.session_state["upload_chunks"] = []
        st.session_state.pop("asked_q", None)
        st.rerun()

    example = st.selectbox(S["examples_label"], S["examples"], key=f"ex-{lang}")
    qkey = f"q-{lang}"
    if st.session_state.get(f"seen-{lang}") != example:
        st.session_state[f"seen-{lang}"] = example
        st.session_state[qkey] = example
    question = st.text_area(S["question"], key=qkey, height=90)

    extra = st.session_state.get("upload_chunks") or None
    should_answer = st.button(S["answer"], type="primary")
    same_question = st.session_state.get("asked_q") == question and bool(question.strip())
    language_changed = same_question and st.session_state.get("asked_lang") != lang
    if should_answer or language_changed:
        if not question.strip():
            st.warning(S["empty_q"])
        else:
            rag = answer_question(question, lang=lang, extra_chunks=extra)
            graph = run_kg(question)
            critic = critique_retrieval(rag["citations"], rag["hits"])
            st.session_state["asked_q"] = question
            st.session_state["asked_lang"] = lang
            st.session_state["asked_view"] = {"rag": rag, "graph": graph, "critic": critic}
    view = st.session_state.get("asked_view") if st.session_state.get("asked_lang") == lang else None
    if view and st.session_state.get("asked_q") == question:
        st.markdown(view["rag"]["answer"])
        edges = view["graph"]["edges"] if view["graph"] else []
        if edges:
            st.markdown(f"**{S['graph']}**")
            for edge in edges:
                note = edge["note_de"] if lang == "de" else edge["note_en"]
                label = relation_label(edge["relation"], lang)
                st.write(f"{edge['src']} — {label} → {edge['dst']}. {note}")
        if view["critic"]:
            critic_line = view["critic"]["notes_en"] if lang == "en" else view["critic"]["notes"]
            st.caption(S["critic"] + ": " + " ".join(critic_line))

with tab_screen:
    st.subheader(S["screen_title"])
    screen_report = cached_screen()
    st.markdown(S["screen_lead"].format(f1=f"{screen_report['f1_mean']:.0%}"))
    description = st.text_area(
        S["description"],
        value="Contract manufacturer of induction-hardened steel shafts. The customer owns the recipe and the OEM contract. The plant has no brand of its own.",
        height=90,
        key="screen-text",
    )
    if st.button(S["classify"]):
        if not description.strip():
            st.warning(S["empty_desc"])
        else:
            st.session_state["screen_decision"] = screen_text(description)
            st.session_state["screen_for"] = description
    decision = st.session_state.get("screen_decision")
    if decision and st.session_state.get("screen_for") == description:
        label = S["yes"] if decision["comparable"] else S["no"]
        st.write(f"**{label}** · {S['prob']} {decision['probability']:.0%}")
        st.write(S["for"] + ": " + ", ".join(decision["reasons_for"]))
        st.write(S["against"] + ": " + ", ".join(decision["reasons_against"]))
    rows = [
        {
            S["company"]: row["name"],
            S["label"]: S["yes"] if row["label"] else S["no"],
            S["fold"]: S["yes"] if row["prediction"] else S["no"],
            "Net Cost Plus": pct(row["net_cost_plus"], lang) if row["net_cost_plus"] else "—",
        }
        for row in screen_report["rows"]
    ]
    st.dataframe(rows, hide_index=True, width="stretch")

with tab_margin:
    st.subheader(f"TNMM {year}")
    left, right = st.columns(2)
    with left:
        st.markdown("**HTPL · Net Cost Plus**")
        st.write(f"{S['sales']}: {money(assessment['htpl']['revenue'], lang)}")
        st.write(f"{S['mfg']}: {money(assessment['htpl']['manufacturing_costs'], lang)}")
        st.write(f"{S['op']}: {money(assessment['htpl']['operating_profit_before_royalty'], lang)}")
        st.write(f"{S['indicator']}: {pct(assessment['htpl']['net_cost_plus'], lang)} · {S['position']}: {lage[assessment['htpl_position']]}")
        st.write(
            f"{S['range']} {pct(assessment['cm_range']['low'], lang)} – {pct(assessment['cm_range']['high'], lang)}, "
            f"{S['median']} {pct(assessment['cm_range']['median'], lang)}."
        )
        if assessment["htpl_adjustment"]:
            st.write(f"{S['gap']}: {money(assessment['htpl_adjustment']['profit_eur'], lang)}")
    with right:
        st.markdown("**HTUS · " + ("Betriebsmarge" if lang == "de" else "Operating margin") + "**")
        st.write(f"{S['oem_sales']}: {money(assessment['htus']['revenue'], lang)}")
        st.write(f"{S['op_us']}: {money(assessment['htus']['operating_profit'], lang)}")
        st.write(f"{S['indicator']}: {pct(assessment['htus']['operating_margin'], lang)} · {S['position']}: {lage[assessment['htus_position']]}")
        st.write(
            f"{S['range']} {pct(assessment['lrd_range']['low'], lang)} – {pct(assessment['lrd_range']['high'], lang)}, "
            f"{S['median']} {pct(assessment['lrd_range']['median'], lang)}."
        )
        if assessment["htus"]["berry_ratio"] is not None:
            berry = f"{assessment['htus']['berry_ratio']:.2f}"
            if lang == "de":
                berry = berry.replace(".", ",")
            st.write(f"Berry Ratio: {berry}")

    st.markdown(f"**{S['history']}**")
    history = [
        {
            S["year_col"]: item["year"],
            "Net Cost Plus": round(item["net_cost_plus"] * 100, 2),
            S["energy_col"]: item["energy"],
        }
        for item in assessment["history"]["HTPL"]
    ]
    st.bar_chart(pd.DataFrame(history).set_index(S["year_col"])[["Net Cost Plus"]], height=220)
    st.caption(S["chart"])
    st.dataframe(history, hide_index=True, width="stretch")

with tab_matrix:
    st.subheader(f"{S['tabs'][4]} {year}")
    st.caption(S["matrix_help"])
    if lang == "en":
        matrix_rows = [
            {
                "Subject": row["gegenstand_en"],
                "Type": row["art_en"],
                "Provider": row["leistungserbringer"],
                "Recipient": row["leistungsempfaenger"],
                "Volume EUR": row["volumen_eur"],
                "Consideration EUR": row["entgelt_eur"],
                "Contract": row["vertrag"] or "—",
                "Method": row["methode_en"],
                "Territories": row["steuerhoheitsgebiete_en"],
                "Outside ordinary taxation": row["ausserhalb_regelbesteuerung_en"],
            }
            for row in case["matrix"]
        ]
    else:
        matrix_rows = [
            {
                "Gegenstand": row["gegenstand"],
                "Art": row["art"],
                "Leistungserbringer": row["leistungserbringer"],
                "Leistungsempfänger": row["leistungsempfaenger"],
                "Volumen EUR": row["volumen_eur"],
                "Entgelt EUR": row["entgelt_eur"],
                "Vertrag": row["vertrag"] or "—",
                "Methode": row["methode"],
                "Steuerhoheitsgebiete": row["steuerhoheitsgebiete"],
                "Außerhalb Regelbesteuerung": row["ausserhalb_regelbesteuerung"],
            }
            for row in case["matrix"]
        ]
    st.dataframe(matrix_rows, hide_index=True, width="stretch")

with tab_eval:
    st.subheader(S["eval_title"])
    report = cached_eval()
    st.metric("Top-3", f"{report['hits']} / {report['total']} · {report['accuracy']:.0%}")
    st.dataframe(
        [
            {
                S["q_col"]: row["question"],
                S["hit_col"]: S["yes_short"] if row["ok"] else S["no_short"],
                S["exp_col"]: ", ".join(row["accept"]),
                S["top_col"]: ", ".join(row["got"]),
            }
            for row in report["rows"]
        ],
        hide_index=True,
        width="stretch",
    )
    st.caption(S["eval_note"])
