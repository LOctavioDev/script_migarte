from pymongo import MongoClient

client = MongoClient('mongodb+srv://octadev:112020a@clusteroctavio.n8a1lsl.mongodb.net/db_residency?retryWrites=true&w=majority&appName=ClusterOctavio')

db = client.db_residency

collection = db.students

student_data = {
    "no_control": "F14390167",
    "nombre": {
        "primero": "Jorge",
        "apellido_paterno": "Aldana",
        "apellido_materno": "Limatitla"
    },
    "generacion": {
        "inicio": {"anio": 2014, "semestre": "Agosto"},
        "fin": {"anio": 2018, "semestre": "Diciembre"}
    },
    "actividad_actual": ["trabaja"],
    "empresa": {
        "nombre": "STARDUST INC. S.A. DE C.V.",
        "ubicacion": {
            "ciudad": "Puebla",
            "municipio": "Huauchinango",
            "estado": "Puebla"
        },
        "puesto": "Desarrollador de aplicaciones móviles",
        "años_en_puesto": 3,
        "tipo_trabajo": "Jefe de área"
    },
    "estatus_trabajo": {
        "tipos": ["contrato"]
    },
    "sector": {
        "categoria": "terciario",
        "tipo": "privado"
    },
    "participacion": "parcial",
    "fuente_contato": "CONTACTOS PERSONALES"
}

result = collection.insert_one(student_data)
print(result.inserted_id)

inserted_student = collection.find_one({"no_control": "F14390167"})
print(inserted_student)

client.close()