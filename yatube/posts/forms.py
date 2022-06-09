from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Форма для редактирования и создания поста."""

    class Meta:
        """Обязательный подкласс."""

        model = Post
        fields = ('text', 'group')
