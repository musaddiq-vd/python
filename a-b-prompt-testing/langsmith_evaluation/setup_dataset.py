"""Create the reusable LangSmith dataset from the local Bedrock A/B test cases."""
import json
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client

BASE_DIR = Path(__file__).resolve().parent
TEST_CASES = BASE_DIR.parent / "bedrock_prompt_ab" / "test_cases.jsonl"
DATASET_NAME = "bedrock-customer-support-ab"

# Reuses the LangSmith key already stored with the Bedrock test project.
load_dotenv(BASE_DIR.parent / "bedrock_prompt_ab" / ".env")


def main() -> None:
    client = Client()
    if client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset already exists: {DATASET_NAME}")
        return

    client.create_dataset(DATASET_NAME, description="Customer-support cases for Bedrock prompt A/B evaluations.")
    with TEST_CASES.open(encoding="utf-8") as cases_file:
        examples = [
            {"inputs": {"customer_input": case["input"]}, "outputs": {"expected_behavior": case["expected"]}, "metadata": {"case_id": case["id"]}}
            for line in cases_file if (case := json.loads(line))
        ]
    client.create_examples(dataset_name=DATASET_NAME, examples=examples)
    print(f"Created {DATASET_NAME} with {len(examples)} test cases in LangSmith.")


if __name__ == "__main__":
    main()
