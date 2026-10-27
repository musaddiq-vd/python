"""Run Prompt A and Prompt B against the same Amazon Bedrock test cases. and saves .html file"""
import csv
import html
import json
import os
import time

import boto3
from langsmith import traceable
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-pro-v1:0")
REGION = os.getenv("AWS_REGION", "ap-south-1")

PROMPTS = {
    "A": "You are a support agent. Answer the customer clearly.",
    "B": (
        "You are a calm customer-support agent. Reply in the customer's language, "
        "acknowledge the issue, give one concrete next step, and never invent order details."
    ),
}

client = boto3.client("bedrock-runtime", region_name=REGION)


@traceable(name="bedrock_prompt_ab")
def ask(prompt_name: str, customer_input: str) -> tuple[str, float]:
    start = time.perf_counter()
    response = client.converse(
        modelId=MODEL_ID,
        system=[{"text": PROMPTS[prompt_name]}],
        messages=[{"role": "user", "content": [{"text": customer_input}]}],
        inferenceConfig={"maxTokens": 250, "temperature": 0},
    )
    output = response["output"]["message"]["content"][0]["text"]
    return output, round(time.perf_counter() - start, 2)


def main() -> None:
    cases = [json.loads(line) for line in open("test_cases.jsonl", encoding="utf-8")]
    results = []
    for case in cases:
        for variant in PROMPTS:
            output, latency = ask(variant, case["input"])
            results.append({**case, "variant": variant, "output": output, "latency_seconds": latency})
    with open("ab_results.csv", "w", newline="", encoding="utf-8") as result_file:
        writer = csv.DictWriter(result_file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    create_html_report(results)
    print("Saved ab_results.csv and ab_report.html.")


def create_html_report(results: list[dict]) -> None:
    grouped = {}
    for result in results:
        grouped.setdefault(result["id"], {"input": result["input"], "expected": result["expected"]})[result["variant"]] = result

    rows = []
    for case in grouped.values():
        a, b = case["A"], case["B"]
        rows.append(f"""<tr>
          <td>{html.escape(case['input'])}</td>
          <td>{html.escape(case['expected'])}</td>
          <td>{html.escape(a['output'])}<small>{a['latency_seconds']} sec</small></td>
          <td>{html.escape(b['output'])}<small>{b['latency_seconds']} sec</small></td>
        </tr>""")

    report = f"""<!doctype html><html><head><meta charset='utf-8'><title>Prompt A/B Report</title>
    <style>body{{font-family:Arial; margin:32px; color:#172033}} table{{border-collapse:collapse;width:100%}}
    th,td{{border:1px solid #ccd4df;padding:14px;vertical-align:top;text-align:left;white-space:pre-wrap;line-height:1.45}}
    th{{background:#172033;color:white}} td:nth-child(3){{background:#fff7ed}} td:nth-child(4){{background:#effcf5}}
    small{{display:block;color:#667085;margin-top:12px}}</style></head><body>
    <h1>Prompt A/B Test Report</h1><p>Compare the orange Prompt A column with the green Prompt B column.</p>
    <table><thead><tr><th>Customer input</th><th>Expected</th><th>Prompt A</th><th>Prompt B</th></tr></thead>
    <tbody>{''.join(rows)}</tbody></table></body></html>"""
    with open("ab_report.html", "w", encoding="utf-8") as report_file:
        report_file.write(report)


if __name__ == "__main__":
    main()
