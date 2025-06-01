import os

from dotenv import load_dotenv

from src.helpers import filter_ner, read_document
from src.helpers.anonymizers import TextAnonymizer
from src.models import create_detector, create_ner_model, create_embedding_generator


load_dotenv()

DEFAULT_LANG_DETECTOR = "xlm"
DEFAULT_EMBEDDING_GENERATOR = "sentence-transformers"   

lang_detector = create_detector(DEFAULT_LANG_DETECTOR)
embedding_generator = create_embedding_generator(DEFAULT_EMBEDDING_GENERATOR)


def detect_doc_language(text: str) -> str:
    """
    This function detects the language of a given document.
    args:
        text: str
    returns:
        str: The language of the document.
    """
    return lang_detector.detect(text)

def anonymize_text(text: str, filtered_ner_result: list[dict]) -> str:
    return TextAnonymizer.anonymize_all(text, filtered_ner_result)

def run_pipeline(file_path: str):
    """
    This function runs the pipeline for a given file path.
    """
    text = read_document(file_path)
    language = detect_doc_language(text)

    if language == "tr":
        ner_model = create_ner_model("turkish")
    else:
        ner_model = create_ner_model("english")

    ner_result = ner_model.resolve(text)
    filtered_ner_result = filter_ner(ner_result)

    anonymized_text = anonymize_text(text, filtered_ner_result)

    embedding = embedding_generator.generate(anonymized_text)

if __name__ == "__main__":
    file_path = "C:/Users/samit/Projects/cv-match-project/src/data/CV_3.pdf"
    run_pipeline(file_path)
