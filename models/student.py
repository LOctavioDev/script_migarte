from typing import List, Optional, Dict

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
        
# ! MODEL OF STUDENT        
class Student:
    def __init__(self, control_number, name, generation, activity, company, employment_status, sector, participation, contact_source):
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
