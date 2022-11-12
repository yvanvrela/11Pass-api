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


### Users

---

![image](https://user-images.githubusercontent.com/65867767/201487371-c98058b2-cd65-4362-a6d4-4d1d8711e613.png)
![image](https://user-images.githubusercontent.com/65867767/201487388-99c7964d-7dba-4fda-8b03-2f1edaaaf86a.png)

### Vaults

---

![image](https://user-images.githubusercontent.com/65867767/201487434-cb38cbee-fba8-432d-8bfa-ec3c95cc60ce.png)
![image](https://user-images.githubusercontent.com/65867767/201487458-73e3b137-7c61-46b8-a824-5e4840e702c7.png)


### Accounts

---

![image](https://user-images.githubusercontent.com/65867767/201487512-6b73e46a-e0bd-4479-873d-65160df5f578.png)
![image](https://user-images.githubusercontent.com/65867767/201487597-807da6e4-4fdd-45ef-9614-06a394c050d3.png)
