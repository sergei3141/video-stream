from rest_framework.test import APITestCase
from django.urls import reverse
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

class VideoUploadTest(APITestCase):
    def test_video_upload_flow(self):
        # Инициализация загрузки
        init_url = reverse('video-upload-init')
        data = {
            'file_name': 'test_video.mp4',
            'file_size': 50000000,
            'mime_type': 'video/mp4',
            'total_chunks': 5,
            'user': None,
            'group_id': 1
        }
        response = self.client.post(init_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        upload_id = response.data['upload_id']

        # Загрузка чанков (симуляция чанков через SimpleUploadedFile)
        chunk_url = reverse('video-chunk-upload', args=[upload_id])
        for i in range(5):
            # Симуляция бинарных данных, имитирующих видеофайл
            chunk_content = BytesIO(b'\x00\x01\x02\x03\x04' * 1024 * 10)  # 10 KB данных
            chunk_file = SimpleUploadedFile(
                f'chunk_{i}.mp4', 
                chunk_content.getvalue(), 
                content_type='video/mp4'  # Указываем тип файла как видео
            )
            response = self.client.patch(chunk_url, {'chunk_index': i, 'chunk': chunk_file}, format='multipart')
            self.assertEqual(response.status_code, 200)

        # Завершение загрузки
        complete_url = reverse('video-upload-complete', args=[upload_id])
        response = self.client.post(complete_url)
        self.assertEqual(response.status_code, 200)
