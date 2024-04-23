# teamfriends #

Interview round 2 for the position of Tech Lead | RC-TL-310324

## Method One: cronjob ##

In this method, we will set a cronjob that will trigger in a set interval to execute a [cronjob](/customers/cron.py). This is achieved using [django-crontab](https://pypi.org/project/django-crontab/) for managing the cronjob. The function will search for the customers with the birthdays that day and send them an email. If it fails to do so, for example, no Gmail account is associated with this application, then it will print the email subject and body in the CLI. In our current configuratoin, we have set this interval to 1 minute for test purpose. If we want to run the cron job everyday at 00:01 AM, we need to change the line from `('*/1 * * * *', 'customers.cron.send_birthday_greetings', '> /proc/1/fd/1 2>&1')` to `('1 0 * * *', 'customers.cron.send_birthday_greetings', '> /proc/1/fd/1 2>&1')` in line 176 in [this file](/teamfriends/settings.py).

For example,

```bash
team_friends  | ic| e: SMTPSenderRefused(530, b'5.7.0 Authentication Required. For more information, go to
team_friends  |        5.7.0  https://support.google.com/mail/?p=WantAuthError f14-20020a170902684e00b001e4008127a7sm10614381pln.137 - gsmtp', 'None')
team_friends  | ###############################################################
team_friends  | Sender email not configured, printing the email boy in the console instead
team_friends  | Email subject: Happy birthday customer 1
team_friends  | Email body: Dear customer 1, happy birthday to you.

```

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
