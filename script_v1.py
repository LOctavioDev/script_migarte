from typing import List, Optional, Dict
from pymongo import MongoClient

client = MongoClient("mongodb+srv://octadev:112020a@clusteroctavio.n8a1lsl.mongodb.net/db_residency?retryWrites=true&w=majority&appName=ClusterOctavio")
db = client.db_residency
students_collection = db.students

class Name:
    def __init__(self, first: str, last: str, middle: Optional[str] = None):
        self.first = first
        self.last = last
        self.middle = middle

class Generation:
    def __init__(self, start: Dict[str, int], end: Dict[str, int]):
        self.start = start
        self.end = end

class Activity:
    def __init__(self, activities: List[str]):
        self.activities = activities

class Company:
    def __init__(self, name: str, location: Dict[str, str], position: str, years_in_position: int, job_type: str):
        self.name = name
        self.location = location
        self.position = position
        self.years_in_position = years_in_position
        self.job_type = job_type

class EmploymentStatus:
    def __init__(self, types: List[str]):
        self.types = types

class Sector:
    def __init__(self, category: str, type: str):
        self.category = category
        self.type = type

class Participation:
    def __init__(self, status: str):
        self.status = status

class ContactSource:
    def __init__(self, source: str):
        self.source = source

class Student:
    def __init__(self, control_number: str, name: Name, generation: Generation, activity: Activity,
                 company: Company, employment_status: EmploymentStatus, sector: Sector,
                 participation: Participation, contact_source: ContactSource):
        self.control_number = control_number
        self.name = name
        self.generation = generation
        self.activity = activity
        self.company = company
        self.employment_status = employment_status
        self.sector = sector
        self.participation = participation
        self.contact_source = contact_source

    def to_dict(self):
        return {
            "control_number": self.control_number,
            "name": {
                "first": self.name.first,
                "last": self.name.last,
                "middle": self.name.middle
            },
            "generation": {
                "start": self.generation.start,
                "end": self.generation.end
            },
            "activity": {
                "activities": self.activity.activities
            },
            "company": {
                "name": self.company.name,
                "location": self.company.location,
                "position": self.company.position,
                "years_in_position": self.company.years_in_position,
                "job_type": self.company.job_type
            },
            "employment_status": {
                "types": self.employment_status.types
            },
            "sector": {
                "category": self.sector.category,
                "type": self.sector.type
            },
            "participation": {
                "status": self.participation.status
            },
            "contact_source": {
                "source": self.contact_source.source
            }
        }

student_example = Student(
    control_number="F14390167",
    name=Name(first="Jorge", last="Aldana", middle="Limatitla"),
    generation=Generation(
        start={"year": 2014, "semester": "August"},
        end={"year": 2018, "semester": "December"}
    ),
    activity=Activity(activities=["works"]),
    company=Company(
        name="STARDUST INC. S.A. DE C.V.",
        location={"city": "Puebla", "municipality": "Huauchinango", "state": "Puebla"},
        position="Mobile Applications Developer",
        years_in_position=3,
        job_type="Department Head"
    ),
    employment_status=EmploymentStatus(types=["contract"]),
    sector=Sector(category="tertiary", type="private"),
    participation=Participation(status="partial"),
    contact_source=ContactSource(source="PERSONAL CONTACTS")
)

students_collection.insert_one(student_example.to_dict())

inserted_student = students_collection.find_one({"control_number": "F14390167"})
print(inserted_student)
