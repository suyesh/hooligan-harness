---
name: harness
description: Implements a high-reliability "Harness Engineering" loop using Planner, Generator, and Evaluator personas. Trigger when a user wants to "implement a feature," "start the harness," or "build with verification."
version: 1.0.0
---
## Objective

To replace one-shot code generation with a structured, self-correcting agentic loop that ensures all code is planned in YAML, implemented via best practices of coding, and verified by an adversarial evaluator before declared complete.

## Instructions

### 1. Phase 0: Initialization

* Read the repository README.md to understand the environment.
* Create .harness/dev_init.md with instructions to run the development server for downstream agents.

### 2. Phase 1: Planning (The Planner)

* Create a technical roadmap at .harness/[nickname].yaml.
* Define specific, quantifiable Acceptance Criteria (AC) for every task.
* Initialize an append-only log at .harness/progress.md to track all session activity.

### 3. Phase 2: Implementation (The Generator)

* Select Task: Identify the next pending task based on depends_on logic.
* Logic Synthesis: Perform an impact analysis and define a testing strategy before writing code.
* Code Generation: Implement logic following SOLID, DRY, and KISS principles.
* Atomic Updates: Every task completion requires a git commit and a progress entry.

### 4. Phase 3: Adversarial Evaluation (The Evaluator)

* Hostile Barrier: Assume the Generator's output is riddled with bugs and happy-path logic.
* Instant Death Gates: Immediately FAIL the task if there is a global regression, linting error, or any lazy code such as placeholders like TODO or FIXME.
* AC Deep-Dive: Confirm every AC has a dedicated test and that test quality metrics like Mock Integrity and Coverage Stability are met.
* Verdict: Return a binary PASS or FAIL. If FAIL, provide a root cause analysis.

### 5. Phase 4: Remediation and Reconciliation

* Remediation: If the Evaluator returns FAIL, the Generator must suspend new work, reproduce the failure locally, and fix the logic until it passes evaluation.
* Reconciliation: Once PASS is achieved, update the YAML task status to done and log the verification evidence including the git hash and test results in progress.md.

## Reference

* Persona - Planner: Focuses on structured YAML roadmap creation and task decomposition.
* Persona - Generator: Focuses on defensive programming, architectural synthesis, and local verification.
* Persona - Evaluator: Acts as the gatekeeper using a Zero-Trust approach to code quality.
