from django.test import TestCase

from checklist.models import (Modelo)

class ModeloModelTest(TestCase):
    @classmethod

    def setUpTestData(self):
        # Cria um objeto para utilização nos testes
        Modelo.objects.create(nome='ABCDEF', descricao='testes automatizados')

    #Testa o tamanho máximo do campo nome
    def test_nome_max_length(self):
        modelo = Modelo.objects.get(id=1)
        max_length = modelo._meta.get_field('nome').max_length
        self.assertEquals(max_length, 100)
    
    #Testa o label do campo descricao
    def test_descricao_label(self):
        modelo = Modelo.objects.get(id=1)
        field_label = modelo._meta.get_field('descricao').verbose_name
        self.assertEquals(field_label, 'Descrição')
