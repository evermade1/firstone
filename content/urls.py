from django.urls import path
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark

urlpatterns = [
    path('upload', UploadFeed.as_view()), #content/views에 있음
    path('profile', Profile.as_view()),
    path('main', Main.as_view()),
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view())
]