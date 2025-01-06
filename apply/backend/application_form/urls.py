from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)


urlpatterns = [
    path("forms/", ApplicationFormView.as_view()),  # 질문 목록 조회
    path("applications/", ApplicationSubmissionView.as_view()),  # 지원서 제출


    path('application/', ApplicantAPIView.as_view()),
    path('applicationsall/', include(router.urls)),
]