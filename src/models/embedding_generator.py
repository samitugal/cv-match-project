from abc import ABC, abstractmethod
from typing import Any, Dict

from transformers import pipeline


class EmbeddingGenerator(ABC):
    @abstractmethod
    def generate(self, text: str) -> str:
        pass

class HuggingFaceEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.pipe = pipeline(
            "feature-extraction",
            model=self.model_name,
            truncation=True,
            max_length=512,
        )

    def generate(self, text: str) -> str:
        return self.pipe(text)
    
    
def create_embedding_generator(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> EmbeddingGenerator:
    generators = {
        "sentence-transformers": HuggingFaceEmbeddingGenerator
    }
    return generators[model_name]()
