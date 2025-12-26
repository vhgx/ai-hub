from django.urls import path
from .views import predict_view, intro_view

urlpatterns = [
    path("", intro_view, name="home"),
    path("predict/", predict_view, name="predict"),
]