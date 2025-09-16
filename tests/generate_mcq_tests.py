import csv, os, uuid

ROOT = os.path.dirname(os.path.dirname(__file__))

def load_rows(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def letter_only(config):
    csv_path = config.get("csv", os.path.join(ROOT, "dataset", "tests.csv"))
    rows = load_rows(csv_path)
    out = []
    for i, r in enumerate(rows):
        out.append({
            "description": (r.get("question","")[:120] + "…") if len(r.get("question",""))>120 else r.get("question",""),
            "vars": {
                "question": r.get("question",""),
                "__expected": (r.get("__expected","") or "").strip().replace("contains: ","").upper(),
                # unique per call
                "uniqueSessionId": f"letter-{i}-{uuid.uuid4().hex[:8]}",
            },
            # only the Nava generator will run here (see tests.providers below)
            "assert": [
                {"type": "regex", "value": "^[A-E]$"},
                {"type": "equals", "value": "{{__expected}}"},
            ],
        })
    return out

def rationale(config):
    csv_path = config.get("csv", os.path.join(ROOT, "dataset", "tests.csv"))
    thr_r = float(config.get("rationale_threshold", 0.7))
    thr_g = float(config.get("groundedness_threshold", 0.7))
    rows = load_rows(csv_path)
    out = []
    for i, r in enumerate(rows):
        out.append({
            "description": (r.get("question","")[:120] + "…") if len(r.get("question",""))>120 else r.get("question",""),
            "vars": {
                "question": r.get("question",""),
                "__expected": (r.get("__expected","") or "").strip().replace("contains: ","").upper(),
                # unique per call
                "uniqueSessionId": f"rationale-{i}-{uuid.uuid4().hex[:8]}",
            },
            "assert": [
                # Structure + letter correctness
                {"type": "javascript", "value": r"""
function ({ output, vars }) {
  const lines = String(output || '').split(/\r?\n/);
  if (lines.length < 3) return 'Expected 3 lines (Answer, Rationale, Citations)';
  const first = lines[0].trim().replace(/^ANSWER:\s*/i, '').trim();
  if (!/^[A-E]$/.test(first)) return `First line must be A–E; got: ${lines[0]}`;
  const exp = (vars.__expected || '').trim();
  if (exp && first !== exp) return `Expected ${exp} but got ${first}`;
  if (!/^Rationale:\s*/i.test(lines[1] || '')) return 'Line 2 must start with "Rationale: "';
  if (!/^Citations:\s*/i.test(lines[2] || '')) return 'Line 3 must start with "Citations: "';
}"""},
                # Judge rationale line only
                {"type": "llm-rubric", "provider": "openai:gpt-4o-mini",
                 "value": "file://rubrics/rationale_quality.txt", "threshold": thr_r},
                # Judge citations line only - feed only the third line via transform
                {"type": "llm-rubric", "provider": "openai:gpt-4o-mini",
                 "value": "file://rubrics/groundedness.txt", "threshold": thr_g,
                 "options": {
                    "transform": "const l=(output||'').split(/\\r?\\n/); return (l[2]||'').replace(/^Citations:\\s*/i,'').trim();"
                 }},
            ],
        })
    return out
