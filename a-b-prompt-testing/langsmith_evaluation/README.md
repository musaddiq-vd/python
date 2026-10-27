# LangSmith evaluation

This folder runs and compares Prompt A vs Prompt B using the Bedrock customer-support test cases.

## Files

- `setup_dataset.py` — uploads local test cases to a LangSmith Dataset.
- `run_experiments.py` — runs Prompt A and B on that Dataset and adds the Gemini `support_quality` score.

## 1. Required configuration

Open `../bedrock_prompt_ab/.env` and set these values. Never commit this file.

```env
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_TRACING=true
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=amazon.nova-pro-v1:0
GEMINI_API_KEY=your_gemini_key
GEMINI_JUDGE_MODEL=gemini-3.6-flash
TEST_LIMIT=5
JUDGE_DELAY_SECONDS=5
```

`TEST_LIMIT=5` and the delay keep Gemini requests below rate limits. Increase the limit only after a successful small run.

## 2. Create the LangSmith Dataset (run once)

From this folder:

```powershell
python setup_dataset.py
```

This creates `bedrock-customer-support-ab` in LangSmith and uploads the cases from `../bedrock_prompt_ab/test_cases.jsonl`.

## 3. Run the A/B experiment

```powershell
python run_experiments.py
```

The script runs both prompts against the configured number of dataset cases. It prints LangSmith links for the Prompt A and Prompt B experiments.

## 4. Review the result

Open the printed LangSmith links and compare:

- `support_quality`: `1` = passes the rubric; `0` = fails.
- latency: lower is faster.
- model output: it should follow the customer's language and expected behavior.

## If Gemini returns HTTP 429

Wait for the API quota to reset, keep `TEST_LIMIT=5`, and run the command again. Do not run repeated 20-case batches on a free/limited API key.
