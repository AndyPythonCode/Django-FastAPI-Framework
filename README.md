<h2 align="center">
    <strong>FastAPI And Django working together</strong>
</h2>
<p align="center">
  <a href="#"><img src="https://i.ibb.co/fNyPwN1/fastapi-django.png" alt="FastAPI-Django"></a>
</2>
<p align="center">
    <em>FastAPI framework, Django framework</em>
</p>

# Installation

```console
$ git clone ...
$ poetry install
```

# Uses

## Django use:

- ORM
- Django administration (panel)
- localhost:8000/panel will be managed by django

## FastAPI use:

- Normal uses
- localhost:8000/ will be managed by fastapi

## Django /admin:

- **http://localhost:8000/panel/admin**

## How i can change prefix '/panel'

- ### settings.py

  - ### PREFIX_MOUNT = '/panel'

# Run it

```console
$ bash runserver.sh

or

$ uvicorn project.wsgi:application --reload
```

# Static files production

<h2 align="center">
    <strong>Whitenoise</strong>
</h2>
</br>

- <h3> <strong>Installation:</strong> </h3>

```console
$ poetry add whitenoise
```

- <h3> <strong>Step 1: </strong> go to 'MIDDLEWARE' in settings.py</h3>

```Python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # add this line
    ...
]

```

- <h3> <strong>Step 2: </strong> uncomment</h3>

```Python
"""Before"""
# FORCE_SCRIPT_NAME = PREFIX_MOUNT

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

"""After"""
FORCE_SCRIPT_NAME = PREFIX_MOUNT

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

- <h3> <strong>Step 3: </strong> fisical files </h3>

```console
$ python manage.py collectstatic
```

# Deploy

<h2 align="center">
    <strong>Vercel</strong>
</h2>
</br>

- <h3> <strong>Installation:</strong> </h3>

```console
$ npm i -g vercel
```

- <h3> <strong>Account:</strong> create an account </h3>

- <h3> <strong>Add new file:</strong> vercel.json </h3>

```yaml
{
  "builds":
    [
      {
        "src": "project/wsgi.py",
        "use": "@vercel/python",
        "config": { "maxLambdaSize": "15mb" },
      },
    ],
  "routes": [{ "src": "/(.*)", "dest": "project/wsgi.py" }],
}
```

- <h3> <strong>Add host:</strong> </h3>

```Python
ALLOWED_HOSTS = ['.vercel.app'] # Allow *.vercel.app
```

- <h3> <strong>it need requirements.txt:</strong> </h3>

```console
$ poetry export -f requirements.txt --without-hashes > requirements.txt
```

- <h3> <strong>Command deploy:</strong> </h3>

```console
$ vercel .
```

- <h3> <strong>Warning:</strong> dont't uses sqlite3 on vercel</h3>

```Python
# It's you uses sqlite3 as a database it's going to give you and error on deploy in vercel
# DON'T USE IT
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# One option: No database configuration
DATABASES = {}

# Second option: Uses another remote database
DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': config('DB_NAME'),

        'USER': config('DB_USER'),

        'PASSWORD': config('DB_PASSWORD'),

        'HOST': config('DB_HOST'),

        'PORT': '5432',

    }
}
```
