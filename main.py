import secrets
import requests
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

# --- CONFIGURATION ---
ADMIN_USER = "gracious"
ADMIN_PASS = "campaign2026"
@app.post("/api/requests", response_model=MaterialRequest)
def create_request(request: MaterialRequest, session: Session = Depends(get_session)):
    session.add(request)
    session.commit()
    session.refresh(request)

    # --- INSTANT EMAIL ALERT ---
    try:
        sender_email = "dmlmedia08@gmail.com"
        app_password = "jitfuxktfpuqenda" 
        receiver_email = "oluwademiladefaminu@gmail.com" # Send it to yourself

        msg = EmailMessage()
        msg.set_content(f"Name: {request.student_name} ({request.level}L)\nTopic: {request.requested_topic}\nPhone: {request.phone_number}")
        msg['Subject'] = f"🚨 New Vault Request from {request.student_name}"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Connect to Gmail's server securely
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Email failed to send: {e}")
    # ----------------------------

    return request
# ---------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- SECURITY DEPENDENCY ---
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- PUBLIC API ROUTES ---

@app.get("/api/courses", response_model=List[Course])
def read_courses(level: Optional[int] = None, semester: Optional[int] = None, session: Session = Depends(get_session)):
    query = select(Course)
    if level: query = query.where(Course.level == level)
    if semester: query = query.where(Course.semester == semester)
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
    if not course: raise HTTPException(status_code=404, detail="Course not found")

    # Log click securely
    session.add(ClickEvent(course_code=course.course_code))
    session.commit()
    return RedirectResponse(url=course.drive_link, status_code=307)

@app.post("/api/requests", response_model=MaterialRequest)
def create_request(request: MaterialRequest, session: Session = Depends(get_session)):
    session.add(request)
    session.commit()
    session.refresh(request)

    # Trigger Instant Phone Alert
    if WEBHOOK_URL:
        message = (
            f"🚨 **New Material Request** 🚨\n"
            f"**Name:** {request.student_name} ({request.level}L)\n"
            f"**Topic:** {request.requested_topic}\n"
            f"**Phone:** {request.phone_number}"
        )
        try:
            # Format tailored for Discord. Adjust if using Telegram.
            requests.post(WEBHOOK_URL, json={"content": message}, timeout=3)
        except Exception as e:
            print(f"Webhook failed: {e}")

    return request

# --- SECURE ADMIN DASHBOARD ---

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, username: str = Depends(get_current_username), session: Session = Depends(get_session)):
    # 1. Fetch pending requests
    pending_requests = session.exec(select(MaterialRequest).order_by(MaterialRequest.timestamp.desc())).all()
    
    # 2. Calculate trending courses (Simple Python count for speed)
    all_clicks = session.exec(select(ClickEvent)).all()
    click_counts = Counter([event.course_code for event in all_clicks])
    trending = [{"course": code, "clicks": count} for code, count in click_counts.most_common(10)]

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "request": request,
            "requests": pending_requests,
            "trending": trending
        }
    )

# MUST BE LAST: Mount the static frontend 
app.mount("/", StaticFiles(directory="static", html=True), name="static")   