from sqlmodel import Session
from database import engine, create_db_and_tables  # <-- Add create_db_and_tables here
from models import Course

# 1. Define your master list of courses here
courses_to_add = [
    {
        "course_code": "GET 301",
        "title": "Engineering Mathematics III",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/drive/folders/1s9m_z8TzgDYCC1IZnRvSXfd1zrU2bTFY?usp=drive_link"
    },
    {
        "course_code": "GET 305",
        "title": "Engineering Statistics and Data Analysis",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/drive/folders/1b7DwxDH8z59ykCbEz3iwP7W3p6Og2EcH?usp=drive_link"
    },
    {
            "course_code": "GET 307",
            "title": "Introduction to Artificial Intelligence, Machine Learning, and Convergent Technologies",
            "level": 300,
            "semester": 1,
            "drive_link": "https://drive.google.com/drive/folders/1plWm-pfU0j3LDb6zgVvyHndmPZfWItud?usp=drive_link"
    },
    {
        "course_code": "MCE 301",
        "title": "Electric Circuit Theory",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/drive/folders/18geyLZZVOMwj8hTMYbKvwVwnPlOTy5P6?usp=drive_link"
    },
    {
        "course_code": "MCE 303",
        "title": "Electromechanical Devices",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/drive/folders/16SuXeINqix8qg-XrP4vvcKqmpxCj7_-h?usp=drive_link"
    },
    {
        "course_code": "MCE 305",
        "title": "Electromagnetic Fields and Waves",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/drive/folders/1pnF4BpNkqsjVTYc1n_5bT0R8DVVkIefU?usp=drive_link"
    },
    {
        "course_code": "MCE 321",
        "title": "Design of Mechatronic Systems",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/drive/folders/1rkH_dJmXcT-yC2twuMpMzidGAe83Iig6?usp=drive_link"
    },
    {
        "course_code": "ENT 312",
        "title": "Venture Creation", # Title wasn't visible in the image
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/drive/folders/1hUnbQyVqrIhBpfACQ7qPsH_pYQ12mczU?usp=drive_link"
    },
    {
        "course_code": "GEL 304",
        "title": "Leadership Imperatives and Enquiry", # Title wasn't visible in the image
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/drive/folders/17aNxYMtRH_WM00pK_j7qdSj1h6FDZsoW?usp=drive_link"
    },
    {
        "course_code": "GET 302",
        "title": "Engineering Mathematics",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/drive/folders/1BlXssPb44DgY_ERw1vILroqjZs6VgQTw?usp=drive_link"
    },
    {
        "course_code": "GET 304",
        "title": "Technical Writing and...", # Complete the title here
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/drive/folders/1gigOOAGLCensaskAECzu-bHs0vQawGsr?usp=drive_linkE"
    },
    {
        "course_code": "GET 306",
        "title": "Renewable Energy",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/drive/folders/1ItGJ6kmoPVxUBhMtj86sWsh0oPSGRJIN?usp=drive_link"
    },
    {
        "course_code": "MCE 102",
        "title": "Introduction to...", # Complete the title here
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/drive/folders/1zBvrqEH_AxBjThFy1lCb6ejDjjeHRjlo?usp=drive_link"
    },
    {
        "course_code": "MCE 302",
        "title": "Signals and Systems",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/drive/folders/1WpfdCOlTQ0EMpudMW4d4Rzh7s93cL2VN?usp=drive_link"
    },
    {
        "course_code": "MCE 304",
        "title": "Digital Electronic...", # Complete the title here
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/drive/folders/18eOaSO3pZL0Ik6KXM6qiKqHKugz_wEqS?usp=drive_link"
    }
    # Just copy-paste this block for every course you have
]

# 2. Inject them into the database
def seed_database():
    create_db_and_tables()  # <-- Add this line right here!
    
    with Session(engine) as session:
        for item in courses_to_add:
            # ... rest of your code ...
            # Create a new Course object
            new_course = Course(
                course_code=item["course_code"].upper().strip(),
                title=item["title"],
                level=item["level"],
                semester=item["semester"],
                drive_link=item["drive_link"]
            )
            session.add(new_course)
            print(f"Added {new_course.course_code} to the vault.")
        
        # Save all changes at once
        session.commit()
        print("\n✅ All courses successfully routed to the database!")

if __name__ == "__main__":
    seed_database()