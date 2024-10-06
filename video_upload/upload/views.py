import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload
from .serializer import VideoUploadInitSerializer, VideoChunkUploadSerializer, VideoChunkCompleteSerializer

class VideoUploadInitView(APIView):
    serializer_class = VideoUploadInitSerializer

    def post(self, request):
        serializer = VideoUploadInitSerializer(data=request.data)
        if serializer.is_valid():
            upload = serializer.save()
            return Response({'upload_id': upload.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoChunkUploadView(APIView):
    serializer_class = VideoChunkUploadSerializer
    def patch(self, request, upload_id):
        try:
            upload = VideoUpload.objects.get(id=upload_id, completed=False)
        except VideoUpload.DoesNotExist:
            return Response({'error': 'Upload not found or already completed'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoChunkUploadSerializer(data=request.data)
        if serializer.is_valid():
            chunk_index = serializer.validated_data['chunk_index']
            chunk_file = serializer.validated_data['chunk']

            if chunk_index != upload.current_chunk_index:
                return Response({'error': 'Incorrect chunk order'}, status=status.HTTP_400_BAD_REQUEST)

            # Сохраняем чанк на диск
            chunk_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', str(upload.id))
            os.makedirs(chunk_dir, exist_ok=True)
            chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_index}")
            
            with open(chunk_path, 'wb') as f:
                for chunk in chunk_file.chunks():
                    f.write(chunk)

            # Обновляем состояние загрузки
            upload.current_chunk_index += 1
            upload.uploaded_chunks += 1
            upload.save()

            return Response({'status': 'Chunk uploaded'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoUploadCompleteView(APIView):
    serializer_class = VideoChunkCompleteSerializer
    def post(self, request, upload_id):
        try:
            upload = VideoUpload.objects.get(id=upload_id, completed=False)
        except VideoUpload.DoesNotExist:
            return Response({'error': 'Upload not found or already completed'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, все ли чанки загружены
        if upload.uploaded_chunks != upload.total_chunks:
            return Response({'error': 'Not all chunks uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # Собираем все чанки в один файл
        chunk_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', str(upload.id))
        output_file_path = os.path.join(settings.MEDIA_ROOT, 'videos', upload.file_name)
        
        with open(output_file_path, 'wb') as output_file:
            for chunk_index in range(upload.total_chunks):
                chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_index}")
                with open(chunk_path, 'rb') as chunk_file:
                    output_file.write(chunk_file.read())

        # Обновляем статус загрузки
        upload.completed = True
        upload.save()

        # Удаляем временные файлы чанков
        for chunk_index in range(upload.total_chunks):
            chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_index}")
            os.remove(chunk_path)
        os.rmdir(chunk_dir)

        return Response({'status': 'Upload complete', 'file_url': output_file_path}, status=status.HTTP_200_OK)
