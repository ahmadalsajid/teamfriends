# teamfriends #

Interview round 2 for the position of Tech Lead | RC-TL-310324

## Run the project ##  

You need to have docker installed on your machine for testing the application
easily. To install Docker on your machine, please follow the official
documentation from [Docker](https://docs.docker.com/engine/install/).

After that, clone this repository to your machine.

```commandline
git clone https://gitlab.com/ahmadalsajid/teamfriends.git
```

**[Optional]** If you want to test sending email using Gmail, follow the
document to configure your Gmail API auth setting from the
[Google documentation](https://developers.google.com/gmail/api/quickstart/python).
If not configured, the `send email` function will log an error mentioning it
can not connect to Google SMTP server and print the
email **subject** and **body** in the console.

Now, create a `.env` file with the below secrets in the project root
[**Please replace with your own credentials**].

```bash
DJANGO_SUPERUSER_EMAIL="sajid@mail.com"
DJANGO_SUPERUSER_USERNAME="sajid"
DJANGO_SUPERUSER_PASSWORD="1qweqwe23"

DEFAULT_FROM_EMAIL=""
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
```

We will be creating a simple DRF application with two APIs, one to retrieve the
users `JWT Token`, another one to create the customer with their name, email
and date of birth. This is the first part of the challenge. This is pretty
straight forward. We have dockerised our application, so that it can be easily
deployed and tested.

The second part of the task is more interesting. We can achieve that in two
ways. The first one, with cron job that is very suitable for these types of
lightweight tasks. We don't need to use any additional resources/tools. We
have django libraries that can manage the cron jobs for us. We have already
implemented that in another branch of this repository named
[cron](https://gitlab.com/ahmadalsajid/teamfriends/-/tree/cron). You just
need to checkout to that branch, and the README.md file has all the necessary
instructions to build the project with docker and the testing instructions there.

```bash
git checkout cron
```

The second method would be using a `Distributed Task Queue` i.e.
[Celery](https://docs.celeryq.dev/en/stable/index.html) and
[Redis](https://redis.io/) or [RabbitMQ](https://www.rabbitmq.com/)
as the broker. For this, we have another branch of this repository named
[schedular](https://gitlab.com/ahmadalsajid/teamfriends/-/tree/schedular). 
The README.md file will instruct you to build the project with docker 
and the testing using Celery and RabbitMQ.

```bash
git checkout schedular
```

## DRF App only ##

We are ready to test our API to create customers. Just run the below command to spin up a docker container locally.

```commandline
docker compose up -d
```

Once the container is up, you can use <http://localhost:8000/admin/> to access the Django admin panel using the username and password provided in the `.env` file.
![login page](/screenshots/admin_login.png)

Also, you can use the admin panel to list/edit the customer from the UI at <http://localhost:8000/admin/customers/customer/>.
![Customer list](/screenshots/list_customers.png)

Also, there are two APIs available, one to obtain the JWT token for authorisation, another one to add customers to the application.

### Login API ###

Make a `POST` request to <http://localhost:8000/api/customer/login/> with the user credential from [Postman](https://www.postman.com/) or similar tool. i.e.

```bash
POST http://localhost:8000/api/customer/login/
Content-Type: application/json
{
    "username":"sajid@mail.com",
    "password":"1qweqwe23"
}
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "token": {
        "refresh": "eyJhbxxxx.bkxxxxiOjF9.l9zxxxxslSQ",
        "access": "eyJhbxxxx.eyJxxxxX0.qSOxxxxIY"
    }
}
```

![Postman login API](/screenshots/login_api.png)

### Create customer API ###

Make a `POST` request to <http://localhost:8000/api/customer/register/> with the customer data and the `JWT token` in the Authorization header.

```bash
POST http://localhost:8000/api/customer/register/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
{
    "name": "customer 1",
    "email": "customer_1@mail.com",
    "date_of_birth": "2023-03-31"
}
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "data": {
        "id": 1,
        "name": "customer 1",
        "email": "customer_1@mail.com",
        "date_of_birth": "2023-03-31"
    }
}
```

![Postman create customer API](/screenshots/create_customer.png)
If you are in the `main` branch of this repository, you will only get the APIs
for login/create customer. You must checkout to `cron` or `schedular` branches
for the second part of the task.
