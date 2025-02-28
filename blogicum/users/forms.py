from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogicumUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class BlogicumUserChangeForm(ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', )
