# Planner

Create the plan YAML File at `.harness/[nickname].yaml`

Read the repository README.md files and create a `.harness/dev_init.md` file with instructions that can run the development server.

Todo: eval - use said script to run repo

## Rules

1. Every task must be small enough to complete in a session. If it is too big, decompose into multiple sub-tasks.
2. If the task is unclear, ask the user clarifying questions.
3. Every task must have a list of acceptance criteria - non-negotiable, mandated by the evaluator.
4. Order tasks based on prerequisites and dependencies.
5. Add files related to the task at hand in the task yaml file section - to help the generator focus
6. Combine related requests into a single task.
7. Create a `.harness/progress.md` file to track progress notes and task completion checklist.` .harness/progress.md` is append-only.

## Task Breakdown Guidelines

Break the feature down into a list of end-to-end task descriptions.

#### Nickname

Use a hyphenated string, with not more than 3 words and not more than 32 characters.

It should be related to the task, human-readable and concise.

Examples:

`fix-info-button`, `add-mincount-var`, `add-logs`

#### Acceptance Criteria

- Specific
- Testable and quantifyable criteria
- Evaluator checks these
- a list of end-to-end feature descriptions

| BAD                  | GOOD                                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------------------------- |
| min_count is correct | Variable is explicitly typed as number (type = number)                                               |
| no errors            | terraform validate completes with no errors                                                          |
| terraform works     | terraform plan shows min_count updated to 10<br />terraform plan shows no unrelated resource changes |

Use this format to generate a list of tasks:

```yaml
nickname: update-min-count
feature: Update min_count in variables.tf
created: '2026-03-26'
status: planned|in_progress|complete
context: Brief description of why this work is needed and any relevant background
tasks:
  - id: '1'
    title: Update min_count variable in terraform to 10
    status: pending|in_progress|complete
    acceptance_criteria:
      - min_count is defined as a numeric variable with value 10 in
        src/datadog/variables.tf
      - 'Variable type enforces a number (e.g., type = number)'
      - terraform validate completes successfully with no errors
      - terraform plan runs successfully and reflects the updated min_count value
      - No unintended changes are introduced in the terraform plan output
    files:
      - src/datadog/variables.tf
    depends_on: []

```

- -
