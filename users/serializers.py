from rest_framework import serializers
from .models import Document

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document  # Ensure this is correct
        fields = ['id', 'customer_name', 'file', 'status', 'created_at']
