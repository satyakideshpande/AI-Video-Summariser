import os
import firebase_admin
import requests
import whisper
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from firebase_admin import storage
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from api.models.video_models import VideoUploadLogs
from moviepy.editor import VideoFileClip
from transformers import pipeline

# Load Whisper model once to avoid repeated loading
whisper_model = whisper.load_model("base")

# Load Hugging Face summarization model once
summarizer = pipeline("summarization")


def extract_audio(video_path, audio_path):
    """Extract audio from a video and save it as a .mp3 file."""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


def transcribe_audio(audio_path):
    """Convert audio into text using Whisper."""
    result = whisper_model.transcribe(audio_path)
    return result['text']


def summarize_text(text):
    """Summarize transcribed text using Hugging Face."""
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']


@swagger_auto_schema(
    method='post',
    operation_description="Upload a video file to Firebase and return the public URL along with an AI-generated summary",
    manual_parameters=[
        openapi.Parameter(
            'video',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description="Video file to upload",
            required=True
        ),
    ],
    responses={200: openapi.Response("Success", openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'video_url': openapi.Schema(type=openapi.TYPE_STRING, description="Firebase public video URL"),
            'summary': openapi.Schema(type=openapi.TYPE_STRING, description="AI-generated summary of the video content"),
        }
    ))},
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  # Enable file upload in Swagger
def upload_video(request):
    try:
        """ Upload video to Firebase, extract & summarize its content """
        if 'video' not in request.FILES and 'video_url' not in request.data:
            return Response({'error': 'No video file provided'}, status=400)

        video_url = request.data.get('video_url')
        temp_path = None  # Track local file path

        if video_url:
            # Download video from URL
            video_download_response = requests.get(video_url, stream=True)
            if video_download_response.status_code == 200:
                video_name = video_url.split("/")[-1]
                temp_path = f'media/{video_name}'
                with open(temp_path, 'wb') as file:
                    for chunk in video_download_response.iter_content(1024):
                        file.write(chunk)
            else:
                VideoUploadLogs.objects.create(
                    file_name=video_url,
                    status="Failed"
                )
                return Response({"error": "Failed to download video"}, status=400)
        else:
            video_file = request.FILES['video']
            temp_path = default_storage.save(f'media/{video_file.name}', video_file)

        # Upload to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'videos/{video_file.name if not video_url else video_name}')
        blob.upload_from_filename(temp_path)
        blob.make_public()  # Make URL accessible

        # Extract audio
        audio_path = f'{os.path.splitext(temp_path)[0]}.mp3'
        extract_audio(temp_path, audio_path)

        # Transcribe audio
        transcription = transcribe_audio(audio_path)

        # Summarize transcription
        summary = summarize_text(transcription)

        # Log success to database
        VideoUploadLogs.objects.create(
            file_name=video_file.name if not video_url else video_name,
            status="Success"
        )

        # Clean up local files
        os.remove(temp_path)
        os.remove(audio_path)

        return Response({'video_url': blob.public_url, 'summary': summary})

    except Exception as e:
        # Log failure to database
        VideoUploadLogs.objects.create(
            file_name=video_file.name if 'video' in request.FILES else video_url,
            status="Failed"
        )
        return Response({'error': str(e)}, status=500)
