from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
import sys, os
from .views import *
# from apply.backend.application_form import views

current_dir = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.abspath(os.path.join(current_dir, "../../../apply/backend"))
sys.path.append(target_path)

urlpatterns = [
    path('signup/', UserRegisterAPIView.as_view()), # 회원가입
    path('signin/', UserLoginAPIView.as_view()), # 로그인
    path('userinfo/', UserAPIView.as_view()), # 관리자 정보 확인
    path('applicants/', ApplicantListAPIView.as_view(), name='applicant-list'),
    path('applicants/<int:pk>/', ApplicantDetailAPIView.as_view(), name='applicant-detail'),
    # path('refresh/', TokenRefreshView.as_view()), # FE에서 만료된 access Token을 보냈을 때
]