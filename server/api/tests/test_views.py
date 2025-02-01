# Import necessary modules for testing
import pytest
from rest_framework.test import APIClient  # Django REST Framework's test client
from django.core.cache import cache  # Cache to test if data is cached
from googletrans import Translator  # Google Translator to simulate translations
from api.models import FAQ, Language, Translation  # Import the models from your Django app

@pytest.mark.django_db
def test_get_faqs_in_english():
    """
    Test retrieving FAQs in English without translation.
    This test ensures that when no language is specified, the FAQs are returned in English.
    """
    client = APIClient()

    # Create an FAQ entry with a question and answer in English
    FAQ.objects.create(question="What is Django?", answer="Django is a Python web framework.")

    # Clear the cache to make sure we are retrieving fresh data
    cache.clear()

    # Make a GET request to the FAQ endpoint without a language parameter (default should be 'en')
    response = client.get("/api/faqs/")

    # Assert that the request was successful (HTTP status code 200)
    assert response.status_code == 200

    # Ensure the response contains the FAQ in English as expected
    assert response.data[0]["question"] == "What is Django?"
    assert response.data[0]["answer"] == "Django is a Python web framework."

    # Check if the FAQs are cached under the key 'faq_translations_en'
    cached_faqs = cache.get("faq_translations_en")
    assert cached_faqs is not None  # Ensure the cache is populated


@pytest.mark.django_db
def test_get_faqs_with_translation():
    """
    Test retrieving FAQs in a non-English language (e.g., French 'fr').
    This test ensures that the FAQs are correctly translated and returned when a language is specified.
    """
    client = APIClient()

    # Create an FAQ in English
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a Python web framework.")

    # Create a new language entry for French
    language = Language.objects.create(code="fr")

    # Use Google Translate to simulate translation
    translator = Translator()
    translated_question = translator.translate(faq.question, src="en", dest="fr").text
    translated_answer = translator.translate(faq.answer, src="en", dest="fr").text

    # Store the translated FAQ in the Translation model
    Translation.objects.create(faq=faq, language=language, question=translated_question, answer=translated_answer)

    # Clear cache to ensure we get fresh data
    cache.clear()

    # Make a GET request to retrieve FAQs in French
    response = client.get("/api/faqs/?lang=fr")

    # Assert that the request was successful
    assert response.status_code == 200

    # Ensure the translated FAQ is returned in French
    assert response.data[0]["question"] == translated_question
    assert response.data[0]["answer"] == translated_answer

    # Check if the FAQs are cached under the key 'faq_translations_fr'
    cached_faqs = cache.get("faq_translations_fr")
    assert cached_faqs is not None  # Ensure the cache is populated for French translations


@pytest.mark.django_db
def test_get_faqs_with_nonexistent_language():
    """
    Test behavior when requesting FAQs in a language that doesn't exist.
    This test ensures that even if a non-existent language is requested, the default (English) FAQ is returned.
    """
    client = APIClient()

    # Create an FAQ in English
    FAQ.objects.create(question="What is Django?", answer="Django is a Python web framework.")

    # Clear cache to ensure we're working with fresh data
    cache.clear()

    # Make a GET request with a non-existent language code 'xyz'
    response = client.get("/api/faqs/?lang=xyz")

    # Assert that the request is successful (status code 200)
    assert response.status_code == 200

    # Ensure the response contains the original English FAQ since the translation doesn't exist
    assert response.data[0]["question"] == "What is Django?"
    assert response.data[0]["answer"] == "Django is a Python web framework."
