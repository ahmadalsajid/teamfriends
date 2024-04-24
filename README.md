# teamfriends #

Interview round 2 for the position of Tech Lead | RC-TL-310324

## Method Two: Task schedular ##

In this method, we will set Celery for task scheduling and RabbitMQ as the
message broker. We have created a [function](/customers/tasks.py) which will
search for the customers with the birthdays that day and email them. If it
fails to do so, for example, no Gmail account is associated with this
application, then it will print the email subject and body in the CLI.
For example,

```bash
celery-worker  | [2024-04-24 12:16:02,684: WARNING/ForkPoolWorker-8] Invalid address 
celery-worker  | [2024-04-24 12:16:02,684: WARNING/ForkPoolWorker-8] "
celery-worker  | [2024-04-24 12:16:02,684: WARNING/ForkPoolWorker-8] "
celery-worker  | [2024-04-24 12:16:02,684: WARNING/ForkPoolWorker-8] '
celery-worker  | [2024-04-24 12:16:02,684: WARNING/ForkPoolWorker-8] )
celery-worker  | [2024-04-24 12:16:02,684: WARNING/ForkPoolWorker-8] Sender email not configured, printing the email boy in the console instead
celery-worker  | [2024-04-24 12:16:02,685: INFO/ForkPoolWorker-8] Email subject: Happy birthday Customer 3
celery-worker  | [2024-04-24 12:16:02,685: INFO/ForkPoolWorker-8] Email body: Dear Customer 3, happy birthday to you.
celery-worker  | [2024-04-24 12:16:02,688: INFO/ForkPoolWorker-8] Task customers.tasks.send_birthday_email_greetings[01ca04a8-766a-48c4-9d4b-8ac1564cedb0] succeeded in 2.6789230850008607s: None

```

To achieve this, we will have four main containers, `api`, `celery-worker`,
`celery-beat`, & `rabbitmq`. The first three containers will be built from
the same [directory](./), and the last one we will pull the image from docker
hub. Everything is configured in the [docker-compose.yml](/docker-compose.yml)
file, so you will need to do nothing here.

For ease of testing, we have configured the task schedular to send the
greetings every minute. If you want to update the time, i.e. send the
greetings everyday at 00:01 AM UTC, just comment out line
[181](https://gitlab.com/ahmadalsajid/teamfriends/-/blob/schedular/teamfriends/settings.py?ref_type=heads&blame=1#L181) and uncomment
[182](https://gitlab.com/ahmadalsajid/teamfriends/-/blob/schedular/teamfriends/settings.py?ref_type=heads&blame=1#L182)
in the [settings.py](/teamfriends/settings.py) file.

## Run the project ##  

We are ready to test our API to create customers. Just run the below command
to spin up the docker containers locally.

```bash
docker compose up
```

Once the containers are up, you can use <http://localhost:8000/admin/> to access
the Django admin panel using the username and password provided in the `.env` file.

![login page](/screenshots/admin_login.png)

Also, you can use the admin panel to list/edit the customer from the UI at
<http://localhost:8000/admin/customers/customer/>.

![Customer list](/screenshots/list_customers.png)

Also, there are two APIs available, one to obtain the JWT token for
authorisation, another one to add customers to the application.

### Login API ###

Make a `POST` request to <http://localhost:8000/api/customer/login/> with the
user credential from [Postman](https://www.postman.com/) or similar tool. i.e.

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

Make a `POST` request to <http://localhost:8000/api/customer/register/> with
the customer data and the `JWT token` in the Authorization header.

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

Finally, we are done here. We just need to input new customer data in our
system, the rest will be handled by the task schedular to send the customers
with a birthday greetings on their birthdays. You will get the emails if you
have configured a Gmail to be used with this application, or the results in the
container logs as an alternate.

When you are done with testing, remove the docker container and images using
```bash
docker compose down -v --rmi local
```
This will help you clean up your docker builds and test the other option.