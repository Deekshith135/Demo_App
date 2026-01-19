# recommendation.py
# Coconut Tree Illness Recommendations (6 illnesses + healthy)
# Severity decided ONLY using confidence score.

from typing import Dict, Any


# -----------------------------
# 1) Confidence -> Severity
# -----------------------------
def get_severity_from_confidence(confidence: float) -> str:
    """
    Severity thresholds:
    <= 40  -> mild
    40-80  -> medium
    > 80   -> severe
    """
    if confidence <= 40:
        return "mild"
    elif 40 < confidence <= 80:
        return "medium"
    else:
        return "severe"


# -----------------------------
# 2) Healthy practices by PART
# -----------------------------
HEALTHY_PRACTICES_BY_PART = {
    "leaves": [
        "Remove dry and old leaves regularly.",
        "Maintain proper spacing for good sunlight + airflow.",
        "Avoid continuous leaf wetness (reduce overhead watering).",
        "Monitor underside of leaves for pests weekly.",
        "Use clean pruning tools and destroy removed infected leaves.",
    ],
    "stem": [
        "Avoid wounds/cuts on trunk (prevents fungal entry).",
        "Keep trunk base clean (remove weeds, debris).",
        "Ensure soil drainage near trunk (no waterlogging).",
        "Do regular inspection for cracks/bleeding/gum oozing.",
        "Apply lime paste at trunk base if recommended by local agriculture officer.",
    ],
    "bud": [
        "Keep crown clean (remove dead crown debris).",
        "Avoid water stagnation in crown region.",
        "Do not injure spindle leaf during intercultural operations.",
        "Inspect spindle leaf for softening, foul smell, or drooping.",
        "Maintain proper nutrition to strengthen crown growth.",
    ],
    "tree": [
        "Maintain proper drainage (avoid water stagnation).",
        "Keep farm clean and remove dead tissue.",
        "Ensure balanced irrigation and avoid overwatering.",
        "Monitor every 7–10 days for early symptoms.",
    ]
}


# -----------------------------
# 3) Disease database (6 illnesses)
# -----------------------------
DISEASE_DB: Dict[str, Dict[str, Any]] = {

    # 1) Bud Rot
    "bud_rot": {
        "name": "Bud Rot",
        "part": "bud",
        "fertilizers": {
            "mild": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Pour into crown (200–300 ml)"},
            ],
            "medium": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Pour into crown (300–500 ml)"},
                {"name": "Carbendazim", "dose": "1 g/L", "apply": "Alternate weekly (crown pour)"},
            ],
            "severe": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Treat nearby trees preventively"},
                {"name": "Bordeaux Mixture", "dose": "1%", "apply": "Crown treatment in rainy season"},
            ],
        },
        "practices": {
            "mild": [
                "Clean crown and remove slightly infected tissue.",
                "Improve drainage and avoid water stagnation in crown.",
            ],
            "medium": [
                "Remove infected spindle leaf and rotten crown tissue carefully.",
                "Repeat crown treatment every 7 days (3 rounds).",
                "Disinfect tools after cutting infected parts.",
            ],
            "severe": [
                "If growing point is dead, recovery chance is low.",
                "Remove severely affected palms to prevent spread.",
                "Give preventive copper treatment for nearby palms.",
            ],
        },
    },

    # 2) Bud Rot Drooping
    "bud_rot_drooping": {
        "name": "Bud Rot Drooping",
        "part": "bud",
        "fertilizers": {
            "mild": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Pour into crown (200–300 ml)"},
            ],
            "medium": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Week 1 crown pour"},
                {"name": "Carbendazim", "dose": "1 g/L", "apply": "Week 2 crown pour (alternate)"},
            ],
            "severe": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Preventive crown pour nearby palms"},
            ],
        },
        "practices": {
            "mild": [
                "Inspect spindle leaf for drooping and rotting smell.",
                "Avoid overhead irrigation into crown.",
            ],
            "medium": [
                "Remove infected crown tissues.",
                "Alternate fungicide crown pour weekly for 3–4 weeks.",
            ],
            "severe": [
                "If crown collapses fully, tree may die.",
                "Remove dead trees and protect surrounding trees.",
            ],
        },
    },

    # 3) Grey Leaf Rot
    "leaves_grey_leaf_rot": {
        "name": "Grey Leaf Rot",
        "part": "leaves",
        "fertilizers": {
            "mild": [
                {"name": "Mancozeb", "dose": "2 g/L", "apply": "Spray both sides of leaves"},
            ],
            "medium": [
                {"name": "Mancozeb", "dose": "2 g/L", "apply": "Spray weekly (2–3 rounds)"},
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Alternate spray optional"},
            ],
            "severe": [
                {"name": "Mancozeb", "dose": "2 g/L", "apply": "Spray weekly (3–4 rounds)"},
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Alternate if spreading"},
            ],
        },
        "practices": {
            "mild": [
                "Remove small infected leaf portions.",
                "Avoid leaf wetness for long duration.",
            ],
            "medium": [
                "Remove heavily infected leaves and destroy them.",
                "Improve sunlight penetration and airflow.",
            ],
            "severe": [
                "Remove multiple infected leaves to reduce spread.",
                "Continue fungicide schedule until controlled.",
            ],
        },
    },

    # 4) Leaf Rot
    "leaf_rot": {
        "name": "Leaf Rot",
        "part": "leaves",
        "fertilizers": {
            "mild": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Leaf spray"},
            ],
            "medium": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Spray weekly"},
                {"name": "Mancozeb", "dose": "2 g/L", "apply": "Alternate optional"},
            ],
            "severe": [
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Weekly spray (3–4 rounds)"},
            ],
        },
        "practices": {
            "mild": [
                "Remove early rotting leaf parts.",
                "Avoid overwatering and improve drainage.",
            ],
            "medium": [
                "Remove infected leaves completely.",
                "Improve airflow by pruning dense foliage.",
            ],
            "severe": [
                "Destroy severely infected leaf material.",
                "Avoid spreading spores by cleaning tools.",
            ],
        },
    },

    # 5) Stem Bleeding
    "stem_bleeding": {
        "name": "Stem Bleeding",
        "part": "stem",
        "fertilizers": {
            "mild": [
                {"name": "Bordeaux Paste", "dose": "Ready paste", "apply": "Apply on cleaned bleeding area"},
            ],
            "medium": [
                {"name": "Bordeaux Paste", "dose": "Ready paste", "apply": "Apply every 15 days (2–3 times)"},
                {"name": "Copper Oxychloride", "dose": "3 g/L", "apply": "Optional spray around affected area"},
            ],
            "severe": [
                {"name": "Bordeaux Paste", "dose": "Ready paste", "apply": "Apply + expert inspection needed"},
            ],
        },
        "practices": {
            "mild": [
                "Scrape infected bark gently and clean with cloth.",
                "Maintain drainage around trunk base.",
            ],
            "medium": [
                "Repeat paste application and avoid trunk injuries.",
                "Keep basal area free from weeds and moisture.",
            ],
            "severe": [
                "Check for root damage/waterlogging.",
                "Consult agriculture officer for severe cases.",
            ],
        },
    },

    # 6) Whitefly
    "whitefly": {
        "name": "Whitefly",
        "part": "leaves",
        "fertilizers": {
            "mild": [
                {"name": "Neem Oil", "dose": "5 ml/L", "apply": "Spray underside of leaves"},
            ],
            "medium": [
                {"name": "Neem Oil", "dose": "5 ml/L", "apply": "Spray weekly 2–3 rounds"},
                {"name": "Insecticidal Soap", "dose": "Few drops/L", "apply": "Mix with neem"},
            ],
            "severe": [
                {"name": "Imidacloprid", "dose": "As per label", "apply": "Spray/drench only if severe"},
            ],
        },
        "practices": {
            "mild": [
                "Use yellow sticky traps near palms.",
                "Wash leaves with water if possible.",
            ],
            "medium": [
                "Remove heavily infested leaves.",
                "Control ants (ants protect whiteflies).",
            ],
            "severe": [
                "Repeat treatment after 10–14 days if needed.",
                "Keep field clean to reduce reinfestation.",
            ],
        },
    },
}


# -----------------------------
# Helpers
# -----------------------------
def normalize_label(label: str) -> str:
    return (label or "").strip().lower()


def normalize_part(part: str) -> str:
    p = (part or "").strip().lower()
    if p == "leaf":
        return "leaves"
    return p


# -----------------------------
# Main function
# -----------------------------
def get_recommendation(predicted_label: str, confidence: float, part: str = None) -> Dict[str, Any]:
    """
    predicted_label: model label like 'leaves_Grey_leaf_rot', 'bud_rot', 'stem_bleeding', 'healthy'
    confidence: score 0-100
    part: optional -> 'leaves'/'stem'/'bud' (used for healthy practices)
    """

    label_key = normalize_label(predicted_label)

    # Convert model label formatting to consistent key
    # Example: leaves_Grey_leaf_rot -> leaves_grey_leaf_rot
    label_key = label_key.replace(" ", "_")

    # ✅ Healthy -> return practices based on part
    if "healthy" in label_key:
        part_norm = normalize_part(part) if part else "tree"
        practices = HEALTHY_PRACTICES_BY_PART.get(part_norm, HEALTHY_PRACTICES_BY_PART["tree"])
        return {
            "disease": "Healthy",
            "status": "healthy",
            "part": part_norm,
            "practices": practices
        }

    # For unknown disease labels
    if label_key not in DISEASE_DB:
        return {
            "error": "Unknown disease label",
            "predicted_label": predicted_label,
            "confidence": float(confidence)
        }

    disease_data = DISEASE_DB[label_key]
    severity = get_severity_from_confidence(confidence)

    return {
        "disease": disease_data["name"],
        "status": "illness",
        "part": disease_data.get("part", "tree"),
        "severity": severity,
        "confidence": float(confidence),
        "fertilizers": disease_data["fertilizers"][severity],
        "practices": disease_data["practices"][severity],
    }
