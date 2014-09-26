from django.forms import ModelForm
from profiles.models import Profile

class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['employee_id', 'computer_preference']
