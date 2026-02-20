from . import views
from django.urls import path



urlpatterns=[
    path('',views.user_listview,name='user_list'),
    path('<int:user_id>/', views.chat_view, name='chat'),


]