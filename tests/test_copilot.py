from tp_copilot.agents.far_agent import run_far
from tp_copilot.agents.margin_agent import assess, german_range, locate
from tp_copilot.agents.orchestrator import ask, run_case, transaction_matrix
from tp_copilot.agents.router import route_question
from tp_copilot.agents.screening_agent import evaluate, screen_text
from tp_copilot.data.group import build_ledger
from tp_copilot.eval.run_eval import run_eval
from tp_copilot.ingest.chunker import chunk_paragraphs
from tp_copilot.retrieval.store import get_store
from tp_copilot.knowledge.graph import query_graph


def test_paragraph_chunker_keeps_numbers():
    text = (
        "1.6. The arm's length principle is the comparison with independents in this sample note.\n"
        "1.33. Delineate the controlled transaction before comparing it with independents.\n"
    )
    chunks = chunk_paragraphs(text, "sample")
    assert [chunk["paragraph"] for chunk in chunks] == ["1.6", "1.33"]


def test_router_sends_methods_to_the_guideline_agent():
    assert "guideline" in route_question("When is TNMM preferred over cost plus?")


def test_router_sends_the_case_to_far_and_margin():
    routes = route_question("Ist die Marge der Härtetechnik in Polen fremdüblich?")
    assert "far" in routes
    assert "margin" in routes


def test_citation_accuracy_is_high():
    report = run_eval()
    assert report["total"] >= 40
    assert report["accuracy"] >= 0.90


def test_tnmm_question_opens_the_comparison_note():
    hits = get_store().search(
        "When should I use TNMM rather than the cost plus method for a contract manufacturer?",
        k=1,
    )
    assert hits[0]["id"] == "oecd-tnmm-vs-costplus"


def test_graph_links_contract_manufacturer_to_tnmm():
    result = query_graph("Lohnfertiger TNMM")
    relations = {(edge["src"], edge["dst"]) for edge in result["edges"]}
    assert ("contract_manufacturer", "TNMM") in relations


def test_german_range_drops_outer_quarters_and_uses_the_median():
    values = [0.031, 0.034, 0.038, 0.042, 0.045, 0.049, 0.052, 0.056, 0.061, 0.064, 0.068, 0.072, 0.079, 0.084]
    rng = german_range(values)
    assert rng["dropped_each_tail"] == 3
    assert rng["low"] == 0.042
    assert rng["high"] == 0.068
    assert abs(rng["median"] - 0.054) < 1e-9
    assert locate(0.02, rng) == "below"
    assert locate(0.05, rng) == "inside"


def test_exported_ledger_matches_the_generator():
    import pandas as pd
    from pathlib import Path

    exported = pd.read_csv(Path("data/group/haertetechnik_bookings.csv"))
    fresh = build_ledger()
    assert len(exported) == len(fresh)
    assert int(exported.amount_eur.sum()) == int(fresh.amount_eur.sum())


def test_intercompany_goods_match_across_entities():
    ledger = build_ledger()
    for year in (2023, 2024, 2025):
        pl_sales = ledger[(ledger.entity == "HTPL") & (ledger.year == year) & (ledger.account == "REV_GOODS")].amount_eur.sum()
        de_purchases = ledger[(ledger.entity == "HTDE") & (ledger.year == year) & (ledger.account == "COST_GOODS_PL")].amount_eur.sum()
        de_sales = ledger[(ledger.entity == "HTDE") & (ledger.year == year) & (ledger.account == "REV_GOODS_US")].amount_eur.sum()
        us_purchases = ledger[(ledger.entity == "HTUS") & (ledger.year == year) & (ledger.account == "COST_GOODS")].amount_eur.sum()
        assert int(pl_sales) == int(de_purchases)
        assert int(de_sales) == int(us_purchases)


def test_2025_case_finds_the_planted_errors_and_2024_does_not():
    case = run_case(2025)
    ids = {finding["id"] for finding in case["findings"]}
    assert {"pl_margin", "us_margin", "royalty_characterization", "missing_contract", "energy_passthrough", "function_transfer_escape"} <= ids
    assert case["assessment"]["htpl_position"] == "below"
    assert case["assessment"]["htus_position"] == "above"
    assert case["assessment"]["htpl_adjustment"]["profit_eur"] > 0
    assert case["critic"]["ok"] is True

    earlier = assess(2024)
    assert earlier["htpl_position"] == "inside"
    assert earlier["htpl"]["net_cost_plus"] == 0.05
    assert abs(case["assessment"]["htpl"]["net_cost_plus"] - 0.02) < 1e-9


def test_matrix_names_every_column_the_leaflet_asks_for():
    matrix = transaction_matrix(2025)
    expected = {
        "gegenstand",
        "art",
        "leistungserbringer",
        "leistungsempfaenger",
        "volumen_eur",
        "entgelt_eur",
        "vertrag",
        "methode",
        "steuerhoheitsgebiete",
        "ausserhalb_regelbesteuerung",
    }
    assert expected <= set(matrix.columns)
    loan = matrix[matrix["art"] == "Darlehen"].iloc[0]
    assert loan["volumen_eur"] != loan["entgelt_eur"]
    assert (matrix["vertrag"] == "").sum() == 1


def test_far_characterizes_the_polish_plant_as_contract_manufacturer():
    profiles = {item["entity"]: item for item in run_far()["profiles"]}
    assert "Lohnfertiger" in profiles["HTPL"]["characterization"]
    assert profiles["HTPL"]["method_key"] == "TNMM"
    assert profiles["HTDE"]["method_key"] == "residual"


def test_screening_rejects_a_bank_and_accepts_a_heat_treater():
    report = evaluate()
    assert report["f1_mean"] >= 0.85
    heat = screen_text(
        "Contract manufacturer doing induction hardening of steel parts to the customer's recipe. No own brand."
    )
    bank = screen_text("Retail bank taking deposits and making loans. No factory.")
    assert heat["comparable"] is True
    assert bank["comparable"] is False


def test_answer_follows_the_requested_language():
    from tp_copilot.agents.rag_agent import answer_question
    from tp_copilot.ingest.chunker import chunks_from_bytes

    german = answer_question("What is the arm's length principle in Article 9?", lang="de")
    english = answer_question("Was ist der Fremdvergleichsgrundsatz nach Randnummer 1.6?", lang="en")
    assert "Studiennotiz" in german["answer"]
    assert "Study note" in english["answer"]

    uploaded = chunks_from_bytes(
        "sample.txt",
        ("9.99. " + ("A portfolio paragraph about a fictional hardening royalty. " * 4)).encode(),
    )
    assert uploaded and uploaded[0]["paragraph"] == "9.99"
    hit = answer_question("fictional hardening royalty paragraph 9.99", lang="en", extra_chunks=uploaded)
    assert hit["citations"][0]["paragraph"] == "9.99"


def test_ask_cites_the_median_rule():
    result = ask("Wie funktioniert das Viertel der kleinsten Werte und der Median nach §1 Abs. 3a AStG?")
    assert result["rag"]["citations"][0]["paragraph"] == "§1 Abs. 3a"
    assert result["critic"]["ok"] is True
