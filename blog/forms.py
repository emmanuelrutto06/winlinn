from django import forms
from .models import Image,Author

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ["name", "image"]

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Name', 'label': 'Name'}),

        }

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ["author_image", "title", "profile"]

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Title', 'label': 'Title'}),
            'profile': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Author Profile', 'rows': 3})

        }