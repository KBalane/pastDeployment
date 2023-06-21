from django import forms


class ImageUploadForm(forms.Form):
    id_image = forms.ImageField()
