import re
from typing import List


class TextAnonymizer:
    @staticmethod
    def anonymize_phone_numbers(text: str) -> str:
        phone_pattern = r"\+?[0-9\s\-\(\)]{7,}"
        return re.sub(phone_pattern, "<PHONE>", text)

    @staticmethod
    def anonymize_email_addresses(text: str) -> str:
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        return re.sub(email_pattern, "<EMAIL>", text)

    @staticmethod
    def anonymize_urls(text: str) -> str:
        url_pattern = r"https?://[^\s]+"
        return re.sub(url_pattern, "<URL>", text)

    @staticmethod
    def mask_likely_personal_info(text: str) -> str:
        lines = text.strip().splitlines()
        masked_lines = []

        for line in lines:
            clean = line.strip()
            if (
                2 <= len(clean.split()) <= 4
                and all(w[0].isupper() for w in clean.split() if w[0].isalpha())
            ):
                masked_lines.append("<PERSONAL INFO>")
            else:
                masked_lines.append(line)
        return "\n".join(masked_lines)

    @staticmethod
    def anonymize_entities(text: str, entities: List[dict]) -> str:
        """
        Replace spans in text based on NER entities with tags like <ORG>, <PER>, etc.
        Args:
            text: The text to anonymize.
            entities: The list of entities to anonymize.
        Returns:
            The anonymized text.
        """
        sorted_entities = sorted(entities, key=lambda e: e["start"], reverse=True)
        for ent in sorted_entities:
            start = ent["start"]
            end = ent["end"]
            label = ent["entity_group"]
            text = text[:start] + f"<{label}>" + text[end:]
        return text

    @classmethod
    def anonymize_all(cls, text: str, entities: List[dict] = None) -> str:
        text = cls.anonymize_email_addresses(text)
        text = cls.anonymize_phone_numbers(text)
        text = cls.anonymize_urls(text)
        text = cls.mask_likely_personal_info(text)
        if entities:
            text = cls.anonymize_entities(text, entities)
        return text
