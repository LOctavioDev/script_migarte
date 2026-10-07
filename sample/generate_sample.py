# ? Genera un .ods de prueba con el mismo layout que lee migration_service.py:
# ? columna 0 = consecutivo, columnas 1..44 = datos, 3 filas de encabezado (skiprows=3)
import pandas as pd

HEADERS = ['NO_CONTROL', 'NOMBRE', 'GENERACION', 'SI', 'NO', 'ESTUDIA', 'ESTUDIA Y TRABAJA', 'NO ESTUDIA NI TRABAJA',
           'EMPRESA', 'CIUDAD', 'MUNICIPIO', 'ESTADO', 'PUESTO', 'Menos de 1 año', '1 Año', '2 AÑOS', '3 AÑOS',
           'Mas de 3 Años', 'OPERARIO', 'TÉCNICO', 'ADMINISTRATIVO', 'SUPERVISOR', 'JEFE DE AREA', 'FUNCIONARIO',
           'DIRECTIVO', 'EMPRESARIO', 'BASE', 'EVENTUAL', 'CONTRATO', 'OTRO', 'EDUCATIVO', 'PRIMARIO', 'SECUNDARIO',
           'TERCIARIO', 'PÚBLICO', 'PRIVADO', 'SOCIAL', 'SI', 'NO', 'PARCIAL', 'BOLSA DE TRABAJO ITSH',
           'CONTACTOS PERSONALES', 'RESIDENCIA PROFESIONAL', 'OTRO']

STUDENTS = [
    ('F14390167', 'ALDANA LIMATITLA JORGE', 'AGOSTO-2014/DICIEMBRE-2018', 'STARDUST INC. S.A. DE C.V.',
     'Puebla', 'Huauchinango', 'Puebla', 'Desarrollador de aplicaciones móviles',
     {'SI', 'Mas de 3 Años', 'JEFE DE AREA', 'CONTRATO', 'TERCIARIO', 'PRIVADO', 'PARCIAL', 'CONTACTOS PERSONALES'}),
    ('F15390201', 'HERNANDEZ CRUZ MARIA', 'ENERO-2015/JUNIO-2019', 'SOFTLAB MX',
     'Xicotepec', 'Xicotepec', 'Puebla', 'Analista de sistemas',
     {'ESTUDIA Y TRABAJA', '2 AÑOS', 'TÉCNICO', 'BASE', 'TERCIARIO', 'PRIVADO', 'BOLSA DE TRABAJO ITSH'}),
    ('F16390333', 'PEREZ GOMEZ LUIS', 'AGOSTO-2016/DICIEMBRE-2020', 'N/A',
     'Huauchinango', 'Huauchinango', 'Puebla', 'N/A',
     {'ESTUDIA', 'Menos de 1 año', 'EVENTUAL', 'EDUCATIVO', 'PÚBLICO', 'RESIDENCIA PROFESIONAL'}),
]

rows = [['REPORTE DE SEGUIMIENTO DE EGRESADOS'] + [''] * 44, [''] * 45, ['#'] + HEADERS]
for i, (control, name, gen, company, city, mun, state, puesto, flags) in enumerate(STUDENTS, start=1):
    data = {'NO_CONTROL': control, 'NOMBRE': name, 'GENERACION': gen, 'EMPRESA': company,
            'CIUDAD': city, 'MUNICIPIO': mun, 'ESTADO': state, 'PUESTO': puesto}
    row = [i]
    for h in HEADERS:
        row.append(data[h] if h in data else (1 if h in flags else 0))
    rows.append(row)

pd.DataFrame(rows).to_excel('sample/RESIDENCIA_ejemplo.ods', engine='odf', header=False, index=False)
print('Generado sample/RESIDENCIA_ejemplo.ods con', len(STUDENTS), 'alumnos')
