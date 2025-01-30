### FastAPI to serve Task Manager API

### Install
1. Clone the app -
```shell
$ git clone https://github.com/raheemazeezabiodun/fast-api-task-manager.git
$ cd fast-api-task-manager
```

2. Install dependencies: (Feel free to use any either virtualenv or pyenv)
```shell
 poetry install
```

3. Copy the `.env.sample` to `.env`
```shell
cp .env.sample .env
```
Feel free to update the database credentials with yours (However, it must be a valid POSTGRESQL credentials)


### Setup database
NOTE: Whatever database credential you use, ensure the user has the SUPERUSER privilege;
```shell

CREATE DATABASE deep_medical_app;
CREATE USER deep_medical_user WITH PASSWORD 'deepmedical';
GRANT ALL PRIVILEGES ON DATABASE deep_medical_user TO deep_medical_app;
ALTER USER deep_medical_user WITH SUPERUSER;

```

### Running the application

```shell
poetry run uvicorn main:app --reload

```
You can access the OpenAPI docs at http://127.0.0.1:8000/redoc

### Running the tests
```shell
poetry run pytest tests/ -vv
```


### Postman collection
Visit http://127.0.0.1:8000/redoc - then download the OpenAPI specification.
Import this file into your postman.