from rest_framework import serializers
from .models import AdminMessage

class AdminMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminMessage
        fields = ['id', 'subject', 'content', 'created_at', 'is_read']
        read_only_fields = ['created_at']