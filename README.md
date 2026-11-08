# Prompt Regression Suite — Offline Baseline

A reproducible regression-testing scaffold using **real SQuAD v1.1 validation data**. It compares two deterministic answer-extraction configurations against the same questions, calculating normalized Exact Match and token F1 plus per-case deltas.

**Honest scope:** These configurations are *not* prompts executed against an LLM. This is a baseline for a future prompt regression runner. No Gemini inference has occurred, and results must not be advertised as Gemini or prompt performance.

## Run (Python 3.10+, standard library only)

```powershell
python -m unittest discover -s tests -v
python prompt_regression.py --limit 100
```

The runner downloads SQuAD validation data from Stanford's public URL on first use. It writes `regression_report.json`, which is gitignored. Internet access is needed for the initial download.

## Future work

- Replace heuristic configurations with real versioned prompt templates and model responses
- Add a Gemini adapter using environment variables, never hardcoded secrets
- Add regression gates, confidence intervals, and case-level review
- Expose a FastAPI endpoint for the unified React dashboard

Dataset: https://rajpurkar.github.io/SQuAD-explorer/

<!-- PORTFOLIO-OVERVIEW-START -->

## Project overview

Compare offline heuristic results against SQuAD references to detect evaluation regressions.

### Technologies and concepts

 - python
 - prompt testing
 - regression testing
 - squad
 - ai evaluation

### Repository information

- **Category:** AI Quality Engineering / Software Testing
- **Evaluation type:** Offline and/or synthetic fixtures, as documented in this repository
- **Source code:** [GitHub repository](https://github.com/gireeshvuyyuru501-design/prompt-regression-suite.git)
- **License:** MIT (subject to repository license file)

### AI Quality Engineering portfolio

This project is part of an 11-project portfolio covering evaluation datasets, structured-output validation, offline scoring, prompt regression, retrieval benchmarking, adversarial testing, agent tool calls, and quality monitoring.

[Explore the integrated AI Quality Engineering Platform](https://github.com/gireeshvuyyuru501-design/ai-quality-engineering-platform)

<!-- PORTFOLIO-OVERVIEW-END -->
