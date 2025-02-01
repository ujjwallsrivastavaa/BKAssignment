from rest_framework import serializers
from .models import FAQ, Translation  # Importing FAQ and Translation models

# Serializer for the FAQ model
class FAQSerializer(serializers.ModelSerializer):
    """
    Serializer for the FAQ model to return basic FAQ data (question and answer).
    """
    class Meta:
        model = FAQ  # Define the model to use
        fields = ['question', 'answer']  # Specify the fields to serialize (question and answer)

# Serializer for translated FAQ data
class TranslatedFAQSerializer(serializers.Serializer):
    """
    Serializer to return the translated version of the FAQ (question and answer).
    """
    question = serializers.CharField()  # Serializes the question field as a CharField
    answer = serializers.CharField()  # Serializes the answer field as a CharField
