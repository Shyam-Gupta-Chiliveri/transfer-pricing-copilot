"""Command line: python -m tp_copilot --eval | --case | "question"."""

from __future__ import annotations

import argparse
import json

from tp_copilot.agents.orchestrator import ask, run_case
from tp_copilot.eval.run_eval import run_eval


def main() -> None:
    parser = argparse.ArgumentParser(description="TP Copilot")
    parser.add_argument("question", nargs="*", help="Guideline question")
    parser.add_argument("--case", action="store_true", help="Run the Härtetechnik case")
    parser.add_argument("--eval", action="store_true", help="Measure citation accuracy")
    parser.add_argument("--year", type=int, default=2025)
    args = parser.parse_args()

    if args.eval:
        report = run_eval()
        print(f"Top-{report['k']} citation accuracy: {report['hits']}/{report['total']} = {report['accuracy']:.1%}")
        for row in report["rows"]:
            mark = "ok" if row["ok"] else "MISS"
            print(f"{mark} {row['id']} got {row['got']} accept {row['accept']}")
        return

    if args.case or not args.question:
        case = run_case(args.year)
        print(f"Härtetechnik AG {case['year']} — {case['ledger_rows']} bookings")
        for finding in case["findings"]:
            print(f"[{finding['severity']}] {finding['title']}")
        print("Critic:")
        for note in case["critic"]["notes"]:
            print(f"- {note}")
        return

    result = ask(" ".join(args.question))
    print(json.dumps({"routes": result["routes"]}, ensure_ascii=False))
    if result["rag"]:
        print(result["rag"]["answer"])


if __name__ == "__main__":
    main()
