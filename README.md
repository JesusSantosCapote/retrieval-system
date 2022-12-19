# retrieval-system

Sistema de recuperación de la información para la asignatura SRI. Matcom Curso 2022

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Introducción:

El proyecto consiste en la implementación de 3 modelos de recuperación de la información
y la integración de los mismos en un sistema que permita hacer consultas sobre distintos corpus.


Se desarrolló el modelo Booleano y vectorial vistos en conferencias así como el modelo basado en indexación por semántica latente (LSI).


## Arquitectura

El proyecto está compuesto por una aplicación en Django que funciona de Backend, usa una base de datos relacional
(sqlite3 en desarrollo y PostgreSQL en producción). Este backend expone una API para la realización de consultas, así
como un sitio de administración que permite administrar los documentos y los corpus.

Se tiene además una aplicación Backend minimalista para la realización de consultas.

## Setup

Para correr el backend siga los siguientes pasos:

1- Instalar dependencias:
```bash
pip install -r requirements/local.txt
```

2- Ejecutar las migraciones para estructurar la base de datos:
```bash
python manage.py migrate
```

3- Montar el servidor:
```bash
python manage.py runserver
```

Opcionalmente puede crear un superusuario para acceder al sitio de administración
```bash
python manage.py createsuperuser
```

Cargar el corpus `Cranfield`
```bash
python manage.py load_cranfield
```

Cargar el corpus `Med`
```bash
python manage.py load_med
```

Después de cargar cada corpus deberá procesarse dicho corpus.
El preprocesamiento de los corpus es una tarea relativamente costosa, pero que se ejecuta cada vez que un corpus cambie y garantiza poder hacer las consultas de forma más rápida.

Para procesar un corpus ejecute:
```bash
python manage.py process_corpus <corpus_name>
```

donde `corpus_name` es el nombre del corpus ('cranfield', 'med') .

### Realizar consultas

Una vez montado el servidor puede realizar consultas mediante la API al endpoint

`http://127.0.0.1:8000/api/search/`

Este endpoint toma varios parametros:

> type: Modelo a usar. Posibles valores: boolean | vectorial[default] | lsi>

> corpus: Corpus sobre el cual hacer la consulta

> query: Consulta a realizar

Ejemplo:

> http://127.0.0.1:8000/api/search/?type=boolean&corpus=cranfield&query=electron%20and%20distribution%20or%20(%20thermodynamic%20and%20heat%20)%20

> http://127.0.0.1:8000/api/search/?type=vectorial&corpus=med&query=acid%20concentration%20in%20testosterone

### Evaluar los modelos

Se implemental las medidas de precisión, recobrado y f1 para
la evaluación de los modelos. Existe un comando para realizar
dicha evaluación sobre un corpus.

`python manage.py evaluate_model corpus model query rel measure`

Donde:

- corpus: nombre del corpus que se utiliza para la evaluación
- model: modelo a evaluar < 'boolean' | 'vectorial' | 'lsi' >
- query: dirección del fichero con las consultas
- rel: dirección del fichero con los documentos relevantes por consultas
- measure: medida a usar para la evaluación < 'precision' | 'recall' | 'f1' >

Los ficheros query y rel se esperan en formato json con la estructura similar a los encontrados en el directorio `datasets`

## Cliente

La aplicación cliente para ejecutar consultas está hecha en Angular con Angular Material.

Para ejecutarla moverse al directorio front-end:

1- Instalar dependencias:
```bash
npm install -g @angular/cli
npm install
```

2- Montar servidor:
```bash
ng serve
```

La aplicación se estará sirviendo en el puerto 4200

