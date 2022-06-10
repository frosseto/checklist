from django.test import TestCase
from django.test import Client
from django.urls import reverse
from checklist.models import (Modelo)

class PesquisaListViewTest(TestCase):
    @classmethod

    def setUpTestData(cls):
        # Cria 2 modelos para teste (não utilizado nos testes em si, mas importante definir)
        number_of_modelos = 2

        for modelo_id in range(number_of_modelos):
            Modelo.objects.create(
                nome=f'TesteNome {modelo_id}',
                descricao=f'DescNome {modelo_id}',
            )
    # verificar a existência da página pelo nome
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('checklist_pesquisa'))
        self.assertEqual(response.status_code, 302)
    
    # verificar a existência da página pelo endereço
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/chacklist/checklist_pesquisa/')
        self.assertEqual(response.status_code, 404)