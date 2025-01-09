from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status
from.serializers import ApplicationSerializer
from django_filters.rest_framework import DjangoFilterBackend
import requests, boto3
from botocore.exceptions import ClientError
from django.conf import settings


# 지원자가 질문 목록을 가져오는 API
class ApplicationFormView(APIView):
    def get(self, request):
        company_name = request.query_params.get("company_name")
        department = request.query_params.get("department")

        if not company_name or not department:
            return Response({"error": "Company name and department are required."}, status=status.HTTP_400_BAD_REQUEST)

        # employ 서비스의 API 호출
        try:
            response = requests.get(
                f"http://127.0.0.1:8001/application_form/forms/?company_name={company_name}&department={department}"
            )
            response_data = response.json()

            if response.status_code == 200:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 지원자가 지원서를 제출하는 API
class ApplicationSubmissionView(APIView):
    def post(self, request):
        form_id = request.data.get("form_id")
        applicant_name = request.data.get("applicant_name")
        application_data = request.data.get("application_data")

        if not form_id or not applicant_name or not application_data:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # employ 서비스의 API 호출
        try:
            response = requests.post(
                "http://127.0.0.1:8001/application_form/applications/",
                json={
                    "form_id": form_id,
                    "applicant_name": applicant_name,
                    "application_data": application_data,
                },
            )
            response_data = response.json()

            if response.status_code == 201:
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_email(applicant_name, applicant_email):
    # AWS SES 클라이언트 생성
    ses_client = boto3.client(
        'ses',
        region_name='ap-northeast-2',  # SES가 활성화된 AWS 리전
        aws_access_key_id='XXX',
        aws_secret_access_key='XXX'
    )

    # 이메일 내용 설정
    subject = "지원서 제출이 완료되었습니다!"
    body_text = f"{applicant_name}님, 지원서가 성공적으로 제출되었습니다!"
    sender_email = "easycruit00@gmail.com"
    recipient_email = applicant_email

    # 이메일 전송
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [recipient_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    },
                }
            }
        )
    except ClientError as e:
        # print(f"Error sending email: {e}")
        pass
    else:
        print("Email sent! Message ID:", response['MessageId'])








class ApplicantAPIView(APIView):
    def post(self, request: Request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():  # 유효성 검사
            application = serializer.save()  # 지원서 객체 생성 및 저장
            # 이메일 전송
            applicant_name = application.name
            applicant_email = application.email
            send_email(applicant_name, applicant_email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# for employ service
from rest_framework import viewsets
from .models import Application

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [DjangoFilterBackend]  # Add filter backend
    filterset_fields = ['applying_to']  # Specify filterable fields