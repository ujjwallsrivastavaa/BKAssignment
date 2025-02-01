import pytest
from api.models import Language, FAQ, Translation  # Import necessary models
from django.core.cache import cache  # Import cache for clearing or testing cache functionality
from unittest.mock import patch  # For mocking external dependencies if needed
from googletrans import Translator  # Google Translate API for translating text


@pytest.mark.django_db
def test_faq_auto_translates_with_google_trans():
    """
    Test to ensure that when a new FAQ is created, it is automatically translated
    into the desired language (using Google Translate).
    """
    # Create a new language (Hindi in this case)
    language = Language.objects.create(code="hi")

    # Create an FAQ with a question and answer in English
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")

    # Assert that the FAQ was successfully created
    assert FAQ.objects.filter(id=faq.id).exists(), "FAQ was not created successfully"

    # Fetch the Translation for the created FAQ in the newly added language
    translation = Translation.objects.filter(faq=faq, language=language).first()

    # Assert that the translation exists
    assert translation is not None, "Translation was not created successfully"

    # Use Google Translate to simulate the translation of the question and answer
    translator = Translator()
    expected_question = translator.translate("What is Django?", src='en', dest='hi').text
    expected_answer = translator.translate("Django is a web framework.", src='en', dest='hi').text

    # Assert that the translated question and answer match the expected values
    assert translation.question == expected_question, f"Expected: {expected_question}, Got: {translation.question}"
    assert translation.answer == expected_answer, f"Expected: {expected_answer}, Got: {translation.answer}"


@pytest.mark.django_db
def test_faq_translation_after_adding_language():
    """
    Test that when a new language is added, existing FAQs are translated into that language.
    """
    # Create a new FAQ in English
    faq = FAQ.objects.create(question="How does Python work?", answer="Python is an interpreted language.")

    # Assert that the FAQ was created successfully
    assert FAQ.objects.filter(id=faq.id).exists(), "FAQ was not created successfully"

    # Create a new language (Bengali in this case)
    language = Language.objects.create(code="bn")

    # Fetch the translation for the created FAQ in the newly added language
    translation = Translation.objects.filter(faq=faq, language=language).first()

    # Assert that the translation exists
    assert translation is not None, "Translation was not created successfully"

    # Use Google Translate to simulate the translation of the question and answer
    translator = Translator()
    expected_question = translator.translate("How does Python work?", src='en', dest='bn').text
    expected_answer = translator.translate("Python is an interpreted language.", src='en', dest='bn').text

    # Assert that the translated question and answer match the expected values
    assert translation.question == expected_question, f"Expected: {expected_question}, Got: {translation.question}"
    assert translation.answer == expected_answer, f"Expected: {expected_answer}, Got: {translation.answer}"
