# teamfriends
Interview round 2 for the position of Tech Lead | RC-TL-310324

## Run the project ##  
You need to have docker installed on your machine for testing the application easily. To install Docker on your machine, please follow the official documentation from [Docker](https://docs.docker.com/engine/install/).

After that, clone this repository to your machine.
```commandline
git clone https://gitlab.com/ahmadalsajid/teamfriends.git
```
**[Optional]** If you want to test sending email using Gmail, follow the document to configure your Gmail API auth setting from the [Google documentation](https://developers.google.com/gmail/api/quickstart/python). If not configured, the `send email` function will log and error mentioning it can not connect to Google SMTP server and print the Email **subject** and **body** in the console   

Now, create a `.env` file with the below secrets in the project root [**Feel free to use your own**].
```bash
DJANGO_SUPERUSER_EMAIL="sajid@mail.com"
DJANGO_SUPERUSER_USERNAME="sajid"
DJANGO_SUPERUSER_PASSWORD="1qweqwe23"

DEFAULT_FROM_EMAIL=""
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
```
We are ready to test our API to create customers. Just run the below command to spin up a docker container locally.
```commandline
docker compose up -d
```
Once the container is up, you can use http://localhost:8000/admin/ to access the Django admin panel using the username and password provided in the `.env` file.
![login page](/screenshots/admin_login.png)

Also, you can use the admin panel to list/edit the customer from the UI at http://localhost:8000/admin/customers/customer/.
![Customer list](/screenshots/list_customers.png)

Also, there are two APIs available, one to obtain the JWT token for authorisation, another one to add customers to the application.

### Login API ###

Make a `POST` request to http://localhost:8000/api/customer/login/ with the user credential from [Postman](https://www.postman.com/) or similar tool. i.e.
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

Make a `POST` request to http://localhost:8000/api/customer/register/ with the customer data and the `JWT token` in the Authorization header.
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

