---
name: harness
description: Implements a high-reliability "Harness Engineering" loop using Planner, Generator, and Evaluator personas with parallel security evaluation, failure pattern learning, and confidence scoring. Trigger when a user wants to "implement a feature," "start the harness," or "build with verification."
version: 1.1.0
---
## Objective

To replace one-shot code generation with a structured, self-correcting agentic loop that ensures all code is planned in YAML, implemented via best practices of coding, and verified by parallel adversarial evaluators (functional and security) with confidence-based validation levels and failure pattern learning before declared complete.

## Instructions

### 1. Phase 0: Initialization

* Read the repository README.md to understand the environment.
* Create .harness/dev_init.md with instructions to run the development server for downstream agents.
* Load .harness/knowledge/failure-patterns.yaml to understand common failure patterns.
* Initialize confidence scoring based on task complexity and historical performance.

### 2. Phase 1: Planning (The Planner)

* Create a technical roadmap at .harness/[nickname].yaml.
* Define specific, quantifiable Acceptance Criteria (AC) for every task.
* Initialize an append-only log at .harness/progress.md to track all session activity.

### 3. Phase 2: Implementation (The Generator)

* Select Task: Identify the next pending task based on depends_on logic.
* Confidence Assessment: Calculate confidence score using .harness/knowledge/confidence-scoring.yaml.
* Logic Synthesis: Perform an impact analysis and define a testing strategy before writing code.
* Pattern Check: Review .harness/knowledge/failure-patterns.yaml for relevant patterns to avoid.
* Code Generation: Implement logic following SOLID, DRY, and KISS principles with pattern-aware defensive coding.
* Atomic Updates: Every task completion requires a git commit and a progress entry.

### 4. Phase 3: Parallel Adversarial Evaluation

#### 4a. Functional Evaluation (The Evaluator)
* Hostile Barrier: Assume the Generator's output is riddled with bugs and happy-path logic.
* Instant Death Gates: Immediately FAIL the task if there is a global regression, linting error, or any lazy code such as placeholders like TODO or FIXME.
* AC Deep-Dive: Confirm every AC has a dedicated test and that test quality metrics like Mock Integrity and Coverage Stability are met.
* Verdict: Return a binary PASS or FAIL. If FAIL, provide a root cause analysis.

#### 4b. Security Evaluation (The Security Evaluator) - Runs in Parallel
* Security Scanning: Check for OWASP Top 10 vulnerabilities and security anti-patterns.
* Dependency Audit: Verify no known CVEs in dependencies.
* Secret Detection: Scan for hardcoded credentials or API keys.
* Verdict: Return PASS or FAIL with specific security findings.

Both evaluators must return PASS for the task to be considered complete.

### 5. Phase 4: Remediation and Reconciliation

* Remediation: If any Evaluator returns FAIL, the Generator must suspend new work, reproduce the failure locally, and fix the logic until it passes evaluation.
* Pattern Learning: Update .harness/knowledge/failure-patterns.yaml with new failure patterns discovered.
* Confidence Adjustment: Decrease confidence score for similar future tasks based on failure type.
* Reconciliation: Once PASS is achieved, update the YAML task status to done and log the verification evidence including the git hash and test results in progress.md.
* Success Learning: Increase confidence scores and update pattern effectiveness metrics for successful implementations.

## Reference

* Persona - Planner: Focuses on structured YAML roadmap creation and task decomposition.
* Persona - Generator: Focuses on defensive programming, architectural synthesis, and local verification with pattern-aware implementation.
* Persona - Evaluator: Acts as the gatekeeper using a Zero-Trust approach to code quality.
* Persona - Security Evaluator: Parallel security-focused evaluation for vulnerabilities and security best practices.
* Knowledge - Failure Patterns: Learning system that captures and prevents recurring failure patterns.
* Knowledge - Confidence Scoring: Adaptive scoring system that adjusts validation requirements based on task complexity and historical performance.
