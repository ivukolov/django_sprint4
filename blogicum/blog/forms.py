from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'location', 'category',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }
