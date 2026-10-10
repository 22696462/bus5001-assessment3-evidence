CATEGORY_RULES = [
    ("GOVERNANCE_OR_CONDUCT", ["manager", "harass", "bully", "fraud", "hide the", "whistle", "misconduct"]),
    ("SUPPLIER_COMPLIANCE", ["supplier", "vendor"]),
    ("ACCESSIBILITY_BARRIER", ["accessib", "wheelchair", "ramp", "lift "]),
    ("WATER_LEAK", ["leak", "flood", "burst pipe"]),
    ("ENERGY_WASTE", ["air conditioning", "lights", "heating", "overnight"]),
    ("WASTE_CONTAMINATION", ["recycling", "bin", "contaminat"]),
]
TEAM = {
    "WATER_LEAK": "FACILITIES",
    "ENERGY_WASTE": "FACILITIES",
    "WASTE_CONTAMINATION": "FACILITIES",
    "ACCESSIBILITY_BARRIER": "ACCESSIBILITY_AND_INCLUSION",
    "SUPPLIER_COMPLIANCE": "PROCUREMENT",
    "GOVERNANCE_OR_CONDUCT": "HUMAN_REVIEW",
    "OTHER": "HUMAN_REVIEW",
}
HIGH_WORDS = ["all morning", "two days", "days", "wheelchair", "burst", "flood", "urgent", "danger", "unsafe"]

def classify(text):
    t = text.lower()
    category = "OTHER"
    for name, words in CATEGORY_RULES:
        if any(w in t for w in words):
            category = name
            break
    if category == "GOVERNANCE_OR_CONDUCT":
        urgency = "CRITICAL"
    elif any(w in t for w in HIGH_WORDS):
        urgency = "HIGH"
    else:
        urgency = "MEDIUM"
    return {"category": category, "urgency": urgency, "team": TEAM[category]}
