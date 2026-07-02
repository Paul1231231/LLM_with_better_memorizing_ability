import os
import json
import pandas as pd
import boto3
from botocore.config import Config
from datasets import load_dataset

# ---------- Config ----------
a = 77
b = 100
OUTPUT_DIR = "summ_code"
os.makedirs(OUTPUT_DIR, exist_ok=True)
AWS_REGION = "us-east-1"
MODEL_ID = "openai.gpt-oss-20b-1:0"   # change if your account uses a different ID
SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "You must answer only from your internal knowledge and the conversation context."
    "If information is uncertain or may be outdated, say so clearly."
)

# ---------- Bedrock client ----------
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    config=Config(retries={"max_attempts": 3, "mode": "standard"})
)

def converse(messages, system_prompt, max_tokens=1024, temperature=0.3):
    """
    messages format (Converse API):
    [
      {"role":"user"|"assistant", "content":[{"text":"..."}]}
    ]
    """
    resp = bedrock.converse(
        modelId=MODEL_ID,
        system=[{"text": system_prompt}],
        messages=messages,
        inferenceConfig={
            "maxTokens": max_tokens,
            "temperature": temperature,
        },
        # No tools, no KB retrieval => no internet retrieval path
    )
    text = resp["output"]["message"]["content"][1]["text"]
    usage = resp.get("usage", {})
    out_tokens = usage.get("outputTokens", None)
    return text, usage, out_tokens

def summarize(question, answer):
    """
    Summarize assistant output into compact actionable memory.
    """
    system_prompt = (
        "Please summarizes the chat history for future conversation."
    )
    user_text = f"Question: {question}\nAnswer: {answer}"

    messages = [
        {"role": "user", "content": [{"text": user_text}]}
    ]
    summary_text, usage, out_tokens = converse(
        messages=messages,
        system_prompt=system_prompt,
        max_tokens=3000,
        temperature=0.2,
    )
    return summary_text, usage, out_tokens
# =========================
# Load dataset
# =========================
dataset = load_dataset(
    "arrow",
    data_files={
        "train": "hf://datasets/microsoft/NextCoderDataset-Conversational/data-00000-of-00001.arrow"
    },
)


cropped_ratio = []

for i in range(a, b):
    # Keep conversation for output file (full responses)
    conversation = []

    # Messages sent to model (your compressed-memory style)
    # In Converse API, system prompt is separate, so keep only user/assistant turns here.
    messages = []

    main_system_prompt = "You are a chatbot."

    for j in range(2):
        k = (j + 1) * 2
        user_input = dataset["train"][i]["messages"][k]["content"]

        # Record user in output conversation + send to model
        conversation.append({"role": "user", "content": user_input})
        messages.append({"role": "user", "content": [{"text": user_input}]})

        # Generate assistant answer
        answer_text, usage_main, out_tokens_main = converse(
            messages=messages,
            system_prompt=main_system_prompt,
            max_tokens=5000,
            temperature=0.3,
        )

        conversation.append({"role": "assistant", "content": answer_text})

        # Summarize/crop answer
        cropped_text, usage_sum, out_tokens_sum = summarize(user_input, answer_text)

        # Compute crop ratio
        # Prefer token counts from Bedrock usage; fallback to text length ratio if missing.

        ratio = out_tokens_sum / out_tokens_main


        cropped_ratio.append(ratio)

        # Replace last user message with summarized assistant memory (matches your original logic)
        # Original code did: pop user then append summarized assistant.
        messages.pop()
        messages.append({"role": "assistant", "content": [{"text": cropped_text}]})

    # Write conversation JSON
    file_name = f"question_{i}.json"
    filepath = os.path.join(OUTPUT_DIR, file_name)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(conversation, f, indent=2, ensure_ascii=False)

    print(f"Done question {i}")

# Save crop ratios
df = pd.DataFrame(cropped_ratio, columns=["crop_ratio"])
df.to_csv("summ_code_1.csv", index=False)
print("Saved crop_code_1.csv")
