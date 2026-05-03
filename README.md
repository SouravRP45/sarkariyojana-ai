# SarkariYojana AI 🇮🇳

An AI-powered Government Scheme Finder for Indian citizens. Discovers welfare schemes based on a citizen's profile and provides a conversational RAG-powered chat interface in English and Hindi.

## 🚀 Features
- **Smart Matching**: Rule-based eligibility matching for Central and State schemes.
- **RAG Chatbot**: Powered by Gemini 2.0 Flash and local ChromaDB to answer complex queries based *only* on official scheme data.
- **Bilingual**: Works in English and Hindi.
- **Glassmorphism UI**: Beautiful, mobile-first responsive design.
- **Free Tier Tech Stack**: Uses local embeddings (`all-MiniLM-L6-v2`) and Gemini's generous free tier.

## 🛠️ Local Setup

1. **Prerequisites**: Python 3.11+
2. **Clone & Setup Env**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure API Key**:
   - Get a free key from [Google AI Studio](https://aistudio.google.com).
   - Copy `backend/.env.example` to `backend/.env` and add your key.
4. **Run Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Open `http://localhost:8000` in your browser.

## 🐳 Docker Setup
```bash
docker-compose up --build
```

## ☁️ Deployment (Render.com)
1. Push this repository to GitHub.
2. Sign in to [Render.com](https://render.com) and click **New > Web Service**.
3. Connect your repository. Render will automatically detect the `render.yaml` file.
4. Set the `GEMINI_API_KEY` environment variable in the Render dashboard.
5. Deploy!

## 📜 License
MIT
