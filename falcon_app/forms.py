from .models import User
from django.forms import ModelForm

class ProfileForm(ModelForm): 
    class Meta: # pylint: disable=no-init
        model = User
        fields = ['first_name','last_name', 'email', 'quota']
