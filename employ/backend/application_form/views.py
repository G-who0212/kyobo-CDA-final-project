from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ApplicationForm, Company, Application
from .utils import get_company_from_token
from django.shortcuts import get_object_or_404
from django.http import Http404

# 회사 담당자가 지원서 양식을 생성하는 API
class ApplicationFormView(APIView):
    def post(self, request):
        company_name = get_company_from_token(request)
        department = request.data.get("department")
        form_schema = request.data.get("form_schema")

        if not company_name or not department or not form_schema:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # company, created = Company.objects.get_or_create(company_name=company_name)

        company = Company.objects(company_name=company_name).first()
        if not company:
            company = Company(company_name=company_name)
            company.save()

        form = ApplicationForm.objects(company=company, department=department).first()
        if form:
            # 기존 지원서 양식이 있으면 업데이트
            form.form_schema = form_schema
            form.save()
            return Response({"message": "Form updated successfully!"}, status=status.HTTP_200_OK)
        else:
            # 새로운 지원서 양식 생성
            form = ApplicationForm(company=company, department=department, form_schema=form_schema)
            form.save()
            return Response({"message": "Form created successfully!"}, status=status.HTTP_201_CREATED)
        
        # form = ApplicationForm(company=company, department=department, form_schema=form_schema)
        # form.save()

        # return Response({"message": "Form created successfully!"}, status=status.HTTP_201_CREATED)
    
    # GET 방식: 특정 회사의 지원서 양식 조회
    def get(self, request):
        company_name = request.query_params.get("company_name")
        department = request.query_params.get("department")

        if not company_name or not department:
            return Response({"error": "Company name and department are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(company_name=company_name)
            form = ApplicationForm.objects.get(company=company, department=department)

            form_data = {
                "id": str(form.id),
                "company_name": form.company.company_name,
                "department": form.department,
                "form_schema": form.form_schema,
            }
            return Response(form_data, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        except ApplicationForm.DoesNotExist:
            return Response({"error": "Form not found for the specified department."}, status=status.HTTP_404_NOT_FOUND)
        

class ApplicationView(APIView):
    # POST 방식: 지원서 제출
    def post(self, request):
        print("Incoming data:", request.data)

        form_id = request.data.get("form_id")
        applicant_name = request.data.get("applicant_name")
        application_data = request.data.get("application_data")
        if not form_id or not applicant_name or not application_data:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            form = ApplicationForm.objects.get(id=form_id)
        except ApplicationForm.DoesNotExist:
            return Response({"error": "Invalid form ID."}, status=status.HTTP_404_NOT_FOUND)

        application = Application(
            form=form,
            applicant_name=applicant_name,
            application_data=application_data
        )
        application.save()

        return Response({"message": "Application submitted successfully!"}, status=status.HTTP_201_CREATED)

    # GET 방식: 특정 지원서 조회 -> 이거 고쳐야함.
    def get(self, request):
        applicantid = request.query_params.get("applicantid")

        if not applicantid:
            return Response({"error": "applicantid is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            application = Application.objects.get(id=applicantid)

            # JSON 데이터로 반환
            return Response({
                "application": {
                    "applicant_name": application.applicant_name,
                    "application_data": application.application_data,
                    "created_at": application.created_at.isoformat(),
                }
            }, status=status.HTTP_200_OK)

        except Application.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DepartmentListView(APIView):
    def get(self, request):
        company_name = get_company_from_token(request)

        try:
            company = Company.objects.get(company_name=company_name)
            departments = ApplicationForm.objects.filter(company=company).distinct('department')

            return Response({"departments": list(departments)}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

class DepartmentApplicantsView(APIView):
    def get(self, request):
        company_name = get_company_from_token(request)
        department = request.query_params.get("department")
        if not company_name or not department:
            return Response({"error": "Company name and department are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(company_name=company_name)
            form = ApplicationForm.objects.get(company=company, department=department)
            applications = Application.objects.filter(form=form)

            applicant_list = [
                {
                    "id": str(application.id),
                    "applicant_name": application.applicant_name,
                    "application_data": application.application_data,
                    "created_at": application.created_at
                }
                for application in applications
            ]

            return Response({"applicants": applicant_list}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        except ApplicationForm.DoesNotExist:
            return Response({"error": "Form not found for the specified department."}, status=status.HTTP_404_NOT_FOUND)