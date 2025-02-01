# Import necessary modules for Django admin customization
from django.contrib import admin  # Import Django's admin module
from .models import Language, FAQ, Translation  # Import the models to be registered in the admin panel
from ckeditor.widgets import CKEditorWidget  # CKEditor widget for rich text fields in the admin
from django import forms  # Django forms module for customization

# ---------------------------------------------
# Register Language Model in the Admin Panel
# ---------------------------------------------
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Language model.
    This allows managing available languages from the Django admin interface.
    """
    list_display = ('code',)  # Display only the language code in the admin list
    search_fields = ('code',)  # Enable searching by language code

# ---------------------------------------------
# Register FAQ Model in the Admin Panel
# ---------------------------------------------
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
    Admin configuration for the FAQ model.
    This enables managing FAQs, including their creation and content.
    """
    list_display = ('question', 'created_at')  # Display the FAQ question and creation date
    search_fields = ('question',)  # Allow searching FAQs by question text
    list_filter = ('created_at',)  # Provide a filter option based on the creation date

# ---------------------------------------------
# Register Translation Model in the Admin Panel
# ---------------------------------------------
@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Translation model.
    This allows managing translated FAQs in different languages.
    """
    list_display = ('faq_question', 'language_code', 'created_at')  
    # Display the original FAQ question, the translation language, and the creation date

    search_fields = ('faq__question', 'language__code')  
    # Enable searching translations by FAQ question text and language code

    list_filter = ('language',)  
    # Allow filtering translations by language

    # Custom method to display the related FAQ question in the admin panel
    def faq_question(self, obj):
        return obj.faq.question  # Retrieve the original question from the related FAQ model
    
    faq_question.admin_order_field = 'faq__question'  # Enable sorting by FAQ question in the admin panel
    faq_question.short_description = 'FAQ Question'  # Display label for the admin column

    # Custom method to display the related language code in the admin panel
    def language_code(self, obj):
        return obj.language.code  # Retrieve the language code from the related Language model
    
    language_code.admin_order_field = 'language__code'  # Enable sorting by language code in the admin panel
    language_code.short_description = 'Language'  # Display label for the admin column
