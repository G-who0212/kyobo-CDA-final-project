from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('application/', ApplicantAPIView.as_view()),
    path('applicationsall/', include(router.urls)),
]
