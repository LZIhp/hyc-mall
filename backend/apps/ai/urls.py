from django.urls import path

from . import views

urlpatterns = [
    path('recommendations/', views.RecommendationView.as_view(), name='ai-recommendations'),
    path('copywriting/', views.CopywritingView.as_view(), name='ai-copywriting'),
    path('assistant/', views.AssistantView.as_view(), name='ai-assistant'),
    path('assistant/sessions/', views.AssistantSessionListView.as_view(), name='ai-assistant-sessions'),
]
