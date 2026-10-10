import json, sys, time, urllib.request

prompt_file, msg_file, tag = sys.argv[1], sys.argv[2], sys.argv[3]
template = open(prompt_file).read()
msgs = json.load(open(msg_file))

def e(*v):
    return {"type": "string", "enum": list(v)}

schema = {
    "type": "object",
    "properties": {"issues": {"type": "array", "maxItems": 3, "items": {
        "type": "object",
        "properties": {
            "issue_category": e("WATER_LEAK", "ENERGY_WASTE", "WASTE_CONTAMINATION", "ACCESSIBILITY_BARRIER", "SUPPLIER_COMPLIANCE", "GOVERNANCE_OR_CONDUCT", "OTHER"),
            "urgency": e("LOW", "MEDIUM", "HIGH", "CRITICAL"),
            "sentiment": e("POSITIVE", "NEUTRAL", "NEGATIVE"),
            "followup_required": e("Y", "N"),
            "recommended_team": e("FACILITIES", "SUSTAINABILITY", "PROCUREMENT", "ACCESSIBILITY_AND_INCLUSION", "GOVERNANCE_AND_COMPLIANCE", "HUMAN_REVIEW"),
            "escalation_reason": {"type": "string"},
            "data_sensitivity_risk": e("NONE", "LOW", "HIGH"),
            "confidence": e("LOW", "MEDIUM", "HIGH"),
            "brief_summary": {"type": "string"},
        },
        "required": ["issue_category", "urgency", "sentiment", "followup_required", "recommended_team", "escalation_reason", "data_sensitivity_risk", "confidence", "brief_summary"],
    }}},
    "required": ["issues"],
}

out = []
for m in msgs:
    prompt = template.replace("PASTE_MESSAGE_HERE", m["message"])
    body = json.dumps({"model": "llama3.2", "prompt": prompt, "stream": False, "format": schema,
                       "options": {"temperature": 0, "seed": 42, "num_predict": 500}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        raw = json.loads(r.read())["response"]
    secs = round(time.time() - t, 1)
    try:
        issues = json.loads(raw)["issues"]
    except Exception:
        issues = []
    out.append({"id": m["id"], "message": m["message"], "seconds": secs,
                "n_issues": len(issues), "issues": issues, "raw": raw})
    print(m["id"], "done,", secs, "s")
json.dump(out, open("results/out_" + tag + ".json", "w"), indent=2)
print("Saved results/out_" + tag + ".json")
