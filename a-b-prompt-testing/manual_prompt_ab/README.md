# Manual prompt A/B test

This folder runs the same customer inputs with Prompt A and Prompt B, then creates a side-by-side HTML report.

## Files

- `test_cases.jsonl` — customer test inputs and expected behavior.
- `run_ab_test.py` — runs both prompts on Amazon Bedrock.
- `ab_report.html` — readable A/B comparison report created after a run.
- `ab_results.csv` — raw output and latency data.

## 1. Required configuration

Open `.env` and set these values. Do not commit or share this file.

```env
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_TRACING=true
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=amazon.nova-pro-v1:0
```

AWS credentials must also have Amazon Bedrock model access in `us-east-1`.

## 2. Add test cases

Add one JSON object per line in `test_cases.jsonl`:

```json
{"id":"21","input":"Mera refund kab aayega?","expected":"refund status aur next step bataye"}
```

- `id` — unique case number.
- `input` — customer message.
- `expected` — ideal behavior to check in the answer.

## 3. Edit Prompt A and Prompt B

Open `run_ab_test.py`. In the `PROMPTS` section, Prompt A is the baseline and Prompt B is the changed version.

Change only the prompt instruction; keep the same test cases for a fair comparison.

## 4. Run the test

```powershell
python run_ab_test.py
```

Each test case creates two Bedrock calls: one for A and one for B.

## 5. Review the result

Open `ab_report.html` in a browser.

- Orange column = Prompt A.
- Green column = Prompt B.
- Compare answer quality, customer language, next step, latency, and invented details.

Choose the prompt that gives better quality with acceptable latency.

## Next step

For LangSmith Dataset and experiment evaluation, use `../langsmith_evaluation/README.md`.
