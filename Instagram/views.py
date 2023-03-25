from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self, request):
        feed_list = feed.objects.all()  # feed에 있는 모든 걸 가져오겠다. = select * from content_feed;
        print(feed_list)
        return render(request, 'Instagram/main.html')
