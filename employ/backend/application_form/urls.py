from django.urls import path
from .views import ApplicationFormView, ApplicationView, DepartmentApplicantsView, DepartmentListView

urlpatterns = [
    path("forms/", ApplicationFormView.as_view()),  # 지원서 양식 생성
    path("applications/", ApplicationView.as_view()), # 지원서 제출
    path("department-list/", DepartmentListView.as_view()),  # 회사별 부서 목록 조회
    path("department-applications/", DepartmentApplicantsView.as_view()), # 특정 회사 특정 부서의 지원자 리스트
]