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
- `configs/nava-provider.yaml` — provider config (Nava backend)
- `datasets/tests.csv` — benchmark dataset (MCQ format)
- `promptfooconfig.yaml` — main Promptfoo config
- `README.md` — documentation (this file)

Users are expected to provide their own **OpenAI API config** (via `.env` or provider YAML).  
We plan to make this more standardized once external providers are fully integrated.

---

## Current Functionality

- **MCQ factual accuracy**  
  - Uses dataset `tests.csv` with `__expected` answers.  
  - Evaluated via `equals` and `contains` assertions.

- **Rationale evaluation (draft)**  
  - Rubric-based scoring (`gpt-4o-mini` as judge).  
  - Checks quality and groundedness of explanations.  

---

## Planned Improvements

1. **Wrapper prompt for MCQs**  
   - Transform CSV question + expected answer into a provider-ready prompt.  
   - Ensure models return **letter-only** answers for factual tests.

2. **Full response grading**  
   - Expand tests to include rationale generation.  
   - Apply rubrics for **quality** and **groundedness**.

3. **Hybrid test blocks**  
   - Support both:
     - Inline/custom prompts (ad-hoc experiments)  
     - Dataset-driven evaluations (CSV)  
   - Allow running subsets with `tags: [letter-only, rationale]`.

---

## Next Steps

- [ ] Implement wrapper prompt for MCQ factual correctness.  
- [ ] Finalize rationale & groundedness rubrics.  
- [ ] Update `promptfooconfig.yaml` with multiple tagged test blocks.  
- [ ] Document usage examples in README (factual-only vs rationale).  
- [ ] Standardize OpenAI provider config for easier onboarding.  
