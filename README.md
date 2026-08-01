# Awesome Real-World RL Efficiency / 真机强化学习样本与时间成本

An evidence-checked map of how physical-robot reinforcement learning reduces—or relocates—sample, robot-time, wall-clock, human, compute, hardware, and engineering cost.

这是一个经过证据核验的真机强化学习资料库，追踪方法如何减少或转移样本、机器人时间、日历时间、人工、计算、硬件和工程成本。

**Literature cutoff / 文献截止：2026-07-31.** This snapshot contains **36 included works: 34 physical-robot core studies and 2 measurement/context papers**.

Canonical repository: <https://github.com/liaohr9/awesome-real-world-rl-efficiency>

## Navigate / 导航

- [中文详细综述](SURVEY.md)
- [English LaTeX survey](paper/main.tex)
- [Review methodology](docs/methodology.md)
- [Evaluation protocol](docs/evaluation_protocol.md)
- [Research gaps](docs/research_gaps.md)
- [Data schema](data/schema.md)
- Data: [papers](data/papers.csv) · [mechanisms](data/mechanism_matrix.csv) · [quantitative evidence](data/quantitative_evidence.csv) · [claims](data/claims_ledger.csv)
- Audits: [atomic time ontology](data/time_ontology.csv) · [claim-to-evidence map](data/claim_evidence.csv) · [tier rationales](data/tier_rationales.csv) · [lifecycle grid](data/lifecycle_cost_grid.csv) · [hardware roles](data/hardware_roles.csv) · [zero-demo basis](data/zero_demo_basis.csv)
- [Validation report](docs/validation_report.md) · [Contributing](CONTRIBUTING.md)

## Companion evidence atlases / 姊妹证据库

- [Automatic reset and failure recovery](https://github.com/liaohr9/awesome-reset-recovery-robot-rl) / [自动复位与失败恢复](https://github.com/liaohr9/awesome-reset-recovery-robot-rl)
- [Human demonstrations and interventions](https://github.com/liaohr9/awesome-human-assistance-robot-rl) / [人工示范与干预依赖](https://github.com/liaohr9/awesome-human-assistance-robot-rl)

## What problem is being measured?

The bottleneck is not just “number of samples.” It is the resource vector required to reach a declared physical-task target:

```text
C = {
  physical steps / episodes,
  active robot-hours,
  elapsed wall-clock,
  reset and operator time,
  demonstrations and prior data,
  compute,
  parallel hardware,
  engineering,
  safety, wear, and maintenance
}
```

The coordinates are **overlapping diagnostic views**, not additive cost terms. For example, active robot-hours can already contain reset/recovery time. They may be summed only after an explicit inclusion matrix removes overlap and a declared price/utility model supplies weights. A fleet may shorten calendar time without reducing aggregate robot-hours; offline RL may reduce target-task exploration while inheriting hundreds of hours of physical data; a learned reset may reduce manual resets without making reset time or failure disappear. For that reason this repository is an **evidence atlas, not a leaderboard** ([CL-EFF-001](data/claims_ledger.csv), [CL-EFF-003](data/claims_ledger.csv), [CL-EFF-023](data/claims_ledger.csv)).

### Audited ledger snapshot

| Ledger | Frozen size | Meaning |
|---|---:|---|
| Quantitative evidence | 424 rows | 408 standard rows (`34 × 12`) plus 16 supplemental quantities; 162 rows are `not_reported`. |
| Time ontology | 88 rows | Atomic task/phase records. Reported phase duration is available for 27/34 works; strict `time_to_declared_target` is available for 14/34 and `NR` for 20/34. |
| Lifecycle cost | 272 rows | Complete `34 × 8` channel grid: 230 `NR`, 35 source-located quantitative components, and 7 qualitative/incomplete proxies. No work reports a full lifecycle total. |
| Hardware roles | 36 rows | Learner, helper/reset, fleet-collector, and evaluation-only roles; helper hardware is not hidden inside learner count. |
| Tier and zero audits | 36 + 19 rows | One E-tier rationale per included work and one source/scope record per explicit zero-demo claim. |
| Claim evidence | 509 links | Every one of 25 synthesis claims resolves to typed evidence; count claims carry executable filters and full membership. |

`reported_phase_duration` and `time_to_declared_target` answer different questions. A run, data-collection program, or model-training job may have a duration without reporting the first time a declared physical target was reached. The strict field is available only when target, evaluator/checkpoint, phase boundary, and task scope can all be identified; “available” does not imply preregistration.

### What counts

- Original technical research with an accessible full paper.
- At least one physical-robot task experiment for a core record.
- RL, or an RL-enabling mechanism, is central to the reported task-learning system.
- The work directly measures, changes, or targets physical interaction, robot-hours, wall-clock, compute, reset, human input, reward engineering, prior data, safety, or wear.
- Two explicitly labeled context papers may define the measurement problem; they cannot support a physical-effectiveness claim.

### What does not count

- Simulation-only results as evidence that a mechanism works reliably on hardware.
- Perception, planning, or language components without task-level robot-policy learning.
- Search snippets or project-page claims used as final numerical evidence.
- Public code treated as independent physical reproduction.
- Missing quantities silently treated as zero.

## How to read the labels

- `R0`–`R4` describe **physical-robot evidence/deployment intensity**.
- `E0`–`E4` describe **sample/time-cost claim strength**.
- `R` and `E` answer different questions: long autonomous operation is not automatically sample-efficient.
- No core work in this snapshot reaches `E4` independent cross-team cost replication ([CL-EFF-011](data/claims_ledger.csv)).

Full definitions are in the [data schema](data/schema.md).

## Three-level taxonomy / 三级机制分类

The taxonomy groups systems by the resource transformation they perform, not by algorithm name. A paper can occupy several Level-3 nodes; the complete many-to-many mapping is in [`mechanism_matrix.csv`](data/mechanism_matrix.csv).

- **L1 — Reduce marginal online interaction / 减少目标在线交互**
  - **L2 — Direct online update efficiency**
    - `EFF-M01` Off-policy replay and actor-critic reuse
  - **L2 — Model-based learning**
    - `EFF-M02` Black-box dynamics and policy search
    - `EFF-M03` Online latent world-model planning
  - **L2 — Representation and goal learning**
    - `EFF-M04` Contrastive representations and imagined goals
  - **L2 — Constrained policy improvement**
    - `EFF-M05` Residual policy around an engineered controller
  - **L2 — Task decomposition**
    - `EFF-M06` Scheduled auxiliary intentions
  - **L2 — Trial-limited policy search**
    - `EFF-M07` One-step or few-episode black-box optimization
- **L1 — Compress elapsed time / 压缩日历时间**
  - **L2 — Parallel physical actors**
    - `EFF-M08` Homogeneous robot-fleet collection
  - **L2 — External physical automation**
    - `EFF-M09` Teacher or helper robot
  - **L2 — Fast online systems**
    - `EFF-M10` Overlapped collection and learning on local accelerators
- **L1 — Remove reset and recovery downtime / 减少复位与恢复停顿**
  - **L2 — Task reciprocity**
    - `EFF-M11` Forward/backward or multi-task self-reset
  - **L2 — Environment/task cycling**
    - `EFF-M12` Pseudo-resets and goal cycles
  - **L2 — Learned recovery**
    - `EFF-M13` Reset or recovery policy from demonstrations/data
  - **L2 — Scripted recovery and fixtures**
    - `EFF-M14` Reorientation, reels, gravity, launchers, or actuated bins
- **L1 — Shift learning out of the target online phase / 将学习移出目标在线阶段**
  - **L2 — Offline real-robot experience**
    - `EFF-M15` Offline pretraining followed by limited online fine-tuning
    - `EFF-M16` Large-scale offline policy learning
  - **L2 — Simulation and prior controllers**
    - `EFF-M17` Simulation-initialized or repertoire-guided transfer
  - **L2 — Learned world models**
    - `EFF-M18` Policy improvement inside a learned video world
- **L1 — Improve exploration information / 提高探索信息量**
  - **L2 — Demonstration bootstrap**
    - `EFF-M19` Initial task demonstrations
  - **L2 — Live supervision**
    - `EFF-M20` Human interventions and corrective actions
  - **L2 — Autonomous data diversification**
    - `EFF-M21` Play, failure data, and continuous multi-task collection
  - **L2 — Reward and progress supervision**
    - `EFF-M22` Learned success/reward classifiers
- **L1 — Adapt instead of relearn / 快速适应而非重新学习**
  - **L2 — Dynamics adaptation**
    - `EFF-M23` Meta-learned dynamics updated online
  - **L2 — Damage/behavior adaptation**
    - `EFF-M24` Repertoire-guided Bayesian adaptation
  - **L2 — Policy adaptation**
    - `EFF-M25` Teacher-mediated real-world adaptation

## Strongest findings / 最稳健结论

| Claim | Evidence-bounded finding | Required limit |
|---|---|---|
| `CL-EFF-002` | Minute- or hour-scale physical learning has been demonstrated on several engineered manipulation, locomotion, and driving tasks. | Each result uses its own task, target, reset, demonstrations, and upstream assets; it is not a minute-scale lifecycle claim. |
| `CL-EFF-004` | Robot fleets improve calendar throughput. | They do not eliminate aggregate physical interaction, hardware, maintenance, or staffing cost. |
| `CL-EFF-005` | Offline RL can avoid target-deployment exploration. | It inherits collection, demonstration, failure-data, labeling, and curation cost. |
| `CL-EFF-009` | Reset-free and continuous systems reduce particular manual reset operations. | They may still depend on reversible tasks, recovery policies, fixtures, batteries, or occasional rescue. |
| `CL-EFF-010` | Adaptation can take only minutes after an upstream prior exists. | It cannot be ranked directly against from-scratch learning without `C_pretrain` and reuse count `K`. |
| `CL-EFF-012` | 15/34 core works lack a clear evaluation-trial denominator. | Cross-paper success-rate comparisons are therefore often underdetermined. |
| `CL-EFF-017` | In the complete 272-cell lifecycle grid, 230 cells are `NR`, 35 contain source-located quantitative components, and 7 contain only qualitative/incomplete proxies; no work reports a full lifecycle total. | This is a reporting-gap finding, not evidence that any named system is unsafe. |
| `CL-EFF-023` | The corpus does not support a universal efficiency ranking or pooled effect size. | Local comparison remains possible when task, target, budget, system boundary, assets, and repetitions match. |

## What methods displace / 成本被移到哪里

| Visible reduction | Typical displaced resource | What must be reported |
|---|---|---|
| Fewer target online transitions | Offline robot data, simulation, pretrained policy/model | Provenance, collection robot-hours, human-hours, compute, reuse count |
| Shorter wall-clock | Fleet size, accelerators, overlapping compute, maintenance | Per-robot hours, actor count over time, duty cycle, learner lag |
| Fewer manual resets | Reverse task, recovery data, fixture/helper robot | Reset attempts, conditional success, duration, rescue fallback |
| Safer/faster exploration | Demonstrations or live intervention | Active and standby operator-minutes, discarded attempts, informational role |
| Few-minute adaptation | Repertoire, meta-training, teacher policy/system | `C_pretrain`, `C_adapt`, transfer support, amortization over `K` deployments |
| Lower-dimensional RL search | Base controller, reward, detector, task fixture | Engineering person-hours, reuse scope, sensitivity to specification errors |
| Less physical policy optimization | World-model data and GPU training | Real-data origin, GPU-hours/energy, model-bias failures, corrective physical trials |

These are cost channels, not accusations: the moved cost may be worthwhile and reusable. The requirement is to expose it ([CL-EFF-006](data/claims_ledger.csv), [CL-EFF-007](data/claims_ledger.csv), [CL-EFF-020](data/claims_ledger.csv), [CL-EFF-024](data/claims_ledger.csv)).

## Awesome list: 34 physical-robot core studies

Each work appears once below under its primary browsing mechanism. The many-to-many taxonomy retains all secondary mechanisms.

### Reduce marginal online interaction

- [SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning](https://doi.org/10.1109/ICRA57147.2024.10610040) (2024) — replay-based fast online learning; **R3/E2** · [Project](https://serl-robot.github.io/) · [Code](https://github.com/rail-berkeley/serl)
- [Learning to Walk via Deep Reinforcement Learning](https://doi.org/10.15607/RSS.2019.XV.011) (2019) — direct model-free locomotion learning; **R3/E1** · [Project](https://sites.google.com/view/minitaur-locomotion/)
- [Learning Visual Robotic Control Efficiently with Contrastive Pre-training and Data Augmentation](https://doi.org/10.1109/IROS47612.2022.9981055) (2022) — contrastive representation plus demonstrations; **R3/E2** · [Project](https://sites.google.com/view/efficient-robotic-manipulation/home)
- [Sample-efficient Reinforcement Learning in Robotic Table Tennis](https://doi.org/10.1109/ICRA48506.2021.9560764) (2021) — trial-limited black-box optimization; **R3/E1**
- [DayDreamer: World Models for Physical Robot Learning](https://proceedings.mlr.press/v205/wu23c.html) (2023) — online latent world-model learning; **R3/E2** · [Project](https://danijar.com/daydreamer) · [Code](https://github.com/danijar/daydreamer)
- [Learning by Playing: Solving Sparse Reward Tasks from Scratch](https://proceedings.mlr.press/v80/riedmiller18a.html) (2018) — scheduled auxiliary intentions; **R3/E1**
- [Visual Reinforcement Learning with Imagined Goals](https://proceedings.neurips.cc/paper/2018/hash/7ec69dd44416c46745f6edd947b470cd-Abstract.html) (2018) — imagined latent goals; **R3/E2** · [Project](https://sites.google.com/site/visualrlwithimaginedgoals/) · [Code](https://github.com/vitchyr/rlkit)
- [Data Efficient Reinforcement Learning for Legged Robots](https://proceedings.mlr.press/v100/yang20a.html) (2020) — black-box dynamics/policy search; **R3/E1**
- [Black-Box Data-efficient Policy Search for Robotics](https://doi.org/10.1109/IROS.2017.8202137) (2017) — few-episode model-based policy search; **R3/E2** · [Code](https://github.com/resibots/blackdrops)
- [Residual Reinforcement Learning for Robot Control](https://doi.org/10.1109/ICRA.2019.8794127) (2019) — residual correction around an engineered controller; **R3/E3**
- [Demonstrating a Walk in the Park: Learning to Walk in 20 Minutes With Model-Free Reinforcement Learning](https://doi.org/10.15607/RSS.2023.XIX.056) (2023) — fast replay-based locomotion learning; **R3/E3** · [Project](https://sites.google.com/berkeley.edu/walk-in-the-park) · [Code](https://github.com/ikostrikov/walk_in_the_park)
- [MoDem-V2: Visuo-Motor World Models for Real-World Robot Manipulation](https://doi.org/10.1109/ICRA57147.2024.10611121) (2024) — online visuo-motor world model; **R3/E2** · [Project](https://sites.google.com/view/modem-v2/home) · [Code](https://github.com/facebookresearch/modemv2)

### Compress elapsed time

- [Continuously Improving Mobile Manipulation with Autonomous Real-World RL](https://proceedings.mlr.press/v270/mendonca25a.html) (2025) — autonomous collection with helper/procedural infrastructure; **R4/E1** · [Project](https://continual-mobile-manip.github.io/)
- [FastRLAP: A System for Learning High-Speed Driving via Deep RL and Autonomous Practicing](https://proceedings.mlr.press/v229/stachowicz23a.html) (2023) — fast local online learning and autonomous practice; **R3/E3** · [Project](https://sites.google.com/view/fastrlap) · [Code](https://github.com/kylestach/fastrlap-release)
- [Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation](https://proceedings.mlr.press/v87/kalashnikov18a.html) (2018) — fleet-scale physical data collection; **R4/E2**
- [Scaling Up Multi-Task Robotic Reinforcement Learning](https://proceedings.mlr.press/v164/kalashnikov22a.html) (2022) — multi-robot, multi-task fleet learning; **R4/E2** · [Project](https://karolhausman.github.io/mt-opt/)
- [Robot Trains Robot: Automatic Real-World Policy Adaptation and Learning for Humanoids](https://openreview.net/forum?id=oRwcxFuN25) (2025) — teacher-robot-mediated physical adaptation; **R3/E3** · [Project](https://robot-trains-robot.github.io/) · [Code](https://github.com/hukz18/Robot-Trains-Robot)

### Remove reset and recovery downtime

- [One Demonstration Is Enough for Real-World Robotic Reinforcement Learning](https://arxiv.org/abs/2607.01651) (2026) — learned recovery plus single-demonstration bootstrap; **R3/E3** · [Project](https://autoserl.github.io/) · [Code](https://github.com/autoserl/AutoSERL)
- [Fully Autonomous Real-World Reinforcement Learning with Applications to Mobile Manipulation](https://proceedings.mlr.press/v164/sun22a.html) (2022) — pseudo-reset and task cycling; **R4/E2** · [Project](https://sites.google.com/view/relmm/)
- [REBOOT: Reuse Data for Bootstrapping Efficient Real-World Dexterous Manipulation](https://proceedings.mlr.press/v229/hu23a.html) (2023) — learned reset/recovery from prior data; **R4/E3** · [Project](https://sites.google.com/view/reboot-dexterous/)
- [Reset-Free Reinforcement Learning via Multi-Task Learning: Learning Dexterous Manipulation Behaviors without Human Intervention](https://doi.org/10.1109/ICRA48506.2021.9561384) (2021) — multi-task self-reset; **R4/E1** · [Project](https://sites.google.com/view/mtrf)
- [Self-Improving Robots: End-to-End Autonomous Visuomotor Reinforcement Learning](https://proceedings.mlr.press/v229/sharma23b.html) (2023) — forward/backward learning with recurring reset support; **R3/E1** · [Project](https://robotics.stanford.edu/blog/self-improving-robots/)

### Shift learning out of the target online phase

- [Don't Start From Scratch: Leveraging Prior Data to Automate Robotic Reinforcement Learning](https://proceedings.mlr.press/v205/walke23a.html) (2023) — prior-data reuse plus limited online learning; **R3/E3** · [Project](https://sites.google.com/view/ariel-berkeley/)
- [World-Gymnast: Training Robots with Reinforcement Learning in a World Model](https://arxiv.org/abs/2602.02454) (2026) — policy learning inside a learned world model; **R3/E3** · [Project](https://world-gymnast.github.io/) · [Code](https://github.com/world-gymnast/world-gymnast)
- [PlayWorld: Learning Robot World Models from Autonomous Play](https://arxiv.org/abs/2603.09030) (2026) — autonomous play data and learned video world; **R3/E3** · [Project](https://robot-playworld.github.io/)
- [AWAC: Accelerating Online Reinforcement Learning with Offline Datasets](https://arxiv.org/abs/2006.09359) (2020) — offline initialization followed by online fine-tuning; **R3/E2** · [Project](https://awacrl.github.io/) · [Code](https://github.com/rail-berkeley/rlkit)
- [COG: Connecting New Skills to Past Experience with Offline Reinforcement Learning](https://proceedings.mlr.press/v155/singh21a.html) (2021) — reuse of prior physical experience; **R2/E2** · [Project](https://sites.google.com/view/cog-rl) · [Code](https://github.com/avisingh599/cog)
- [Pre-Training for Robots: Offline RL Enables Learning New Tasks in a Handful of Trials](https://roboticsproceedings.org/rss19/p019.html) (2023) — offline pretraining plus few-trial adaptation; **R3/E3** · [Project](https://sites.google.com/view/ptr-final/) · [Code](https://github.com/Asap7772/PTR)
- [Q-Transformer: Scalable Offline Reinforcement Learning via Autoregressive Q-Functions](https://proceedings.mlr.press/v229/chebotar23a.html) (2023) — large-scale offline physical-robot policy learning; **R2/E2** · [Project](https://qtransformer.github.io/)
- [Real World Offline Reinforcement Learning with Realistic Data Source](https://doi.org/10.1109/ICRA48891.2023.10161474) (2023) — physical dataset and human/robot cost accounting; **R2/E2** · [Project](https://sites.google.com/view/real-orl)

### Improve exploration information

- [Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning](https://doi.org/10.1126/scirobotics.ads5033) (2025) — demonstrations plus online intervention; **R3/E3** · [Project](https://hil-serl.github.io/) · [Code](https://github.com/rail-berkeley/hil-serl)
- [Real-world Reinforcement Learning from Suboptimal Interventions](https://arxiv.org/abs/2512.24288) (2025) — learning from corrective/suboptimal interventions; **R3/E3** · [Project](https://silri-rl.github.io/) · [Code](https://github.com/nuomizai/HIL-RL)

### Adapt instead of relearn

- [Learning to Adapt in Dynamic, Real-World Environments Through Meta-Reinforcement Learning](https://openreview.net/forum?id=HyztsoC5Y7) (2019) — meta-learned dynamics adaptation; **R2/E2** · [Project](https://sites.google.com/berkeley.edu/metaadaptivecontrol)
- [Robots that Can Adapt Like Animals](https://doi.org/10.1038/nature14422) (2015) — repertoire-guided damage adaptation; **R2/E3**

## Measurement/context works (2)

These sources define real-world RL constraints and measurement concerns. Their **R0/E0** label means they must not be used as physical-effectiveness evidence.

- [Challenges of Real-World Reinforcement Learning](https://mlanthology.org/icmlw/2019/dulacarnold2019icmlw-challenges/) (2019) — problem-definition context; **R0/E0**
- [Challenges of Real-World Reinforcement Learning: Definitions, Benchmarks and Analysis](https://doi.org/10.1007/S10994-021-05961-4) (2021) — benchmark/measurement context; **R0/E0** · [Code](https://github.com/google-research/realworldrl_suite)

## Reporting checklist

A credible new result should report:

- [ ] exact robot, task, initial-state distribution, success event, target threshold, and trial denominator;
- [ ] physical transitions, episodes/trials, control frequency, action repeat, and active robot-hours;
- [ ] elapsed wall-clock with reset, recovery, update, evaluation, idle, and maintenance boundaries;
- [ ] robot count over time, aggregate robot-hours, duty cycle, and learner/actor overlap;
- [ ] demonstrations, discarded attempts, labels, interventions, resets, rescue, monitoring, and operator-minutes;
- [ ] prior-data provenance, simulation/model/controller assets, compute duration, GPU count, and reuse/amortization rule;
- [ ] reset/recovery attempts, coverage, success, latency, fallback, and unrecoverable failures;
- [ ] collisions, safety aborts, damage, wear, consumables, downtime, and failed development runs;
- [ ] at least three independent seeds where feasible, including failures, with performance versus steps, robot-hours, wall-clock, and operator-hours;
- [ ] both a **target-task marginal ledger** and a **full lifecycle ledger**.

The operational template and comparison gates are in [`docs/evaluation_protocol.md`](docs/evaluation_protocol.md).

## Critical warnings

> **`NR` is not zero.** It means the value was not located in the verified source. Numeric zero is retained only when explicitly source-reported.

> **Context papers are not physical-robot reliability evidence.** They support definitions and measurement design only.

> **No universal ranking.** Tasks, success thresholds, action rates, resets, parallelism, prior assets, and lifecycle boundaries differ too much for a pooled leaderboard.

> **Code is not reproduction.** The 15/34 official-code count records availability at verification time, not independent physical replication.

## Reproduce the audit

```bash
make validate
python3 scripts/test_validator.py
make paper
make clean
```

Validation is offline and uses only the Python standard library. Online link health is deliberately separate so the core check is deterministic.

## Contributing

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md). A paper suggestion needs an original-source locator, physical-evidence classification, resource-boundary extraction, and corresponding updates to every affected ledger. Claims that only improve a headline proxy without exposing displaced cost will not be merged as lifecycle conclusions.

## License and citation

Repository text, tables, and scripts are available under the [MIT License](LICENSE). Paper contents and linked external code remain under their original terms. Citation metadata is in [`CITATION.cff`](CITATION.cff).
