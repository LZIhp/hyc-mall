from rest_framework import serializers

from .models import AIRecommendation, AICopywriting, AIAssistantSession


class RecommendationRequestSerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=10, min_value=1, max_value=50)


class AIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRecommendation
        fields = ('id', 'product_ids', 'reason', 'created_at')


class CopywritingRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    selling_points = serializers.CharField()


class AICopywritingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AICopywriting
        fields = ('id', 'title', 'description', 'selling_points', 'created_at')


class AssistantRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=False)
    message = serializers.CharField()


class AIAssistantSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIAssistantSession
        fields = ('id', 'title', 'messages', 'created_at', 'updated_at')
