# Research gaps and falsifiable studies

## Priority summary

The corpus shows that particular engineered tasks can be learned in minutes or hours, and that offline data, world models, fleets, demonstrations, reset policies, or adaptation can reduce a selected phase. It does **not** establish which approach is cheapest end to end. The decisive missing variables are lifecycle boundaries, success denominators, parallelism, operator occupancy, safety/wear, and failed runs.

- **P0:** required for credible next-generation benchmark claims.
- **P1:** likely to change method selection or deployment conclusions.
- **P2:** deployment-economics extensions once the core ledger is available.

Each gap below ends with a falsifiable study: a result that could confirm or reject the proposed mechanism-level claim.

## P0-1 — End-to-end lifecycle ledgers

### Evidence gap

Among 34 core works, robot-hours are `NR` in 16 and wall-clock in 8. The complete 272-cell lifecycle grid has 230 `not_reported` cells, 35 source-located quantitative components, and seven qualitative/incomplete proxies; no work reports a full lifecycle total ([CL-EFF-014](../data/claims_ledger.csv), [CL-EFF-017](../data/claims_ledger.csv)). Real-ORL is a rare explicit example of a large physical and human bill behind offline learning, but it does not make the rest of the corpus estimable ([CL-EFF-005](../data/claims_ledger.csv)).

### Falsifiable study

For two tasks, implement an online replay method, offline-to-online method, and world-model method. Pre-register the lifecycle boundary and record all physical, human, compute, reset, evaluation, and failed-run events. Test:

```text
H0: the ordering by target-online robot-hours
    is unchanged after full lifecycle accounting.
```

Reject `H0` if any pair reverses under a preregistered lifecycle cost vector or Pareto dominance relation. Publish both ledgers even if no reversal occurs.

## P0-2 — Operator occupancy for reset, monitoring, and intervention

### Evidence gap

Intervention-based learning shows strong task results, but operator-minutes and continuous monitoring are not standardized ([CL-EFF-008](../data/claims_ledger.csv)). Reset-reduced systems may still require early manual resets, recurring rescue, battery changes, fixtures, or reversible task cycles ([CL-EFF-009](../data/claims_ledger.csv)).

### Falsifiable study

Compare demonstration-only, intervention, learned-recovery, and scripted-reset conditions under:

1. equal physical transitions;
2. equal active operator-minutes;
3. equal presence-bound minutes.

Log every human interval and role. Test whether intervention retains its sample advantage under an equal operator-time budget. A disappearance or reversal falsifies the claim that robot samples alone capture the benefit.

## P0-3 — Frozen success thresholds and denominators

### Evidence gap

Fifteen of 34 core works lack a clear evaluation-trial denominator ([CL-EFF-012](../data/claims_ledger.csv)). Success may mean three 15-minute windows, eight attempts, ten composite trials, 100 task trials, or a curve readout. A source-reported phase duration is `NR` in 7/34, but that field may be a run, data-collection, model-training, or program span. Under the separate target/evaluator/task/boundary rule, strict time-to-declared-target is `NR` in 20/34 and available in only 14/34 ([CL-EFF-025](../data/claims_ledger.csv)).

### Falsifiable study

Freeze a task evaluator, target `tau`, minimum trial count, confidence interval, evaluation cadence, and right-censoring rule across at least three methods and two sites. Test:

```text
H0: method ordering is invariant to reasonable preregistered
    choices of trial denominator and threshold.
```

Report all preregistered thresholds rather than selecting the one with the desired ordering. A ranking flip establishes sensitivity and rules out a universal headline.

## P0-4 — Independent E4 replication

### Evidence gap

No core work reaches independent cross-team E4 cost evidence; official public code exists for 15/34 but does not establish physical replication ([CL-EFF-011](../data/claims_ledger.csv), [CL-EFF-018](../data/claims_ledger.csv)).

### Falsifiable study

Run a registered multi-site replication with at least three independent teams and two hardware instances per method. Freeze software commit, task, evaluator, hardware budget, reset protocol, and target. Replicate both the original engineered configuration and a minimal task-specific-engineering configuration.

Falsify transportability if the original confidence region for time-to-threshold or robot-hours excludes a substantial share of site-level results. Report site variance, engineering person-hours, failures, and hardware faults—not just a pooled mean.

## P0-5 — Safety, wear, downtime, and failed development runs

### Evidence gap

Collision, E-stop, fall, replacement, maintenance, consumable, downtime, and failed-seed counts are recurrent and important reporting gaps. The full lifecycle grid makes their per-work status inspectable instead of inferring a superlative from selected examples ([CL-EFF-017](../data/claims_ledger.csv)).

### Falsifiable study

Compare a high-exploration baseline and a constrained/supervised method across all initiated seeds. Predefine safety event types and include aborted runs as right-censored costs. Test whether the method that minimizes successful-run samples also minimizes:

```text
total robot-hours across all runs / safe successful policy
```

A reversal falsifies the use of successful-run sample count as a safety-aware efficiency proxy.

## P1-1 — Fleet throughput versus aggregate cost

### Evidence gap

Fleet studies establish large-scale data collection and calendar throughput but do not consistently expose calendar time, maintenance, duty cycle, and staffing. Fleet wall-clock cannot be read as aggregate sample reduction ([CL-EFF-003](../data/claims_ledger.csv), [CL-EFF-004](../data/claims_ledger.csv)).

### Falsifiable study

Hold learner, task distribution, and target data amount fixed. Run 1-, 2-, 4-, and 8-robot configurations. Report calendar duration, aggregate robot-hours, maintenance, object logistics, staffing, energy, policy-version lag, and performance.

Test whether calendar speedup remains linear after operational overhead. Saturation or declining resource efficiency falsifies a simple `1/N` time model.

## P1-2 — Prior-data provenance and amortization

### Evidence gap

Offline-to-online and offline methods inherit real physical collections, failures, labels, and curation. Data origin, robot-hours, human-hours, licensing, and target-distribution overlap are incompletely reported ([CL-EFF-005](../data/claims_ledger.csv)).

### Falsifiable study

Publish a provenance card for every dataset shard. Compare:

- target-only learning;
- shared prior plus target learning;
- shared prior with lifecycle cost allocated over `K` tasks.

Test performance for matched target marginal cost and matched full lifecycle cost. Vary `K`; estimate break-even `K*`. If the method never reaches break-even within the declared asset lifetime, falsify the deployment-efficiency claim while retaining any target-marginal benefit.

## P1-3 — World-model compute and physical correction cost

### Evidence gap

World models can move policy optimization away from hardware, but the ledger shifts toward real model data, accelerators, energy, and control of model bias ([CL-EFF-006](../data/claims_ledger.csv)). Compute is `NR` in 21/34 core works ([CL-EFF-015](../data/claims_ledger.csv)).

### Falsifiable study

For direct online, latent world-model, and video-world conditions, publish a Pareto surface over:

- real robot-hours;
- GPU-hours and energy;
- wall-clock;
- final success and OOD robustness;
- model-induced unsafe proposals and corrective physical trials.

Run three comparisons: equal physical budget, equal compute budget, and equal lifecycle budget. If the advantage exists only under one omitted resource, reject a general efficiency claim and retain the bounded one.

## P1-4 — Adaptation versus from-scratch learning

### Evidence gap

Fast physical adaptation inherits a repertoire, meta-training set, pretrained policy, teacher system, or simulation. Its final minutes cannot be compared directly with from-scratch training ([CL-EFF-010](../data/claims_ledger.csv)).

### Falsifiable study

Report `C_pretrain`, `C_adapt`, expected reuse `K`, and asset lifetime. Compare:

1. from scratch;
2. the same prior without the adaptation algorithm;
3. adaptation under the same total lifecycle budget;
4. perturbations inside and outside the prior support.

Falsify broad adaptation efficiency if gains vanish outside hand-covered perturbations or break-even reuse exceeds the plausible deployment count.

## P1-5 — Step and episode semantics

### Evidence gap

Physical steps are `NR` in 22/34 works, episodes in 19/34, and control frequency in 30/34 ([CL-EFF-013](../data/claims_ledger.csv), [CL-EFF-016](../data/claims_ledger.csv)). One episode can be a five-second gait rollout, a grasp, an assembly, or a long evaluation window.

### Falsifiable study

Publish timestamped transitions, action repeat, frequency, episode-duration distribution, active action time, and reset time. Compare the ranking produced by transitions, trials, robot-hours, and wall-clock on the same task.

A ranking change falsifies interchangeability of the sample proxies. A stable ranking across all four supports a local proxy—not a cross-task one.

## P1-6 — Embodiment and task external validity

### Evidence gap

The corpus is dominated by fixed or structured manipulation, with smaller locomotion, driving, dexterous, and mobile-manipulation slices. Fixtures, fixed cameras, fiducials, reversible goals, and controlled object supply may not transfer to homes, hospitals, mixed production lines, or outdoor operation.

### Falsifiable study

Create a stratified suite with fixed manipulation, mobile manipulation, locomotion, dexterity, and a human-shared setting. Each class should include both cleanly reversible and irreversible failures. Apply the same lifecycle schema and at least two mechanism families.

Test whether a mechanism's relative resource reduction transfers across task classes. A task-by-mechanism interaction falsifies embodiment-independent claims and identifies the mechanism's operational support.

## P1-7 — Reward, detector, and progress-supervision engineering

### Evidence gap

Learned success/reward classifiers and hand-designed rewards can make sparse tasks learnable, but data collection, label adjudication, prompt/specification work, and false detector outputs are rarely costed. Controller and reward engineering can shrink the RL search while moving cost to human design ([CL-EFF-020](../data/claims_ledger.csv), [CL-EFF-024](../data/claims_ledger.csv)).

### Falsifiable study

Compare hand-coded reward, learned classifier, and task-level outcome evaluator under equal total specification/label person-hours. Freeze an independent audit set for detector errors. Measure task performance, unsafe false positives, false negatives, rework time, and reuse on a second task.

Falsify “cheap supervision” if label/specification labor or downstream correction dominates the physical savings under the same boundary.

## P2-1 — Engineering assets as reusable capital

### Evidence gap

Controllers, fixtures, helper robots, task graphs, reward programs, and safety systems may be expensive once and cheap to reuse. Current reports rarely disclose development person-hours, maintenance, or reuse count ([CL-EFF-020](../data/claims_ledger.csv), [CL-EFF-024](../data/claims_ledger.csv)).

### Falsifiable study

Track an artifact across at least ten related deployments. Report development, integration, maintenance, modification, and decommissioning cost. Estimate:

```text
amortized_engineering_cost(K) =
  fixed_development_cost / K + per_deployment_integration_cost
```

Test whether reuse follows the declared curve or requires task-specific re-engineering. Persistent high integration cost falsifies the assumption that a seemingly fixed asset amortizes cleanly.

## P2-2 — Value-aware resource vectors without a universal scalar

### Evidence gap

Different users value wall-clock, robot wear, operator time, compute, and safety differently. A universal weighted score would hide those choices ([CL-EFF-001](../data/claims_ledger.csv), [CL-EFF-023](../data/claims_ledger.csv)).

### Falsifiable study

Publish the raw resource vector and compute scenario-specific Pareto fronts for, for example:

- a small academic lab;
- a fleet operator;
- a safety-critical deployment;
- an energy-constrained edge site.

Vary transparent prices/constraints. If one method dominates across all plausible scenarios, that local dominance is robust. If the preferred method changes, the result falsifies a universal rank and makes the decision boundary explicit.

## Cross-gap contradiction tests

| Surface contradiction | Hidden boundary difference | Decisive measurement |
|---|---|---|
| “Learns in minutes” vs “needs hundreds of thousands of trials” | Engineered single task vs fleet-scale data/generalization | Same task, target, and lifecycle boundary |
| “Reset-free” vs recurring rescue/battery work | Avoiding exact initial state vs unattended operation | Operator occupancy, rescue rate, duty cycle |
| “Offline saves robot data” vs hundreds of collection hours | Target marginal cost vs inherited lifecycle cost | Provenance and amortization |
| “World model removes real RL” vs real data/GPU burden | Location of policy optimization vs model acquisition | Equal physical, compute, and lifecycle budgets |
| “Two-minute adaptation” vs “twenty-minute learning” | Inherited prior vs from-scratch | `C_pretrain + K*C_adapt` |
| “Few episodes” vs unknown elapsed cost | Trial count vs reset/compute/human time | Timestamped end-to-end event log |

## Minimum high-value benchmark

A tractable benchmark that addresses the largest gaps would:

1. use one fixed manipulation task and one mobile/locomotion task;
2. compare replay-based online learning, offline-to-online learning, world-model learning, demonstration/intervention, and reset/recovery mechanisms;
3. freeze success definitions and evaluators;
4. run at least three independent seeds and retain failures;
5. replicate at two independent sites;
6. match physical transitions, robot-hours, wall-clock, operator-hours, and lifecycle budget in separate analyses;
7. publish interaction, reset, intervention, safety, maintenance, and compute event logs;
8. report a Pareto frontier rather than one ranking.

This single design would directly test lifecycle accounting, operator cost, E4 replication, safety/wear, proxy interchangeability, and task transfer.
