# teamfriends #

Interview round 2 for the position of Tech Lead | RC-TL-310324

## Method One: cronjob ##

In this method, we will set a cronjob that will trigger in a set interval to
execute a [function](/customers/cron.py). This is achieved using
[django-crontab](https://pypi.org/project/django-crontab/) for managing the
cronjob. The function will search for the customers with the birthdays that
day and email them. If it fails to do so, for example, no Gmail
account is associated with this application, then it will print the email
subject and body in the CLI.
For example,

```bash
team_friends  | ic| e: SMTPSenderRefused(530, b'5.7.0 Authentication Required. For more information, go to
team_friends  |        5.7.0  https://support.google.com/mail/?p=WantAuthError f14-20020a170902684e00b001e4008127a7sm10614381pln.137 - gsmtp', 'None')
team_friends  | ###############################################################
team_friends  | Sender email not configured, printing the email boy in the console instead
team_friends  | Email subject: Happy birthday customer 1
team_friends  | Email body: Dear customer 1, happy birthday to you.

```

In our current configuration, we have set this
interval to 1 minute for test purpose. If we want to run the cron job
everyday at 00:01 AM, we need to change the line from

 ```bash
 ('*/1 * * * *', 'customers.cron.send_birthday_greetings', '> /proc/1/fd/1 2>&1')
 ```

 to

```bash
('1 0 * * *', 'customers.cron.send_birthday_greetings', '> /proc/1/fd/1 2>&1')
 ```

in line [176](https://gitlab.com/ahmadalsajid/teamfriends/-/blob/cron/teamfriends/settings.py?ref_type=heads&blame=1#L176)
in [this file](/teamfriends/settings.py).

## Run the project ##  

We are ready to test our API to create customers. Just run the below command
to spin up a docker container locally.

```bash
docker compose up
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
