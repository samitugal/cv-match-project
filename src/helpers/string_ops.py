import unicodedata
from typing import Optional

def strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )

def mask_likely_personal_info(text: str) -> str:
    lines = text.strip().splitlines()
    masked_lines = []

    for line in lines:
        clean = line.strip()
        words = clean.split()

        if (
            2 <= len(words) <= 4
            and all(w[0].isupper() for w in words if w and w[0].isalpha())
        ):
            masked_lines.append("<PERSONAL INFO>")
        else:
            masked_lines.append(line)

    return "\n".join(masked_lines)
