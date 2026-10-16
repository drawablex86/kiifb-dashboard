# KIIFB Dashboard — Agent Kit

This starter kit contains the core instructions for building the KIIFB Accountability & Public Value Dashboard incrementally.

## Files

- `agent.md` — agent role, operating rules, evidence standards and task-driven workflow.
- `architecture.md` — recommended architecture, data model, data flow and technical decisions.
- `datasources.md` — source registry and download/acquisition instructions.
- `TASKS.md` — initial task board and acceptance criteria.

## Getting started in a repository

1. Copy these files into the repository root.
2. Ask your coding agent to read `agent.md`, `architecture.md`, `datasources.md`, and `TASKS.md`.
3. Instruct it to execute **T001 only** first: inspect the repository and report the baseline. It should not implement the entire dashboard in the first run.
4. Review the repo audit, then ask it to proceed to the next task or small batch.
5. Require it to update the task board and relevant documentation after every material change.

The agent should download public data into `data/raw/` when appropriate, preserve original files, create manifest entries and reproducible processed datasets, and update `datasources.md` whenever it discovers a source.

All figures listed in the instructions are provisional starting points until verified against their original source tables and reporting dates.
