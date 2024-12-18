from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    profile_image = forms.ImageField(label='Profile Image', required=False)
    # Agrega otros campos personalizados aquí

    def save(self, request):
        user = super().save(request)
        user.profile_image = self.cleaned_data.get('profile_image')
        user.save()
        return user
