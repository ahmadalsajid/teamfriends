# teamfriends #

Interview round 2 for the position of Tech Lead | RC-TL-310324

## Method Two: Task schedular ##

In this method, we will set a Celery and rabbitmq, rest is after setup



## Run the project ##  

We are ready to test our API to create customers. Just run the below command
to spin up a docker container locally.

```bash
docker compose up -d
```

Once the container is up, you can use <http://localhost:8000/admin/> to access
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
system, the rest will be handled by the cron job to send the customers
with a birthday greetings on their birthdays. You will get the emails if you
have configured a Gmail to be used with this application, or the results in the
container logs as an alternate. 
