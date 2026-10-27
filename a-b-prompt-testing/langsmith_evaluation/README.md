# LangSmith evaluation

This folder contains the LangSmith-only setup. It reuses test cases and the LangSmith API key from `../bedrock_prompt_ab`.

Run:

```powershell
python setup_dataset.py
```

Then run both prompt experiments:

```powershell
python run_experiments.py
```

Before running, add `GEMINI_API_KEY` to `../bedrock_prompt_ab/.env`. The script uses Gemini's HTTP API as an offline judge and saves a `support_quality` score into each LangSmith experiment; no extra Python package is needed.
