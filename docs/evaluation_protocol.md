# Evaluation protocol for real-world RL efficiency

## 1. Goal

This protocol evaluates whether a method reduces a physical-robot learning burden, where that burden moves, and under what operational conditions the result holds. It is prospective: authors should freeze the accounting boundary, target, and event vocabulary before training.

A single sample count is insufficient. Report a resource vector:

```text
C = (
  physical transitions and trials,
  aggregate active robot-hours,
  elapsed wall-clock,
  operator active and standby time,
  reset/recovery/maintenance time,
  demonstrations and prior physical data,
  compute and energy,
  parallel hardware and fixtures,
  engineering labor,
  safety and wear events
)
```

These coordinates are overlapping diagnostic views: aggregate active robot-hours can already contain reset/recovery action time. Do not add them until an inclusion matrix removes overlap; do not collapse the resulting vector into a scalar unless weights and the intended decision context are declared. This implements [CL-EFF-001](../data/claims_ledger.csv).

## 2. Freeze two accounting boundaries

Every result should publish both:

1. **Target-task marginal ledger** — resources newly consumed after all prior assets already exist.
2. **Full lifecycle ledger** — marginal resources plus a declared allocation of upstream data, simulation, model/controller/reward engineering, hardware, and evaluation.

Record:

| Boundary field | Required definition |
|---|---|
| `study_start` | Start of task-specific preparation counted in the study. |
| `online_start` | First physical transition used by the target online learner. |
| `threshold_time` | First frozen evaluation checkpoint that reaches the declared target. |
| `study_end` | End of the last included evaluation/operation. |
| `development_runs_included` | Whether pilots, failed seeds, reward/reset tuning, and aborted runs are counted. |
| `prior_assets_cutoff` | Datasets, simulation, policies, representations, world models, controllers, fixtures, and task graphs inherited by the target task. |
| `amortization_rule` | Allocation of one-time resources across tasks, robots, sites, or expected deployments. |

If a quantity is unknown, record `NR`; do not assign zero. If a cost is shared, publish both the unallocated total and the allocation rule.

## 3. Freeze task and success semantics

At minimum publish:

- robot model and anonymized hardware instance;
- observation and action spaces;
- control interface, frequency, action repeat, and pauses;
- initial-state distribution and object replenishment;
- success set and tolerance;
- failure and safety sets;
- horizon, timeout, and continuing-task boundary;
- evaluation initial-state generator;
- target threshold `tau`;
- number of evaluation trials and independence unit;
- evaluation cadence and checkpoint-selection rule;
- confidence interval and right-censoring rule.

Define time-to-threshold as:

```text
T_tau = first preregistered evaluation checkpoint
        whose frozen evaluator reaches threshold tau
```

For retrospective literature extraction, this repository uses a slightly weaker but explicit `time_to_declared_target`: source-declared target, identifiable evaluator/checkpoint, named task/phase, and start/end boundary. Only 14/34 core works meet that rule; 20/34 are `NR`. A reported run, data-collection, model-training, or program duration is preserved separately and never promoted to target time by being numeric ([CL-EFF-025](../data/claims_ledger.csv)).

A final success rate without its trial denominator is not sufficient for precise cross-paper comparison. Fifteen of 34 core studies in this snapshot lack a clear denominator ([CL-EFF-012](../data/claims_ledger.csv)).

## 4. Physical interaction ledger

Report per robot, per task, per seed, and in aggregate:

| Field | Unit | Rule |
|---|---:|---|
| `physical_transitions` | transitions | Count physical control decisions; report action repeat separately. |
| `physical_episodes` | episodes | Use the frozen episode boundary; use `NA` only for a genuinely continuing task. |
| `physical_trials` | trials | State whether retries share the same initial condition. |
| `active_task_seconds` | seconds | Robot executing the target task. |
| `active_reset_seconds` | seconds | Robot executing exact/functional/pseudo reset actions. |
| `active_recovery_seconds` | seconds | Robot executing recovery after a failure state. |
| `evaluation_transitions` | transitions | Physical interaction used for model selection/final evaluation. |
| `development_transitions` | transitions | Reward, detector, hyperparameter, fixture, safety, or recovery development. |
| `learner_robot_count(t)` | robots | Primary physical learner count. |
| `helper_reset_robot_count(t)` | robots | Teacher/helper hardware used for reset or recovery. |
| `fleet_collection_count(t)` | robots | Physical actors collecting data in parallel. |
| `evaluation_robot_count` | robots | Evaluation-only hardware; never infer a count from qualitative platform wording. |

Aggregate robot time:

```text
H_robot_aggregate = sum_r active_robot_seconds(r) / 3600
```

Do not infer active robot-hours from transitions unless frequency, action repeat, idle periods, and reset boundaries are known. Thirty of 34 core works do not report control frequency ([CL-EFF-016](../data/claims_ledger.csv)).

## 5. Wall-clock decomposition

Report elapsed time from the declared start to target:

```text
T_wall =
  T_task_execution
  + T_policy_update_blocking
  + T_reset
  + T_recovery
  + T_human_rescue
  + T_maintenance
  + T_evaluation
  + T_idle_or_queue
```

Also record learner compute that overlaps physical execution rather than adding overlapped durations twice. A long run does not establish a high duty cycle without this decomposition.

Operational duty cycle:

```text
duty_cycle = productive_task_execution_time / total_study_wall_time
```

Robot active duty cycle:

```text
robot_active_duty =
  (task + reset + recovery action time) / total_study_wall_time
```

The two differ when robots reset/recover without producing target-task data.

## 6. Fleet accounting

For a fleet of `N` actors report:

- `N(t)`, not only peak `N`;
- per-robot task, reset, maintenance, and idle time;
- aggregate robot-hours;
- calendar duration;
- learner throughput and policy-version lag;
- synchronization/queue time;
- operator staffing, replenishment, and maintenance;
- capital hardware and spares;
- failures and replacement periods.

If a one-robot matched baseline exists:

```text
calendar_speedup(N) = T_wall(1) / T_wall(N)
```

Do not call `calendar_speedup` a sample reduction. Fleet systems primarily change throughput and may increase aggregate operating cost ([CL-EFF-003](../data/claims_ledger.csv), [CL-EFF-004](../data/claims_ledger.csv)).

## 7. Reset, recovery, safety, and maintenance events

Publish one timestamped row per event:

```csv
event_id,run_id,robot_id,start_time,end_time,event_type,trigger_type,
trigger_source,entry_state_class,target_set,attempt_index,outcome,fallback,
human_active_seconds,human_standby_required,safety_severity,
damage_or_wear,notes
```

Controlled `event_type` values should include:

- `task_execution`;
- `success_transition`;
- `failure_detected`;
- `safety_abort`;
- `backup_policy`;
- `local_recovery`;
- `task_level_recovery`;
- `exact_reset`;
- `functional_reset`;
- `pseudo_reset`;
- `human_rescue`;
- `maintenance`;
- `replenishment`;
- `calibration`;
- `resume`.

A safety abort is not a reset. Failure detection, containment, recovery, reset, and return-to-operation are separate events even when they occur in sequence.

For every trigger report detector/rule/human source, threshold, persistence window, detection latency, and false-positive/false-negative audit. For every reset/recovery attempt report entry-state class, eligibility, target set, timeout, outcome, duration, fallback, human time, and safety/wear consequences.

### Required reliability quantities

```text
P_reset = successful_reset_attempts / all_reset_attempts

recovery_coverage =
  observed_failure_states_eligible_for_autonomous_recovery
  / all_observed_failure_states

P_recover_given_eligible =
  successful_eligible_recoveries / eligible_recovery_attempts

P_system_recover =
  all_failures_returned_autonomously / all_observed_failures
```

Report coverage and conditional recovery success together. A high success rate over a narrow, hand-selected recoverable subset is not system reliability. Learned reset is not zero-cost; the corpus includes reset policies with imperfect source-reported success ([CL-EFF-021](../data/claims_ledger.csv)).

For time to first human rescue or unrecoverable failure, publish a censored survival curve, median if estimable, and number at risk—not only the longest successful run.

## 8. Human-time ledger

Log elapsed intervals and tag all roles served:

```csv
human_interval_id,run_id,operator_id,start_time,end_time,active_or_standby,
role_tags,trigger,interface,robot_blocked,output_units,quality_check,notes
```

Role tags:

- demonstration;
- goal example;
- preference/success/stage label;
- reward or prompt design;
- online takeover/action correction;
- reset/rescue;
- maintenance/calibration;
- monitoring;
- evaluation;
- data curation;
- system engineering.

Count elapsed person-time once even if the same intervention supplies safety control, a corrective action, and a label. Preserve the multiple informational roles as tags.

Report:

| Human quantity | Definition |
|---|---|
| Active demonstration minutes | Includes discarded or failed demonstrations. |
| Active label minutes | Creation, adjudication, and validation. |
| Active intervention minutes | Takeover/correction during online operation. |
| Active reset/rescue minutes | Physical restoration or extraction. |
| Active maintenance minutes | Batteries, replenishment, repair, calibration, fixtures, network/sensor work. |
| Presence-bound minutes | Required watch/standby time even without action. |
| Engineering person-hours | Task, reward, detector, recovery, safety, fixture, and system integration. |
| Evaluation person-hours | Running/judging trials, checkpoint selection, and curation. |
| Allocated prior labor | Declared share of upstream data/model/controller labor. |

```text
active_human_minutes_per_robot_hour =
  total_active_human_minutes / aggregate_robot_hours
```

Demonstration count alone is not human time. Intervention-based results should compare methods under both matched robot-step and matched operator-time budgets ([CL-EFF-007](../data/claims_ledger.csv), [CL-EFF-008](../data/claims_ledger.csv)).

## 9. Prior data, simulation, and world-model accounting

For every inherited dataset publish:

- robot/site/task/policy provenance;
- success, failure, and intervention composition;
- transitions, episodes, robot-hours, and human-hours;
- labeling and curation time;
- data cleaning/exclusion rules;
- license and distribution overlap with the target evaluation;
- whether collection hardware matches target hardware.

For simulation/world models publish:

- simulator/model training data and physical calibration;
- accelerator type/count and elapsed compute duration;
- GPU-hours/accelerator-hours, energy when measurable, and model size;
- number of simulated/imagined transitions;
- real corrections after model exploitation or sim-to-real failure;
- physical safety events attributable to model mismatch.

Offline learning and world-model learning can genuinely reduce target online exploration while transferring cost upstream ([CL-EFF-005](../data/claims_ledger.csv), [CL-EFF-006](../data/claims_ledger.csv)). The marginal and lifecycle ledgers must show both statements.

## 10. Adaptation amortization

For an adaptation method report:

```text
C_total(K) = C_pretrain + K * C_adapt
C_from_scratch_total(K) = K * C_from_scratch
```

Publish `C_pretrain`, `C_adapt`, the expected reuse count `K`, asset lifetime, and break-even `K*`. Compare:

1. from scratch;
2. same prior without adaptation;
3. same total lifecycle budget;
4. perturbations within and outside prior support.

Few-minute adaptation cannot be directly ranked against from-scratch learning when the former inherits simulation repertoires, meta-training, or teacher policies ([CL-EFF-010](../data/claims_ledger.csv)).

## 11. Compute, safety, wear, and failed runs

Compute reporting must include model/algorithm phase, device type/count, duration, peak memory, and whether it overlaps collection. Hardware names without duration do not establish compute cost.

Safety/wear reporting should count by seed:

- collision, hard stop, E-stop, fall, out-of-bounds event, and manual catch;
- early safety termination;
- damaged/replaced parts and consumables;
- repair/maintenance person-hours;
- robot downtime;
- failed, diverged, and abandoned development runs.

A useful secondary quantity is:

```text
safe_successes_per_robot_hour =
  successful_frozen_evaluations
  / robot_hours_across_all_started_runs
```

It cannot replace the vector. Its purpose is to keep failed and safety-terminated runs in the denominator. The complete corpus audit contains 272 lifecycle cells: 230 are `not_reported`, 35 contain a source-located quantitative component, and seven contain a qualitative/incomplete proxy. This supports a bounded reporting-gap claim, not a claim that any named system is unsafe ([CL-EFF-017](../data/claims_ledger.csv)).

## 12. Learning curves and uncertainty

For at least three independent training seeds where feasible, publish:

- performance versus physical transitions;
- performance versus aggregate robot-hours;
- performance versus elapsed wall-clock;
- performance versus operator-hours;
- final performance;
- time-to-threshold;
- normalized area under the curve at a fixed, predeclared budget.

For normalized performance `p(b)` over budget `B`:

```text
NAUC_B = (1 / B) * integral_0^B p(b) db
```

`NAUC_B` is comparable only under a shared budget unit, task, evaluator, evaluation cadence, and target distribution. Report each seed and a median; use an interval suitable for the small sample, and retain failed seeds. One long physical run is valuable system-feasibility evidence but not a stable effect-size estimate.

## 13. Six comparison gates

Two methods may be called more sample- or time-efficient only if every applicable gate matches or is explicitly corrected:

| Gate | Required match/correction | If unmet |
|---|---|---|
| G1 Task/platform | Embodiment, sensors, actions, horizon, initial states | Report separate feasibility; no ranking. |
| G2 Performance | Success definition, threshold, trials, uncertainty | Do not compare time-to-threshold. |
| G3 Budget | Same steps, episodes, robot-hours, or preregistered conversion | State each reported value only. |
| G4 Boundary | Reset, setup, demo, compute, evaluation, maintenance inclusion | Compare only the jointly covered sub-ledger. |
| G5 Parallelism/assets | Robot count, accelerators, prior data, pretrained policy/model | Separate marginal and lifecycle cost. |
| G6 Repetition | Independent seeds/sites/hardware and failed runs | Treat as demonstration-level evidence. |

Explicitly invalid direct comparisons include:

- adaptation minutes versus from-scratch minutes;
- fleet wall-clock versus single-robot aggregate robot-hours;
- one paper's episode versus another task's episode;
- step count converted to time with unknown frequency/action repeat;
- success rates with unknown or unequal denominators;
- offline deployment cost with upstream data production omitted;
- world-model policy-optimization time with model-data/compute omitted;
- few physical trials described as low elapsed-time cost when wall-clock is `NR` ([CL-EFF-022](../data/claims_ledger.csv)).

## 14. Minimum machine-readable record

One row per task, seed, and accounting boundary should include:

| Group | Required fields |
|---|---|
| Identity | task, robot, sensors, action space, control Hz, seed, date, site |
| Performance | success event, threshold, `k/n`, interval, OOD split |
| Interaction | train/demo/reset/recovery/evaluation/development transitions and trials |
| Time | active robot-hours, wall-clock, and full decomposition |
| Human | active and standby intervals by role, maintenance, engineering |
| Parallelism | robot/actor/learner/GPU counts and duty cycle |
| Prior assets | dataset/sim/model/controller provenance, size, collection/compute/labor |
| Reset/recovery | event-level attempts, coverage, success, latency, fallback |
| Safety/wear | collisions, aborts, damage, consumables, repair, downtime |
| Integrity | failed seeds, excluded runs, inclusion flags, `NR` reason |

## 15. Reporting completeness levels

- **L0 — Performance only:** final performance/curve; efficiency is not auditable.
- **L1 — Online core:** performance denominator, transitions/episodes, robot-hours, wall-clock, and parallelism.
- **L2 — Lifecycle:** L1 plus demos/prior data, compute, human time, reset/recovery, safety/wear, engineering, and failed runs.
- **L3 — Reproducible lifecycle:** L2 plus machine-readable logs, public protocol, and independent physical replication.

These prospective `L*` levels are not the same as this repository's retrospective `E*` evidence tiers.
