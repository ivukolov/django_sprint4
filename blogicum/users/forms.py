from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

User = get_user_model()


class BlogicumUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class BlogicumUserChangeForm(ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', )
