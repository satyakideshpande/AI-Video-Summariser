AI Video Summarizer 🎥✨
This project is an AI-powered video summarization tool that extracts key insights from videos by:

Uploading videos to Firebase Storage

Extracting audio from the video

Transcribing the audio using Whisper AI

Summarizing the transcribed text using Hugging Face LLM

Tech Stack 🛠️
Backend: Python, Django, Django REST Framework

AI Models:

Whisper (Speech-to-Text)

Hugging Face Transformers (Text Summarization)

Storage: Firebase Cloud Storage

Frontend: React.js (Vite)

Database: PostgreSQL (or any configured DB for Django)

APIs: REST API (Django)

Features 🚀
✅ Upload videos via file upload or URL
✅ Extract audio from video
✅ Convert speech to text using Whisper AI
✅ Generate a summarized version of the video content
✅ Store videos securely on Firebase
✅ REST API for integration with other applications

Installation & Setup ⚙️
1️⃣ Backend Setup (Django + FastAPI)
Clone the repository
bash
Copy
Edit
git clone <your-github-repo-url>
cd ai-video-summarizer
Create a virtual environment & install dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

pip install -r requirements.txt
Set up Firebase credentials
Add your firebase_admin.json file in the root directory

Ensure your settings.py has Firebase configuration

Run the backend
bash
Copy
Edit
python manage.py runserver
2️⃣ Frontend Setup (React + Vite)
Navigate to frontend folder
bash
Copy
Edit
cd frontend/summary-scribe-react
Install dependencies
bash
Copy
Edit
npm install
Run the frontend
bash
Copy
Edit
npm run dev
API Endpoints 🌐
Upload Video
Endpoint: POST /upload-video/

Body: multipart/form-data

Response:

json
Copy
Edit
{
  "video_url": "https://your-firebase-link.com/video.mp4",
  "summary": "This is the AI-generated summary of the video..."
}
Environment Variables 🔑
Create a .env file with:

plaintext
Copy
Edit
FIREBASE_CREDENTIALS=firebase_admin.json
HUGGINGFACE_API_KEY=your_api_key
