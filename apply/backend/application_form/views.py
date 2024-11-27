from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status
from.serializers import ApplicationSerializer
from django_filters.rest_framework import DjangoFilterBackend
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

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
    # body_html = f"""
    # <html lang="ko">
    # <head>
    #     <meta charset="UTF-8">
    #     <title>지원 확인 메일</title>
    # </head>
    # <body style="text-align: center;">
    #     <h1>{applicant_name}님, 지원서가 성공적으로 제출되었습니다!</h1>
    #     <p>지원해 주셔서 감사합니다.</p>
    #     <div>
    #         <img src="https://email-image-easycruit.s3.ap-northeast-2.amazonaws.com/Easycruit.png" alt="Easycruit Logo" style="width: 100px; margin: 10px 0;">
    #         <img src="https://email-image-easycruit.s3.ap-northeast-2.amazonaws.com/kyobodtslogo.jpg" alt="Kyobo DTS Logo" style="width: 150px;">
    #     </div>
    #     <p>이 메일은 자동 발송된 메일입니다. 문의사항이 있으면 <a href="mailto:easycruit00@gmail.com">easycruit00@gmail.com</a>으로 연락해 주세요.</p>
    # </body>
    # </html>
    # """

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