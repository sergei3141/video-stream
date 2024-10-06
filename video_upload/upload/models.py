from django.db import models
from django.contrib.auth.models import User

class VideoUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    group_id = models.IntegerField(null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # В байтах
    mime_type = models.CharField(max_length=50)
    uploaded_chunks = models.IntegerField(default=0)  # Количество загруженных чанков
    total_chunks = models.IntegerField()  # Всего чанков
    current_chunk_index = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    checksum = models.CharField(max_length=64, null=True, blank=True)  # Контрольная сумма для проверки целостности

    def __str__(self):
        return f"Upload {self.file_name} (user: {self.user}, group: {self.group_id})"
