from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

POSTGRES={
    'default':{
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME':'solicitudes',
        'USER':'solicitudes',
        'PASSWORD':'solicitudes',
        'HOST':'localhost',
        'PORT':5432,
    }
}