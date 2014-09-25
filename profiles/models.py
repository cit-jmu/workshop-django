from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  MAC = 'mac'
  PC  = 'pc'
  COMPUTER_PREFERENCE_CHOICES = (
    (MAC, 'Mac'),
    (PC, 'PC'),
  )

  # relationship to the user model
  user = models.OneToOneField(User)

  employee_id = models.PositiveIntegerField()
  phone_number = models.CharField(max_length=25)
  mailbox = models.CharField(max_length=25)
  department = models.CharField(max_length=255)
  affiliation = models.CharField(max_length=25)
  nickname = models.CharField(max_length=25, blank=True)
  computer_preference = models.CharField(max_length=6,
                                         choices=COMPUTER_PREFERENCE_CHOICES,
                                         default=PC)

  def __unicode__(self):
    return "%s" % self.user
