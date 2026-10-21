# Workflow smoke test — Issue #1

Local verification record for [Issue #1](https://github.com/batuzunoglu/scientific-experiment-selection/issues/1).
Status: local checks passed; researcher approved the local diff and publication. GitHub publication was pending when this record was prepared.
All outputs below were observed during this session, not simulated.

## Environment and starting state

Commands were run from `/home/batuhan/research/scientific-experiment-selection`.
Timestamps were sampled before verification:

| Command | Observed output | Exit code |
| --- | --- | --- |
| `date -u '+%Y-%m-%dT%H:%M:%SZ'` | `2026-10-21T15:36:48Z` | 0 |
| `date '+%Y-%m-%dT%H:%M:%S%:z (%Z)'` | `2026-10-21T11:36:48-04:00 (EDT)` | 0 |
| `git branch --show-current` | `test/workflow-issue-1` | 0 |
| `git status --short` | No output (clean starting working tree) | 0 |
| `git rev-parse HEAD` | `843946995a497adbd7710cb8eaf5f62aae77e4ae` | 0 |
| `uname -srmo` | `Linux 7.0.0-29-generic x86_64 GNU/Linux` | 0 |
| `uv --version` | `uv 0.13.4 (x86_64-unknown-linux-gnu)` | 0 |
| `uv run python --version` (approved retry) | `Python 3.12.14` | 0 |

`cat /etc/os-release` exited 0 and reported `PRETTY_NAME="Ubuntu 26.04.1 LTS"` (excerpt).

## Required checks

The following outputs are from approved retries outside the sandbox after the cache-access failures recorded below.

### Diagnostic — PASS (exit 0)

```sh
uv run python -m scientific_experiment_selection doctor
```

```text
project_version: 0.1.0
python_version: 3.12.14
platform: Linux
project_directory: /home/batuhan/research/scientific-experiment-selection
scientific_runs: none
OK: package imports and Python executes (not a scientific validation).
```

### Unit tests — PASS (exit 0; 2 tests)

```sh
uv run python -m unittest discover -s tests -v
```

```text
test_diagnostics_have_required_keys (test_doctor.InfrastructureSmokeTests.test_diagnostics_have_required_keys) ... ok
test_version (test_doctor.InfrastructureSmokeTests.test_version) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

## Initial failures and recovery

Each initial sandboxed uv command exited 2 before Python ran.

`uv run python --version`:

```text
error: Could not acquire lock
  cause: Could not create temporary file
  cause: Read-only file system (os error 30) at path "/home/batuhan/.cache/uv/.tmpa7ufpw"
```

`uv run python -m scientific_experiment_selection doctor`:

```text
error: Could not acquire lock
  cause: Could not create temporary file
  cause: Read-only file system (os error 30) at path "/home/batuhan/.cache/uv/.tmpS7G8QM"
```

`uv run python -m unittest discover -s tests -v`:

```text
error: Could not acquire lock
  cause: Could not create temporary file
  cause: Read-only file system (os error 30) at path "/home/batuhan/.cache/uv/.tmpePwYkc"
```

Issue retrieval also required recovery. `gh issue view 1 --repo batuzunoglu/scientific-experiment-selection` initially exited 1:

```text
error connecting to api.github.com
check your internet connection or https://githubstatus.com
```

The approved network retry of the same command exited 1:

```text
GraphQL: Projects (classic) is being deprecated in favor of the new Projects experience, see: https://github.blog/changelog/2024-05-23-sunset-notice-projects-classic/. (repository.issue.projectCards)
```

The following explicit-field query exited 0 and returned Issue #1's title, body, URL, number, and OPEN state:

```sh
gh issue view 1 --repo batuzunoglu/scientific-experiment-selection --json number,title,body,url,state
```

## Scope and remaining limits

- These checks establish package import/execution and two infrastructure assertions only. They do not establish scientific validity, model performance, or laboratory results.
- No scientific data, analysis code, evaluation rules, or dependency files were edited. No installation or autonomous agent setup was performed.
- At initial verification, no commit, push, pull request, or merge had been performed. The researcher subsequently replied `approve` to the local diff; commit, push, and PR creation are the next actions. Merge requires separate approval.
- GitHub visibility of this report and ChatGPT reading it through a connected repository remain unverified; the full workflow acceptance criteria are not yet complete.
- The handoff now links this report after researcher review, as requested in Issue #1.
