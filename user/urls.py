from django.urls import path
from .views import join, login, logout, Uploadprofile

urlpatterns = [
    path('join', join.as_view()),  # content/views에 있음
    path('login', login.as_view()),
    path('logout', logout.as_view()),
    path('profile/upload', Uploadprofile.as_view())
]
