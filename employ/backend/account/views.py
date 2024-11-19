from django.shortcuts import render, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token # access token & refresh token
from rest_framework.permissions import IsAuthenticated

from .serializers import UserLoginSerializer, UserRegisterSerializer, UserSerializer, ApplicationSerializer, ApplicationPartialSerializer
from .models import User
import requests
from rest_framework import status

# from apply.backend.application_form import views, models


class UserRegisterAPIView(APIView):
    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token: Token = TokenObtainPairSerializer.get_token(user)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": str(token.access_token),
                        "refresh": str(token),
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request: Request):
        token_serializer = TokenObtainPairSerializer(data=request.data) # 로그인 정보를 바탕으로 토큰 발급
        if token_serializer.is_valid():
            user = token_serializer.user
            serializer = UserLoginSerializer(user)
            return Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": token_serializer.validated_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request: Request):
        user = request.user  # 현재 토큰으로 인증된 사용자
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        user = request.user  # 현재 인증된 사용자
        serializer = UserSerializer(user, data=request.data, partial=True)  # 부분 업데이트 허용
        if serializer.is_valid():  # 유효성 검사
            serializer.save()  # 유저 정보 업데이트
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        user = request.user  # 현재 인증된 사용자
        user.delete()  # 사용자 계정 삭제
        return Response({"detail": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    

class ApplicantListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        # apply 서비스의 API 호출
        # print(f"user company {user.company}")
        response = requests.get(f'http://apply-service.default.svc.cluster.local:80/api/applicationsall/applications/?applying_to={user.company}')
        # response = requests.get(f'http://127.0.0.1:8000/api/applicationsall/applications/?applying_to={user.company}')
        
        if response.status_code == 200:
            data = response.json()
            # print("Fetched data:", data)
            filtered_data = [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'submitted_at': item['submitted_at'],
                    'phone_num': item['phone_num'],
                    'date_of_birth': item['date_of_birth']
                }
                for item in data
            ]
            # print("Filtered data:", filtered_data)
            serializer = ApplicationPartialSerializer(data=filtered_data, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Failed to fetch applications'}, status=response.status_code)

class ApplicantDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        # 특정 지원자의 정보를 apply 서비스에서 가져옴
        response = requests.get(f'http://apply-service.default.svc.cluster.local:80/api/applicationsall/applications/{pk}/')
        # response = requests.get(f'http://127.0.0.1:8000/api/applicationsall/applications/{pk}/')
        
        if response.status_code == 200:
            data = response.json()
            # 회사 일치 여부 확인
            # print(f"data: {data}")
            if data['applying_to'] == user.company:
                serializer = ApplicationSerializer(data=data)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Unauthorized access to this application.'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({'error': 'Application not found'}, status=response.status_code)