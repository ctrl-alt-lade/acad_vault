from sqlmodel import Session, select
from database import engine, create_db_and_tables  # <-- create_db_and_tables imported
from models import Course

# 1. Master list of courses mapped to transcript titles
courses_to_add = [
    # --- 100 LEVEL: 1ST SEMESTER ---
    {
        "course_code": "CHM 101",
        "title": "General Chemistry I",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1UQPSPDkX2NOdHjw6AkmFOonNzViQ9dbY&usp=drive_copy"
    },
    {
        "course_code": "GEL 101",
        "title": "Principles and Practice of Excellent Living",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1Qh2VlUnHT_fI3VTA-J95KgSUHNDh9BF_&usp=drive_copy"
    },
    {
        "course_code": "GET 101",
        "title": "Engineer in Society",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1o0aOI5gNr1VqJAAtxkgI9wOsv_zpYw2c&usp=drive_copy"
    },
    {
        "course_code": "GST 111",
        "title": "Communication in English",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=10I_Nz6wEL-FojKgX7wlpaDP8qo3KlTEy&usp=drive_copy"
    },
    {
        "course_code": "LIB 101",
        "title": "Use of Library, Study Skills and ICT",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1NXny3pxiFkNyamaymHotFJt2ShW_crs5&usp=drive_copy"
    },
    {
        "course_code": "MTH 101",
        "title": "Elementary Mathematics I (Algebra & Trigonometry)",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1GTEeFZsm8GLk3Wg25HAWWwM54zW5jJ5d&usp=drive_copy"
    },
    {
        "course_code": "PHY 101",
        "title": "General Physics I (Mechanics)",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1v1ExuSbUlp89QQyRg7dvMhWkm5av7ILc&usp=drive_copy"
    },
    {
        "course_code": "PHY 103",
        "title": "General Physics III (Behaviour of Matter)",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1HQ-1BA23KQ_1-zfqZcVKPwkRYDxTvObi&usp=drive_copy"
    },
    {
        "course_code": "STA 112",
        "title": "Probability I",
        "level": 100,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1WSL68V3BSO9bmnDJG36oFmOi8CJrycZS&usp=drive_copy"
    },

    # --- 100 LEVEL: 2ND SEMESTER ---
    {
        "course_code": "CHM 102",
        "title": "General Chemistry II",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1gMsXbxnuwLekD0SKFubsIBAW3b-iprxL&usp=drive_copy"
    },
    {
        "course_code": "EES 102",
        "title": "Fundamentals of Entrepreneurship",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1fKLGogE-tLZfF1JTJya8S43jG2JxH2az&usp=drive_copy"
    },
    {
        "course_code": "GEL 102",
        "title": "Public Speaking Essentials",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1gMsXbxnuwLekD0SKFubsIBAW3b-iprxL&usp=drive_copy"
    },
    {
        "course_code": "GET 102",
        "title": "Engineering Graphics and Solid Modelling I",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1fKLGogE-tLZfF1JTJya8S43jG2JxH2az&usp=drive_copy"
    },
    {
        "course_code": "GST 112",
        "title": "Nigerian Peoples and Culture",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1ezCSmMOQpG0iZxW7oIfEO88CbWO8-CNt&usp=drive_copy"
    },
    {
        "course_code": "MCE 102",
        "title": "Introduction to Mechatronics Engineering",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1clRDJ-oNl7bo2hzj1o75G33EFMgEsI2U&usp=drive_copy"
    },
    {
        "course_code": "MTH 102",
        "title": "Elementary Mathematics II (Calculus)",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1DmHdXe2A7WSvgfzS6jXOmPFYzFAy4vwc&usp=drive_copy"
    },
    {
        "course_code": "MTH 103",
        "title": "Elementary Mathematics III (Vectors, Geometry & Dynamics)",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=15ojQe1xdx9bl1Ptwy1xmlWiKzCBU_etC&usp=drive_copy"
    },
    {
        "course_code": "PHY 102",
        "title": "General Physics II (Electricity & Magnetism)",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1n82MVL9gN7Nyez5O-qWyXmOHWvJsV2yv&usp=drive_copy"
    },
    {
        "course_code": "PHY 108",
        "title": "General Practical Physics II",
        "level": 100,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1HTYxsclpqMJ7DGb-iYssHIV7l4FWgw4v&usp=drive_copy"
    },

    # --- 200 LEVEL: 1ST SEMESTER ---
    {
        "course_code": "ENT 211",
        "title": "Entrepreneurship and Innovation",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1QVF8tg04TMzP3M9KEwaH5AXHRVoKsMXF&usp=drive_copy"
    },
    {
        "course_code": "GEL 203",
        "title": "Principles and Fundamentals of Godly Living",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=15_vGIKq-iYYX0uhDu97YMMnn6U1nzhaE&usp=drive_copy"
    },
    {
        "course_code": "GET 201",
        "title": "Applied Electricity I",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1GOGB_wSvJm3ba8zCgwDLcFdc6W2ngq2w&usp=drive_copy"
    },
   {
        "course_code": "GET 201 (Archive)",
        "title": "Applied Electricity I (Alternate Folder)",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1oaw3WPpeJt6OAD7XCxjz7sFr1k5D1JvQ&usp=drive_copy"
    },
    {
        "course_code": "GET 203",
        "title": "Engineering Graphics and Solid Modelling I",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=16Yfrc0RFW0fFnBSBQKYhStbHtyuAI1yT&usp=drive_copy"
    },
    {
        "course_code": "GET 209",
        "title": "Engineering Mathematics I",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1bBIupep2Cv96Gg0H3nrZVT6vNkuDJ6H5&usp=drive_copy"
    },
    {
        "course_code": "GET 211",
        "title": "Computing and Software Engineering",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1krO9BgGpN9L4bbBp9WGvwImSI13ztmjZ&usp=drive_copy"
    },
    {
        "course_code": "GET 205",
        "title": "Fundamentals of Fluid Mechanics",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1ki4KEJ3J9REDVg6lrpcjef19F28qfqTB&usp=drive_copy"
    },
    {
        "course_code": "ITC 201",
        "title": "Information Technology Certification (ITC) I",
        "level": 200,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1BkU8rtl6UwBNYZS-lgo8KzrFm48lSrqS&usp=drive_copy"
    },

    # --- 200 LEVEL: 2ND SEMESTER ---
    {
        "course_code": "EEE 202",
        "title": "[Course Title Unknown]",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1onzrzZ_v7YWZhSDh-2AhtHWT21ahnM1G&usp=drive_copy"
    },
    {
        "course_code": "EEE 204",
        "title": "[Course Title Unknown]",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1wFz5ZJjyi1qopRY-3NTn5dr3cFZP8cvP&usp=drive_copy"
    },
    {
        "course_code": "EES 202",
        "title": "Knowledge Acquisition",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1UQdu9lljJdjow7Gg4S4fwIC7HgbEjY-h&usp=drive_copy"
    },
    {
        "course_code": "GEL 202",
        "title": "Godly Disposition",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1mWp9O42jxFvlhNPC8ADVtf3BheDCYQCR&usp=drive_copy"
    },
    {
        "course_code": "GET 204",
        "title": "Students Workshop Practice",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1pfA-e699oy0UNSyWLf-HZFycmGU6zFai&usp=drive_copy"
    },
    {
        "course_code": "GET 202",
        "title": "Engineering Materials",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=10e5F4lRmJExMttXVs9Tr-7VZyEotL4IY&usp=drive_copy"
    },
    {
        "course_code": "GET 206",
        "title": "Fundamentals of Thermodynamics",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1yxFhfmNbUfqLNSZGAnD9tG-0Vso7y1ju&usp=drive_copy"
    },
    {
        "course_code": "GET 208",
        "title": "Strength of Materials",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1LLGUmDU6LGus9_tYZ3uwwVCm1kHb2vfJ&usp=drive_copy"
    },
    {
        "course_code": "GET 210",
        "title": "Engineering Mathematics II",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=16KOjPoUsHweYvgc637WfdP8MMg_oOaLz&usp=drive_copy"
    },
    {
        "course_code": "GST 212",
        "title": "Philosophy, Logic and Human Existence",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1IS0JB1GDapXjYVFH-sAz_qqFR-55kupd&usp=drive_copy"
    },
    {
        "course_code": "ITC 212",
        "title": "[Course Title Unknown]",
        "level": 200,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1OMhxQgb3au4M_Fr-U-n0ZwIpFR5YqJ8B&usp=drive_copy"
    },

    # --- 300 LEVEL: 1ST SEMESTER ---
    {
        "course_code": "CSA 301",
        "title": "New Horizons",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1aN-QsPj0UQeiEMlxs9lq7WE9qW80m-Yj&usp=drive_copy"
    },
    {
        "course_code": "EEE 303",
        "title": "[Course Title Unknown]",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1yxNRcv-1jof7IH-MO-Uh0qHo-FWFLSTK&usp=drive_copy"
    },
    {
        "course_code": "EEE 311",
        "title": "[Course Title Unknown]",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=156d4OovlCrAhOhUa_L1z5kXN5Y8En3jU&usp=drive_copy"
    },
    {
        "course_code": "EES 301",
        "title": "Knowledge Application",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1OLFapQLJdaR_UBK6b8Mji3j3KuVzlTav&usp=drive_copy"
    },
    {
        "course_code": "GEL 303",
        "title": "Sustainable Leadership, Governance and Development",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1hUyYcujjrCd6uIdcoxpupUMHAGUvUvZF&usp=drive_copy"
    },
    {
        "course_code": "GET 301",
        "title": "Engineering Mathematics III",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1kK4qjd0EiCa6md7wm-bLDsuxX0IaAKNQ&usp=drive_copy"
    },
    {
        "course_code": "GET 305",
        "title": "Engineering Statistics and Data Analytics",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1ZlqUSEQszmVze3EG6Zilvjq_3x6GqR5u&usp=drive_copy"
    },
    {
        "course_code": "GET 307",
        "title": "Introduction to AI, Machine Learning & Convergent Tech",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1VU1DClXt-XvFo1iTThBBQrhEywJ0EYQZ&usp=drive_copy"
    },
    {
        "course_code": "MCE 301",
        "title": "Electric Circuit Theory",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1kMBlKOh9b-7BvLj-eQYl220csPJMUO2N&usp=drive_copy"
    },
    {
        "course_code": "MCE 303",
        "title": "Electromechanical Devices",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=12gJroWmkRim5yUjslMboRalJi16PPx8K&usp=drive_copy"
    },
    {
        "course_code": "MCE 305",
        "title": "Electromagnetic Fields and Waves",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=1Vdjz4KeG13gKUl0Ka15NbQDZ-_7cHcT2&usp=drive_copy"
    },
    {
        "course_code": "MCE 321",
        "title": "Design of Mechatronics and Robotics Systems I",
        "level": 300,
        "semester": 1,
        "drive_link": "https://drive.google.com/open?id=12XZoA_J9MWY3rYiAYs1W6FETtltyLmtv&usp=drive_copy"
    },

    # --- 300 LEVEL: 2ND SEMESTER ---
    {
        "course_code": "EEE 324",
        "title": "[Course Title Unknown]",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1Red2EPZe-PzsIUklfVYBUftVp86--ra2&usp=drive_copy"
    },
    {
        "course_code": "EEE 326",
        "title": "[Course Title Unknown]",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1e9RCdkvnIWM1qTnBQzVRXcMKhTor6Puy&usp=drive_copy"
    },
    {
        "course_code": "ENT 312",
        "title": "Venture Creation",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1aWGcRPPid_DXem-mbyh78n63vqT0OFhD&usp=drive_copy"
    },
    {
        "course_code": "GEL 304",
        "title": "Leadership Imperatives and Enquiry",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1ZqRb4lLSCNx0XuEOiCEwrC0p1xA573vN&usp=drive_copy"
    },
    {
        "course_code": "GET 302",
        "title": "Engineering Mathematics IV",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1IaDG2pJWwIbioyXE_fr865aRLTyV1HBv&usp=drive_copy"
    },
    {
        "course_code": "GET 304",
        "title": "Technical Writing & Communication",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1_b1Az_Ex4UR5fhUAMXFYpTjfkkSIpo8Q&usp=drive_copy"
    },
    {
        "course_code": "GET 306",
        "title": "Renewable Energy Systems and Technology",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1VUWSbezBaeIH_rOhgHlaAzRWHV4hUdNc&usp=drive_copy"
    },
    {
        "course_code": "MCE 302",
        "title": "Signals and Systems Analysis",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1H_ldUoayv6xhRB_jjgnM8X7H1fHRelWK&usp=drive_copy"
    },
    {
        "course_code": "MCE 304",
        "title": "Digital Electronic Circuits",
        "level": 300,
        "semester": 2,
        "drive_link": "https://drive.google.com/open?id=1l8FqpdcufOfBz54NggHtKVN-R2BniAnn&usp=drive_copy"
    }
]

# 2. Inject them into the database
def seed_database():
    create_db_and_tables()  
    
    with Session(engine) as session:
        for item in courses_to_add:
            course_code_clean = item["course_code"].upper().strip()
            
            # 1. Check if the course already exists in the live vault
            existing_course = session.exec(select(Course).where(Course.course_code == course_code_clean)).first()
            
            if existing_course:
                # 2. If it exists, just update it with the new committee links
                existing_course.title = item["title"]
                existing_course.level = item["level"]
                existing_course.semester = item["semester"]
                existing_course.drive_link = item["drive_link"]
                session.add(existing_course)
                print(f"Updated existing course: {course_code_clean}")
            else:
                # 3. If it does not exist, add it fresh
                new_course = Course(
                    course_code=course_code_clean,
                    title=item["title"],
                    level=item["level"],
                    semester=item["semester"],
                    drive_link=item["drive_link"]
                )
                session.add(new_course)
                print(f"Added new course: {course_code_clean}")
        
        # Save all changes at once
        session.commit()
        print("\n✅ All courses successfully synced to the live database!")

if __name__ == "__main__":
    seed_database()