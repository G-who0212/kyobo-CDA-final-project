from django.urls import path
from .views import *

urlpatterns = [
    path('application/', RecordAPIView.as_view()),
]