from django.urls import path
from user_notes import views

urlpatterns = [
    path('usernotes/', views.UserNoteList.as_view()),
    path('usernotes/<int:pk>/', views.UserNoteDetail.as_view())
]
