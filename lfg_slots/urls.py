from django.urls import path
from lfg_slots import views

urlpatterns = [
    path('lfg_slots/', views.LFG_SlotList.as_view()),
    path('lfg_slots/<int:pk>/', views.LFG_SlotDetail.as_view())
]
