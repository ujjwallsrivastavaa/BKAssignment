# Import necessary modules
from django.db import models  # Django's ORM for defining database models
from ckeditor.fields import RichTextField  # Provides a rich text editor for formatted content
from googletrans import Translator  # Google Translate API for automatic translations
from django.core.cache import cache  # Django caching framework to store translation results

# ---------------------------------------------
# Language Model: Stores available languages for translations
# ---------------------------------------------
class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Language code (e.g., 'fr' for French, 'es' for Spanish)

    def save(self, *args, **kwargs):
        """ 
        Override the save method to automatically translate all existing FAQs 
        when a new language is added to the database.
        """
        is_new_language = self._state.adding  # Check if this is a new language being added

        super().save(*args, **kwargs)  # Save the new language entry in the database

        if is_new_language:  # If a new language is added, translate all existing FAQs
            translator = Translator()  # Initialize the Google Translate API

            all_faqs = FAQ.objects.all()  # Retrieve all existing FAQs
            for faq in all_faqs:
                # Translate question and answer from English to the newly added language
                translated_question = translator.translate(faq.question, src='en', dest=self.code).text
                translated_answer = translator.translate(faq.answer, src='en', dest=self.code).text

                # Create and save the translated FAQ entry in the Translation model
                Translation.objects.create(
                    faq=faq,
                    language=self,
                    question=translated_question,
                    answer=translated_answer
                )

# ---------------------------------------------
# FAQ Model: Stores frequently asked questions in English
# ---------------------------------------------
class FAQ(models.Model):
    question = models.TextField()  # Stores the FAQ question in text format
    answer = RichTextField()  # Stores the FAQ answer with rich text formatting (using CKEditor)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the FAQ is created

    def save(self, *args, **kwargs):
        """ 
        Override the save method to translate the FAQ into all available languages 
        and update the cache to keep translations fresh.
        """
        cache_key = "faq_translations_en"  # Cache key for storing English FAQs
        cache.delete(cache_key)  # Clear cache to ensure updated FAQs are stored
        super().save(*args, **kwargs)  # Save the FAQ in the database

        translator = Translator()  # Initialize Google Translate API
        all_languages = Language.objects.all()  # Retrieve all available languages

        # Iterate through all languages and create translations
        for lang in all_languages:
            if lang.code:
                cache_key = f"faq_translations_{lang.code}"  # Cache key for each translated language
                cache.delete(cache_key)  # Clear translation cache to refresh data
                
                # Translate question and answer from English to the target language
                translated_question = translator.translate(self.question, src='en', dest=lang.code).text
                translated_answer = translator.translate(self.answer, src='en', dest=lang.code).text
                
                # Save the translated FAQ in the Translation model
                Translation.objects.create(
                    faq=self,
                    language=lang,
                    question=translated_question,
                    answer=translated_answer
                )

# ---------------------------------------------
# Translation Model: Stores translated FAQs for different languages
# ---------------------------------------------
class Translation(models.Model):
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='translations')  
    # Links to the original FAQ (deleting the FAQ deletes all translations)
    
    language = models.ForeignKey(Language, on_delete=models.CASCADE)  
    # Links to the corresponding language of the translation

    question = models.TextField()  # Stores the translated question
    answer = RichTextField()  # Stores the translated answer (supports rich text formatting)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the translation is created
