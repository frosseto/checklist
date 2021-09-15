from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path

from .views import index
from .views_checklist import (sao_inicio,
                              sao_ordem,
                              sao_ordem_edit,
                              sao_ordem_save,
                              sao_ordem_cancel,
                              sao_proxima_ordem)
                              

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', index),
    path('accounts/',include('django.contrib.auth.urls')),

    path('checklist', sao_inicio, name='sao_inicio'),
    path('checklist/ordem/<int:ordem>', sao_ordem, name='sao_ordem'),
    path('checklist/ordem/<int:ordem>/edit/', sao_ordem_edit, name='sao_ordem_edit'),
    path('checklist/ordem/<int:ordem>/save/', sao_ordem_save, name='sao_ordem_save'),
    path('checklist/ordem/<int:ordem>/cancel/', sao_ordem_cancel, name='sao_ordem_cancel'),
    path('checklist/ordem/pordem/', sao_proxima_ordem, name='sao_proxima_ordem'),

]
