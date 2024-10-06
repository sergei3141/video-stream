from django.urls import path
from .views import VideoUploadInitView, VideoChunkUploadView, VideoUploadCompleteView

urlpatterns = [
    path('video/upload/init/', VideoUploadInitView.as_view(), name='video-upload-init'),
    path('video/upload/<int:upload_id>/chunk/', VideoChunkUploadView.as_view(), name='video-chunk-upload'),
    path('video/upload/<int:upload_id>/complete/', VideoUploadCompleteView.as_view(), name='video-upload-complete'),
]
