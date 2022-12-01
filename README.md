# Test task on FastApi, Tornado and RabbitMQ

Installation
---------

##### Clone a repository
```git
git clone https://github.com/vadushkin/TestTaskRostelecom.git
```

##### Change a folder
```shell
cd TestTaskRostelecom
```


#### Create file `.env` or delete ```.example``` from .env.example

#### Fill in the data in the file `.env`

### Example:

```dotenv
# RabbitMQ
RABBITMQ_DEFAULT_USER=rabbit
RABBITMQ_DEFAULT_PASS=mypassword
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_CONSUME_QUEUE=user_appeals
RABBITMQ_EXCHANGE_NAME=exchange_appeals

# DataBase
DB_PROVIDER=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=user_appeal
DB_HOST=db
DB_PORT=5432
```

### Run Docker

```docker
docker-compose up --build
```

Api
---

* `http://localhost:8080/` - Form
* `http://localhost:15672/` - RabbitMQ

Credentials
-----------

It's default settings in `.env`


#### RabbitMQ:
 * Login: `rabbit` 
 * Password: `mypassword`

#### DataBase:
 * Host: `localhost`
 * Port: `5433`
 * Database: `user_appeal` 
 * Username: `postgres`
 * Password: `password`