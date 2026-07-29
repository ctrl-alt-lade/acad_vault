from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_code: str = Field(index=True, unique=True)  # e.g., "GET 301"
    title: str                                          # e.g., "Engineering Mathematics"
    level: int                                          # 100, 200, 300
    semester: int                                       # 1 or 2
    drive_link: str                                     # Google Drive Folder URL

class ClickEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_code: str = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MaterialRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_name: str
    phone_number: str
    level: int
    requested_topic: str
    status: str = Field(default="Pending")
    timestamp: datetime = Field(default_factory=datetime.utcnow)