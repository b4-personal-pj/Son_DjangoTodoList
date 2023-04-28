from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name="post-view"),
    path('detail-post/<int:post_id>/', views.DetailPostView.as_view(), name="detail-post"),
]
