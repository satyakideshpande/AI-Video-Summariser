from django.urls import path
from api.views.video_views import upload_video

urlpatterns = [
    path('upload/', upload_video, name='upload-video'),
]
