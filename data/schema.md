# Data schema / 数据模式

This repository publishes ten UTF-8 comma-separated tables. The auditable chain is:

```text
papers.csv
  ├─ mechanism_matrix.csv
  ├─ quantitative_evidence.csv ─ time_ontology.csv
  │                              ├─ hardware_roles.csv
  │                              └─ zero_demo_basis.csv
  ├─ tier_rationales.csv
  └─ lifecycle_cost_grid.csv
              ↓
       claims_ledger.csv ─ claim_evidence.csv
```

The canonical join key is `work_id`. Multi-valued cells use `;`. Existing IDs are stable. The literature cutoff is `2026-07-31`.

## Global controls

| Concept | Rule |
|---|---|
| Missing value | `NR` means no value was located in the verified original source. It is not zero. |
| Semantic missing value | `NR`, `... NR`, `unknown`, `not reported`, and `unavailable` may not appear in a nonmissing value/unit/denominator. Partial reporting belongs in atomic rows or `partial_scope`. |
| Explicit zero | Numeric `0` is permitted only with an original-source basis and a row in `zero_demo_basis.csv`. |
| Approximation | Preserve `about`, `approximately`, ranges, and bounds; use `source_reported_approximate`. |
| Derived value | Reviewer arithmetic uses `derived`, names its operands, and never implies author reporting. |
| Units | Steps, episodes, trials, elapsed hours, interaction hours, aggregate robot-hours, and compute-hours are distinct. |
| Locator | A numerical or missingness row needs an original page/table/figure/section locator. Internal paths and unpublished evidence-card paths are forbidden. |
| Evidence boundary | Context works define measurement; they do not establish physical-robot effectiveness. |
| Diagnostic coordinates | Resource-vector coordinates can overlap. They may not be summed without an inclusion matrix and explicit weights. |

## Evidence tiers

### Physical-robot tier (`real_robot_tier`)

| Tier | Meaning |
|---|---|
| `R0` | Context/definition source; no physical effectiveness attribution. |
| `R1` | Limited physical illustration without sufficient task-level evidence. |
| `R2` | Physical evaluation of a learned policy, but not a strong online/autonomous training demonstration. |
| `R3` | Direct physical training, adaptation, or task-level learning with a located cost claim. |
| `R4` | Extended autonomous, continuous, reset-reduced, or fleet-scale physical operation. |

### Frozen efficiency decision table (`efficiency_claim_tier`)

The tier is an evidence-strength label, not an algorithm score. Apply the first row whose requirements are satisfied after considering the caps below.

| Tier | Positive requirement | Typical cap / reason |
|---|---|---|
| `E0` | Context only; no core physical cost effect. | Context cannot enter physical quantitative ranking. |
| `E1` | A physical result with qualitative, incomplete, or single-setting cost evidence. | No usable comparison/declared target, or a single run with severe denominator/boundary gaps. |
| `E2` | A located quantitative physical cost. | Important target, comparison, repeat, task-scope, or lifecycle-boundary gaps prevent E3. |
| `E3` | Task-level quantitative evidence **and** (`usable_comparison=yes` **or** `declared_target=yes`). | Still not independent replication; missing lifecycle channels remain explicit. |
| `E4` | E3 plus an independent team physically reproduces the cost result under a matched task, target, and accounting boundary. | `independent_replication=yes` is mandatory. No work in this snapshot is E4. |

Operational tie-breaks:

1. A matched same-study comparison can satisfy E3 without strict time-to-target; a declared target can satisfy E3 without a baseline.
2. A duration alone is not a declared target. Fixed run, collection-program, or model-training duration remains phase evidence.
3. A single successful run, plot-only endpoint, missing evaluation denominator, or only simulation-side ablation can lower a record to E1/E2.
4. Lifecycle incompleteness does not automatically prohibit E3, but must remain in the rationale and prevents an end-to-end-cost claim.
5. Every assignment is recorded in `tier_rationales.csv`; the validator enforces the E3 and E4 minimum conditions.

### Source grade

| Grade | Meaning |
|---|---|
| `A` | Verified original paper/proceedings/publisher source. |
| `B` | Verified original preprint or similarly authoritative source that was not peer reviewed at the cutoff. |

## `papers.csv`

One canonical row per included work: 36 rows, comprising 34 `included_core` and two `included_context` records. Metadata, platform, task, source locator, performance, extracted resources, and limitations are retained. Important time/hardware fields have these public semantics:

| Field | Definition |
|---|---|
| `work_id` | Stable ASCII key and BibTeX key. |
| `reported_phase_duration` | Raw source-reported duration summary. It may describe a run, task, data collection, model training, adaptation, or program. It is **not** automatically time-to-target. |
| `robot_hours` | Aggregate active/collection robot-hours, not inferred from elapsed time. |
| `wall_clock_hours` | Elapsed duration, not inferred from robot-hours. |
| `num_parallel_robots` | Primary learner/data-fleet count only; helpers and evaluation-only hardware are normalized in `hardware_roles.csv`. |
| `evidence_locator` | Original-source page/table/figure/section pointer. |
| `efficiency_claim_tier` | Frozen E0–E4 outcome with a matching rationale row. |

Other fields retain their literal CSV names: canonical title/year/venue/DOI/arXiv/official links; screening and R/topic tiers; robot/task/training descriptions; success definition/result and trials; steps/episodes/control rate/compute/demonstrations; reset, reward, prior-data, wear/safety and displaced-cost descriptions; verification grade and limitations.

## `mechanism_matrix.csv`

One row per Level-3 mechanism (`EFF-M01`–`EFF-M25`). `work_ids` is the supporting core set. `physical_evidence_tiers` is the exact `work_id:R*/E*` mapping. A work may support several mechanisms.

## `quantitative_evidence.csv`

There are **424 rows**: **408 standard rows** (`34 × 12`) plus 16 supplemental quantities. Each standard work has exactly these controlled `metric_name` values:

1. `reported_phase_duration`
2. `time_to_declared_target`
3. `physical_steps_or_transitions`
4. `physical_episodes_or_rollouts`
5. `control_frequency`
6. `active_or_aggregate_robot_hours`
7. `elapsed_wall_clock`
8. `primary_data_robot_count`
9. `reported_compute_resource_or_duration`
10. `demonstration_count`
11. `evaluation_trial_count`
12. `reported_success_result`

`reported_phase_duration` is a summary index; the atomic values and phase/task boundaries are in `time_ontology.csv`. `time_to_declared_target` is available only if the target, evaluator/checkpoint, named phase/task, and start/end boundary are identifiable. This corpus uses a source-declared-target rule; availability does not imply preregistration.

| Field | Definition |
|---|---|
| `claim_id` | Stable quantitative ID `QE-EFF-0001`–`QE-EFF-0424`. |
| `metric_family`, `metric_name` | Controlled resource family and quantity. |
| `value`, `unit`, `denominator` | Source-compatible value or the strict `NR/NR/NR` missing triplet. |
| `comparison_baseline` | Same-study comparator or `NR`. |
| `physical_platform` | Physical system boundary. |
| `evidence_locator` | Exact original-source locator; unpublished path references are forbidden. |
| `reporting_status` | `source_reported`, `source_reported_approximate`, `derived`, `mixed_or_ambiguous`, or `not_reported`. |
| `interpretation_limit` | Scope, partial coverage, ambiguity, or non-comparability warning. |

## `time_ontology.csv`

Eighty-eight atomic source statements separate `target_online_learning`, `target_adaptation`, `physical_run`, `upstream_data_collection`, `model_training`, `evaluation`, and `program_total`. Each row names:

- `task_scope` and `clock_basis` (`elapsed_wall_clock`, `physical_interaction_time`, `aggregate_robot_hours`, or `compute_wall_clock`);
- one `duration_value`/`duration_unit`;
- `target_definition`, `threshold_rule_available`, and `evaluator_or_checkpoint`;
- `boundary_start`, `boundary_end`, and `partial_scope`.

Rows with `threshold_rule_available != no` determine the 14/34 strict target-time availability set. Run/data/model/program durations cannot enter that set only because they are numeric.

## `hardware_roles.csv`

Thirty-six rows distinguish `learner`, `helper_reset`, `fleet_collector`, and `evaluation_only`. `count_status=not_reported` requires numeric count `NR`. Robot Trains Robot and the mobile-manipulation system each expose one learner plus one helper/reset robot; World-Gymnast's nonnumeric hardware wording remains `NR`.

## `lifecycle_cost_grid.csv`

The complete **272-row (`34 × 8`)** grid contains:

- `active_human_time`
- `standby_monitoring_time`
- `reset_recovery_cost`
- `engineering_setup_time`
- `safety_exposure`
- `wear_maintenance_downtime`
- `failed_development_runs`
- `prior_data_cost`

Statuses distinguish `source_reported`, `source_reported_component`, `derived_component`, `proxy_only`, and `not_reported`. A component/proxy is not a full channel total. The current grid has 230 `not_reported` cells, 35 source-located quantitative components, and seven qualitative/incomplete proxies; it does not justify a scalar lifecycle total.

## `tier_rationales.csv`

One row per included work records the assigned E tier, frozen decision rule, evidence IDs, comparison/target flags, denominator and lifecycle quality, independent-replication status, adjudication, rationale, and original locator.

## `zero_demo_basis.csv`

One row per numeric zero in `demonstration_count` (19 rows). `zero_scope` is `target-task demonstrations only`; upstream simulation, autonomous data, prior controllers, reset demonstrations, engineering, and labor remain separately reported or unknown.

## `claims_ledger.csv` and `claim_evidence.csv`

`claims_ledger.csv` contains 25 bounded synthesis statements (`CL-EFF-001`–`CL-EFF-025`) with mandatory scope, confidence, caveat, and full supporting membership.

`claim_evidence.csv` makes the next hop explicit:

```text
CL-EFF-* → QE-EFF-* / LC-EFF-* / TR-EFF-* / PAPER-EFF-* → original locator
```

Count claims carry a controlled `executable_filter`, frozen `expected_count`, and complete row/work membership. The validator recomputes each supported filter from the public CSVs; a representative subset is not permitted.

## Update invariants

1. Add a work only after original full-text physical-evidence screening and metadata verification.
2. Keep `work_id` and all existing row IDs stable.
3. Keep phase/task durations atomic; never promote a run/program/compute span into target time without target/evaluator/boundaries.
4. Keep helper/fleet/evaluation hardware roles explicit.
5. Keep every missing standard quantity as `NR/NR/NR + not_reported`; never hide a semantic sentinel inside free text.
6. Add an original-source locator for every quantitative, time, lifecycle, tier, zero, and claim-evidence row.
7. Update executable claim membership and narrative counts from the data, not by hand.
8. Run `make validate`, `python3 scripts/test_validator.py`, and a clean paper build before release.
