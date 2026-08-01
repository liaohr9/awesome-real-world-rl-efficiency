# Review methodology

## 1. Review question and frozen scope

This repository is a systematic evidence map/scoping survey of:

> What does available physical-robot evidence show about the resources required to train or adapt reinforcement-learning policies to a verified task-performance target under a full-cost accounting boundary?

The search and inclusion cutoff is **2026-07-31**. The corpus is frozen at 36 works: 34 core empirical studies and 2 context/measurement sources. The repository does not claim exhaustive database coverage; it reports an evidence-checked corpus assembled through the documented public routes available during the review.

The unit of inclusion is the canonical paper family, not every preprint/conference/journal version. The stable `work_id` joins the bibliography and all data tables.

## 2. Eligibility boundary

### Core inclusion

A core record had to satisfy all of the following:

1. original technical research;
2. accessible full paper;
3. at least one physical-robot task experiment;
4. reinforcement learning, or an RL-enabling mechanism, central to the task-learning system;
5. direct measurement, change, or target involving at least one burden: physical interaction, robot-hours, wall-clock, compute, fleet, reset, human input, reward engineering, prior data, safety, or wear.

A physical-robot solution could remain included even when particular cost fields were `NR`. Inclusion says the method addresses the bottleneck; it does not say its entire lifecycle cost was reported.

### Context inclusion

Context records may define real-world RL constraints, benchmarks, or measurement concepts without physical training evidence. They receive `R0/E0`, are excluded from quantitative physical ledgers, and cannot support effectiveness or reliability conclusions.

### Exclusion codes

| Code | Reason |
|---|---|
| `EX1` | Simulation-only, without physical-robot task evaluation. |
| `EX2` | No reward/return-driven learning and no RL-enabling mechanism. |
| `EX3` | Perception, planning, or language only, without task-level policy learning. |
| `EX4` | Inference or hardware benchmark only. |
| `EX5` | Full text or claimed physical experiment could not be verified. |
| `EX6` | Non-technical or secondary-only record. |
| `EX7` | Duplicate/version of a retained canonical family. |
| `EX8` | Published after the cutoff. |
| `EX9` | Component metric could not be linked to robot task performance. |

## 3. Search strategy

The core concept blocks were:

```text
(robot* OR manipulation OR locomotion OR navigation OR quadruped
 OR humanoid OR aerial OR drone OR soft-robot)
AND
("reinforcement learning" OR "actor critic" OR "policy optimization"
 OR "offline RL" OR "model-based RL")
AND
("real robot" OR "physical robot" OR "real-world" OR on-robot
 OR "hardware experiment")
```

An efficiency supplement added:

```text
(robot* AND ("reinforcement learning" OR "offline RL"))
AND
("sample efficient" OR "data efficient" OR "robot hours" OR wall-clock
 OR "training time" OR "time to threshold" OR "online learning"
 OR "few trials" OR "rapid adaptation" OR "world model")
```

The cost block was not mandatory in the core query. This avoids omitting papers that contain resource measurements but do not advertise “sample efficiency” in the title or abstract.

Discovery and verification routes included arXiv, PMLR, OpenReview, RSS and other official proceedings/publisher pages, DOI/Crossref metadata, official author/lab project pages, official repositories, and backward/forward chaining from verified anchors. Public web search supported discovery, never final numerical extraction.

Scopus and Web of Science were treated as additive databases but were not searched because authenticated access was not available in the review run. Search result totals were not exposed by the public search interface, so those counts remain `NR`; the review does not manufacture a PRISMA-style database-hit total.

## 4. Screening flow

The screening inventory contains 73 canonical candidates:

| Decision at cutoff | Count |
|---|---:|
| Included core | 34 |
| Included context | 2 |
| Terminal full-text exclusion | 5 |
| Pending full text | 31 |
| Pending title/abstract | 1 |
| **Total** | **73** |

The 32 pending candidates are future expansion leads, not evidence. They are not used to raise coverage counts or support synthesis claims.

The five terminal exclusions comprised a reset-related paper without retained efficiency evidence, an earlier world-model paper superseded by the canonical included family for this question, a non-RL foundation-policy route, and two simulation-only/offline algorithm papers. Version/identity conflicts were resolved at the canonical-family level.

Screening proceeded as:

1. capture discovery route and temporary ID;
2. deduplicate by DOI, arXiv/OpenReview/PMLR identity, and title;
3. model-assisted title/abstract decision;
4. full-text or authoritative-original check;
5. physical-robot evidence check;
6. burden-mechanism and exact-locator check;
7. official code/project check;
8. root-level consistency verification;
9. retain both the initial and verification decisions in the internal audit trail.

This was **not independent dual screening**. The root verification was a managed consistency/error-detection layer in the same model-assisted workflow. That limits conventional inter-rater reliability claims.

## 5. Full-text extraction

Each core paper received structured extraction for:

- transitions, episodes, trials, control rate, and active robot-hours;
- reported run/data/model/program duration, elapsed wall-clock, and separately qualified time-to-declared-target;
- fleet size, summed robot-hours, and overlap between collection and learning;
- learner/world-model compute;
- demonstrations, intervention, reset, supervision, reward labels, and engineering labor;
- reset/recovery mechanisms and fixtures;
- prior robot data, simulation, foundation/world models, pretrained representations, and controllers;
- wear, collision, emergency-stop, breakage, consumable, and maintenance evidence;
- success definition, result, denominator, and exact locator.

Every numerical extraction had to retain a page, table, figure, section, or appendix locator in [`quantitative_evidence.csv`](../data/quantitative_evidence.csv). Abstracts and project pages could establish candidacy or public-link status but could not establish a final quantitative value.

## 6. Evidence grading

Three orthogonal labels are retained:

- `R*`: physical deployment/training evidence;
- `E*`: strength of the cost claim;
- `source_grade`: authority/status of the verified source.

They are intentionally not collapsed. An R4 system may demonstrate long autonomous operation while giving incomplete sample or lifecycle accounting. An E3 paper may make a strong task-specific efficiency claim without independent replication. Source grade and peer-review status do not replace either dimension.

The snapshot contains:

| Dimension | Distribution |
|---|---|
| Physical tier | R4: 6; R3: 23; R2: 5; R0 context: 2 |
| Efficiency tier | E3: 13; E2: 14; E1: 7; E0 context: 2 |
| E4 replication | 0 |
| Official public code among core works | 15/34 |

Code availability records a verified official repository at the check date. It is not independent physical reproduction.

## 7. Data transformation and synthesis

The public evidence chain has ten tables. Four establish the core corpus and synthesis (`papers`, `mechanism_matrix`, `quantitative_evidence`, and `claims_ledger`). Six make previously implicit judgments executable:

- [`time_ontology.csv`](../data/time_ontology.csv): 88 atomic task/phase durations and boundary audits;
- [`claim_evidence.csv`](../data/claim_evidence.csv): 509 typed claim-to-row-to-locator links;
- [`tier_rationales.csv`](../data/tier_rationales.csv): one frozen E-tier rationale for each of 36 included works;
- [`lifecycle_cost_grid.csv`](../data/lifecycle_cost_grid.csv): the full 272-row (`34 × 8`) cost-channel grid;
- [`hardware_roles.csv`](../data/hardware_roles.csv): 36 learner/helper/fleet/evaluation role rows;
- [`zero_demo_basis.csv`](../data/zero_demo_basis.csv): source basis and scope for all 19 explicit zero-demo rows.

Mechanisms are many-to-many. A system using replay, demonstrations, a learned reward, and a reset fixture contributes to several nodes. Resource coordinates are also overlapping diagnostic views: aggregate active robot-hours can already include reset/recovery. The review never sums them without an explicit inclusion matrix and weights.

Every one of the 25 synthesis claims maps through `claim_evidence.csv` to a quantitative, lifecycle, tier, or canonical-paper row and an original locator. Corpus counts use executable filters with complete membership; representative examples cannot support a full-corpus count.

## 8. Quantitative ledger and time ontology

Each of 34 core works has 12 standard rows: `reported_phase_duration`, strict `time_to_declared_target`, physical steps, episodes, control frequency, robot-hours, wall-clock, primary data-robot count, compute, demonstrations, evaluation trials, and success result. This gives **408 standard rows**; 16 supplemental resource/event quantities bring the total to **424**.

The two time fields have different semantics:

- `reported_phase_duration` asks whether the source reports a duration for a named run, data collection, model training, target online phase, evaluation, adaptation, or program. It is available for 27/34 works.
- `time_to_declared_target` asks whether that duration is linked to a source-declared target, an identifiable evaluator/checkpoint, a named task/phase, and start/end boundaries. It is available for 14/34 works and `NR` for 20/34. Availability does not imply preregistration.

Different tasks/phases are not summed. For example, the 12 HIL-SERL policy durations are retained as 12 atomic Table-1 rows; their heterogeneous durations are not published as a study-wide total. Model-training time in World-Gymnast, 30 hours of PlayWorld collection, and MT-Opt's 16-month program span remain correctly typed durations but do not become physical target time.

Reporting status is `source_reported`, `source_reported_approximate`, `derived`, `mixed_or_ambiguous`, or `not_reported`. Current quantitative counts are 172, 70, 17, 3, and **162**, respectively. Every missing standard row uses the exact `NR/NR/NR` triplet. The validator also rejects semantic sentinels such as `program wall-clock NR` inside a nonmissing row.

Nineteen numeric zeros remain because original sources explicitly report zero **target-task demonstrations**. Their scope/basis table prevents that zero from implying no simulation, autonomous data, reset demonstrations, prior controller, engineering, or labor.

## 9. Missingness, lifecycle, and non-comparability audit

Structured missingness among the 34 core works is generated from rows:

| Field | `NR` | Available |
|---|---:|---:|
| Reported phase duration | 7 | 27 |
| Strict time-to-declared-target | 20 | 14 |
| Physical steps/transitions | 22 | 12 |
| Episodes/rollouts | 19 | 15 |
| Robot-hours | 16 | 18 |
| Wall-clock | 8 | 26 |
| Compute | 21 | 13 |
| Evaluation-trial denominator | 15 | 19 |
| Control frequency | 30 | 4 |

The lifecycle grid audits active human time, standby monitoring, reset/recovery, engineering setup, safety exposure, wear/maintenance downtime, failed development runs, and prior-data cost for every core work. Of 272 cells, 230 are `not_reported`, 35 contain a source-located quantitative component, and seven are qualitative/incomplete proxies. No row set supports a full scalar lifecycle total.

Hardware accounting separates primary learner/data actors from helper/reset robots, fleet collectors, and evaluation-only hardware. Robot Trains Robot and the mobile-manipulation system therefore expose the second helper robot rather than hiding it behind a learner count of one; World-Gymnast's nonnumeric hardware description remains `NR`.

Availability still does not imply comparability. Tasks, clocks, targets, episodes, reset boundaries, assets, and repeats differ. The review therefore does not compute a pooled effect size or rank algorithms globally.

## 10. Identity and source integrity

Canonical identity was checked using DOI, venue, arXiv/OpenReview/PMLR identifiers, and title. Particular care was required for similarly named or misfiled records. The public projection retains only the corrected canonical identities and official links.

The bibliography contains exactly the 36 verified included keys. It was promoted from the verified source set without inventing entries. Local source files, acquisition paths, manifests, and internal verification notes are deliberately absent from this public repository.

## 11. Known limitations

- Public-route discovery may miss records indexed only in inaccessible databases or described with unusual terminology.
- The corpus is manipulation-heavy and concentrated after 2018.
- Model-assisted screening plus root verification is not independent dual review.
- Successful published systems create publication and survivorship bias; failed development runs are rarely available.
- Five core works were preprints at the cutoff; future versions may change metadata or evidence.
- Cross-paper tasks, success thresholds, resets, frequencies, prior assets, and cost boundaries are heterogeneous.
- Missing displaced costs can be named as channels but not estimated.
- Official links and repository status can change after their verification date.

## 12. Reproduction

Run the deterministic repository audit:

```bash
make validate
python3 scripts/test_validator.py
```

Build the standalone survey:

```bash
make paper
make clean
```

The offline validator checks schemas, row widths, stable IDs, semantic missing sentinels, atomic target-time boundaries, executable claim membership, lifecycle completeness, E3/E4 decision minima, hardware roles, zero scope, metadata/BibTeX parity, citations, links, release URL, and forbidden public artifacts. The companion test mutates six protected invariants and requires every corrupted copy to fail. Online URL availability is intentionally excluded from this deterministic gate.
