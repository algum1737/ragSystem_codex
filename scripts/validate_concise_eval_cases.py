#!/usr/bin/env python3
"""Validate concise lightweight eval case schema without running RAG."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VALID_DOC_TYPES = {None, "일반", "유료서비스", "위치기반서비스", "운영정책"}


def _fail(errors: list[str], message: str) -> None:
    errors.append(message)


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_rule(case_id: str, rule: Any, field_name: str, index: int, errors: list[str]) -> None:
    if not isinstance(rule, dict):
        _fail(errors, f"{case_id}.{field_name}[{index}] must be an object")
        return

    for key in ("id", "description"):
        if not _is_non_empty_string(rule.get(key)):
            _fail(errors, f"{case_id}.{field_name}[{index}].{key} must be a non-empty string")

    terms = rule.get("terms")
    if not isinstance(terms, list) or not terms:
        _fail(errors, f"{case_id}.{field_name}[{index}].terms must be a non-empty list")
    elif not all(_is_non_empty_string(term) for term in terms):
        _fail(errors, f"{case_id}.{field_name}[{index}].terms must contain only non-empty strings")

    min_matches = rule.get("min_matches")
    if not isinstance(min_matches, int) or min_matches < 1:
        _fail(errors, f"{case_id}.{field_name}[{index}].min_matches must be a positive integer")
    elif isinstance(terms, list) and min_matches > len(terms):
        _fail(errors, f"{case_id}.{field_name}[{index}].min_matches cannot exceed terms length")


def validate_cases(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"failed to load JSON: {exc}"]

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return ["top-level 'cases' must be a non-empty list"]

    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            _fail(errors, f"cases[{index}] must be an object")
            continue

        case_id = case.get("id")
        if not _is_non_empty_string(case_id):
            _fail(errors, f"cases[{index}].id must be a non-empty string")
            case_id = f"cases[{index}]"
        elif case_id in seen_ids:
            _fail(errors, f"duplicate case id: {case_id}")
        else:
            seen_ids.add(case_id)

        for key in ("source_case_id", "question"):
            if not _is_non_empty_string(case.get(key)):
                _fail(errors, f"{case_id}.{key} must be a non-empty string")

        if case.get("doc_type") not in VALID_DOC_TYPES:
            _fail(errors, f"{case_id}.doc_type is invalid: {case.get('doc_type')!r}")

        for key in ("required_points", "forbidden_claims"):
            rules = case.get(key)
            if not isinstance(rules, list):
                _fail(errors, f"{case_id}.{key} must be a list")
                continue
            if key == "required_points" and not rules:
                _fail(errors, f"{case_id}.{key} must not be empty")
            for rule_index, rule in enumerate(rules):
                _validate_rule(str(case_id), rule, key, rule_index, errors)

        if not isinstance(case.get("expected_not_found"), bool):
            _fail(errors, f"{case_id}.expected_not_found must be a boolean")

        for key in ("max_answer_length", "min_source_count"):
            value = case.get(key)
            if not isinstance(value, int) or value < 1:
                _fail(errors, f"{case_id}.{key} must be a positive integer")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate concise lightweight eval case schema.")
    parser.add_argument("path", type=Path, nargs="?", default=Path("eval/concise_test_cases.json"))
    args = parser.parse_args()

    errors = validate_cases(args.path)
    if errors:
        for error in errors:
            print(f"concise eval schema error: {error}", file=sys.stderr)
        return 1

    data = json.loads(args.path.read_text(encoding="utf-8"))
    print(f"concise eval case schema valid: {len(data['cases'])} cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
