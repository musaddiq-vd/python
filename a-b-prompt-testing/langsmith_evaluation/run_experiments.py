"""Run Prompt A and Prompt B as separate LangSmith experiments."""
import os
import json
import time
import urllib.request
from pathlib import Path

import boto3
from dotenv import load_dotenv
from langsmith import Client

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / "bedrock_prompt_ab" / ".env")

DATASET_NAME = "bedrock-customer-support-ab"
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-pro-v1:0")
REGION = os.getenv("AWS_REGION", "us-east-1")
PROMPTS = {
    "A": "You are a support agent. Answer the customer clearly.",
    "B": (
        "You are a calm customer-support agent. Reply in the customer's language, "
        "acknowledge the issue, give one concrete next step, and never invent order details."
    ),
}

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
langsmith = Client()
JUDGE_MODEL = os.environ.get("GEMINI_JUDGE_MODEL", "gemini-3.6-flash")
TEST_LIMIT = int(os.environ.get("TEST_LIMIT", "5"))
JUDGE_DELAY_SECONDS = float(os.environ.get("JUDGE_DELAY_SECONDS", "5"))


def target(prompt_name: str):
    def run(inputs: dict) -> dict:
        start = time.perf_counter()
        response = bedrock.converse(
            modelId=MODEL_ID,
            system=[{"text": PROMPTS[prompt_name]}],
            messages=[{"role": "user", "content": [{"text": inputs["customer_input"]}]}],
            inferenceConfig={"maxTokens": 250, "temperature": 0},
        )
        return {
            "response": response["output"]["message"]["content"][0]["text"],
            "latency_seconds": round(time.perf_counter() - start, 2),
        }
    return run


def support_quality(run, example) -> dict:
    """Ask Gemini to judge one generated customer-support response."""
    customer_input = example.inputs["customer_input"]
    expected = example.outputs["expected_behavior"]
    response = run.outputs["response"]
    judge_prompt = f"""You are grading a customer-support answer.
Customer input: {customer_input}
Expected behavior: {expected}
Model response: {response}

Give score 1 only if the response follows expected behavior, uses the customer's language,
is polite, gives a concrete next step, and invents no details. Otherwise give 0.
Return JSON only: {{"score": 0 or 1, "reason": "short reason"}}."""
    time.sleep(JUDGE_DELAY_SECONDS)
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{JUDGE_MODEL}:generateContent",
        data=json.dumps({"contents": [{"parts": [{"text": judge_prompt}]}]}).encode("utf-8"),
        headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as api_response:
        result_text = json.loads(api_response.read())["candidates"][0]["content"]["parts"][0]["text"]
    data = json.loads(result_text.strip().removeprefix("```json").removesuffix("```").strip())
    return {"key": "support_quality", "score": data["score"], "comment": data["reason"]}


def main() -> None:
    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError("Add GEMINI_API_KEY to ../bedrock_prompt_ab/.env before running.")
    examples = list(langsmith.list_examples(dataset_name=DATASET_NAME))[:TEST_LIMIT]
    for variant in PROMPTS:
        results = langsmith.evaluate(
            target(variant),
            data=examples,
            experiment_prefix=f"bedrock-prompt-{variant}",
            description=f"Amazon Bedrock {MODEL_ID}: Prompt {variant} on customer-support dataset.",
            metadata={"prompt_variant": variant, "model": MODEL_ID, "region": REGION},
            max_concurrency=1,
            evaluators=[support_quality],
        )
        print(f"Prompt {variant} experiment: {results.url}")


if __name__ == "__main__":
    main()
