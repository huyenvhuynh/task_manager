from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('', views.discussion_list, name='discussion_list'),
    path('<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('add/', views.add_discussion, name='add_discussion'),
]