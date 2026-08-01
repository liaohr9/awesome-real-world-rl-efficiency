#!/usr/bin/env python3
"""Negative mutation tests for semantic validator invariants."""

from __future__ import annotations

import csv
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def mutate_csv(path: Path, predicate, updates: dict[str, str]) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    changed = 0
    for row in rows:
        if predicate(row):
            row.update(updates)
            changed += 1
            break
    if changed != 1:
        raise AssertionError(f"mutation target not unique/found in {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "scripts/validate.py"],
        cwd=root,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def expect_rejected(name: str, mutation) -> None:
    with tempfile.TemporaryDirectory(prefix="efficiency-validator-") as temp:
        copy = Path(temp) / "repository"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
        mutation(copy)
        result = run_validator(copy)
        if result.returncode == 0:
            raise AssertionError(f"negative case passed unexpectedly: {name}")
        print(f"PASS negative: {name}")


def expect_git_metadata_ignored() -> None:
    with tempfile.TemporaryDirectory(prefix="efficiency-validator-git-") as temp:
        copy = Path(temp) / "repository"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
        fixture = copy / ".git/objects/aa/fixture"
        fixture.parent.mkdir(parents=True)
        fixture.write_bytes(b"\x00\xff\x80synthetic-git-object")
        result = run_validator(copy)
        if result.returncode != 0:
            print(result.stdout)
            raise AssertionError("validator must ignore Git metadata")
        print("PASS positive: Git metadata ignored")


def main() -> int:
    baseline = run_validator(ROOT)
    if baseline.returncode != 0:
        print(baseline.stdout)
        raise AssertionError("baseline validator must pass before negative tests")

    expect_git_metadata_ignored()

    expect_rejected(
        "semantic missing sentinel",
        lambda root: mutate_csv(
            root / "data/quantitative_evidence.csv",
            lambda row: row["claim_id"] == "QE-EFF-0001",
            {"value": "duration NR", "reporting_status": "source_reported"},
        ),
    )
    expect_rejected(
        "unresolved locator path",
        lambda root: mutate_csv(
            root / "data/quantitative_evidence.csv",
            lambda row: row["claim_id"] == "QE-EFF-0001",
            {"evidence_locator": "evidence_cards/internal.md"},
        ),
    )
    expect_rejected(
        "E3 without comparison or target",
        lambda root: mutate_csv(
            root / "data/tier_rationales.csv",
            lambda row: row["assigned_tier"] == "E3",
            {"usable_comparison": "no", "declared_target": "no"},
        ),
    )
    expect_rejected(
        "E4 without independent replication",
        lambda root: mutate_csv(
            root / "data/tier_rationales.csv",
            lambda row: row["work_id"] == "luo2024serl",
            {"assigned_tier": "E4", "independent_replication": "no"},
        ),
    )
    expect_rejected(
        "World-Gymnast nonnumeric actor count",
        lambda root: mutate_csv(
            root / "data/hardware_roles.csv",
            lambda row: row["work_id"] == "sharma2026worldgymnast",
            {"count": "real evaluation hardware", "count_status": "source_reported"},
        ),
    )
    expect_rejected(
        "unresolved claim evidence ID",
        lambda root: mutate_csv(
            root / "data/claim_evidence.csv",
            lambda row: row["claim_evidence_id"] == "CE-EFF-0001",
            {"evidence_id": "QE-EFF-9999"},
        ),
    )
    print("PASS: 6/6 semantic negative mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
