import json, sys, time, urllib.request, os

prompt_file = sys.argv[1]
template = open(prompt_file).read()
name = os.path.splitext(os.path.basename(prompt_file))[0]

messages = [
    "There is a water leak in Building C that has been running all morning.",
    "I want to report that one of our suppliers may not meet our sustainability policy.",
    "The accessible entrance near the main building has been blocked for two days.",
]

results = []
for msg in messages:
    prompt = template.replace("PASTE_MESSAGE_HERE", msg).replace("<message text>", msg)
    body = json.dumps({
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "seed": 42},
    }).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    start = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        out = json.loads(r.read())["response"]
    secs = round(time.time() - start, 1)
    try:
        json.loads(out)
        valid = True
    except Exception:
        valid = False
    print("MESSAGE:", msg)
    print("VALID JSON:", valid, "| seconds:", secs)
    print(out)
    print("-" * 60)
    results.append({"message": msg, "valid_json": valid, "seconds": secs, "output": out})

with open("results/" + name + "_outputs.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved results/" + name + "_outputs.json")
