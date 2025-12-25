"""FastAPI Quiz Application."""
import random
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .parser import parse_quiz_markdown

app = FastAPI(title="Quiz ATBM")

# Setup static files and templates
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Load questions once at startup
QUIZ_FILE = BASE_DIR.parent / "docs" / "300 câu ATBM dành cho HS tiểu học.md"
QUESTIONS = parse_quiz_markdown(str(QUIZ_FILE))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render quiz homepage."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_questions": len(QUESTIONS)
    })


@app.get("/api/questions")
async def get_questions(shuffle: bool = True, limit: int = 10):
    """Get quiz questions."""
    questions = QUESTIONS.copy()
    if shuffle:
        random.shuffle(questions)
    if limit:
        questions = questions[:limit]
    
    # Return without correct answers for client
    return [{
        "id": q["id"],
        "question": q["question"],
        "options": q["options"]
    } for q in questions]


@app.post("/api/check")
async def check_answer(question_id: int, answer: str):
    """Check if answer is correct."""
    for q in QUESTIONS:
        if q["id"] == question_id:
            is_correct = q["correct"] == answer.upper()
            return {
                "correct": is_correct,
                "correct_answer": q["correct"]
            }
    return {"error": "Question not found"}
