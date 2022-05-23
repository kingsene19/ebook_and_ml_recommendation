from django import forms
from .models import Revue

class RevueForm(forms.ModelForm):

    contenu = forms.CharField(widget=forms.Textarea, label="Avis", help_text='Requis')
    note = forms.IntegerField(min_value=0, max_value=5, label="Note",help_text="Requis")

    class Meta:
        model = Revue
        fields = ("contenu", "note")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contenu'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Votre avis...'})
        self.fields['note'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': '[1-5]'})
