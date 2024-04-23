from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--email', help="Admin's email")
        parser.add_argument('--password', help="Admin's password")

    def handle(self, *args, **options):
        try:
            _user = get_user_model()
            if not _user.objects.filter(username=options['username']).exists():
                print('here in create_superuser')
                _created = _user.objects.create_superuser(username=options['username'],
                                                          email=options['email'],
                                                          password=options['password'])
                print(_created)
            else:
                print('user already exists')
        except Exception as e:
            print(e)
