# Research Charter — Approved Roadmap

**Working title:** Scientific Experiment Selection with Reinforcement Learning and AI Agents

**Research goal:** Develop and compare AI systems that select useful scientific experiments, improve or verify predictive models under changing laboratory conditions, and reduce experimental cost.

**Initial testbed:** Ce–ARS UV–Vis spectroscopy for PFAS detection. Raw measurements and historical well labels require evidence-aware processing; uncertain identities and QC records must not be silently treated as verified.

## Six phases

1. **Data preparation and baseline ML.** Build a traceable dataset; train baseline models to identify individual PFAS compounds; measure generalization across experimental batches.
2. **Traditional experiment selection.** Benchmark random selection, design of experiments (DoE), active learning and Bayesian experimental-design/optimization strategies under matched experimental budgets.
3. **Reinforcement learning.** Implement a sequential experiment-selection environment; design, test and explain rewards for model improvement, experimental cost and decision validity; train numerical RL policies against the traditional baselines.
4. **Scientific AI agents.** Build and compare prompt-only SLM agents, tool-using SLM agents, RL-trained SLM agents and useful hybrid agent/Bayesian strategies. Measure tool-call validity, decision quality, cost and reliability.
5. **Real laboratory validation.** Run additional physical measurements when needed, including prospective closed-loop comparisons with fixed budgets, independent evaluation data and human approval of laboratory actions.
6. **Research publication and portfolio.** Report results and limitations with reproducible code and evidence-backed figures; prepare the PhD proposal, manuscript and an accessible GitHub portfolio.

**Core commitment:** RL, reward engineering and tool-using / RL-trained scientific agents are central comparison arms, not optional add-ons. No method is assumed to outperform simpler baselines. If an RL/SLM approach cannot be credibly trained with existing observations, establish a documented simulator or replay benchmark, then seek new physical data where scientifically useful. Distinguish simulated and prospective experimental evidence.

## First practical milestone

Start with **two coequal single-analyte supervised tasks**: six-class PFAS identity classification and PFAS concentration regression, evaluated separately because preprocessing may affect chemical identity and absolute absorbance information differently. Preserve a Raw-spectrum comparator; exact transformations and feature sets require scientific review. **Proposed** datasets: Exp3 for training/development (72 candidate wells), Exp5 for external-batch evaluation (53 candidates), and Exp8 as a locked final independent-batch holdout (18 candidates). These counts are *candidate* historical labels, not individually verified preparations. Preserve exclusions, review flags and all unresolved composition conflicts.

Work begins at [Issue #5](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5): Phase A, dataset contract / reproducible non-fitting preprocessing, before any model fitting. The first ML experiments are a prerequisite to meaningful RL/agent comparison, **not** the final research objective.

## Evaluation and research safeguards

- Protect untouched test data from model choice, feature selection, reward design and agent tool access; do not confuse technical replicates with independent batches.
- Use the same candidate experiments, lab-budget constraints, held-out evaluation and stopping criteria for all experiment-selection approaches.
- Report performance versus experiment budget, uncertainty, reliability, action/tool errors, failure cases and variability over seeds/scenarios.
- Never invent measurements or outcomes, infer preparation identities from spectral shape alone, or claim unpublished simulation outputs as wet-lab results.
- Keep original raw exports unchanged, cite provenance, review public sharing scope, and use a human-in-the-loop gate for new laboratory actions.

**Deliverables:** reproducible scientific software, comparison benchmark, trained/evaluated RL and SLM-agent prototypes, prospective laboratory validation, PhD proposal, manuscript, and a job/internship-ready portfolio.

Document every new substantive methodological decision and observed outcome in the append-only [Research Lab Notebook](RESEARCH_LAB_NOTEBOOK.md), distinguishing approvals, proposals and past experimental evidence.

**Open technical decisions:** exact supervised targets and split approvals; action/state space; reward weights; group/batch independence; simulator reliability; model adaptation procedure; experiment costs and protocols; SLM training feasibility. These are engineering/research choices to test and document, not reasons to drop the committed RL or agent comparison arms.
