# Entornos virtuales

Crear entorno vitual linux

```
python3 -m venv venv
source venv/bin/activate

```
Crear entorno vitual en Window

```
python3 -m venv venv
.\venv\Scripts\Activate
```

Instalar librerías desde un archivo

    pip install -r requirements/local.txt

Crear migraciones

    python3 manage.py makemigrations

    python3 manage.py migrate

Crear super usuario

    python3 manage.py createsuperuser

Crear datos iniciales en la BD

    python3 manage.py runscript poblar_bd

Ejecutar proyecto

    python3 manage.py runserver
