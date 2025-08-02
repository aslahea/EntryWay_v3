from django import forms
from .models import CustomUser

class UserBioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
