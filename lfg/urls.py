from django.urls import path
from lfg import views

urlpatterns = [
    path('lfg/', views.LFGList.as_view()),
    path('lfg/<int:pk>/', views.LFGDetail.as_view())
]
