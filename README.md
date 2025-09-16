# Chatbot Evaluation using Promptfoo

This repo contains reproducible evaluation configs and datasets for testing and comparing a SNAP/social safety net chatbot using [Promptfoo](https://promptfoo.dev/).

The evaluation pipeline checks:
- **Factual accuracy** on multiple-choice questions
- **Rationale quality** (LLM-as-judge)
- **Groundedness** (does the explanation cite real sources?)
- **Hygiene & latency** (basic safety and response time)

---

## Quick start

### 1. Install dependencies
```bash
npm install -g promptfoo
```

### 2. Configure API keys
```env
OPENAI_API_KEY = "YOUR_API_KEY"
```

### 3. Run evaluations
```bash
promptfoo eval -c configs/promptfooconfig.yaml
```

### 4. View results
```bash
promptfoo view results/latest
```

## Repo Structure
```bash
configs/
  promptfooconfig.yaml    
  providers.yaml          
  scoring.yaml            
datasets/
  tests.csv              
prompts/
  mcq-letter-only.txt    
  mcq-rationale-citations.txt 
rubrics/
  rationale_quality.md 
  groundedness.md              
results/                
README.md 
```

## OpenAI Provider

- Create your own provider file locally under `configs/openai-provider.yaml` with content like:
  ```yaml
  - id: openai:gpt-4o-mini
    config:
      apiKey: ${OPENAI_API_KEY}
  ```