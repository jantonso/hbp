DEBUG = False

TEMPLATE_DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}

# Update database configuration with $DATABASE_URL
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']