from django.urls import path
from . import views

urlpatterns = [
    path('choices/', views.choice_list, name='choice_list'),
    path('choices/<int:pk>/', views.choice_detail, name='choice_detail'),
    path('groups/', views.group_list, name='group_list'),
    # path('groups/<int:pk>/', views.group_detail, name='group_detail'),
]
