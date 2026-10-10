# Q3 results: LLM triage of ESG messages

Evidence for BUS5001 Assessment 3, Question 3 (LLM-based ESG message triage).

## Setup

- Model: llama3.2 (Ollama, run locally on a CPU-only laptop)
- Settings: temperature 0, seed 42 (repeatable output)
- Script: `run_triage.py` in the repo root, run once per prompt
- Prompts: `prompts/prompt_v1_original.txt` (from the assignment brief) and `prompts/prompt_v2_revised.txt` (revised)

## Files

| File | Contents |
|---|---|
| `prompt_v1_original_outputs.json` | Model output for the original prompt on 3 messages |
| `prompt_v2_revised_outputs.json` | Model output for the revised prompt on 3 messages |

Each record holds the message, whether the output was valid JSON, the response time in seconds, and the raw model output.

## Test messages

1. There is a water leak in Building C that has been running all morning.
2. I want to report that one of our suppliers may not meet our sustainability policy.
3. The accessible entrance near the main building has been blocked for two days.

## Summary of observations

| Message | Original prompt | Revised prompt |
|---|---|---|
| 1. Water leak | Facilities, LOW | WATER_LEAK, HIGH, FACILITIES |
| 2. Supplier compliance | ESG, MEDIUM | SUPPLIER_COMPLIANCE, MEDIUM, SUSTAINABILITY |
| 3. Blocked accessible entrance | Facility, LOW | ACCESSIBILITY_BARRIER, MEDIUM, ACCESSIBILITY_AND_INCLUSION |

- Original prompt: all outputs were valid JSON, but category, team and sensitivity values were free text and inconsistent (for example "Facilities" and "Facility").
- Revised prompt: all outputs were valid JSON and used the allowed values. Urgency for message 3 was MEDIUM although the prompt's own definition implies HIGH.
- Sample size is three messages and one run per prompt, so these results are indicative only.

## Still to add

- Rule-based baseline and Hugging Face zero-shot comparison (Q3b)
