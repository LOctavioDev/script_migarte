# Script de migración de egresados

Script en Python que lee la hoja de cálculo de seguimiento de egresados (formato `.ods` o `.xlsx`), transforma cada fila en un documento estructurado y lo guarda en MongoDB.

![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2-150458?style=flat-square&logo=pandas&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-PyMongo_4-47A248?style=flat-square&logo=mongodb&logoColor=white)
![LibreOffice](https://img.shields.io/badge/Formato-ODS-18A303?style=flat-square&logo=libreofficecalc&logoColor=white)

## Contenido

- [Proyectos relacionados](#proyectos-relacionados)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Variables de entorno](#variables-de-entorno)
- [Uso](#uso)
- [Formato de la hoja de cálculo](#formato-de-la-hoja-de-cálculo)
- [Documento generado](#documento-generado)
- [Archivo de ejemplo](#archivo-de-ejemplo)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Limitaciones conocidas](#limitaciones-conocidas)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Proyectos relacionados

| Proyecto | Descripción |
|---|---|
| [backend-residencias](https://github.com/LOctavioDev/backend-residencias) | API REST del sistema de seguimiento de egresados. |
| [frontend-residencias](https://github.com/LOctavioDev/frontend-residencias) | Panel de administración. |
| [script_migarte](https://github.com/LOctavioDev/script_migarte) | Este repositorio. |

## Requisitos

- [Python](https://www.python.org/) 3.10 o superior
- Una instancia de [MongoDB](https://www.mongodb.com/)

## Instalación

```bash
git clone https://github.com/LOctavioDev/script_migarte.git
cd script_migarte
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # edita los valores
```

## Variables de entorno

| Variable | Obligatoria | Descripción |
|---|---|---|
| `MONGO_URI` | Sí | Cadena de conexión a MongoDB. Ejemplo: `mongodb://usuario:password@localhost:27017/?authSource=admin` |

Los documentos se guardan en la base `db_residency`, colección `students`.

## Uso

1. Coloca la hoja de cálculo en la raíz del proyecto con el nombre `RESIDENCIAxlsx.ods`. Para usar otro nombre, cambia `excel_file` en `main.py`.
2. Ejecuta:

```bash
python main.py
```

El script imprime cada documento en formato JSON y al final un resumen:

```
Migración completa: 3 alumnos guardados en db_residency.students
```

Cada registro se guarda con una operación *upsert* usando `no_control` como clave: si el número de control ya existe, se actualiza; si no, se crea. Por eso el script puede ejecutarse varias veces sin duplicar registros.

## Formato de la hoja de cálculo

- Las **tres primeras filas** se consideran encabezados y se omiten.
- La **primera columna** (A) se ignora; normalmente es un consecutivo.
- Las **columnas B a AS** (44 columnas) contienen los datos, en este orden:

| Columnas | Contenido | Valores |
|---|---|---|
| `NO_CONTROL` | Número de control | Texto |
| `NOMBRE` | Nombre completo | `APELLIDO_PATERNO APELLIDO_MATERNO NOMBRE` |
| `GENERACION` | Periodo | `MES-AÑO/MES-AÑO`, por ejemplo `AGOSTO-2014/DICIEMBRE-2018` |
| `SI`, `NO`, `ESTUDIA`, `ESTUDIA Y TRABAJA`, `NO ESTUDIA NI TRABAJA` | Actividad actual | `1` marca la opción |
| `EMPRESA`, `CIUDAD`, `MUNICIPIO`, `ESTADO`, `PUESTO` | Empresa actual | Texto |
| `Menos de 1 año`, `1 Año`, `2 AÑOS`, `3 AÑOS`, `Mas de 3 Años` | Antigüedad en el puesto | `1` marca la opción |
| `OPERARIO`, `TÉCNICO`, `ADMINISTRATIVO`, `SUPERVISOR`, `JEFE DE AREA`, `FUNCIONARIO`, `DIRECTIVO`, `EMPRESARIO` | Nivel del puesto | `1` marca la opción |
| `BASE`, `EVENTUAL`, `CONTRATO`, `OTRO` | Condición laboral | `1` marca la opción |
| `EDUCATIVO`, `PRIMARIO`, `SECUNDARIO`, `TERCIARIO` | Sector económico | `1` marca la opción |
| `PÚBLICO`, `PRIVADO`, `SOCIAL` | Tipo de organización | `1` marca la opción |
| `SI`, `NO`, `PARCIAL` | Participación | `1` marca la opción |
| `BOLSA DE TRABAJO ITSH`, `CONTACTOS PERSONALES`, `RESIDENCIA PROFESIONAL`, `OTRO` | Medio por el que obtuvo el empleo | `1` marca la opción |

Las celdas vacías se guardan como `null`.

## Documento generado

Ejemplo de un documento guardado en MongoDB (ver también [`ejemplo.json`](ejemplo.json)):

```json
{
  "no_control": "F14390167",
  "nombre": {
    "primero": "JORGE",
    "apellido_paterno": "ALDANA",
    "apellido_materno": "LIMATITLA"
  },
  "generacion": {
    "inicio": { "anio": 2014, "semestre": "AGOSTO" },
    "fin": { "anio": 2018, "semestre": "DICIEMBRE" }
  },
  "actividad_actual": ["trabaja"],
  "empresa": {
    "nombre": "STARDUST INC. S.A. DE C.V.",
    "ubicacion": { "ciudad": "Puebla", "municipio": "Huauchinango", "estado": "Puebla" },
    "puesto": "Desarrollador de aplicaciones móviles",
    "años_en_puesto": 4,
    "tipo_trabajo": "jefe de area"
  },
  "estatus_trabajo": { "tipos": ["contrato"] },
  "sector": { "categoria": "terciario", "tipo": "privado" },
  "participacion": "parcial",
  "fuente_contacto": "contactos personales"
}
```

`años_en_puesto` toma los valores `0` (menos de 1 año), `1`, `2`, `3` o `4` (más de 3 años).

## Archivo de ejemplo

Si no cuentas con la hoja de cálculo original, puedes generar una de prueba con tres egresados ficticios:

```bash
python sample/generate_sample.py
cp sample/RESIDENCIA_ejemplo.ods RESIDENCIAxlsx.ods
python main.py
```

## Estructura del proyecto

```
.
├── config/
│   └── db.py                  Conexión a MongoDB
├── models/
│   └── student.py             Clases del modelo de egresado
├── sample/
│   └── generate_sample.py     Genera una hoja de cálculo de prueba
├── services/
│   └── migration_service.py   Lectura, transformación y guardado
├── utils/
│   └── excel_reader.py        Lectura genérica de hojas de cálculo
├── ejemplo.json               Ejemplo de documento
├── main.py                    Punto de entrada
└── requirements.txt
```

## Limitaciones conocidas

- La hoja tiene columnas con el mismo nombre (`SI`, `NO` y `OTRO`). pandas renombra las repetidas, por lo que **participación** se calcula con las columnas `SI`/`NO` de actividad actual, y **fuente de contacto** con `OTRO` de condición laboral.
- Si `NOMBRE` tiene menos de tres palabras o `GENERACION` no sigue el formato esperado, la fila provoca un error.
- El formato del documento (campos en español) es distinto al modelo `Student` de [backend-residencias](https://github.com/LOctavioDev/backend-residencias). Por eso el script escribe en una base separada (`db_residency`) y los registros migrados no aparecen en el panel.

## Contribuir

1. Haz un fork del repositorio.
2. Crea una rama para tu cambio: `git checkout -b feature/mi-cambio`.
3. Prueba con el archivo de ejemplo antes de enviar cambios.
4. Envía un pull request describiendo el cambio.

## Licencia

Distribuido bajo la licencia MIT. Consulta [LICENSE](LICENSE) para más información.

Copyright (c) 2024 Luis Octavio.
