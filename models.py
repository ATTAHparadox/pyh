from django.db import models
from account.models import Account
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    options = ArrayField(models.CharField(max_length=200))
    
    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    patient = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer

class Appointment(models.Model):

    appointment_status_choices = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
    )

    patient = models.ForeignKey(Account, related_name='patient', on_delete=models.CASCADE, null=True)
    appointment_number = models.UUIDField(default=uuid4, editable=False)
    is_paid = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=200)
    appointment_for = models.CharField(max_length=200)
    appointment_status = models.CharField(max_length=200, choices=appointment_status_choices, default='Pending')
    preffered_date = models.DateField()
    preffered_time_range = models.CharField(max_length=200)
    counsellor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='counsellor', null=True, blank=True)
    # def __str__(self):
    #     return self.patien