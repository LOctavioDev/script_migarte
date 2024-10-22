from models.student import Student
from config.db import get_db_connection
# from utils.excel_reader import read_excel
import pandas as pd
import json
import re

def migrate_data(excel_file):
    # db = get_db_connection()
    # students_collection = db.students
    
    df = pd.read_excel(excel_file, usecols=[1, 2, 3], skiprows=3, header=None, names=['NO_CONTROL', 'NOMBRE', 'GENERACION'])
    
    for index, row in df.iterrows():
        control_number = row['NO_CONTROL']
        name = row['NOMBRE']
        generation = row['GENERACION']

        name_parts = name.split()
        first_name = name_parts[-1] 
        last_name = name_parts[0]
        middle_name = name_parts[1]


        generation_parts = re.split(r'[-/ ]+', generation)
        print(f'==={generation_parts}===')
        if len(generation_parts) >= 4:
            start_semester = generation_parts[0]
            start_year = int(generation_parts[1])
            end_semester = generation_parts[2]
            end_year = int(generation_parts[3])


        student_data = {
            "no_control": control_number,
            "nombre": {
                "primero": first_name,
                "apellido_paterno": last_name,
                "apellido_materno": middle_name
            },
            "generacion": {
                "inicio": { "anio": start_year, "semestre": start_semester }, 
                "fin": { "anio": end_year, "semestre": end_semester }
            }
        }

        print(json.dumps(student_data, indent=4, ensure_ascii=False))