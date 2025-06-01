from abc import ABC, abstractmethod
from typing import Any, Dict

from transformers import pipeline


class LanguageDetector(ABC):
    @abstractmethod
    def detect(self, text: str) -> str:
        pass


class HuggingFaceXLMDetector(LanguageDetector):
    def __init__(self):
        self.model_name = "papluca/xlm-roberta-base-language-detection"
        self.pipe = pipeline(
            "text-classification",
            model=self.model_name,
            truncation=True,
            max_length=512,
        )

    def detect(self, text: str) -> str:
        text = text[:2000]
        result = self.pipe(text)
        return result[0]["label"]


class LangDetectDetector(LanguageDetector):

    def detect(self, text: str) -> str:
        from langdetect import detect

        text = text[:2000]
        return detect(text)


def create_detector(detector_type: str = "xlm") -> LanguageDetector:
    detectors = {"xlm": HuggingFaceXLMDetector, "langdetect": LangDetectDetector}
    return detectors[detector_type]()
