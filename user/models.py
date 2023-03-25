from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class User(AbstractBaseUser):  # 프로필 사진, 닉네임, 이름, 이메일주소(회원가입 아이디), 비밀번호(디폴트 사용)
    profile_image = models.TextField()
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField()
    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = "user"
