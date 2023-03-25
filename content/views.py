from uuid import uuid4
import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
from Instagram.settings import MEDIA_ROOT
from .models import feed, like, reply, bookmark


# Create your views here.
class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if not email:  # 로그인 안 한 상태로 접속한 경우
            return render(request, "user/login.html")

        user1 = User.objects.filter(email=email).first()
        if not user1:  # 유저 정보가 db 내에 없는 경우
            return render(request, "user/login.html")

        feed_object_list = feed.objects.all().order_by('-id')  # feed에 있는 모든 걸 가져오겠다. = select * from content_feed;
        feed_list = []
        for i in feed_object_list:
            reply_object_list = reply.objects.filter(feed_id=i.id)
            reply_list = []
            for j in reply_object_list:
                user = User.objects.filter(email=j.email).first()
                reply_list.append(dict(reply_content=j.reply_content,
                                       nickname=user.nickname))
            user = User.objects.filter(email=i.email).first()
            like_count = like.objects.filter(feed_id=i.id, is_like=True).count()
            reply_count = reply.objects.filter(feed_id=i.id).count()
            is_liked = like.objects.filter(feed_id=i.id, email=email, is_like=True).exists()
            is_marked = bookmark.objects.filter(feed_id=i.id, email=email, is_bookmark=True).exists()
            feed_list.append(dict(id=i.id,
                                  image=i.image,
                                  content=i.content,
                                  like_count=like_count,
                                  nickname=user.nickname,
                                  profile_image=user.profile_image,
                                  reply_list=reply_list,
                                  reply_count=reply_count,
                                  is_liked=is_liked,
                                  is_marked=is_marked))

        return render(request, 'Instagram/main.html', context=dict(feeds=feed_list, user=user1))


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:  # 파일 저장하는 코드
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        email = request.session.get('email', None)

        feed.objects.create(image=image, content=content, email=email)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        if not email:  # 로그인 안 한 상태로 접속한 경우
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()
        if not user:  # 유저 정보가 db 내에 없는 경우
            return render(request, "user/login.html")

        feed_list = feed.objects.filter(email=email).all().order_by('-id')
        feed_count = feed.objects.filter(email=email).count()
        like_list = list(like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = feed.objects.filter(id__in=like_list)
        bookmark_list = list(bookmark.objects.filter(email=email, is_bookmark=True).values_list('feed_id', flat=True))
        bookmark_feed_list = feed.objects.filter(id__in=bookmark_list)
        return render(request, 'content/profile.html',
                      context=dict(feed_list=feed_list, feed_count=feed_count, like_feed_list=like_feed_list,
                                   bookmark_feed_list=bookmark_feed_list, user=user))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)
        reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)
        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        is_like = request.data.get('is_like', True)
        if is_like == 'True' or is_like == 'true':
            is_like = True
        else:
            is_like = False

        email = request.session.get('email', None)
        tmplike = like.objects.filter(feed_id=feed_id, email=email).first()
        if tmplike:
            tmplike.is_like = is_like
            tmplike.save()
        else:
            like.objects.create(feed_id=feed_id, is_like=is_like, email=email)
        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        is_bookmark = request.data.get('is_bookmark', True)
        if is_bookmark == 'True' or is_bookmark == 'true':
            is_bookmark = True
        else:
            is_bookmark = False

        email = request.session.get('email', None)
        tmpbookmark = bookmark.objects.filter(feed_id=feed_id, email=email).first()
        if tmpbookmark:
            tmpbookmark.is_bookmark = is_bookmark
            tmpbookmark.save()
        else:
            bookmark.objects.create(feed_id=feed_id, is_bookmark=is_bookmark, email=email)
        return Response(status=200)
