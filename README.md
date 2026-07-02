# LLM_with_better_memorizing_ability
Final year project : Building a llm chatbot with better memorizing ability using context engineering

This project is inspired by Context research by Chroma.
Here’s a polished **GitHub README** draft tailored to your final-year project report. It highlights the technical depth, experimental rigor, and practical relevance of your work while keeping it recruiter- and developer-friendly:

---

# 🤖 Troubleshooting Copilot for ML Workloads – Context Rot

## 📌 Overview
This repository contains the code and experiments for my **final-year project at The Chinese University of Hong Kong**.  
The project investigates **context rot in Large Language Models (LLMs)** and proposes a novel **cropping-based suppression method** to improve chatbot performance when handling long context windows.  

Key contributions:
- ⚡ **Cropping vs. Summarizing**: Demonstrates that cropping preserves more task-critical information than recursive summarization.  
- 🧠 **Memorization & Cohesion**: Improves chatbot memory retention and code cohesion in ML troubleshooting scenarios.  
- 📊 **Evaluation Framework**: Benchmarked on **MT-Bench** and **NextCoder-Conversational** datasets with custom metrics.  
- 🔒 **Secure Coding Practices**: Ensures minimal, safe modifications to user-provided ML code snippets.  

---

## 🛠 Features
- **Advantage of cropping**
-   - Selectively retains useful information (code, parameters, hardware details)
    - Discarding redundant explanations.
    - Logical discontinous may slightly enhance the memorizing ability


---

## 📂 Project Structure
```
├── src/                 # Core chatbot and suppression methods
│   ├── cropping/        # Cropping-based suppression logic
│   ├── summarizing/     # Baseline summarization approach
│   ├── evaluation/      # Metrics & LLM-as-a-judge scripts
├── experiments/         # Results, tables, and figures
├── docs/                # Final report and notes
└── README.md            # Project overview
```

---

## ⚙️ Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/Paul1231231/LLM_with_better_memorizing_ability.git
cd LLM_with_better_memorizing_ability
```

---

## 🚀 Usage
Run chatbot with cropping suppression:
```bash
python src/cropping/chatbot.py 
```

Run baseline summarization chatbot:
```bash
python src/summarizing/chatbot.py 
```

Evaluate with custom metrics:
```bash
python src/evaluation/run_eval.py --metric memorizing
```

---

## 📊 Results
- **Memorizing Ability**: Cropping outperforms summarization by **14.6%** on MT-Bench.  
- **Coding Cohesion**: Cropping achieves **+30% higher pass rate** in preserving user code.  
- **Suppression Ratio**: Cropping reduces context size by ~41% while retaining critical details.  

---

## 🔒 Security Notes
- Minimal edits to user code to avoid introducing vulnerabilities.  
- Input validation and safe handling of ML scripts.  

---

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for details.

---

Got it — let’s add a **KV cache defense section** to your README so that anyone reviewing your repo understands the design trade-offs clearly. Here’s a suggested addition:

---

## ⚡ KV Cache Behavior

Unlike traditional chatbots that store the KV cache as:

```
System Prompt > Q1 > A1 > Q2 > A2 > ...
```

our cropping-based chatbot maintains the cache as:

```
System Prompt > Crop Message 1 > Crop Message 2 > ...
```

This means the cropped message is re‑fed into the cache each time, slightly increasing the token input compared to a traditional chatbot.  

### Why this is acceptable:
- **Alignment with modern LLM usage**: Long chains of thought and reasoning tokens are already common in advanced LLM workflows. Higher token input is becoming the norm.  
- **Preservation of critical details**: Cropping ensures that code snippets, parameters, and user intent are retained, which outweighs the cost of extra tokens.  
- **Trade-off**: The only drawback is the **time required for cropping**, but this is offset by the improved memorization ability and code cohesion demonstrated in experiments.  

In short, while the KV cache grows differently than in traditional chatbots, the design is intentional and justified by the performance gains in ML troubleshooting scenarios.



