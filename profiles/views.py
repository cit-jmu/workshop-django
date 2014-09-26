from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from profiles.forms import ProfileForm

@login_required
def show(request):
  form = ProfileForm(instance=request.user.profile)
  return render(request, 'profiles/show.html', {'form': form})
