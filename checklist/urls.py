from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path

from .views import index
from .views_checklist import (checklist_nova,
                              checklist,
                              checklist_edit,
                              checklist_edit_cancel,
                              checklist_save,
                              checklist_pesquisa,
                              checklist_nova_selecao,
                              checklist_relatorio)
                              

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', index),
    path('accounts/',include('django.contrib.auth.urls')),
    #path('jet/', include('jet.urls', 'jet')), 
    #path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    path('checklist_pesquisa', checklist_pesquisa, name='checklist_pesquisa'),
    path('checklist_nova', checklist_nova_selecao, name='checklist_nova_selecao'),
    path('checklist_relatorio', checklist_relatorio, name='checklist_relatorio'),

    path('nova/<int:pk>/', checklist_nova, name='checklist_nova'),
    path('checklist/<int:pk>/', checklist, name='checklist'),
    path('checklist/<int:pk>/edit/', checklist_edit, name='checklist_edit'),
    path('checklist/<int:pk>/save/', checklist_save, name='checklist_save'),
    path('checklist/<int:pk>/cancel/', checklist_edit_cancel, name='checklist_edit_cancel'),

    path('django_plotly_dash/', include('django_plotly_dash.urls')),

]

