from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

    # def clean_message(self):
    #     email_id = self.cleaned_data.get("email_id")
    #     dbuser = User.objects.filter(name=email_id)
    #     if not dbuser:
    #         raise forms.ValidationError("User does not exist in our db!")
    #     return email_id


class SignupForm(forms.Form):
    CHOICES = (('True', 'T'),
               ('False', 'F'))
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.CharField(max_length=100)
    member_type = forms.CharField(max_length=100)
    is_staff = forms.BooleanField(required=False)
    is_verified = forms.BooleanField(required=False)
