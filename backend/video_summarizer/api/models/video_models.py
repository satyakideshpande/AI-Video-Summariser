from django.db import models

class VideoUploadLogs(models.Model):
    status_choices = ['Success', 'Failed']

    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    video_uploaded_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[(s, s) for s in status_choices])

    class Meta:
        db_table = 'video_upload_logs'  # Specify the table name explicitly
