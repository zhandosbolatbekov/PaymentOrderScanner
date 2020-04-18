from django.urls import path
from .views import *

urlpatterns = [
    path('images/upload', ImageCreate.as_view()),
    path('images/<int:pk>', ImageDetail.as_view()),
    path('images', ImageList.as_view()),
]