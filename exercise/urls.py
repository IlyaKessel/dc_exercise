from django.urls import re_path
from engine import views

urlpatterns = [
    re_path(r'^', views.ProxyView.as_view(), name='proxy'),
]
