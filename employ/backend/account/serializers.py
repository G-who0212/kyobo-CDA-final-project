from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User

User = get_user_model()


from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer): # 회원가입
    password2 = serializers.CharField(write_only=True)  # password2 필드 추가

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'name', 'company']  # 필요한 필드만 나열
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # password와 password2가 일치하는지 검증
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    # create 메서드 수정: password2는 저장하지 않음
    def create(self, validated_data):
        validated_data.pop('password2')  # password2 필드를 제거
        user = User.objects.create_user(**validated_data)  # create_user 메서드 사용
        return user

class UserLoginSerializer(serializers.ModelSerializer): # 로그인
    class Meta:
        model = User
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'company')

class ApplicationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    applying_to = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    date_of_birth = serializers.CharField(max_length=6)
    phone_num = serializers.CharField(max_length=15)
    email = serializers.EmailField(max_length=100)
    residence = serializers.CharField(max_length=100)
    educational_background = serializers.CharField(max_length=50)
    school = serializers.CharField(max_length=100)
    major = serializers.CharField(max_length=100)
    certificate = serializers.CharField(max_length=200)
    it_experience = serializers.CharField(max_length=200)
    education_experience = serializers.CharField(max_length=50)
    it_career_experience = serializers.CharField(max_length=50)
    card_possession = serializers.CharField(max_length=100)
    motivation_career_plan = serializers.CharField()
    source_of_info = serializers.CharField(max_length=100)
    submitted_at = serializers.DateField()



class ApplicationPartialSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    submitted_at = serializers.DateField()
    phone_num = serializers.CharField(max_length=15)
    date_of_birth = serializers.CharField(max_length=6)