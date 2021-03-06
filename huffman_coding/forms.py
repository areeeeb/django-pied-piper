from django import forms


class TextFileForm(forms.Form):
    text_file = forms.FileField(label='Upload Text File')


class ImageFileForm(forms.Form):
    image_file = forms.ImageField(label='Upload .bmp Image File')


class BinaryFileForm(forms.Form):
    binary_file = forms.FileField(label='Upload compressed.bin File')
