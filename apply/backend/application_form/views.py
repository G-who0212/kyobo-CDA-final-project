from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status
from.serializers import ApplicationSerializer

class RecordAPIView(APIView):
    def post(self, request: Request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():  # 유효성 검사
            serializer.save()  # 유저 정보 업데이트
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)