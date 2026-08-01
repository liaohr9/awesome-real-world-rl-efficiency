#!/usr/bin/env python3
"""Deterministic offline semantic validator for the efficiency evidence atlas."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
REPOSITORY_URL = "https://github.com/liaohr9/awesome-real-world-rl-efficiency"
RTR_URL = "https://openreview.net/forum?id=oRwcxFuN25"

PAPERS_HEADER = [
    "work_id", "title", "year", "venue", "doi", "arxiv_id",
    "official_paper_url", "project_url", "code_url", "code_status",
    "license", "last_verified", "screening_status", "real_robot_tier",
    "topic_evidence_tier", "efficiency_claim_tier", "peer_review_status",
    "robot_platform", "embodiment", "tasks", "real_robot_training",
    "evidence_locator", "success_definition", "success_result",
    "evaluation_trials", "reported_phase_duration", "real_steps",
    "real_episodes", "control_frequency_hz", "robot_hours",
    "wall_clock_hours", "num_parallel_robots", "compute", "demo_count",
    "reset_type", "reward_engineering", "prior_data", "wear_safety",
    "claimed_reduction", "reduction_type", "hidden_or_displaced_cost",
    "source_verified_against_original", "source_grade", "limitations",
]
MECHANISM_HEADER = [
    "mechanism_id", "level1", "level2", "level3", "definition", "work_ids",
    "physical_evidence_tiers", "core_tradeoff", "failure_modes",
]
QUANT_HEADER = [
    "claim_id", "work_id", "metric_family", "metric_name", "value", "unit",
    "denominator", "comparison_baseline", "physical_platform",
    "evidence_locator", "source_grade", "reporting_status", "interpretation_limit",
]
CLAIMS_HEADER = [
    "claim_id", "claim_text", "claim_scope", "work_ids", "evidence_type",
    "confidence", "caveat", "intended_section",
]
TIME_HEADER = [
    "time_id", "work_id", "phase", "task_scope", "clock_basis",
    "duration_value", "duration_unit", "target_definition",
    "threshold_rule_available", "evaluator_or_checkpoint", "boundary_start",
    "boundary_end", "partial_scope", "evidence_locator", "source_grade",
    "reporting_status", "interpretation_limit",
]
CLAIM_EVIDENCE_HEADER = [
    "claim_evidence_id", "claim_id", "evidence_id", "relation",
    "executable_filter", "expected_count", "member_work_ids", "source_locator", "notes",
]
TIER_HEADER = [
    "tier_rationale_id", "work_id", "assigned_tier", "decision_rule",
    "evidence_ids", "usable_comparison", "declared_target",
    "denominator_quality", "lifecycle_boundary", "independent_replication",
    "adjudication", "rationale", "evidence_locator",
]
LIFECYCLE_HEADER = [
    "lifecycle_id", "work_id", "cost_channel", "value", "unit", "denominator",
    "reporting_status", "component_or_proxy", "evidence_locator", "interpretation_limit",
]
HARDWARE_HEADER = [
    "hardware_id", "work_id", "role", "count", "count_status", "simultaneity",
    "peak_system_robot_count", "boundary", "evidence_locator", "interpretation_limit",
]
ZERO_HEADER = [
    "zero_basis_id", "work_id", "quantitative_evidence_id", "zero_value",
    "zero_scope", "zero_basis", "upstream_data_status", "evidence_locator",
    "interpretation_limit",
]

TABLES = {
    "data/papers.csv": PAPERS_HEADER,
    "data/mechanism_matrix.csv": MECHANISM_HEADER,
    "data/quantitative_evidence.csv": QUANT_HEADER,
    "data/claims_ledger.csv": CLAIMS_HEADER,
    "data/time_ontology.csv": TIME_HEADER,
    "data/claim_evidence.csv": CLAIM_EVIDENCE_HEADER,
    "data/tier_rationales.csv": TIER_HEADER,
    "data/lifecycle_cost_grid.csv": LIFECYCLE_HEADER,
    "data/hardware_roles.csv": HARDWARE_HEADER,
    "data/zero_demo_basis.csv": ZERO_HEADER,
}
REQUIRED_FILES = {
    "README.md", "SURVEY.md", "CITATION.cff", "CONTRIBUTING.md", "LICENSE",
    "Makefile", ".gitignore", ".github/workflows/validate.yml",
    "paper/main.tex", "paper/references.bib", "data/schema.md",
    "docs/methodology.md", "docs/evaluation_protocol.md", "docs/research_gaps.md",
    "docs/validation_report.md", "scripts/validate.py", "scripts/test_validator.py",
    *TABLES,
}

STANDARD_METRICS = {
    "reported_phase_duration", "time_to_declared_target",
    "physical_steps_or_transitions", "physical_episodes_or_rollouts",
    "control_frequency", "active_or_aggregate_robot_hours", "elapsed_wall_clock",
    "primary_data_robot_count", "reported_compute_resource_or_duration",
    "demonstration_count", "evaluation_trial_count", "reported_success_result",
}
LIFECYCLE_CHANNELS = {
    "active_human_time", "standby_monitoring_time", "reset_recovery_cost",
    "engineering_setup_time", "safety_exposure", "wear_maintenance_downtime",
    "failed_development_runs", "prior_data_cost",
}
REPORTING_STATUSES = {
    "source_reported", "source_reported_approximate", "derived",
    "mixed_or_ambiguous", "not_reported",
}
SEMANTIC_SENTINEL = re.compile(
    r"(?i)(?:^|[\s;:,(/])(?:NR|N/A|NA|unknown|not[ _-]?reported|unavailable)(?:$|[\s;:,.!)])"
)
PATHLIKE_LOCATOR = re.compile(
    r"(?i)(?:evidence_cards/|(?:^|[\s;])work/|(?:^|[\s;])sources/|\.md(?:$|[;\s])|phase\s*2)"
)
BUILD_SUFFIXES = {".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".pdf", ".pyc", ".toc"}
BUILD_NAMES = {".DS_Store", "main.synctex.gz"}


def fail(message: str) -> None:
    ERRORS.append(message)


def read_text(relative: str) -> str:
    try:
        return (ROOT / relative).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"{relative}: cannot read UTF-8 text: {exc}")
        return ""


def repository_files(pattern: str = "*"):
    """Yield public repository files while excluding Git's private metadata."""
    for path in ROOT.rglob(pattern):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or not path.is_file():
            continue
        yield path


def load_csv(relative: str, header: list[str]) -> list[dict[str, str]]:
    try:
        with (ROOT / relative).open(newline="", encoding="utf-8-sig") as handle:
            raw = list(csv.reader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        fail(f"{relative}: cannot parse CSV: {exc}")
        return []
    if not raw:
        fail(f"{relative}: empty CSV")
        return []
    if raw[0] != header:
        fail(f"{relative}: header mismatch; got {raw[0]!r}")
    rows: list[dict[str, str]] = []
    for line, values in enumerate(raw[1:], 2):
        if len(values) != len(header):
            fail(f"{relative}:{line}: expected {len(header)} columns, got {len(values)}")
            continue
        row = dict(zip(header, values, strict=True))
        if relative != "data/papers.csv" and any(value == "" for value in values):
            fail(f"{relative}:{line}: blank field; use a controlled marker")
        rows.append(row)
    return rows


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def check_unique(rows: list[dict[str, str]], field: str, relative: str) -> None:
    counts = Counter(row[field] for row in rows)
    bad = sorted(key for key, count in counts.items() if not key or count != 1)
    if bad:
        fail(f"{relative}: non-unique/empty {field}: {bad}")


def check_required_tree() -> None:
    for relative in sorted(REQUIRED_FILES):
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"required file missing/empty: {relative}")
    for path in repository_files():
        if path.suffix.lower() in BUILD_SUFFIXES or path.name in BUILD_NAMES:
            fail(f"build/source artifact must not remain: {path.relative_to(ROOT)}")
        if "__pycache__" in path.parts:
            fail(f"Python cache must not remain: {path.relative_to(ROOT)}")


def check_private_paths_and_locators(tables: dict[str, list[dict[str, str]]]) -> None:
    forbidden = ["/" + "Users" + "/", "/" + "home" + "/", "file" + "://", "work" + "/phase"]
    for path in repository_files():
        if path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            continue
        relative = path.relative_to(ROOT).as_posix()
        text = read_text(relative)
        if any(token in text for token in forbidden) or re.search(r"(?i)\b[a-z]:\\", text):
            fail(f"{relative}: contains a local/private path")
    for relative, rows in tables.items():
        for line, row in enumerate(rows, 2):
            for field in ("evidence_locator", "source_locator"):
                if field not in row:
                    continue
                value = row[field]
                if PATHLIKE_LOCATOR.search(value):
                    fail(f"{relative}:{line}: unresolved/path-like {field}: {value!r}")


def check_papers(rows: list[dict[str, str]]) -> tuple[set[str], set[str]]:
    check_unique(rows, "work_id", "data/papers.csv")
    if len(rows) != 36:
        fail(f"data/papers.csv: expected 36 rows, got {len(rows)}")
    status = Counter(row["screening_status"] for row in rows)
    if status != Counter({"included_core": 34, "included_context": 2}):
        fail(f"data/papers.csv: bad screening distribution {dict(status)}")
    paper_ids = {row["work_id"] for row in rows}
    core_ids = {row["work_id"] for row in rows if row["screening_status"] == "included_core"}
    for row in rows:
        for field in ("official_paper_url", "project_url", "code_url"):
            value = row[field].strip()
            if value:
                parsed = urlsplit(value)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    fail(f"{row['work_id']}: invalid {field}={value!r}")
        if row["screening_status"] == "included_context":
            if (row["topic_evidence_tier"], row["real_robot_tier"], row["efficiency_claim_tier"]) != ("context", "R0", "E0"):
                fail(f"{row['work_id']}: context work must be context/R0/E0")
        elif row["topic_evidence_tier"] != "core":
            fail(f"{row['work_id']}: core work has wrong topic role")
    rtr = next((row for row in rows if row["work_id"] == "hu2025robottrainsrobot"), None)
    if not rtr or rtr["official_paper_url"] != RTR_URL:
        fail("data/papers.csv: Robot Trains Robot must use final CoRL OpenReview URL")
    return paper_ids, core_ids


def check_mechanisms(rows: list[dict[str, str]], papers: dict[str, dict[str, str]], core_ids: set[str]) -> None:
    check_unique(rows, "mechanism_id", "data/mechanism_matrix.csv")
    if {row["mechanism_id"] for row in rows} != {f"EFF-M{i:02d}" for i in range(1, 26)}:
        fail("data/mechanism_matrix.csv: IDs must be EFF-M01..EFF-M25")
    covered: set[str] = set()
    for row in rows:
        ids = set(split_ids(row["work_ids"]))
        covered |= ids
        if not ids or not ids <= core_ids:
            fail(f"{row['mechanism_id']}: work_ids must be nonempty core IDs")
        tier_map = {}
        for item in split_ids(row["physical_evidence_tiers"]):
            if ":" not in item:
                fail(f"{row['mechanism_id']}: malformed tier item {item!r}")
                continue
            work_id, tier = item.split(":", 1)
            tier_map[work_id] = tier
        if set(tier_map) != ids:
            fail(f"{row['mechanism_id']}: tier IDs differ from work_ids")
        for work_id, tier in tier_map.items():
            expected = f"{papers[work_id]['real_robot_tier']}/{papers[work_id]['efficiency_claim_tier']}"
            if tier != expected:
                fail(f"{row['mechanism_id']}: {work_id} tier {tier} != {expected}")
    if covered != core_ids:
        fail(f"data/mechanism_matrix.csv: core coverage mismatch missing={sorted(core_ids-covered)}")


def check_quantitative(rows: list[dict[str, str]], core_ids: set[str]) -> dict[str, list[dict[str, str]]]:
    check_unique(rows, "claim_id", "data/quantitative_evidence.csv")
    if len(rows) != 424 or {row["claim_id"] for row in rows} != {f"QE-EFF-{i:04d}" for i in range(1, 425)}:
        fail("data/quantitative_evidence.csv: expected QE-EFF-0001..0424 (424 rows)")
    by_work: dict[str, list[dict[str, str]]] = defaultdict(list)
    zeros: list[dict[str, str]] = []
    for line, row in enumerate(rows, 2):
        by_work[row["work_id"]].append(row)
        if row["work_id"] not in core_ids:
            fail(f"data/quantitative_evidence.csv:{line}: non-core work")
        if row["reporting_status"] not in REPORTING_STATUSES:
            fail(f"{row['claim_id']}: invalid reporting_status")
        if not row["evidence_locator"].strip() or not row["interpretation_limit"].strip():
            fail(f"{row['claim_id']}: locator/interpretation limit required")
        triplet = (row["value"], row["unit"], row["denominator"])
        if row["reporting_status"] == "not_reported":
            if triplet != ("NR", "NR", "NR"):
                fail(f"{row['claim_id']}: not_reported requires NR/NR/NR")
        else:
            for field in ("value", "unit", "denominator"):
                if SEMANTIC_SENTINEL.search(row[field]):
                    fail(f"{row['claim_id']}: nonmissing {field} contains semantic missing sentinel {row[field]!r}")
        if re.fullmatch(r"[+-]?0(?:\.0+)?", row["value"].strip()):
            zeros.append(row)
            if row["metric_name"] != "demonstration_count" or row["reporting_status"] != "source_reported":
                fail(f"{row['claim_id']}: unapproved numeric zero")
    if set(by_work) != core_ids:
        fail("data/quantitative_evidence.csv: core coverage mismatch")
    for work_id, work_rows in by_work.items():
        standard = [row["metric_name"] for row in work_rows if row["metric_name"] in STANDARD_METRICS]
        if len(standard) != 12 or set(standard) != STANDARD_METRICS:
            fail(f"{work_id}: expected exactly 12 standard metric rows")
    if len(zeros) != 19:
        fail(f"data/quantitative_evidence.csv: expected 19 explicit zeros, got {len(zeros)}")
    q336 = next(row for row in rows if row["claim_id"] == "QE-EFF-0336")
    if q336["reporting_status"] != "not_reported":
        fail("QE-EFF-0336 must be not_reported")
    q106 = next(row for row in rows if row["claim_id"] == "QE-EFF-0106")
    if q106["reporting_status"] != "not_reported":
        fail("QE-EFF-0106 must be not_reported")
    return by_work


def check_time(rows: list[dict[str, str]], quant: list[dict[str, str]], core_ids: set[str]) -> None:
    check_unique(rows, "time_id", "data/time_ontology.csv")
    if len(rows) != 88 or {row["work_id"] for row in rows} != core_ids:
        fail("data/time_ontology.csv: expected 88 atomic rows covering all 34 core works")
    eligible: set[str] = set()
    for row in rows:
        if row["reporting_status"] == "not_reported":
            if (row["duration_value"], row["duration_unit"], row["target_definition"], row["evaluator_or_checkpoint"], row["boundary_start"], row["boundary_end"]) != ("NR",) * 6:
                fail(f"{row['time_id']}: not_reported time row has non-NR boundary/value")
        else:
            if SEMANTIC_SENTINEL.search(row["duration_value"]):
                fail(f"{row['time_id']}: duration contains semantic missing sentinel")
            if row["threshold_rule_available"] != "no":
                eligible.add(row["work_id"])
                for field in ("target_definition", "evaluator_or_checkpoint", "boundary_start", "boundary_end"):
                    if SEMANTIC_SENTINEL.search(row[field]) or not row[field].strip():
                        fail(f"{row['time_id']}: target-linked row lacks {field}")
    strict_available = {
        row["work_id"] for row in quant
        if row["metric_name"] == "time_to_declared_target" and row["reporting_status"] != "not_reported"
    }
    if len(strict_available) != 14 or eligible != strict_available:
        fail(f"strict time membership mismatch: quant={sorted(strict_available)} ontology={sorted(eligible)}")


def check_lifecycle(rows: list[dict[str, str]], core_ids: set[str]) -> None:
    check_unique(rows, "lifecycle_id", "data/lifecycle_cost_grid.csv")
    if len(rows) != 272:
        fail(f"data/lifecycle_cost_grid.csv: expected 272 rows, got {len(rows)}")
    by_work: dict[str, list[str]] = defaultdict(list)
    allowed = {"source_reported", "source_reported_component", "derived_component", "proxy_only", "not_reported"}
    for row in rows:
        by_work[row["work_id"]].append(row["cost_channel"])
        if row["reporting_status"] not in allowed:
            fail(f"{row['lifecycle_id']}: invalid status")
        if row["reporting_status"] == "not_reported" and (row["value"], row["unit"], row["denominator"]) != ("NR", "NR", "NR"):
            fail(f"{row['lifecycle_id']}: not_reported requires NR triplet")
    if set(by_work) != core_ids:
        fail("data/lifecycle_cost_grid.csv: core coverage mismatch")
    for work_id, channels in by_work.items():
        if len(channels) != 8 or set(channels) != LIFECYCLE_CHANNELS:
            fail(f"{work_id}: incomplete/duplicate lifecycle grid")


def check_hardware(rows: list[dict[str, str]], core_ids: set[str]) -> None:
    check_unique(rows, "hardware_id", "data/hardware_roles.csv")
    if len(rows) != 36 or {row["work_id"] for row in rows} != core_ids:
        fail("data/hardware_roles.csv: expected 36 rows covering 34 core works")
    allowed = {"learner", "helper_reset", "fleet_collector", "evaluation_only"}
    if any(row["role"] not in allowed for row in rows):
        fail("data/hardware_roles.csv: invalid role")
    for work_id in ("hu2025robottrainsrobot", "mendonca2025continuous"):
        work_rows = [row for row in rows if row["work_id"] == work_id]
        helpers = [row for row in work_rows if row["role"] == "helper_reset" and row["count"] == "1"]
        learners = [row for row in work_rows if row["role"] == "learner" and row["count"] == "1"]
        if len(helpers) != 1 or len(learners) != 1:
            fail(f"{work_id}: must expose one learner and one helper/reset robot")
    world = [row for row in rows if row["work_id"] == "sharma2026worldgymnast"]
    if len(world) != 1 or world[0]["role"] != "evaluation_only" or world[0]["count_status"] != "not_reported" or world[0]["count"] != "NR":
        fail("World-Gymnast hardware count must be evaluation_only/NR/not_reported")


def check_tiers(rows: list[dict[str, str]], papers: dict[str, dict[str, str]]) -> None:
    check_unique(rows, "tier_rationale_id", "data/tier_rationales.csv")
    if len(rows) != 36 or {row["work_id"] for row in rows} != set(papers):
        fail("data/tier_rationales.csv: expected one row per paper")
    for row in rows:
        expected = papers[row["work_id"]]["efficiency_claim_tier"]
        if row["assigned_tier"] != expected:
            fail(f"{row['work_id']}: tier rationale mismatch")
        if row["assigned_tier"] == "E3" and row["usable_comparison"] != "yes" and row["declared_target"] != "yes":
            fail(f"{row['work_id']}: E3 requires usable comparison OR declared target")
        if row["assigned_tier"] == "E4" and row["independent_replication"] != "yes":
            fail(f"{row['work_id']}: E4 requires independent replication")


def check_zero_basis(rows: list[dict[str, str]], quant: list[dict[str, str]]) -> None:
    check_unique(rows, "zero_basis_id", "data/zero_demo_basis.csv")
    zero_q = {row["claim_id"] for row in quant if row["metric_name"] == "demonstration_count" and row["value"] == "0"}
    mapped = {row["quantitative_evidence_id"] for row in rows}
    if len(rows) != 19 or mapped != zero_q:
        fail("data/zero_demo_basis.csv: must map every and only the 19 explicit zero-demo rows")
    for row in rows:
        if row["zero_scope"] != "target-task demonstrations only":
            fail(f"{row['zero_basis_id']}: zero scope is too broad")


def check_claims(rows: list[dict[str, str]], paper_ids: set[str], core_ids: set[str]) -> None:
    check_unique(rows, "claim_id", "data/claims_ledger.csv")
    if len(rows) != 25 or {row["claim_id"] for row in rows} != {f"CL-EFF-{i:03d}" for i in range(1, 26)}:
        fail("data/claims_ledger.csv: expected CL-EFF-001..025")
    covered: set[str] = set()
    for row in rows:
        ids = set(split_ids(row["work_ids"]))
        if not ids or not ids <= paper_ids:
            fail(f"{row['claim_id']}: invalid/empty work_ids")
        covered |= ids & core_ids
        if row["confidence"] not in {"high", "moderate"} or not row["caveat"].strip():
            fail(f"{row['claim_id']}: confidence/caveat invalid")
        if re.search(r"(?i)phase\s*2", row["claim_scope"]):
            fail(f"{row['claim_id']}: public scope contains internal phase name")
    if covered != core_ids:
        fail("data/claims_ledger.csv: core coverage mismatch")
    by_id = {row["claim_id"]: row for row in rows}
    official_code = "纳入的 36 篇工作中有 16 篇定位到 official public code；其中核心工作为 15/34。"
    if official_code not in by_id["CL-EFF-018"]["claim_text"]:
        fail("CL-EFF-018: official-code population must distinguish 16/36 included from 15/34 core")
    if len(split_ids(by_id["CL-EFF-012"]["work_ids"])) != 15 or "完整的 15 篇成员" not in by_id["CL-EFF-012"]["caveat"]:
        fail("CL-EFF-012: evaluation-denominator claim must expose all 15 members")


def check_claim_evidence(
    rows: list[dict[str, str]], claims: list[dict[str, str]], quant: list[dict[str, str]],
    lifecycle: list[dict[str, str]], tiers: list[dict[str, str]], papers: list[dict[str, str]],
) -> None:
    check_unique(rows, "claim_evidence_id", "data/claim_evidence.csv")
    claim_ids = {row["claim_id"] for row in claims}
    mapped_claims = {row["claim_id"] for row in rows}
    if mapped_claims != claim_ids:
        fail(f"data/claim_evidence.csv: claim coverage mismatch missing={sorted(claim_ids-mapped_claims)}")
    valid_evidence = (
        {row["claim_id"] for row in quant}
        | {row["lifecycle_id"] for row in lifecycle}
        | {row["tier_rationale_id"] for row in tiers}
        | {f"PAPER-EFF-{row['work_id']}" for row in papers}
    )
    for row in rows:
        if row["claim_id"] not in claim_ids or row["evidence_id"] not in valid_evidence:
            fail(f"{row['claim_evidence_id']}: unresolved claim/evidence ID")
        if not row["source_locator"].strip() or not split_ids(row["member_work_ids"]):
            fail(f"{row['claim_evidence_id']}: locator/member required")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["executable_filter"] != "none":
            grouped[row["executable_filter"]].append(row)

    quant_filters = re.compile(r"^quant\.metric_name=([^ ]+) AND quant\.reporting_status=not_reported$")
    for expression, mappings in grouped.items():
        expected_values = {row["expected_count"] for row in mappings}
        if len(expected_values) != 1 or not next(iter(expected_values)).isdigit():
            fail(f"claim evidence filter {expression!r}: expected_count is inconsistent")
            continue
        expected = int(next(iter(expected_values)))
        match = quant_filters.fullmatch(expression)
        if match:
            selected = [row for row in quant if row["metric_name"] == match.group(1) and row["reporting_status"] == "not_reported"]
            if len(selected) != expected or {row["evidence_id"] for row in mappings} != {row["claim_id"] for row in selected}:
                fail(f"claim evidence filter {expression!r}: executable membership/count mismatch")
        elif expression == "lifecycle.reporting_status=not_reported":
            selected = [row for row in lifecycle if row["reporting_status"] == "not_reported"]
            if len(selected) != expected or {row["evidence_id"] for row in mappings} != {row["lifecycle_id"] for row in selected}:
                fail("lifecycle claim-evidence membership/count mismatch")
        elif expression == "papers.code_status=official_public":
            selected = [row for row in papers if row["code_status"] == "official_public"]
            if len(selected) != expected or {row["member_work_ids"] for row in mappings} != {row["work_id"] for row in selected}:
                fail("official-code claim-evidence membership/count mismatch")
        elif expression == "tier.assigned_tier=E4":
            selected = [row for row in tiers if row["assigned_tier"] == "E4"]
            if len(selected) != expected or expected != 0 or len(mappings) != 34:
                fail("E4 zero-count audit must cover all 34 nonmembers")
        else:
            fail(f"unsupported executable_filter: {expression!r}")


def parse_bib(text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    starts = list(re.finditer(r"@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,", text))
    for index, match in enumerate(starts):
        body = text[match.end(): starts[index + 1].start() if index + 1 < len(starts) else len(text)]
        fields = {}
        for field_match in re.finditer(r"(?ms)^\s*([A-Za-z]+)\s*=\s*\{(.*?)\}\s*,?\s*$", body):
            fields[field_match.group(1).lower()] = field_match.group(2).strip()
        entries[match.group(1)] = fields
    return entries


def normalize_bib(value: str) -> str:
    return re.sub(r"[{}]", "", value).strip()


def check_bibliography(papers: list[dict[str, str]]) -> None:
    entries = parse_bib(read_text("paper/references.bib"))
    paper_ids = {row["work_id"] for row in papers}
    if set(entries) != paper_ids:
        fail(f"paper/references.bib: key mismatch missing={sorted(paper_ids-set(entries))}")
    for paper in papers:
        entry = entries.get(paper["work_id"], {})
        for csv_field, bib_field in (("title", "title"), ("year", "year"), ("doi", "doi"), ("official_paper_url", "url")):
            expected = paper[csv_field].strip()
            if expected and normalize_bib(entry.get(bib_field, "")) != expected:
                fail(f"{paper['work_id']}: BibTeX {bib_field} differs from papers.csv")
    tex = read_text("paper/main.tex")
    cited: set[str] = set()
    for match in re.finditer(r"\\cite[a-zA-Z*]*\s*\{([^}]+)\}", tex):
        cited |= {item.strip() for item in match.group(1).split(",") if item.strip()}
    if cited != paper_ids:
        fail(f"paper/main.tex: citation closure mismatch missing={sorted(paper_ids-cited)} extra={sorted(cited-paper_ids)}")
    qauthors = normalize_bib(entries.get("chebotar2023qtransformer", {}).get("author", ""))
    expected_order = [
        "Chebotar, Yevgen", "Vuong, Quan", "Hausman, Karol", "Xia, Fei", "Lu, Yao",
        "Irpan, Alex", "Kumar, Aviral", "Yu, Tianhe", "Herzog, Alexander", "Pertsch, Karl",
        "Gopalakrishnan, Keerthana", "Ibarz, Julian", "Nachum, Ofir", "Sontakke, Sumedh Anand",
        "Salazar, Grecia", "Tran, Huong T.", "Peralta, Jodilyn", "Tan, Clayton",
        "Manjunath, Deeksha", "Singh, Jaspiar", "Zitkovich, Brianna", "Jackson, Tomas",
        "Rao, Kanishka", "Finn, Chelsea", "Levine, Sergey",
    ]
    if qauthors.split(" and ") != expected_order:
        fail("chebotar2023qtransformer: author order/names differ from official PMLR record")


def check_markdown_links() -> None:
    link_re = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
    for path in repository_files("*.md"):
        relative = path.relative_to(ROOT).as_posix()
        for match in link_re.finditer(read_text(relative)):
            raw = match.group(1).strip().strip("<>")
            target = raw.split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"{relative}: link escapes repository: {raw}")
                continue
            if not resolved.exists():
                fail(f"{relative}: unresolved relative link: {raw}")


def check_public_contract(tables: dict[str, list[dict[str, str]]]) -> None:
    schema = read_text("data/schema.md")
    for metric in STANDARD_METRICS:
        if f"`{metric}`" not in schema:
            fail(f"data/schema.md: missing controlled metric {metric}")
    for relative in ("README.md", "SURVEY.md", "paper/main.tex", "docs/methodology.md", "docs/validation_report.md"):
        text = read_text(relative)
        normalized = text.replace("31 July 2026", "2026-07-31")
        if "2026-07-31" not in normalized:
            fail(f"{relative}: cutoff missing")
        for token in ("424", "408", "162"):
            if token not in text:
                fail(f"{relative}: regenerated count {token} missing")
    readme = read_text("README.md")
    for phrase in ("is not zero", "evidence atlas, not a leaderboard", "overlapping diagnostic"):
        if phrase.lower() not in readme.lower():
            fail(f"README.md: required phrase missing: {phrase}")
    for relative in TABLES:
        if f"]({relative})" not in readme:
            fail(f"README.md: missing navigation link to {relative}")
    for paper in tables["data/papers.csv"]:
        if paper["official_paper_url"] and paper["official_paper_url"] not in readme:
            fail(f"README.md: work not reachable: {paper['work_id']}")
    for relative in ("README.md", "paper/main.tex", "CITATION.cff"):
        if REPOSITORY_URL not in read_text(relative):
            fail(f"{relative}: stable repository URL missing")
    corpus_text = "\n".join(read_text(path) for path in ("README.md", "SURVEY.md", "paper/main.tex", "docs/methodology.md", "docs/research_gaps.md"))
    if "23.75" in corpus_text or "22.75" in corpus_text:
        fail("public narrative must not present cross-task HIL-SERL duration sums")


def main() -> int:
    check_required_tree()
    tables = {relative: load_csv(relative, header) for relative, header in TABLES.items()}
    check_private_paths_and_locators(tables)
    papers = tables["data/papers.csv"]
    paper_ids, core_ids = check_papers(papers)
    papers_by_id = {row["work_id"]: row for row in papers}
    check_mechanisms(tables["data/mechanism_matrix.csv"], papers_by_id, core_ids)
    check_quantitative(tables["data/quantitative_evidence.csv"], core_ids)
    check_time(tables["data/time_ontology.csv"], tables["data/quantitative_evidence.csv"], core_ids)
    check_lifecycle(tables["data/lifecycle_cost_grid.csv"], core_ids)
    check_hardware(tables["data/hardware_roles.csv"], core_ids)
    check_tiers(tables["data/tier_rationales.csv"], papers_by_id)
    check_zero_basis(tables["data/zero_demo_basis.csv"], tables["data/quantitative_evidence.csv"])
    check_claims(tables["data/claims_ledger.csv"], paper_ids, core_ids)
    check_claim_evidence(
        tables["data/claim_evidence.csv"], tables["data/claims_ledger.csv"],
        tables["data/quantitative_evidence.csv"], tables["data/lifecycle_cost_grid.csv"],
        tables["data/tier_rationales.csv"], papers,
    )
    check_bibliography(papers)
    check_markdown_links()
    check_public_contract(tables)

    if ERRORS:
        print(f"FAIL: {len(ERRORS)} integrity error(s)")
        for index, message in enumerate(ERRORS, 1):
            print(f"{index:02d}. {message}")
        return 1

    quant = tables["data/quantitative_evidence.csv"]
    statuses = Counter(row["reporting_status"] for row in quant)
    print("PASS: offline repository semantic integrity checks")
    print("  required files: 27")
    print("  papers: 36 (34 core, 2 context)")
    print("  mechanisms: 25 (6 Level-1 groups)")
    print(f"  quantitative evidence: 424 ({statuses['not_reported']} NR, 19 explicit zeros)")
    print("  standard grid: 408 (34 x 12); supplemental: 16")
    print("  time ontology: 88 atomic rows; strict target time: 14 available / 20 NR")
    print("  lifecycle grid: 272 (34 x 8); hardware roles: 36")
    print("  tier rationales: 36; synthesis claims: 25; claim-evidence links: 509")
    print("  bibliography/citations and critical metadata: 36/36")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
