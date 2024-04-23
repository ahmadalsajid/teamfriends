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
```commandline
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
![login page](/screenshots/11111.png)
