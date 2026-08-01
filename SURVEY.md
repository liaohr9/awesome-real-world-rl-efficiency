# 真机强化学习中的样本与时间成本：从单一 headline 到可审计资源账本

**文献截止：2026-07-31**

## 1. 摘要

真机强化学习经常用“多少步”“多少分钟”“多少次尝试”描述效率，但这些 headline proxy 回答的是不同问题。物理 transition 衡量控制决策数，却不包含 action duration、reset、compute wait 与人工；wall-clock 能反映日历速度，却会被并行机器人和重叠计算压缩；offline RL、world model 与 adaptation 可以显著减少目标在线交互，却继承数据、仿真、GPU、teacher system 或 pretrained policy 的成本。因此，样本与时间瓶颈不能由一个数字评价。

本综述基于截至截止日核验的 36 篇工作，其中 34 篇为 physical-robot core studies，2 篇为 measurement/context sources。我们将方法归为六类资源变换、25 个 Level-3 mechanisms，并用 424 行定量证据（408 个标准行、16 个 supplemental rows）和 25 条主张账本约束叙述。核心结论是：分钟级或小时级真机学习在若干工程化任务上确实存在，但它不是“端到端系统从零建立只需几分钟”；fleet、offline data、demonstration、reset policy、world model 和 adaptation 都可能产生真实收益，同时把成本移到另一个阶段。现有语料不支持跨任务统一排行榜，也没有独立跨团队的 E4 成本复现。

本文的目标不是选出“最优算法”，而是回答三个更可检验的问题：

1. 某方法减少了哪个资源坐标？
2. 它把成本移到哪里，并依赖哪些前置资产？
3. 在怎样的统一日志与评测协议下，两个结果才可以比较？

## 2. 问题定义与边界

### 2.1 从 sample count 改为 resource vector

达到预先声明的物理任务性能阈值 `tau` 所需成本记为：

```text
C = {
  physical steps / episodes / trials,
  active robot-hours,
  elapsed wall-clock,
  reset / recovery / maintenance time,
  active and standby operator time,
  demonstrations / labels / prior data,
  compute and energy,
  parallel robots / fixtures / helper hardware,
  engineering labor,
  safety and wear
}
```

这些坐标是可能重叠的诊断视图：例如 aggregate active robot-hours 可以已经包含 reset/recovery 时间。只有 inclusion matrix 完成去重、且决策场景给出公开价格/效用权重时，才能形成标量成本；不能直接把坐标相加（`CL-EFF-001`）。原因不是“指标越多越好”，而是不同机制直接作用于不同坐标：

- replay 和更快 online learner 主要减少 target-task marginal interaction；
- fleet 主要压缩日历时间；
- reset/recovery 系统减少停顿和人工恢复；
- offline/world-model 方法把学习移出 target online phase；
- demonstration/intervention 提高每个样本的信息量；
- adaptation 用共享 prior 换取更低的 per-deployment cost。

### 2.2 两个必须同时报告的成本边界

**目标任务边际成本（marginal target cost）**：已有 dataset、world model、controller、fixture 和预训练策略之后，为新任务额外消耗的资源。

**完整生命周期成本（lifecycle cost）**：边际成本加上 upstream data、simulation、model/controller/reward engineering、hardware、evaluation、maintenance 与 failed runs 的显式分摊。

两者都合理，但回答不同问题。部署者问“已有资产时再加一个任务多少钱”需要边际账本；研究比较“从零获得能力的总代价”需要生命周期账本。只公布更小的一个会使转移成本不可见（`CL-EFF-024`）。

### 2.3 纳入什么

核心工作必须是 original technical research，能够取得并核验全文，至少包含一个 physical-robot task experiment，且 RL 或 RL-enabling mechanism 对任务学习是核心。工作还必须直接测量、改变或瞄准 interaction、robot-hours、wall-clock、compute、fleet、reset、human input、reward engineering、prior data、safety 或 wear 中至少一个负担。

允许某些字段为 `NR`。这表示工作与瓶颈相关但来源没有报告该值，并不表示值为零。

### 2.4 不纳入什么

- simulation-only 结果不能证明 physical reliability；
- perception/planning/language component 若没有 task-level robot policy learning，不进入核心语料；
- search snippet、媒体摘要和项目页不能作为最终数值证据；
- public code 不能自动升级为独立真机复现；
- context paper 只能支撑定义和测量框架，不能支撑 physical effectiveness；
- 少量 trials 在 wall-clock 为 `NR` 时不能被写成低 elapsed-time cost（`CL-EFF-022`）。

## 3. 系统检索与纳入排除流程

### 3.1 检索问题

检索问题是：

> 在完整成本边界下，已有真机证据如何描述 RL 策略达到可验证任务性能所需的资源，以及方法如何改变这些资源？

检索组合 robot/embodiment、reinforcement learning、physical hardware 三个概念块，并补充 sample-efficient、robot-hours、wall-clock、few trials、rapid adaptation、world model 等效率词。效率词不是核心查询的硬条件，避免漏掉正文报告成本但标题不使用“sample efficiency”的工作。

检索与核验路径包括 arXiv、PMLR、OpenReview、RSS/IEEE/NeurIPS 等官方 proceedings 或 publisher page、DOI 元数据、官方项目页与 repository，以及 verified anchors 的 backward/forward chaining。Scopus 与 Web of Science 在本轮没有可用认证访问，因此只被记录为 additive sources，没有被描述为已搜索。

### 3.2 流程和库存

流程依次为 discovery route capture、canonical deduplication、title/abstract screening、full-text check、physical evidence check、burden/locator extraction、official project/code check 和 root consistency verification。

这不是 independent dual screening：root verification 是同一 model-assisted workflow 内的 consistency/error-detection layer，不能据此声明 inter-rater reliability。

| 流程量 | 值 | 分母/范围 | 平台 | Locator | Status | 解释限制 |
|---|---:|---|---|---|---|---|
| 候选记录 | 73 | 全部 canonical candidates | 跨平台 review inventory | [methodology §4](docs/methodology.md) | reviewer-counted | 公共检索没有暴露完整结果总数，不能解释为数据库穷举召回率。 |
| 核心纳入 | 34 | 73 candidates | physical-robot corpus | [papers table](data/papers.csv) | reviewer-counted, full-text verified | 语料偏向 manipulation 与 2018 年以后研究。 |
| Context 纳入 | 2 | 73 candidates | measurement context | [papers table](data/papers.csv) | reviewer-counted | R0/E0，不能支持硬件有效性。 |
| 终止排除 | 5 | 73 candidates | cross-platform | [methodology §4](docs/methodology.md) | reviewer-counted | 其余 32 条仍为 pending，不等于排除。 |
| Pending | 32 | 73 candidates | cross-platform | [methodology §4](docs/methodology.md) | reviewer-counted | 未进入任何结论或数量分母。 |

### 3.3 数据抽取原则

每个 core work 抽取 identity、robot/task、physical training、success definition/result/trials、steps、episodes、control frequency、robot-hours、wall-clock、parallel robots、compute、demonstrations、reset、reward engineering、prior assets、safety/wear、claimed reduction、displaced cost、source grade、locator 与 limitations。

每个数值必须有原文页码、表格、图、章节或附录 locator。Reviewer arithmetic 单独标为 `derived`；带约数、区间或 lower bound 的值保持 `source_reported_approximate`，不被改写成精确点估计。

## 4. 证据等级与主张账本

### 4.1 三条互不替代的证据轴

`R0–R4` 描述 physical-robot evidence/deployment intensity；`E0–E4` 描述 sample/time claim strength；`source_grade` 描述来源权威性。三者不能互相替代：

- R4 长时自主运行回答 reset/operation 能力，不自动证明 sample efficiency（`CL-EFF-019`）；
- E3 表示 task-specific quantitative evidence 较强，不表示跨团队复现；
- peer review 或 source grade A 不保证 lifecycle fields 完整；
- official public code 记录可用性，不是 independent reproduction（`CL-EFF-018`）。

| 证据分布 | 值 | 分母 | 平台 | Locator | Status | 解释限制 |
|---|---:|---:|---|---|---|---|
| R4 / R3 / R2 core | 6 / 23 / 5 | 34 core works | 跨 physical platforms | [papers table](data/papers.csv) | reviewer-classified | R 表示部署/训练证据，不表示成本主张强度。 |
| E3 / E2 / E1 core | 13 / 14 / 7 | 34 core works | 跨 physical platforms | [papers table](data/papers.csv) | reviewer-classified | 不同 task 和 threshold 不能按 tier 排名。 |
| E4 | 0 | 34 core works | 跨 physical platforms | `CL-EFF-011`, [claims](data/claims_ledger.csv) | not located in verified corpus | “未核验到”不等于方法不可复现。 |
| Official public code | 15 | 34 core works | cross-platform software status | `CL-EFF-018`, [papers](data/papers.csv) | verified at snapshot date | 仓库状态会变化；代码不等于真机复现。 |

### 4.2 主张账本为何必要

[`claims_ledger.csv`](data/claims_ledger.csv) 的 24 行不是摘要标签，而是叙述上限。每行同时记录：

- `claim_text`：允许的最强表述；
- `claim_scope`：适用 population 和 accounting boundary；
- `work_ids`：支持来源；
- `evidence_type` 与 `confidence`；
- `caveat`：不能在转述时删除的限制。

例如，“分钟级学习已经展示”必须同时保留 task-specific threshold、reset、demo 与 upstream engineering 的限制（`CL-EFF-002`）；“world model 减少 physical exploration”必须同时写出 model data、GPU 与 model bias（`CL-EFF-006`）。

## 5. 三层机制 taxonomy

分类的 Level 1 是被改变的资源位置，Level 2 是生命周期介入环节，Level 3 是可实现、可失败的具体机制。一个 system 可以多标签。

### 5.1 L1：减少目标在线阶段的物理交互

- Direct online update efficiency
  - `EFF-M01` Off-policy replay and actor-critic reuse
- Model-based learning
  - `EFF-M02` Black-box dynamics and policy search
  - `EFF-M03` Online latent world-model planning
- Representation and goal learning
  - `EFF-M04` Contrastive representations and imagined goals
- Constrained policy improvement
  - `EFF-M05` Residual policy around an engineered controller
- Task decomposition
  - `EFF-M06` Scheduled auxiliary intentions
- Trial-limited policy search
  - `EFF-M07` One-step or few-episode black-box optimization

### 5.2 L1：压缩 elapsed wall-clock

- Parallel physical actors
  - `EFF-M08` Homogeneous robot fleet collection
- External physical automation
  - `EFF-M09` Teacher/helper robot
- Fast online systems
  - `EFF-M10` Overlapped collection and learning on local accelerators

### 5.3 L1：减少 reset 与 recovery downtime

- Task reciprocity
  - `EFF-M11` Forward/backward or multi-task self-reset
- Environment/task cycling
  - `EFF-M12` Pseudo-resets and goal cycles
- Learned recovery
  - `EFF-M13` Reset/recovery policy from demonstrations or data
- Scripted recovery and fixtures
  - `EFF-M14` Reorientation, reels, gravity, launchers, actuated bins

### 5.4 L1：把学习移出目标 online phase

- Offline real-robot experience
  - `EFF-M15` Offline pretraining plus limited online fine-tuning
  - `EFF-M16` Large-scale offline policy learning
- Simulation and prior controllers
  - `EFF-M17` Simulation-initialized or repertoire-guided transfer
- Learned world models
  - `EFF-M18` RL/policy improvement inside a learned video world

### 5.5 L1：提高 exploration information

- Demonstration bootstrap
  - `EFF-M19` Initial task demonstrations
- Live supervision
  - `EFF-M20` Human interventions and corrective actions
- Autonomous data diversification
  - `EFF-M21` Play, failure data, and continuous multi-task collection
- Reward/progress supervision
  - `EFF-M22` Learned success/reward classifiers

### 5.6 L1：快速适应而不是重新学习

- Dynamics adaptation
  - `EFF-M23` Meta-learned dynamics updated online
- Damage/behavior adaptation
  - `EFF-M24` Repertoire-guided Bayesian adaptation
- Policy adaptation
  - `EFF-M25` Teacher-mediated real-world adaptation

完整定义、work mappings、R/E labels、trade-offs 和 failure modes 见 [mechanism matrix](data/mechanism_matrix.csv)。

## 6. 按机制综合相关工作

### 6.1 Replay、快速系统和 direct online learning

Off-policy replay 可以对同一批 physical transitions 做多次 learner update；local accelerator、asynchronous collection 与快速 policy deployment 则减少控制与更新之间的阻塞。SERL、HIL-SERL、Walk in the Park 和 FastRLAP 展示了这一组合在 manipulation、locomotion 和 driving 上的工程可行性。

但“算法 sample-efficient”与“系统 elapsed-time efficient”不是同义词。Replay ratio、learner latency、policy staleness、control loop、reset fixture、demonstration 和 reward classifier 共同决定结果。若只复制 actor-critic 而没有复制 data pipeline 与 reset mechanism，headline time 不一定能复现。

### 6.2 Model-based、world model 与 representation

Black-box dynamics、latent world model 和 representation learning 都试图从每个 physical sample 提取更多信息。低维 dynamics/policy search 适合 short-horizon、可建模系统；latent world model 适合像素任务但容易受到 contact discontinuity 和 model exploitation；contrastive representation 或 imagined goal 能降低视觉学习负担，但仍依赖任务 reward、goal semantics 或 demonstrations。

World-model 系统的关键边界是“RL 在哪里发生”：policy optimization 在模型中并不等于整个能力没有 real-robot cost。还需计算 model data、physical calibration、GPU-hours、unsafe model proposals 与 corrective trials（`CL-EFF-006`）。

### 6.3 Fleet 与 calendar throughput

Fleet 把多个 physical actors 的 collection 叠加，从而缩短获得大数据集的日历时间。这对 large-scale grasping、multi-task corpus 和 offline policy learning 很重要。

然而：

```text
aggregate_robot_hours = sum over all robots
calendar_time ≠ aggregate_robot_hours
```

必须同时报告 `N(t)`、每台 robot 的 duty cycle、maintenance、object logistics、operator staffing 与 learner policy lag。Fleet 是 throughput mechanism，不是 sample count 消失机制（`CL-EFF-003`, `CL-EFF-004`）。

### 6.4 Reset、recovery 与 continuous operation

常见策略包括 forward/backward reciprocity、multi-task self-reset、pseudo-reset goal cycles、learned recovery 和 scripted fixtures。它们减少人工把 robot 精确放回初始状态的次数，并能延长 collection horizon。

“Reset-free”不能被解释为“无人维护”：可逆任务可能改变数据分布，learned reset 会失败，scripted fixture 需要设计与维护，long run 还可能需要换电、replenishment 和偶发 rescue（`CL-EFF-009`）。Safety abort 也不是 reset；failure detection、containment、recovery、reset 和 resume 应分别记录。

### 6.5 Offline data 与 offline-to-online

Offline pretraining 可以让 target task 避免随机探索，并在少量 online trials 中调整。但 physical dataset 由 robot-hours、demonstrations、failures、labels、curation 和 hardware operation 构成。数据来源是否同 robot、camera、action interface 和 test distribution，也决定 transfer 是否真实。

因此应同时发布：

```text
target marginal cost
upstream dataset lifecycle cost
amortized cost over K target tasks
```

如果 prior 被许多任务复用，amortization 可能非常有利；如果 prior 与新任务高度专用，省下的 online cost 可能只是前移（`CL-EFF-005`）。

### 6.6 Demonstration、intervention 与 reward supervision

Demonstration 把危险随机探索替换为有信息的状态动作；intervention 在策略接近失败时提供纠正；success/reward classifier 把稀疏目标转成可训练信号。这些机制可提高每个 physical sample 的监督密度。

需要避免两种错误：

1. demonstration count 被当成 person-time；
2. intervention 被同时计作 safety、action label 和 reset 三份人工时。

正确做法是按时间区间计一次人工，再用 role tags 标记它提供的多种信息。Matched comparison 既要对齐 robot steps，也要对齐 active/standby operator-minutes（`CL-EFF-007`, `CL-EFF-008`）。

### 6.7 Residual control、procedural prior 与工程资产

Residual policy、base controller、task graph、teacher robot 和 fixture 能缩小 RL 搜索空间，并可能显著减少危险探索。它们不是“不纯”的方法，而是系统设计选择。

问题在于 engineering cost 通常不在论文的 sample/time 表中。该成本可能一次开发、多次复用，也可能每个 task 都要重做。应报告 development person-hours、integration、maintenance、适用任务数和 reuse count，而不是把它隐含为零（`CL-EFF-020`, `CL-EFF-024`）。

### 6.8 Adaptation

Meta-dynamics、behavior repertoire 和 teacher-mediated adaptation 把 from-scratch learning 改写为在 prior 附近的局部搜索。它们可以使 deployment phase 很短。

公平账本是：

```text
C_total(K) = C_pretrain + K * C_adapt
C_scratch(K) = K * C_from_scratch
```

只有同时给出 `C_pretrain`、`C_adapt`、reuse `K` 与 prior support，才能解释 few-minute result。Adaptation minutes 不能直接与 from-scratch minutes 排名（`CL-EFF-010`）。

## 7. 定量证据、缺失性与不可比较量

### 7.1 可追溯实例

下表有意保留 value、denominator、platform、locator、reporting status 与 interpretation limit。它展示“数值可审计”的写法，不构成排序。

| Work / metric | Value | Denominator | Physical platform | Locator | Reporting status | Interpretation limit |
|---|---|---|---|---|---|---|
| SERL reported phase duration | PCB 20 min; cable 31 min; paired relocation 105 min | source-defined task/policy phase; atomic rows in `time_ontology.csv` | Franka arm | PDF p.8 Table 2; pp.4,8; `QE-EFF-0001/0391` | source_reported | Strict target linkage is retained separately; relocation covers two policies and full lifecycle is not reported. |
| Walk in the Park interaction/time | 20,000 steps; about 17 min interaction and 20 min elapsed | one source-defined flat-ground learning run; four repeated hardware runs reported | Unitree Go1 | PDF p.1; p.2 Table I; p.3; pp.5–6; `QE-EFF-0342/0343/0352` | source_reported / approximate | Matched algorithm ablations are mainly simulated; task-specific result is not a cross-task unit. |
| MoDem-V2 task times | 8, 8, 70, 140 min | one main run for each of four source-defined tasks | Franka robot | PDF pp.5–6,9–10; `QE-EFF-0353` | source_reported | Demonstration collection and setup time are `NR`; single main run per task. |
| FastRLAP time | typically under 20 min, as little as 5 min; plots extend to 30–40 min | source-defined course/run | small autonomous ground vehicle | PDF pp.2–7,10; p.14 Table 4; `QE-EFF-0078/0083` | source_reported_approximate | Headline minimum must remain beside the longer plot horizon; lifecycle boundary is incomplete. |
| QT-Opt fleet scale | 7 robots; 580,000 attempts; about 800 aggregate robot-hours | full reported physical grasp corpus | seven KUKA arms | PDF pp.1–2,14,21; `QE-EFF-0388` | source_reported_approximate | Calendar duration, staffing, downtime and maintenance are `NR`; this is throughput, not low-sample evidence. |
| Real-ORL data/labor | over 800 robot-hours; over 270 human-hours | full reported data/evaluation lifecycle; over 6,500 train/evaluation trajectories | real-robot manipulation platform | PDF pp.1–2,5,10,16; `QE-EFF-0333/0335/0375` | source_reported_approximate | Dataset totals mix training/evaluation; platform count, calendar duration and staffing profile are `NR`. |
| REBOOT reset success | 0.608; 0.667; 0.367 | reset-policy evaluations for three reported objects/tasks | custom dexterous hand/camera system | PDF appendix E/F p.20; `QE-EFF-0377` | source_reported | Residual rescue and downtime are not quantified; values do not transfer to other reset systems. |
| World-Gymnast compute | 4×H200 140GB for RL; RL 1–2 days; world-model training also uses reported A100 resources | reported training job/model and optional about 100 real trajectories per task | AutoEval robot setup | PDF pp.4–7,15–16; appendix A.4 Table 5; `QE-EFF-0100/0107` | source_reported_approximate / source_reported | Main RL is in the model; full inherited physical-data collection is not reported. |
| PlayWorld upstream resources | 30 robot-hours play; 8×H200 for about 2 days world-model compute | full reported play collection/model training scope | DROID hardware setup | PDF pp.2,4–7,10,23; `QE-EFF-0126/0129` | source_reported | End-to-end task lifecycle and reset metrics are `NR`; method-specific code was not located at cutoff. |
| Cully et al. adaptation | under 2 min; at most about 20–30 physical controller tests; millions of simulated behaviors upstream | source-defined post-damage adaptation and predeployment repertoire | six-legged robot and robot arm | PDF p.1; Methods pp.18,20; `QE-EFF-0298/0300/0383` | source_reported_approximate | Not from-scratch learning; exact upstream compute and energy are `NR`. |

### 7.2 Missingness 是结果，不是空白字符

424 行账本由 34 篇 core work × 12 个标准维度的 408 行，加 16 个 supplemental rows 组成。时间采用双层 ontology：`reported_phase_duration` 记录来源给出的 run/data/model/program/task phase 时长，`time_to_declared_target` 只在 target、evaluator/checkpoint、task/phase 与 start/end boundary 均可定位时 available。下表中的 `NR` 表示在 verified source 中没有定位到符合该字段定义的值。

| 字段 | NR | 分母 | 平台 | Locator | Status | 解释限制 |
|---|---:|---:|---|---|---|---|
| Reported phase duration | 7 | 34 core works | cross-platform corpus | `CL-EFF-025`; [time ontology](data/time_ontology.csv) | executable-filter count | 只说明某个 phase 有时长，不自动说明何时达到目标。 |
| Strict time-to-declared-target | 20 | 34 core works | cross-platform corpus | `CL-EFF-025`; [time ontology](data/time_ontology.csv) | executable-filter count | 14/34 available；source-declared target 不等于 preregistered threshold。 |
| Physical steps/transitions | 22 | 34 core works | cross-platform corpus | `CL-EFF-013`; [quantitative ledger](data/quantitative_evidence.csv) | reviewer-counted missingness | 不同 control frequency/action repeat 下不可直接换算。 |
| Episodes/rollouts | 19 | 34 core works | cross-platform corpus | `CL-EFF-013`; [quantitative ledger](data/quantitative_evidence.csv) | reviewer-counted missingness | Episode horizon 与任务语义不同。 |
| Robot-hours | 16 | 34 core works | cross-platform corpus | `CL-EFF-014`; [quantitative ledger](data/quantitative_evidence.csv) | reviewer-counted missingness | Active、aggregate 与 elapsed 不能混用。 |
| Wall-clock | 8 | 34 core works | cross-platform corpus | `CL-EFF-014`; [quantitative ledger](data/quantitative_evidence.csv) | executable-filter count | Setup/reset/compute/downtime inclusion flags 不一致。 |
| Compute | 21 | 34 core works | cross-platform corpus | `CL-EFF-015`; [quantitative ledger](data/quantitative_evidence.csv) | reviewer-counted missingness | 仅有硬件型号也不足以得到 GPU-hours 或能耗。 |
| Evaluation denominator | 15 | 34 core works | cross-platform corpus | `CL-EFF-012`; [quantitative ledger](data/quantitative_evidence.csv) | reviewer-counted missingness | 没有 `k/n` 时 success rate 的不确定性不可审计。 |
| Control frequency | 30 | 34 core works | cross-platform corpus | `CL-EFF-016`; [quantitative ledger](data/quantitative_evidence.csv) | reviewer-counted missingness | 即使频率已知，idle/reset/action repeat 仍要记录。 |

整个 quantitative ledger 有 162 个 `not_reported` 行，value/unit/denominator 均保留 `NR`。其中的 19 个 numeric zero 只来自来源明确报告的 zero target-task demonstrations；每一个都有 [`zero_demo_basis.csv`](data/zero_demo_basis.csv) 中的 scope 与 upstream-data 限制，它们不是 missing-value imputation。

完整 lifecycle grid 另有 272 行（34 works × 8 channels）：230 格为 `not_reported`，35 格只有来源可定位的定量组件，7 格只有 qualitative/incomplete proxy；没有一篇报告完整生命周期总成本。因此本文把它写成“反复出现且重要的披露缺口”，而不是推断这些系统不安全、成本必然更高或某一 channel 已经精确量化（`CL-EFF-017`）。

### 7.3 为什么不能做 pooled ranking

跨论文至少有六组不一致：

1. embodiment、sensor、action、horizon 与 initial-state distribution；
2. success definition、threshold、trial denominator 与 evaluation cadence；
3. steps/episode 的时间语义；
4. reset、setup、compute、evaluation 和 maintenance 的 inclusion boundary；
5. fleet size、prior data、pretrained asset；
6. independent seed、site 与 failed run completeness。

因此语料不支持 global algorithm ranking 或 pooled effect size（`CL-EFF-023`）。允许的是在同 task、同 threshold、同 budget、同 boundary 和同 upstream assets 下做局部比较。

## 8. 方法解决了什么、把成本移到哪里、依赖什么假设

| 机制 | 直接解决 | 典型转移成本 | 必要假设 | 主要 failure mode |
|---|---|---|---|---|
| Replay / fast online | 重复利用 transitions，减少 learner idle | GPU、implementation、reward/reset pipeline | off-policy updates 稳定且 learner 不阻塞 control | stale data、latency、reward error |
| Black-box/model-based | 用模型或低维搜索减少 trials | compute、model calibration | dynamics 可在少量数据下预测 | contact discontinuity、model bias |
| Representation/goal | 提高视觉样本信息 | pretraining data、goal/reward design | latent distance 与任务进度一致 | shortcut、distribution shift |
| Fleet | 缩短 calendar time | capital、staffing、maintenance、logistics | data quality 在 actors 间一致 | bottleneck 转到 learner/operations |
| Reset/recovery | 减少 manual reset downtime | recovery data、fixture、reverse task | failure states 可检测且可恢复 | compounding failure、uncovered state |
| Offline-to-online | 避免 target random exploration | physical prior corpus、labels、curation | prior support 覆盖 target | distribution shift、hidden data bill |
| World model | 把 policy search 移出硬件 | real model data、GPU、energy | model captures task-critical physics | exploitation、unsafe transfer |
| Demonstration | 把随机探索换成 informative states | skilled operator、discarded attempts | demos 覆盖关键 support | narrow behavior、labor undercount |
| Intervention | 在线修正危险/低价值探索 | continuous monitoring、operator policy | intervention 及时且一致 | operator dependence、biased data |
| Reward classifier | 提供 dense/automatic supervision | labels/specification/audit | classifier 与 true success 对齐 | reward hacking、false success |
| Residual/base controller | 缩小 policy search | controller/fixture engineering | base policy 覆盖大部分任务 | controller mismatch、reuse failure |
| Adaptation | 避免每次 from scratch | repertoire/meta-data/teacher | perturbation 在 prior support 内 | OOD damage、amortization too small |

“转移”不等于“没有价值”。如果 upstream asset 可跨许多任务复用，转移可能是最经济的设计。要求只是把它公开并给出复用范围。

## 9. 统一评测协议

详细字段与公式见 [evaluation protocol](docs/evaluation_protocol.md)。最低协议包括：

### 9.1 冻结边界和目标

- 声明 `study_start`、`online_start`、`threshold_time`、`study_end`；
- 声明 development/failed runs 是否计入；
- 冻结 success event、`tau`、evaluation trial number、cadence、CI 与 right-censoring；
- 列出 prior assets cutoff 与 amortization rule。

### 9.2 发布四类 event log

1. physical interaction：task/reset/recovery/evaluation/development transitions；
2. reset/recovery/safety/maintenance：trigger、entry state、attempt、outcome、duration、fallback；
3. human intervals：active/standby、role tags、robot blocked、output units；
4. compute：phase、device、count、start/end、overlap with collection、energy。

### 9.3 同时给出四条学习曲线

- performance vs physical steps；
- performance vs active/aggregate robot-hours；
- performance vs elapsed wall-clock；
- performance vs operator-hours。

在可行时至少运行三个 independent seeds，保留 failure/abort。one-main-run 可作为 system feasibility evidence，不能给出稳定 effect size。

### 9.4 六个 comparison gates

| Gate | 必须匹配或校正 |
|---|---|
| G1 | task/platform/sensor/action/horizon/initial states |
| G2 | success definition/threshold/trials/uncertainty |
| G3 | steps/episodes/robot-hours 等 budget |
| G4 | reset/setup/demo/compute/evaluation/maintenance boundary |
| G5 | robot count/prior data/model/controller/accelerator |
| G6 | independent seeds/sites/hardware/failed runs |

任一 gate 不满足时，只报告各自可行性或共同覆盖的子账本，不声称 A 比 B 更省。

## 10. 研究缺口与可证伪实验

### P0：生命周期账本

同一任务比较 online replay、offline-to-online 和 world-model。预注册全生命周期 ledger，检验按 target robot-hours 的排序在加入 upstream data、human、compute、reset、maintenance 和 failed runs 后是否反转。排序反转就否定 headline proxy 的充分性。

### P0：operator occupancy

在相同 robot steps、active operator-minutes 和 presence-bound minutes 三种预算下比较 demonstration、intervention、learned recovery 与 scripted reset。若 intervention 优势在 matched operator budget 下消失，则 robot samples 不能单独代表效率。

### P0：E4 multi-site replication

至少三个 independent teams、两台硬件实例，冻结 commit、task、evaluator、reset protocol 和 target。若原论文的 cost interval 不能覆盖大部分 site results，则方法的 transportability 被否定，而不是通过 pooled mean 隐藏 site variance。

### P0：safety/wear/failed runs

把 collision、E-stop、fall、damage、maintenance、downtime 和 aborted seeds 计入所有 started runs。检验最少 successful-run samples 的方法是否仍最小化 `robot-hours / safe successful policy`；若排名反转，successful-run sample count 不是 safety-aware proxy。

### P1：fleet scaling

固定 learner、task distribution 和 target data volume，运行 1/2/4/8 robots。测 calendar time、aggregate robot-hours、staffing、maintenance、energy 与 policy lag。若 speedup 随 N 饱和，否定简单 `1/N` 日历模型。

### P1：world model Pareto surface

对 direct online、latent world model 和 video world 分别做 equal physical budget、equal compute budget 与 equal lifecycle budget。若优势仅在忽略某个资源时存在，则只能保留 bounded claim。

### P1：adaptation break-even

公布 `C_pretrain`、`C_adapt`、asset lifetime 和 `K*`。测试 prior support 内外的扰动。若 realistic deployment count 小于 break-even 或 OOD gain 消失，则否定 broad deployment-efficiency claim。

### P1：embodiment transfer

在 fixed manipulation、mobile manipulation、locomotion、dexterity 和 human-shared tasks 上使用同一 ledger。显著 task × mechanism interaction 会否定 embodiment-independent claim，并定义机制的适用域。

完整研究议程见 [research gaps](docs/research_gaps.md)。

## 11. 局限性

1. 公共检索路径可能漏掉只能通过付费数据库或非典型术语发现的工作。
2. 语料偏向结构化 manipulation，长期户外、soft robot、多机器人协作与 human-shared setting 更少。
3. Model-assisted screening 加 root verification 不是独立双人系统综述。
4. 已发表成功系统带来 publication/survivorship bias；失败开发运行通常不可得。
5. 截止日有五篇 core works 为 preprint，未来版本可能改变 metadata 或 evidence。
6. Missing displaced cost 只能被标记为 channel，不能估计 magnitude。
7. Source-reported number 也可能只覆盖 online subphase，不自动成为 lifecycle value。
8. Public repository/code status 随时间变化。
9. 本综述不做 pooled effect size，因此不能回答“平均提高多少百分比”。
10. Context sources 只支持 measurement framing，不支持 physical reliability。

## 12. 可维护性、数据文件与复现

### 12.1 十张表的职责

- [`papers.csv`](data/papers.csv)：36 篇 canonical identity、tiers、metrics、displaced cost、limitations；
- [`mechanism_matrix.csv`](data/mechanism_matrix.csv)：25 个 mechanisms 与 many-to-many work mapping；
- [`quantitative_evidence.csv`](data/quantitative_evidence.csv)：424 条带 denominator/platform/locator/status/limit 的数值与 missingness；
- [`time_ontology.csv`](data/time_ontology.csv)：88 条 atomic task/phase time records；
- [`hardware_roles.csv`](data/hardware_roles.csv)：learner/helper-reset/fleet/evaluation hardware roles；
- [`lifecycle_cost_grid.csv`](data/lifecycle_cost_grid.csv)：272 条完整 channel grid；
- [`tier_rationales.csv`](data/tier_rationales.csv)：36 条 E0–E4 判定理由；
- [`zero_demo_basis.csv`](data/zero_demo_basis.csv)：19 条 explicit-zero scope/basis；
- [`claims_ledger.csv`](data/claims_ledger.csv)：25 条可写入叙事的 bounded claims；
- [`claim_evidence.csv`](data/claim_evidence.csv)：509 条 claim→typed evidence→original locator 映射。

字段定义和 controlled values 见 [data schema](data/schema.md)。

### 12.2 更新顺序

1. 核验 original full text 和 canonical metadata；
2. 更新 paper row 与 BibTeX key；
3. 更新 quantitative rows，保持 source qualifier 和 locator；
4. 更新 mechanism mapping；
5. 先更新 claim ledger，再扩展 narrative；
6. 运行 validator 与 LaTeX build；
7. 不提交 PDF、local acquisition path 或 build artifact。

### 12.3 复现命令

```bash
make validate
python3 scripts/test_validator.py
make paper
make clean
```

离线 validator 使用 Python standard library，检查 required files、CSV schema/row widths、unique IDs、work coverage、BibTeX equality、LaTeX citations、Markdown relative links、URL syntax、cutoff/warnings、NR-zero invariants 和 forbidden artifacts。

## 13. 参考工作索引

### 13.1 Physical-robot core studies（34）

| Work ID | 年份 | R/E | 论文 |
|---|---:|---|---|
| `luo2024serl` | 2024 | R3/E2 | [SERL](https://doi.org/10.1109/ICRA57147.2024.10610040) |
| `luo2025hilserl` | 2025 | R3/E3 | [HIL-SERL](https://doi.org/10.1126/scirobotics.ads5033) |
| `liu2026autoserl` | 2026 | R3/E3 | [AutoSERL](https://arxiv.org/abs/2607.01651) |
| `walke2023ariel` | 2023 | R3/E3 | [ARIEL](https://proceedings.mlr.press/v205/walke23a.html) |
| `sun2022relmm` | 2022 | R4/E2 | [ReLMM](https://proceedings.mlr.press/v164/sun22a.html) |
| `hu2023reboot` | 2023 | R4/E3 | [REBOOT](https://proceedings.mlr.press/v229/hu23a.html) |
| `mendonca2025continuous` | 2025 | R4/E1 | [Continuously Improving Mobile Manipulation](https://proceedings.mlr.press/v270/mendonca25a.html) |
| `stachowicz2023fastrlap` | 2023 | R3/E3 | [FastRLAP](https://proceedings.mlr.press/v229/stachowicz23a.html) |
| `hu2025robottrainsrobot` | 2025 | R3/E3 | [Robot Trains Robot](https://openreview.net/forum?id=oRwcxFuN25) |
| `sharma2026worldgymnast` | 2026 | R3/E3 | [World-Gymnast](https://arxiv.org/abs/2602.02454) |
| `zhao2025silri` | 2025 | R3/E3 | [SiLRI](https://arxiv.org/abs/2512.24288) |
| `yin2026playworld` | 2026 | R3/E3 | [PlayWorld](https://arxiv.org/abs/2603.09030) |
| `haarnoja2019walk` | 2019 | R3/E1 | [Learning to Walk](https://doi.org/10.15607/RSS.2019.XV.011) |
| `zhan2022ferm` | 2022 | R3/E2 | [FERM](https://doi.org/10.1109/IROS47612.2022.9981055) |
| `tebbe2021tabletennis` | 2021 | R3/E1 | [Robotic Table Tennis](https://doi.org/10.1109/ICRA48506.2021.9560764) |
| `wu2023daydreamer` | 2023 | R3/E2 | [DayDreamer](https://proceedings.mlr.press/v205/wu23c.html) |
| `kalashnikov2018qtopt` | 2018 | R4/E2 | [QT-Opt](https://proceedings.mlr.press/v87/kalashnikov18a.html) |
| `kalashnikov2022mtopt` | 2022 | R4/E2 | [MT-Opt](https://proceedings.mlr.press/v164/kalashnikov22a.html) |
| `riedmiller2018sacx` | 2018 | R3/E1 | [SAC-X](https://proceedings.mlr.press/v80/riedmiller18a.html) |
| `nair2020awac` | 2020 | R3/E2 | [AWAC](https://arxiv.org/abs/2006.09359) |
| `singh2021cog` | 2021 | R2/E2 | [COG](https://proceedings.mlr.press/v155/singh21a.html) |
| `kumar2023ptr` | 2023 | R3/E3 | [PTR](https://roboticsproceedings.org/rss19/p019.html) |
| `chebotar2023qtransformer` | 2023 | R2/E2 | [Q-Transformer](https://proceedings.mlr.press/v229/chebotar23a.html) |
| `nair2018rig` | 2018 | R3/E2 | [RIG](https://proceedings.neurips.cc/paper/2018/hash/7ec69dd44416c46745f6edd947b470cd-Abstract.html) |
| `gupta2021resetfreemtl` | 2021 | R4/E1 | [Reset-Free Multi-Task RL](https://doi.org/10.1109/ICRA48506.2021.9561384) |
| `yang2020dataefficientlegged` | 2020 | R3/E1 | [Data-Efficient Legged RL](https://proceedings.mlr.press/v100/yang20a.html) |
| `nagabandi2019metarl` | 2019 | R2/E2 | [Meta-RL Adaptation](https://openreview.net/forum?id=HyztsoC5Y7) |
| `cully2015adaptanimals` | 2015 | R2/E3 | [Robots that Adapt Like Animals](https://doi.org/10.1038/nature14422) |
| `chatzilygeroudis2017blackdrops` | 2017 | R3/E2 | [Black-DROPS](https://doi.org/10.1109/IROS.2017.8202137) |
| `johannink2019residual` | 2019 | R3/E3 | [Residual RL](https://doi.org/10.1109/ICRA.2019.8794127) |
| `zhou2023realorl` | 2023 | R2/E2 | [Real-ORL](https://doi.org/10.1109/ICRA48891.2023.10161474) |
| `wurss2023locality` | 2023 | R3/E3 | [Walk in the Park](https://doi.org/10.15607/RSS.2023.XIX.056) |
| `lancaster2024modemv2` | 2024 | R3/E2 | [MoDem-V2](https://doi.org/10.1109/ICRA57147.2024.10611121) |
| `sharma2023medalpp` | 2023 | R3/E1 | [MEDAL++](https://proceedings.mlr.press/v229/sharma23b.html) |

### 13.2 Measurement/context sources（2）

| Work ID | 年份 | R/E | 论文 | 使用边界 |
|---|---:|---|---|---|
| `dulacarnold2019challenges` | 2019 | R0/E0 | [Challenges of Real-World Reinforcement Learning](https://mlanthology.org/icmlw/2019/dulacarnold2019icmlw-challenges/) | 只用于 problem definition。 |
| `dulacarnold2021challenges` | 2021 | R0/E0 | [Definitions, Benchmarks and Analysis](https://doi.org/10.1007/S10994-021-05961-4) | 只用于 measurement/benchmark context。 |

---

**三条不可删除的警告**

1. `NR` 不是零；numeric zero 只表示来源明确报告的零。
2. Context papers 不建立 physical-robot reliability。
3. 本语料不支持 universal algorithm ranking；局部比较必须通过统一 comparison gates。
