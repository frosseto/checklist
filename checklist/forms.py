from django import forms
from .models import (SAO,
                     Modelo)

class SAOForm(forms.ModelForm):
    #campos somente leitura
    ordem = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    uep = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    descricaoordem = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    resultado = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    datafimreal = forms.DateField(widget = forms.DateInput(attrs={'readonly':'readonly'}))
    executadopor = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    encerradotecnicamentepor = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    confirmadopor = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    status = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    observacaoop = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'readonly':'readonly'}))
    observacaoanalista = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'readonly':'readonly'}))
    observacaolocal = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'readonly':'readonly'}))
    class Meta:
        model = SAO
        fields = ('ordem','descricaoordem','uep','resultado','datafimreal','executadopor','confirmadopor','encerradotecnicamentepor','observacaoop','observacaolocal','observacaoanalista','status')

        