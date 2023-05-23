from django.urls import path
from profiles import views
from .views import user_email

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
    path('profiles/email/<int:user_id>/', user_email, name='user_email'),
]
