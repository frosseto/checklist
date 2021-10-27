from django.db import models
from django.conf import settings
from django.db.models.fields import related
from django.utils.timezone import now
from notifications.models import notify_handler
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.auth.models import User,Permission,Group

STATUS_CHOICES = (
    ('Aguardando analista','Aguardando analista'),
    ('Ordem analisada','Ordem analisada'),)

ITEM_TIPOS = (
    ('CHECKBOX','checkbox'),
    ('TEXT','text'),
    ('COMBOBOX','combobox'),)

LISTA_VERIFICACAO_STATUS = (
    ('Em elaboração','Em elaboração'),
    ('Aguardando Aprovador','Aguardando Aprovador'),
    ('Aprovada','Aprovada'),)

# Checklist

class Modelo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=1024, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Modelo'

    def __str__(self):
        return self.nome

class Grupo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=1024, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Grupo'

    def __str__(self):
        return self.nome

class Acesso(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    modelo_fk = models.ForeignKey(Modelo, models.DO_NOTHING, db_column="Modelo_FK", blank=False, null=False)
    usuario_fk = models.ForeignKey(User, models.CASCADE, db_column="Usuario_FK", blank=False, null=False)
    grupo_fk = models.ForeignKey(Group, models.CASCADE, db_column="Grupo_FK", blank=False, null=False)
    
    class Meta:
        managed = True
        db_table = 'Acesso'


class Item(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=1024, blank=True, null=True)
    itemtipo = models.CharField(db_column='ItemTipo', max_length=50, blank=True, null=True, choices=ITEM_TIPOS)
    modelo_fk = models.ForeignKey(Modelo, models.DO_NOTHING, db_column="Modelo_FK", blank=True, null=True)
    valorpadrao = models.CharField(db_column="ValorPadrao", max_length=100, blank=True, null=True)
    valor_choice = models.CharField(db_column="ValorChoice", max_length=255, blank=True, null=True)
    grupo_fk = models.ForeignKey(Grupo, models.DO_NOTHING, db_column="Grupo_FK", blank=True, null=True)
    editavel = models.BooleanField(db_column='Editavel', blank=False, null=False,default=True)

    
    class Meta:
        managed = True
        db_table = 'Item'

class ListaVerificacao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)
    observacao = models.CharField(db_column='Observacao', max_length=1024, blank=True, null=True)
    criadopor = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)
    criadoem = models.DateTimeField(db_column='CriadoEm', blank=True, null=True)
    modificadopor = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    modificadoem = models.DateTimeField(db_column='ModificadoEm', blank=True, null=True)
    modelo_fk = models.ForeignKey(Modelo, models.DO_NOTHING, db_column="Modelo_FK", blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True, choices=LISTA_VERIFICACAO_STATUS)
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.criadopor = request.user
        obj.modificadopor = request.user
        super().save_model(request, obj, form, change)

    class Meta:
        managed = True
        db_table = 'ListaVerificacao'


class ListaVerificacaoxItemxResposta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    listaverificacao_fk = models.ForeignKey(ListaVerificacao, models.DO_NOTHING, db_column="ListaVerificacao_FK", blank=True, null=True)
    item_fk = models.ForeignKey(Item, models.DO_NOTHING, db_column="Item_FK", blank=True, null=True)
    resposta = models.CharField(db_column="Resposta", max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ListaVerificacaoxItemxResposta'


class NotificationCTA(models.Model):
    #id = models.AutoField(db_column='ID', primary_key=True)
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    cta_link = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.cta_link)


def custom_notify_handler(*args, **kwargs):
    notifications = notify_handler(*args, **kwargs)
    cta_link = kwargs.get("cta_link", "")
    for notification in notifications:
        NotificationCTA.objects.create(notification=notification, cta_link=cta_link)
    return notifications


notify.disconnect(notify_handler, dispatch_uid='notifications.models.notification')
notify.connect(custom_notify_handler)  # , dispatch_uid='notifications.models.notification')