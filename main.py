import os
import secrets
from typing import List, Optional
from collections import Counter
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select
import smtplib
from email.message import EmailMessage

from database import create_db_and_tables, get_session
from models import Course, ClickEvent, MaterialRequest

app = FastAPI(title="Academic Vault API", version="2.0")
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")

# --- CONFIGURATION (now pulled from environment variables) ---
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "changeme")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD")
ALERT_RECEIVER_EMAIL = os.getenv("ALERT_RECEIVER_EMAIL", SENDER_EMAIL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # If this throws, EVERY route 500s (this is likely what's happening now).
    # Wrapping in try/except + logging so Vercel logs actually show the real cause
    # instead of a bare crash, and so a bad DB connection doesn't nuke static routes.
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"[STARTUP ERROR] Failed to initialize database: {e}")
        raise


# --- SECURITY DEPENDENCY ---
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# --- PUBLIC API ROUTES ---

@app.get("/api/courses", response_model=List[Course])
def read_courses(level: Optional[int] = None, semester: Optional[int] = None, session: Session = Depends(get_session)):
    query = select(Course)
    if level:
        query = query.where(Course.level == level)
    if semester:
        query = query.where(Course.semester == semester)
    return session.exec(query).all()


@app.post("/api/courses", response_model=Course)
def create_course(course: Course, session: Session = Depends(get_session)):
    course.course_code = course.course_code.upper().strip()
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


@app.get("/api/go/{course_code}")
def redirect_to_drive(course_code: str, session: Session = Depends(get_session)):
    clean_code = course_code.upper().strip()
    course = session.exec(select(Course).where(Course.course_code == clean_code)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    session.add(ClickEvent(course_code=course.course_code))
    session.commit()
    return RedirectResponse(url=course.drive_link, status_code=307)


# --- SINGLE, CONSOLIDATED /api/requests ROUTE (duplicate removed) ---
@app.post("/api/requests", response_model=MaterialRequest)
def create_request(request: MaterialRequest, session: Session = Depends(get_session)):
    session.add(request)
    session.commit()
    session.refresh(request)

    # --- INSTANT EMAIL ALERT (best-effort; never blocks the request) ---
    if SENDER_EMAIL and SENDER_APP_PASSWORD and ALERT_RECEIVER_EMAIL:
        try:
            msg = EmailMessage()
            msg.set_content(
                f"Name: {request.student_name} ({request.level}L)\n"
                f"Topic: {request.requested_topic}\n"
                f"Phone: {request.phone_number}"
            )
            msg["Subject"] = f"🚨 New Vault Request from {request.student_name}"
            msg["From"] = SENDER_EMAIL
            msg["To"] = ALERT_RECEIVER_EMAIL

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5)
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Email failed to send: {e}")
    else:
        print("Email alert skipped: SENDER_EMAIL/SENDER_APP_PASSWORD not configured.")

    return request


# --- SECURE ADMIN DASHBOARD ---

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, username: str = Depends(get_current_username), session: Session = Depends(get_session)):
    pending_requests = session.exec(select(MaterialRequest).order_by(MaterialRequest.timestamp.desc())).all()

    all_clicks = session.exec(select(ClickEvent)).all()
    click_counts = Counter([event.course_code for event in all_clicks])
    trending = [{"course": code, "clicks": count} for code, count in click_counts.most_common(10)]

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "request": request,
            "requests": pending_requests,
            "trending": trending,
        },
    )


# MUST BE LAST: Mount the static frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
