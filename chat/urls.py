from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),
    path('api/index/', views.api_index, name='api_index'),
    path('api/chat/', views.api_chat, name='api_chat'),
]
