# Contributing

Contributions are welcome when they improve the evidence trail rather than only lengthening the paper list.

## Before opening a change

Confirm that the candidate:

1. was public by the current literature cutoff or is part of an explicitly proposed cutoff update;
2. is original technical research with an accessible full paper;
3. contains a physical-robot task experiment for a core record;
4. uses RL or an RL-enabling mechanism centrally;
5. measures or changes at least one resource in the sample/time lifecycle.

Simulation-only, benchmark/context, or measurement papers may be proposed as context, but they must be labeled `R0/E0` and cannot support physical effectiveness.

## Required evidence for a paper addition

Provide:

- canonical title, authorship identity, year, venue, DOI/arXiv/OpenReview/PMLR identifier, and official paper URL;
- stable proposed `work_id`;
- physical robot, task, success definition, result, and trial denominator;
- exact page/table/figure/section locators for every numerical value;
- physical interaction, robot-hours, wall-clock, parallelism, compute, demonstrations, human input, reset/recovery, prior assets, safety/wear, and engineering fields;
- `NR` for values not located in the source;
- an R tier, E tier, source grade, and explicit limitations;
- official project/code links only when their relationship to the paper is verified;
- displaced-cost channels and assumptions.

Do not infer zero from silence. Do not convert steps to time without frequency, action repeat, pauses, and reset boundaries. Do not equate code availability with physical reproduction.

## Files to update

A new core paper normally requires coordinated edits to:

- `data/papers.csv`;
- `paper/references.bib`;
- `data/quantitative_evidence.csv` (the 12 standard rows plus justified supplemental rows);
- `data/time_ontology.csv` (one atomic task/phase statement per duration; never join distinct clocks);
- `data/hardware_roles.csv` and `data/lifecycle_cost_grid.csv`;
- `data/tier_rationales.csv` and `data/zero_demo_basis.csv`;
- `data/mechanism_matrix.csv`;
- `data/claims_ledger.csv` and `data/claim_evidence.csv` if any synthesis/count boundary changes;
- `README.md`, `SURVEY.md`, and `paper/main.tex`;
- `docs/methodology.md` and `docs/validation_report.md` counts.

Existing IDs must remain stable. Multi-valued cells use semicolons.

## Claim changes

Narrative claims must remain inside the wording, scope, confidence, and caveat in `data/claims_ledger.csv`. If new evidence justifies a stronger claim, change the ledger first and explain:

- the new supporting work IDs;
- the population/accounting boundary;
- whether the evidence is source-reported, derived, or a missingness audit;
- why the previous caveat changes.

This repository does not accept universal rankings or pooled effect sizes unless all comparison gates are genuinely matched.

## Local checks

```bash
make validate
python3 scripts/test_validator.py
make paper
make clean
make validate
```

The final tree must contain no downloaded paper PDF, private/local acquisition path, LaTeX build product, cache, or editor temporary file.

## Pull-request summary

State:

- exactly which works, mechanisms, quantities, and claims changed;
- original-source locators checked;
- whether any existing value or ID changed;
- validator result and LaTeX page count;
- unresolved metadata, evidence, or link concerns.
