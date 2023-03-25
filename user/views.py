import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from Instagram.settings import MEDIA_ROOT
from .models import User
from django.contrib.auth.hashers import make_password


# Create your views here.
class join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):  # 회원가입
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email, nickname=nickname, name=name, password=make_password(password),
                            profile_image="default_profile.jpg")

        return Response(status=200)


class login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):  # 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))
        if user.check_password(password):
            # 로그인을 했다. 세션 or 쿠키에 넣는다.
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))


class logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class Uploadprofile(APIView):
    def post(self, request):
        file = request.FILES['file'] #파일 불러오기
        email = request.data.get('email') #이메일 불러오기 
        uuid_name = uuid4().hex #파일 이름 바꾸는 로직 사용하여 랜덤 고유값 만들기
        save_path = os.path.join(MEDIA_ROOT, uuid_name) #그 값을 media_root에 저장
        with open(save_path, 'wb+') as destination:  # 파일 저장하는 코드
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name #그렇게 만든 이름을 프로필 이미지라는 변수에 저장

        user = User.objects.filter(email=email).first() #유저에서 필터로 이메일 동일한 유저 찾기
        user.profile_image = profile_image #해당 유저의 프로필 이미지 바꿔주기
        user.save() #create에서는 자동저장이므로 필요없지만 변경사항이 있으므로 저장

        return Response(status=200)
