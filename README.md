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
