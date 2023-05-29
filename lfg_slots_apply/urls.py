from django.urls import path
from lfg_slots_apply import views

urlpatterns = [
    path('lfg_slots_apply/',
         views.LFGSlotApplyList.as_view()),
    path('lfg_slots_apply_pagination/',
         views.LFGSlotApplyPagination.as_view()),
    path('lfg_slots_apply/<int:pk>/',
         views.LFGSlotApplyDetail.as_view()),
    path('lfg_slots_apply_update/<int:pk>/',
         views.LFGSlotUpdateDetail.as_view())
]
