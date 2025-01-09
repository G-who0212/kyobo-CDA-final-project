from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    is_active = BooleanField(default=True) # 활성화된 사용자인지 설정 False이면 비활성화된 사용자로, 로그인할 수 없음.
    is_admin = BooleanField(default=False)# 관리자 권한을 가진 사용자인지 -> Django의 관리자 사이트로 로그인할 수 있는지.

    USERNAME_FIELD = 'email' # 로그인 ID로 지정할 필드

    REQUIRED_FIELDS = ['name', 'company']

    objects = UserManager()

    def __str__(self):
        return self.name
    
    @property
    def is_staff(self):
        return self.is_admin