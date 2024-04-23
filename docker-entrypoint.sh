if [ -f .env ]; then
   source .env
fi

python manage.py makemigrations
python manage.py migrate --noinput
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py ensure_adminuser --username="$DJANGO_SUPERUSER_USERNAME" \
    --email="$DJANGO_SUPERUSER_EMAIL" \
    --password="$DJANGO_SUPERUSER_PASSWORD"
fi

# add cronjob to send birthday greetings to the customers
python manage.py crontab remove
python manage.py crontab add
python manage.py crontab show
service cron start

$@
