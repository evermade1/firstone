from django.db import models


# Create your models here.
class feed(models.Model):
    content = models.TextField()  # 댓글내용
    image = models.TextField()  # 피드 이미지
    email = models.EmailField(default="")  # 글쓴이


class like(models.Model):
    feed_id = models.IntegerField(default=0)  # 어떤 컨텐츠에 좋아요 눌렀는지
    email = models.EmailField(default="")  # 좋아요 누른 사람
    is_like = models.BooleanField(default=True)  # 좋아요 눌렀는지 여부 - 눌렀다 취소시 업데이트 되도록 함


class reply(models.Model):
    feed_id = models.IntegerField(default=0)  # 어떤 컨텐츠에 댓글 눌렀는지
    email = models.EmailField(default='')  # 댓글 단 사람
    reply_content = models.TextField()


class bookmark(models.Model):
    feed_id = models.IntegerField(default=0)  # 어떤 컨텐츠에 북마크 눌렀는지
    email = models.EmailField(default="")  # 북마크 누른 사람
    is_bookmark = models.BooleanField(default=True)  # 아직 저장되어 있는지 여부
