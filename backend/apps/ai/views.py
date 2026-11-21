from rest_framework import generics
from rest_framework.response import Response

from common.permissions import IsUser, IsMerchant
from .models import AIRecommendation, AICopywriting, AIAssistantSession
from .serializers import (
    RecommendationRequestSerializer,
    AIRecommendationSerializer,
    CopywritingRequestSerializer,
    AICopywritingSerializer,
    AssistantRequestSerializer,
    AIAssistantSessionSerializer,
)
from .services import generate_recommendations, generate_copywriting, assistant_reply


class RecommendationView(generics.GenericAPIView):
    """生成推荐（POST）+ 历史记录（GET）"""
    permission_classes = [IsUser]
    serializer_class = RecommendationRequestSerializer

    def post(self, request):
        serializer = RecommendationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        limit = serializer.validated_data['limit']
        result = generate_recommendations(request.user, limit)
        rec = AIRecommendation.objects.create(
            user=request.user,
            product_ids=[r['product_id'] for r in result],
            reason='根据浏览与收藏偏好推荐',
        )
        return Response({'recommendations': result, 'recommendation_id': rec.id})

    def get(self, request):
        qs = AIRecommendation.objects.filter(user=request.user).order_by('-created_at')
        return Response(AIRecommendationSerializer(qs, many=True).data)


class CopywritingView(generics.GenericAPIView):
    """生成商品文案（商家）"""
    permission_classes = [IsMerchant]
    serializer_class = CopywritingRequestSerializer

    def post(self, request):
        serializer = CopywritingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = generate_copywriting(data['name'], data['category'], data['selling_points'])
        cw = AICopywriting.objects.create(
            merchant=request.user,
            title=result['title'],
            description=result['description'],
            selling_points=result['selling_points'],
        )
        return Response(AICopywritingSerializer(cw).data)


class AssistantView(generics.GenericAPIView):
    """购物助手对话（用户）"""
    permission_classes = [IsUser]
    serializer_class = AssistantRequestSerializer

    def post(self, request):
        serializer = AssistantRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id')

        result = assistant_reply(message)

        if session_id:
            session = AIAssistantSession.objects.filter(id=session_id, user=request.user).first()
            if not session:
                return Response({'detail': '会话不存在'}, status=404)
        else:
            session = AIAssistantSession.objects.create(
                user=request.user,
                title=message[:50],
                messages=[],
            )

        messages = session.messages or []
        messages.append({'role': 'user', 'content': message})
        messages.append({'role': 'assistant', 'content': result['reply']})
        session.messages = messages
        session.save()

        return Response({
            'session_id': session.id,
            'reply': result['reply'],
            'products': result['products'],
            'suggestions': result['suggestions'],
        })


class AssistantSessionListView(generics.ListAPIView):
    """助手会话列表（用户）"""
    permission_classes = [IsUser]
    serializer_class = AIAssistantSessionSerializer

    def get_queryset(self):
        return AIAssistantSession.objects.filter(user=self.request.user).order_by('-updated_at')
