from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.response import Response
from googletrans import Translator  # For translation using Google Translate
from .models import FAQ, Translation, Language  # Import models for FAQ, Translation, and Language
from .serializers import FAQSerializer, TranslatedFAQSerializer  # Import serializers for FAQ and Translated FAQ

class FAQListView(APIView):
    def get(self, request, *args, **kwargs):
        """ Expected Output:
        # When a user makes a GET request to the '/api/faqs/' endpoint with the `lang` query parameter:
        # - If the 'lang' parameter is 'en' or not provided:
        #   1. The response will contain the list of FAQs in English.
        #   2. The FAQ data will be returned from cache if it has been cached previously.
        #   3. If FAQs are not cached, they will be retrieved from the database, serialized, cached, and returned.
        #   
        # - If a different 'lang' parameter is provided (e.g., 'fr' for French):
        #   1. The response will contain the list of FAQs translated into the specified language (if a translation exists).
        #   2. If the translation for a specific FAQ doesn't exist, the original FAQ (in English) will be returned.
        #   3. Translated FAQs will be cached for future use."""



        # Retrieve the 'lang' query parameter from the request, defaulting to 'en' (English) if not provided
        lang_code = request.query_params.get('lang', 'en')
        
        # Case 1: If the requested language is 'en' or no language is provided, fetch English FAQs
        if lang_code == 'en' or not lang_code:
            cache_key = "faq_translations_en"  # Define a unique cache key for English FAQs
            cached_faqs = cache.get(cache_key)  # Try to get cached FAQs from cache
            if cached_faqs:
                # If cached data is found, return it directly as a response
                return Response(cached_faqs)
            
            # If no cached data is found, retrieve all FAQs from the database
            faqs = FAQ.objects.all()
            # Serialize the FAQs using the FAQSerializer
            serializer = FAQSerializer(faqs, many=True)
            # Cache the serialized FAQ data for future requests
            cache.set(cache_key, serializer.data, timeout=None)  
            # Return the serialized FAQ data as a response
            return Response(serializer.data)
        
        # Case 2: If the requested language is not 'en', handle language-specific FAQs
        try:
            # Try to fetch the Language object for the requested lang_code from the database
            language = Language.objects.get(code=lang_code)
        except Language.DoesNotExist:
            # If the language is not found in the database, attempt to create it
            translator = Translator()
            try:
                # Try a test translation to check if the language code is valid
                translator.translate('Test', src='en', dest=lang_code)
                # If successful, create a new Language object in the database
                language = Language.objects.create(code=lang_code)
            except Exception as e:
                # If the translation fails or there is another issue, set language to None
                language = None  

        # Define a unique cache key based on the requested language for storing translated FAQs
        cache_key = f"faq_translations_{lang_code}"
        # Check if translations for the requested language are already cached
        cached_translations = cache.get(cache_key)

        if cached_translations:
            # If cached translations are found, return them as a response
            return Response(cached_translations)

        # If no cached translations are found, retrieve all FAQs from the database
        faqs = FAQ.objects.all()
        translated_faqs = []  # Initialize an empty list to store translated FAQs

        # Iterate through each FAQ to check if a translation exists for the requested language
        for faq in faqs:
            translation = None
            if language:
                # If a language object exists, try to fetch the translation for the FAQ in that language
                translation = Translation.objects.filter(faq=faq, language=language).first()

            if translation:
                # If a translation exists, append the translated question and answer to the list
                translated_faqs.append({
                    'question': translation.question,
                    'answer': translation.answer,
                })
            else:
                # If no translation exists, append the original FAQ (in English) to the list
                translated_faqs.append({
                    'question': faq.question,
                    'answer': faq.answer,
                })

        # Cache the translated FAQs for future requests to avoid redundant database queries
        cache.set(cache_key, translated_faqs, timeout=None)

        # Serialize the translated FAQ data (or fallback to the original FAQ) using the TranslatedFAQSerializer
        serializer = TranslatedFAQSerializer(translated_faqs, many=True)
        # Return the serialized data as a response
        return Response(serializer.data)
