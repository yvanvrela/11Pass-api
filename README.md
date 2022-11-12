# 11Pass API

## Description

This project is a API REST for a password manager based on vaults containing accounts, by FastApi for the [11Pass App](https://github.com/JanetteIsasa/password_manager_app "11Pass App").

### Features
---

Features included:

- Data modeling with pydantic.
- Data validation.
- Repository of users.
- Repository of vaults.
- Repository of accounts.
- Repository of credit cards.
- SQLAlchemy - Postgresql.
- Alembic - Migrations.
- JWT Authentication.
- FastAPI Router.
- Docker-Compose.
- Clean Architecture.

### Requirements:

- Python >= 3.6

### Instalation

---

1. Clone or download de repository:

   `$ git clone https://github.com/yvanvrela/11Pass-api.git`

2. Open the console inside the project directory and create a virtual environment (You can skip this step if you have docker installed).

    `$ python3 -m venv venv`
    `$ source venv/bin/activate`

3. Install the app.

    `(venv) $ pip install -r requirements.txt`

### Basic Usage

---

Once you are running the server open the Swagger UI App to checkout the API documentation.

Ff you run it on to localhost, the address would be http://localhost:8000/docs


### Images

---

![image](https://user-images.githubusercontent.com/65867767/201487226-19ddaf52-2a60-4b6b-8051-7a2b577c0a59.png)
![image](https://user-images.githubusercontent.com/65867767/201485911-2051268f-a50f-416c-9b6d-d4b730f9718e.png)

