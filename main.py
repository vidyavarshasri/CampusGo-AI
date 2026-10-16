from pathlib import Path

import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Project location
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Create application
app = FastAPI(
    title="CampusGo AI",
    description="AI-powered student companion",
    version="1.0.0",
)

# Serve frontend files
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

# Local AI settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"


# Data received from the frontend
class ChatRequest(BaseModel):
    message: str


class CareerRequest(BaseModel):
    skills: list[str]
    interests: str = ""


# Home page
@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


# Check whether Ollama and the model are available
@app.get("/api/health")
def health():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=3,
        )
        response.raise_for_status()

        models = response.json().get("models", [])

        installed = any(
            model.get("name", "").startswith(MODEL_NAME)
            for model in models
        )

        return {
            "app": "CampusGo AI",
            "ollama": "connected",
            "model": MODEL_NAME,
            "model_installed": installed,
        }

    except requests.RequestException:
        return {
            "app": "CampusGo AI",
            "ollama": "disconnected",
            "model": MODEL_NAME,
            "model_installed": False,
        }


# AI study assistant
@app.post("/api/chat")
def chat(data: ChatRequest):
    message = data.message.strip()

    if not message:
        return {"reply": "Please enter a question."}

    prompt = f"""
You are CampusGo AI, a student learning assistant.

Explain Python, web development, science and other study
topics in simple English. Use Telugu if requested.

Give step-by-step answers when helpful.
Do not invent sources, jobs or events.
Be clear when you are uncertain.
Never ask students for passwords or sensitive details.

Student question: {message}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )
        response.raise_for_status()

        answer = response.json().get("response", "").strip()

        return {
            "reply": answer or "The AI returned an empty answer."
        }

    except requests.RequestException:
        return {
            "reply": (
                "Local AI is unavailable. Check Ollama and "
                "confirm the Gemma model is installed."
            )
        }


# AI career roadmap
@app.post("/api/career")
def career(data: CareerRequest):
    skills = ", ".join(data.skills) or "Not provided"
    interests = data.interests.strip() or "Not provided"

    prompt = f"""
Create a beginner-friendly student career roadmap.

Student skills: {skills}
Student interests: {interests}

Include:
1. Possible career paths
2. Skills to learn
3. A four-week study plan
4. Beginner projects
5. Topics to practice

Do not guarantee employment or salary.
Explain that this is AI-generated guidance.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )
        response.raise_for_status()

        return {
            "roadmap": response.json().get("response", "")
        }

    except requests.RequestException:
        return {
            "roadmap": (
                "AI is unavailable. Start Ollama and "
                "check the Gemma model installation."
            )
        }


# Sample events; these are not live listings
@app.get("/api/events")
def events():
    return {
        "demo": True,
        "events": [
            {
                "title": "Python Practice Meetup",
                "category": "Learning",
                "details": "Practice Python problems.",
            },
            {
                "title": "Student Project Day",
                "category": "Projects",
                "details": "Share projects and learn together.",
            },
            {
                "title": "Hackathon Preparation",
                "category": "Hackathon",
                "details": "Prepare a problem statement and prototype.",
            },
        ],
    }


# Sample food menu; no real orders
@app.get("/api/food")
def food():
    return {
        "demo": True,
        "items": [
            {"name": "Veg Sandwich", "price": 40},
            {"name": "Idli", "price": 30},
            {"name": "Lemon Rice", "price": 50},
        ],
    }


# Simulated ride endpoint
@app.post("/api/rides")
def rides():
    return {
        "demo": True,
        "message": (
            "Demo only. No driver is contacted and "
            "no ride is booked."
        ),
    }