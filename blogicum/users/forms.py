from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model

# Получаем модель пользователя.
User = get_user_model()


class BlogicumUserCreationForm(UserCreationForm):
    # Наследуем класс Meta от соответствующего класса родительской формы.
    # Так этот класс будет не перезаписан, а расширен.
    class Meta(UserCreationForm.Meta):
        model = User


class BlogicumUserChangeForm(ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', )
