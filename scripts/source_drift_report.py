#!/usr/bin/env python3
"""Report source drift signals from a saved RAG eval result."""

from __future__ import annotations

import argparse
import json
import os
import sys
import unicodedata
from pathlib import Path
from typing import Any


def _basename(path: str) -> str:
    return unicodedata.normalize("NFC", os.path.basename(path))


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _case_map(test_cases_path: Path) -> dict[str, dict[str, Any]]:
    data = _load_json(test_cases_path)
    return {case["id"]: case for case in data.get("cases", [])}


def _source_set(sources: list[str]) -> set[str]:
    return {_basename(source) for source in sources}


def _fmt(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _has_generation_failure(case: dict[str, Any]) -> bool:
    if case.get("answer_accuracy") not in (None, 1.0):
        return True
    if case.get("faithfulness") not in (None, 1.0):
        return True
    if case.get("expected_not_found") is True and case.get("not_found_success") is not True:
        return True
    return False


def build_report(
    eval_result: dict[str, Any],
    test_cases: dict[str, dict[str, Any]],
    min_source_recall: float,
    min_rag_precision: float,
    watch_source_recall: float,
    watch_rag_precision: float,
) -> tuple[str, bool]:
    lines: list[str] = []
    critical_cases: list[dict[str, Any]] = []
    watch_cases: list[dict[str, Any]] = []

    summary = eval_result.get("summary", {})
    lines.append("# Source Drift Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- `total_cases`: `{summary.get('total_cases', len(eval_result.get('cases', [])))}`")
    for key in (
        "accuracy_mean",
        "faithfulness_mean",
        "not_found_success_rate",
        "rag_normalized_source_precision@k_mean",
        "source_recall@k_mean",
    ):
        if key in summary:
            lines.append(f"- `{key}`: `{_fmt(summary[key])}`")

    for case in eval_result.get("cases", []):
        case_id = case.get("id", "")
        recall = case.get("source_recall_at_k")
        precision = case.get("rag_normalized_source_precision_at_k")
        generation_failed = _has_generation_failure(case)
        critical = generation_failed
        if recall is not None and recall < min_source_recall:
            critical = True
        if precision is not None and precision < min_rag_precision:
            critical = True

        watch = False
        if recall is not None and recall < watch_source_recall:
            watch = True
        if precision is not None and precision < watch_rag_precision:
            watch = True

        relevant = _source_set(test_cases.get(case_id, {}).get("relevant_sources", []))
        rag_sources = _source_set(case.get("rag_retrieved_sources", []))
        missing = sorted(relevant - rag_sources)
        unexpected = sorted(rag_sources - relevant)
        row = {
            "id": case_id,
            "question": case.get("question", ""),
            "source_recall": recall,
            "rag_precision": precision,
            "answer_accuracy": case.get("answer_accuracy"),
            "faithfulness": case.get("faithfulness"),
            "not_found_success": case.get("not_found_success"),
            "missing": missing,
            "unexpected": unexpected,
            "generation_failed": generation_failed,
        }
        if critical:
            critical_cases.append(row)
        elif watch:
            watch_cases.append(row)

    lines.append("")
    lines.append("## Critical Cases")
    lines.append("")
    if critical_cases:
        lines.extend(_case_table(critical_cases))
    else:
        lines.append("- 없음.")

    lines.append("")
    lines.append("## Watch Cases")
    lines.append("")
    if watch_cases:
        lines.extend(_case_table(watch_cases))
    else:
        lines.append("- 없음.")

    lines.append("")
    lines.append("## Thresholds")
    lines.append("")
    lines.append(f"- critical source recall: `< {_fmt(min_source_recall)}`")
    lines.append(f"- critical rag normalized source precision: `< {_fmt(min_rag_precision)}`")
    lines.append(f"- watch source recall: `< {_fmt(watch_source_recall)}`")
    lines.append(f"- watch rag normalized source precision: `< {_fmt(watch_rag_precision)}`")

    return "\n".join(lines) + "\n", bool(critical_cases)


def _case_table(cases: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Case | Recall | RAG Precision | Accuracy | Faithfulness | Missing Relevant Sources | Unexpected RAG Sources |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for case in cases:
        missing = ", ".join(case["missing"]) if case["missing"] else "-"
        unexpected = ", ".join(case["unexpected"]) if case["unexpected"] else "-"
        lines.append(
            "| {id} | {recall} | {precision} | {accuracy} | {faithfulness} | {missing} | {unexpected} |".format(
                id=case["id"],
                recall=_fmt(case["source_recall"]),
                precision=_fmt(case["rag_precision"]),
                accuracy=_fmt(case["answer_accuracy"]),
                faithfulness=_fmt(case["faithfulness"]),
                missing=missing,
                unexpected=unexpected,
            )
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate source drift report from eval result JSON.")
    parser.add_argument("eval_result", type=Path)
    parser.add_argument("--test-cases", type=Path, default=Path("eval/test_cases.json"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--min-source-recall", type=float, default=0.5)
    parser.add_argument("--min-rag-precision", type=float, default=0.5)
    parser.add_argument("--watch-source-recall", type=float, default=0.75)
    parser.add_argument("--watch-rag-precision", type=float, default=0.75)
    parser.add_argument("--fail-on-critical", action="store_true")
    args = parser.parse_args()

    eval_result = _load_json(args.eval_result)
    test_cases = _case_map(args.test_cases)
    report, has_critical = build_report(
        eval_result=eval_result,
        test_cases=test_cases,
        min_source_recall=args.min_source_recall,
        min_rag_precision=args.min_rag_precision,
        watch_source_recall=args.watch_source_recall,
        watch_rag_precision=args.watch_rag_precision,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

    if args.fail_on_critical and has_critical:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
