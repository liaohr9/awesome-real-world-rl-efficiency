# Validation report

## Scope

This report covers the public repository snapshot with literature cutoff `2026-07-31` and release audit date `2026-08-01`. Validation has three layers: deterministic semantic integrity, negative mutation tests, and a clean standalone LaTeX build. Online link health is intentionally excluded from the offline gate.

## Frozen inventory

| Artifact | Expected |
|---|---:|
| Included works | 36 (34 core, 2 context) |
| Level-1 / Level-3 mechanisms | 6 / 25 |
| Quantitative evidence | 424 (408 standard + 16 supplemental) |
| Quantitative status | 172 reported; 70 approximate; 17 derived; 3 ambiguous; 162 `not_reported` |
| Atomic time ontology | 88 rows; strict target time 14 available / 20 `NR` |
| Lifecycle grid | 272 (`34 × 8`): 230 `NR`, 35 quantitative components, 7 proxies |
| Hardware roles | 36 rows |
| Tier rationales | 36 rows; E4 = 0 |
| Explicit-zero bases | 19 rows |
| Synthesis claims / evidence links | 25 / 509 |
| BibTeX entries and LaTeX citation closure | 36 / 36 |
| Required public files | 27 |

## Semantic checks

The offline validator checks:

- fixed headers, widths, unique stable IDs, 34-core/2-context split, and complete joins;
- exactly 12 standard metric rows for every core work;
- strict `NR/NR/NR + not_reported`, plus rejection of semantic sentinels such as `program wall-clock NR` in nonmissing values;
- 88 atomic time rows and exact equality between target-qualified ontology membership and the 14-work strict target-time set;
- the complete 34×8 lifecycle grid and controlled component/proxy statuses;
- learner, helper/reset, fleet-collector, and evaluation-only hardware roles, including the two helper-robot cases and World-Gymnast's numeric `NR`;
- frozen E-tier parity, E3's `comparison OR declared target` minimum, and E4's independent-replication requirement;
- exact mapping of all 19 zero-demo values to source basis, target-task scope, and upstream-data warning;
- every claim resolving to typed evidence and an original locator; count claims are recomputed from executable filters and complete membership;
- no internal `evidence_cards/`, source, work, or local absolute paths in public locators;
- canonical Robot Trains Robot CoRL URL, Q-Transformer official PMLR author order, paper/BibTeX title/year/DOI/URL parity, and 36/36 citation closure;
- Markdown links, official URL syntax, stable repository URL, corpus notices, and absence of build/cache artifacts.

## Negative mutation tests

`scripts/test_validator.py` copies the repository to an isolated temporary directory and verifies rejection of six corruptions:

1. semantic missing sentinel in a nonmissing quantitative row;
2. unresolved internal locator path;
3. E3 without comparison or declared target;
4. E4 without independent replication;
5. World-Gymnast's qualitative hardware wording promoted to a reported count;
6. unresolved claim-evidence ID.

Result: **PASS, 6/6 corruptions rejected**.

## Results

### Offline repository validator

Result: **PASS**.

```text
PASS: offline repository semantic integrity checks
  required files: 27
  papers: 36 (34 core, 2 context)
  mechanisms: 25 (6 Level-1 groups)
  quantitative evidence: 424 (162 NR, 19 explicit zeros)
  standard grid: 408 (34 x 12); supplemental: 16
  time ontology: 88 atomic rows; strict target time: 14 available / 20 NR
  lifecycle grid: 272 (34 x 8); hardware roles: 36
  tier rationales: 36; synthesis claims: 25; claim-evidence links: 509
  bibliography/citations and critical metadata: 36/36
```

### LaTeX and clean-tree gate

- A clean `make paper` build passed with TeX Live 2025 and `latexmk` 4.86a: 15 pages, 428,319 bytes, PDF 1.7.
- The final log contains no undefined citations, undefined references, or overfull boxes. BibTeX emits five expected empty-`journal` warnings for preprints; each entry retains its authoritative URL and publication type.
- `make clean` removes the PDF and every TeX intermediate; the semantic validator and all six negative mutations pass again after cleaning.
- No generated PDF is retained in the source deliverable.

## Interpretation limits

- Internal consistency cannot prove that an external URL stays live or that every extraction is independently correct.
- Source grades and exact locators enable audit; they are not independent physical replication.
- Strict target-time availability means source-declared target plus evaluator/checkpoint and boundaries, not preregistration.
- Lifecycle component/proxy coverage is not a full scalar cost.
- `NR` is not zero, context sources do not establish physical reliability, and the corpus does not support a universal ranking.
