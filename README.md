# CampusGo AI

**Your Campus. Your World. One App.**

CampusGo AI is an offline-first AI student companion prototype.

## Features

- Local AI study assistant using Ollama and Gemma
- AI-generated career roadmap
- Sample student events
- Sample campus food menu
- Optional browser location access
- Demo-only campus ride request

## Technologies

- Python
- FastAPI
- HTML, CSS and JavaScript
- Ollama
- Gemma 3 1B
- Git and GitHub

## Requirements

Install Python, Git and Ollama before running the project.

## Installation

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Download the AI model:

```powershell
ollama pull gemma3:1b
```

## Run the application

```powershell
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## API documentation

Open http://127.0.0.1:8000/docs

## Current limitations

Events and food are sample data.
Rides are simulated; no driver is contacted.
Location displays coordinates only.
Live jobs, PDF question answering, student accounts,
interactive maps and notifications are not implemented yet.

## Privacy

Location permission is optional.
Do not enter sensitive personal information.