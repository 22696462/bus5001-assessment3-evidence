import json, sys, csv, random, os
from rules import classify

s = sys.argv[1]
msg_file = {"dev": "messages_dev.json", "heldout": "heldout_unlabeled.json"}[s]
msgs = json.load(open(msg_file))
v2 = {r["id"]: r for r in json.load(open("results/out_v2_" + s + ".json"))}
v3 = {r["id"]: r for r in json.load(open("results/out_v3_" + s + ".json"))}
zs = {r["id"]: r for r in json.load(open("results/out_zeroshot_" + s + ".json"))}

def llm_row(r):
    if not r["issues"]:
        return ("NO OUTPUT", "NO OUTPUT", "NO OUTPUT")
    i = r["issues"][0]
    return (i["issue_category"], i["urgency"], i["recommended_team"])

rng = random.Random(int.from_bytes(os.urandom(8), "big"))
os.makedirs("private", exist_ok=True)
rows, key, amb = [], {}, []
for m in msgs:
    i = m["id"]
    rr = classify(m["message"])
    outputs = {
        "llm_v2": llm_row(v2[i]),
        "llm_v3": llm_row(v3[i]),
        "rules": (rr["category"], rr["urgency"], rr["team"]),
        "zeroshot": (zs[i]["category"], zs[i]["urgency"], zs[i]["team"]),
    }
    names = list(outputs.keys())
    rng.shuffle(names)
    key[str(i)] = {}
    for code, name in zip("ABCD", names):
        key[str(i)][code] = name
        c, u, t = outputs[name]
        rows.append([s, i, m["message"], code, c, u, t, "", "", "", ""])
    amb.append([s, i, m["message"], "", ""])

with open("results/review_" + s + ".csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["set", "msg_id", "message", "code", "category", "urgency", "team", "cat_rating", "urg_rating", "team_rating", "notes"])
    w.writerows(rows)
with open("results/ambiguity_" + s + ".csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["set", "msg_id", "message", "ambiguous_Y_or_N", "notes"])
    w.writerows(amb)
json.dump(key, open("private/key_" + s + ".json", "w"), indent=1)
print("Wrote results/review_" + s + ".csv and results/ambiguity_" + s + ".csv")
print("The key is in private/. Do NOT open it until you have finished rating.")
