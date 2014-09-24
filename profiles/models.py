from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  MAC = 'mac'
  PC  = 'pc'
  COMPUTER_PREFERENCE_CHOICES = (
    (MAC, 'Mac'),
    (PC, 'PC'),
  )

  user = models.OneToOneField(User)
  employee_id = models.PositiveIntegerField()
  phone_number = models.CharField(max_length=25, editable=False)
  mailbox = models.CharField(max_length=25, editable=False)
  department = models.CharField(max_length=255, editable=False)
  affiliation = models.CharField(max_length=25, editable=False)
  nickname = models.CharField(max_length=25, editable=False, blank=True)
  computer_preference = models.CharField(max_length=6,
                                         choices=COMPUTER_PREFERENCE_CHOICES,
                                         default=PC)
  
