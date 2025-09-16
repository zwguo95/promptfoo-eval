# Chatbot Evaluation with Promptfoo

This repo contains reproducible configs and datasets for evaluating a SNAP/social safety net chatbot using [Promptfoo](https://promptfoo.dev/).

The evaluation pipeline checks:
- **Factual correctness** (letter-only multiple-choice answers)
- **Rationale quality** (LLM-as-judge rubric scoring)
- **Groundedness** (checks if explanations cite real sources)
- **Hygiene & latency** (basic safety and response time)

---

## Current Structure

- `configs/generateUniqueId.js` — helper script for consistent IDs  
- `configs/nava-provider.yaml` — provider config (Nava backend; expects `{{prompt}}`)  
- `dataset/tests.csv` — benchmark dataset (MCQ format, includes `question` and `__expected`)  
- `prompts/mcq-letter-only.txt` — wrapper prompt for factual accuracy tests  
- `promptfooconfig.yaml` — main Promptfoo config  
- `README.md` — documentation (this file)  

Users should provide their own **OpenAI/Nava API config** (via `.env` or provider YAML).

---

## Current Functionality

- **Letter-only MCQ evaluation**  
  - CSV contains `question` and `__expected` (like `A`, `B`, etc.).  
  - Prompt wrapper enforces single-letter answers.  
  - Assertions check both output shape (`^[A-E]$`) and match with `__expected`.

---

## Usage

1. **Install Promptfoo**  
   ```bash
   npm install -g promptfoo
````

2. **Configure API keys**
   Create `.env` in the repo root (add `.env` to `.gitignore`):

   ```bash
   OPENAI_API_KEY="your_api_key_here"
   ```

3. **Run evaluations**

   ```bash
   # Run all tests (letter-only by default)
   npx promptfoo eval -c promptfooconfig.yaml

   # View results interactively
   npx promptfoo view -c promptfooconfig.yaml
   ```

   > In the viewer, enable **Table Settings → Show full prompt** to confirm that the wrapper prompt is being sent instead of the raw question.

---

## Planned Improvements

* Add **rationale scenario**: full answer with rationale and citations.
* Add **rubric-based grading** with `gpt-4o-mini` as judge for rationale quality and groundedness.
* Support running subsets with tags (`--tags letter-only`, `--tags rationale`).
* Standardize provider configs for easier onboarding.
