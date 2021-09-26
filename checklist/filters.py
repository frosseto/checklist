import django_filters
from django_filters import DateRangeFilter, DateFilter, BooleanFilter
from django import forms
from .models import (OrdemPesquisa,
                     Modelo)

class modeloFilter(django_filters.FilterSet):
    class Meta:
        model = Modelo
        fields = ['nome', 'descricao']

class ordemFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='datafimreal',lookup_expr=('gte'),) 
    end_date = DateFilter(field_name='datafimreal',lookup_expr=('lte'))
    date_range = DateRangeFilter(field_name='datafimreal')
    #modificadaaposanalise = BooleanFilter(field_name='modificadaaposanalise',widget=forms.CheckboxInput)
    #naoencoupenanexos = BooleanFilter(field_name='naoencoupenanexos',widget=forms.CheckboxInput)
    class Meta:
        model = OrdemPesquisa
        fields = ['ordem', 'uep', 'resultado','datafimreal','modificadaaposanalise','status']


    def __init__(self, data=None, *args, **kwargs):
        # if filterset is bound, use initial values as defaults
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get('initial')

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super().__init__(data, *args, **kwargs)
