from django.forms import ModelForm
from profiles.models import Profile

class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['computer_preference']
