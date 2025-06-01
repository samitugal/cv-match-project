import pytest

from src.models.ner_models import create_ner_model


def test_turkish_ner_model():
    model = create_ner_model(language="turkish")
    result = model.resolve("Sami Tuğal, Ege Üniversitesi'nden mezun oldu.")
    assert len(result) > 0
    assert any("PER" in entity[1] for entity in result)
    assert any("ORG" in entity[1] for entity in result)


def test_english_ner_model():
    model = create_ner_model(language="english")
    result = model.resolve("John Doe works at Google in New York.")
    assert len(result) > 0
    assert any("PER" in entity[1] for entity in result)
    assert any("ORG" in entity[1] for entity in result)
    assert any("LOC" in entity[1] for entity in result)


def test_invalid_language():
    with pytest.raises(KeyError):
        create_ner_model(language="invalid")
