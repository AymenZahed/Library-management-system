from rest_framework import serializers
from .models import Notification, NotificationTemplate, NotificationLog

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user_id", "type", "subject", "message", "status", "sent_at", "created_at"]
        read_only_fields = ["id", "sent_at", "created_at"]

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ["id", "name", "type", "subject_template", "message_template", "created_at"]
        read_only_fields = ["id", "created_at"]

class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = ["id", "notification", "status", "detail", "created_at"]
        read_only_fields = ["id", "created_at"]

class SendFromTemplateSerializer(serializers.Serializer):
    template_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    context = serializers.DictField(child=serializers.CharField(), required=False)
    # allow override of type/subject/message if needed
    type = serializers.ChoiceField(choices=Notification.TYPE_CHOICES, required=False)