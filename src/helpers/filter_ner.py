SKILL_TERMS = {"SQL", "AI", "AML & KYC", "ET", "LowCode", "NoCode", "Computer Engineering", "Low"}

def filter_ner(entities: list[dict], skill_terms=SKILL_TERMS) -> list[dict]:
    filtered = []

    for ent in entities:
        if ent.get("entity_group") == "ORG":
            word = ent.get("word", "")
            if not any(skill.lower() in word.lower() for skill in skill_terms):
                filtered.append(ent)

    return filtered
