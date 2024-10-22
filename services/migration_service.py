from models.student import Student
from config.db import get_db_connection
# from utils.excel_reader import read_excel
import pandas as pd
import json
import re

names_excel = ['NO_CONTROL', 'NOMBRE', 'GENERACION', 'SI', 'NO', 'ESTUDIA', 'ESTUDIA Y TRABAJA', 'NO ESTUDIA NI TRABAJA', 
               'EMPRESA', 'CIUDAD', 'MUNICIPIO', 'ESTADO', 'PUESTO', 'Menos de 1 año', '1 Año', '2 AÑOS', '3 AÑOS', 
               'Mas de 3 Años', 'OPERARIO','TÉCNICO', 'ADMINISTRATIVO', 'SUPERVISOR', 'JEFE DE AREA', 'FUNCIONARIO',
               'DIRECTIVO', 'EMPRESARIO', 'BASE', 'EVENTUAL', 'CONTRATO', 'OTRO', 'EDUCATIVO', 'PRIMARIO', 'SECUNDARIO',
               'TERCIARIO', 'PÚBLICO', 'PRIVADO', 'SOCIAL', 'SI', 'NO', 'PARCIAL', 'BOLSA DE TRABAJO ITSH', 
               'CONTACTOS PERSONALES', 'RESIDENCIA PROFESIONAL', 'OTRO']

usecols_me = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
              30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]

def migrate_data(excel_file):
    # db = get_db_connection()
    # students_collection = db.students
    
    df = pd.read_excel(excel_file, usecols=usecols_me, skiprows=3, header=None, names=names_excel)
    
    for index, row in df.iterrows():
        control_number = row['NO_CONTROL']
        name = row['NOMBRE']
        generation = row['GENERACION']
        company = row['EMPRESA']
        city = row['CIUDAD']
        state = row['ESTADO']
        municipality = row['MUNICIPIO']
        puesto = row['PUESTO']

        # ? NOMBRE COMPLETO
        name_parts = name.split()
        first_name = name_parts[-1] 
        last_name = name_parts[0]
        middle_name = name_parts[1]

        # ? GENERACION
        generation_parts = re.split(r'[-/ ]+', generation)
        if len(generation_parts) >= 4:
            start_semester = generation_parts[0]
            start_year = int(generation_parts[1])
            end_semester = generation_parts[2]
            end_year = int(generation_parts[3])
            
        # ? ACTIVIDAD ACTUAL
        
        actividad_actual = []
        if row['SI'] == 1:
            actividad_actual.append('trabaja')
        if row['NO'] == 1:
            actividad_actual.append('no trabaja')
        if row['ESTUDIA'] == 1:
            actividad_actual.append('estudia')
        if row['ESTUDIA Y TRABAJA'] == 1:
            actividad_actual.append('trabaja y estudia')
        if row['NO ESTUDIA NI TRABAJA'] == 1:
            actividad_actual.append('no estudia ni trabaja')
            
        # ? ANIOS EN PUESTO
        years_in_position = 0
        if row['Menos de 1 año'] == 1:
            years_in_position = 0
        if row['1 Año'] == 1:
            years_in_position = 1
        if row['2 AÑOS'] == 1:
            years_in_position = 2
        if row['3 AÑOS'] == 1:
            years_in_position = 3
        if row['Mas de 3 Años'] == 1:
            years_in_position = 4
        
        # ? TIPO TRABAJO
        job_type = 'operario' if row['OPERARIO'] == 1 else 'N/A'
        job_type = 'tecnico' if row['TÉCNICO'] == 1 else job_type
        job_type = 'administrativo' if row['ADMINISTRATIVO'] == 1 else job_type
        job_type = 'supervisor' if row['SUPERVISOR'] == 1 else job_type
        job_type = 'jefe de area' if row['JEFE DE AREA'] == 1 else job_type
        job_type = 'funcionario' if row['FUNCIONARIO'] == 1 else job_type
        job_type = 'directivo' if row['DIRECTIVO'] == 1 else job_type
        job_type = 'empresario' if row['EMPRESARIO'] == 1 else job_type
        
        # ? ESATUS TRABAJO
        job_status = []
        if row['BASE'] == 1:
            job_status.append('base')
        if row['EVENTUAL'] == 1:
            job_status.append('eventual')
        if row['CONTRATO'] == 1:
            job_status.append('contrato')
        if row['OTRO'] == 1:
            job_status.append('otro')
        
        # ? SECTOR DE CATEGORIA
        sector_category = 'educativo' if row['EDUCATIVO'] == 1 else 'N/A'
        sector_category = 'primario' if row['PRIMARIO'] == 1 else sector_category
        sector_category = 'secundario' if row['SECUNDARIO'] == 1 else sector_category
        sector_category = 'terciario' if row['TERCIARIO'] == 1 else sector_category
        
        # ? TIPO CATEGORIA
        type_category = 'publico' if row['PÚBLICO'] == 1 else 'N/A'
        type_category = 'privado' if row['PRIVADO'] == 1 else type_category
        type_category = 'social' if row['SOCIAL'] == 1 else type_category
        
        # ? PARTICIPACION
        participation = 'si' if row['SI'] == 1 else 'N/A'
        participation = 'no' if row['NO'] == 1 else participation
        participation = 'parcial' if row['PARCIAL'] == 1 else participation
        
        # ? FUENTE DE CONTACTO
        contact_source = 'bolsa de trabajo' if row['BOLSA DE TRABAJO ITSH'] == 1 else 'N/A'
        contact_source = 'contactos personales' if row['CONTACTOS PERSONALES'] == 1 else contact_source
        contact_source = 'residencia profesional' if row['RESIDENCIA PROFESIONAL'] == 1 else contact_source
        contact_source = 'otro' if row['OTRO'] == 1 else contact_source
        
    
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
            },
            "actividad_actual": actividad_actual, 
            "empresa": {
                "nombre": company,
                "ubicacion": {
                    "ciudad": city,
                    "municipio": municipality,
                    "estado": state
                },
                "puesto": puesto,
                "años_en_puesto": years_in_position,
                "tipo_trabajo": job_type
            },
            "estatus_trabajo": {
                "tipos": job_status
            },
            "sector": {
                "categoria": sector_category,
                "tipo": type_category
            },
            "participacion": participation,
            "fuente_contacto": contact_source
        }

        print(json.dumps(student_data, indent=4, ensure_ascii=False))
