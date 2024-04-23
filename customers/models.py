from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return f'{self.name}, DOB:{self.date_of_birth}'
