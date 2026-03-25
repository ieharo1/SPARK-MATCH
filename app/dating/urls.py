from django.urls import path
from . import views

urlpatterns = [
    path('discover/', views.discover, name='discover'),
    path('swipe/', views.swipe, name='swipe'),
    path('matches/', views.matches_list, name='matches_list'),
    path('chat/<int:match_id>/', views.chat, name='chat'),
    path('chat/<int:match_id>/messages/', views.get_new_messages, name='get_new_messages'),
    path('unmatch/<int:match_id>/', views.unmatch, name='unmatch'),
]
