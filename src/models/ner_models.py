import logging
from abc import ABC, abstractmethod
from typing import Literal

import torch
from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          pipeline)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NERModel(ABC):
    def __init__(self, model_name: str):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name).to(
            self.device
        )
        self.ner_pipe = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
            device=self.device,
        )

        logger.info(f"Using device: {self.device}")
        logger.info(f"Model name: {self.model_name}")

    @abstractmethod
    def resolve(self, text: str) -> list[tuple[str, str]]:
        pass


class HuggingFaceBertNerModel(NERModel):
    def __init__(self, model_name: str = "dslim/bert-base-NER"):
        super().__init__(model_name)

    def resolve(self, text: str) -> list[tuple[str, str]]:
        return self.ner_pipe(text)


class HuggingFaceBertBasedTurkishNerModel(NERModel):
    def __init__(self, model_name: str = "savasy/bert-base-turkish-ner-cased"):
        super().__init__(model_name)

    def resolve(self, text: str) -> list[tuple[str, str]]:
        return self.ner_pipe(text)


class HuggingFaceBertBasedMultiLanguageNerModel(NERModel):
    def __init__(self, model_name: str = "Davlan/xlm-roberta-base-ner-hrl"):
        super().__init__(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

    def resolve(self, text: str) -> list[tuple[str, str]]:
        return self.ner_pipe(text)


def create_ner_model(
    language: str = Literal["turkish", "english", "multi"]
) -> NERModel:
    switcher = {
        "turkish": HuggingFaceBertBasedTurkishNerModel,
        "english": HuggingFaceBertNerModel,
        "multi": HuggingFaceBertBasedMultiLanguageNerModel,
    }
    return switcher[language]()
