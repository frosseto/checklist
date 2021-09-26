from django.db import models
from django.conf import settings
from django.db.models.fields import related
from django.utils.timezone import now

UEP_CHOICES = (
    ('PMLZ','PMLZ'),
    ('PMXL','PMXL'),
    ('P66','P66'),
    ('P67','P67'),
    ('P68','P68'),
    ('P69','P69'),
    ('P70','P70'),)

RESULTADO_CHOICES = (
    ('Em análise','Em análise'),
    ('Conforme','Conforme'),
    ('Leve','Leve'),
    ('Média','Média'),
    ('Grave','Grave'),)

STATUS_CHOICES = (
    ('Aguardando analista','Aguardando analista'),
    ('Ordem analisada','Ordem analisada'),)

ITEM_TIPOS = (
    ('CHECKBOX','CheckBox'),
    ('TEXT','Text'),
    ('COMBOBOX','ComboBox'),)

class OrdemPesquisa(models.Model):
    tblsaoid = models.IntegerField(db_column='tblSAOID')  # Field name made lowercase.
    uep = models.CharField(db_column='UEP', max_length=255, blank=True, null=True, choices=UEP_CHOICES)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True, choices=STATUS_CHOICES)  # Field name made lowercase.
    ordem = models.CharField(db_column='Ordem', max_length=255, primary_key=True)  # Field name made lowercase.
    descricaoordem = models.CharField(db_column='DescricaoOrdem', max_length=255, blank=True, null=True)  # Field name made lowercase.
    observacaoanalista = models.TextField(db_column='ObservacaoAnalista', blank=True, null=True)  # Field name made lowercase.
    observacaoop = models.TextField(db_column='ObservacaoOp', blank=True, null=True)  # Field name made lowercase.
    resultado = models.CharField(db_column='Resultado', max_length=255, blank=True, null=True, choices=RESULTADO_CHOICES)  # Field name made lowercase.
    dataanalise = models.DateField(db_column='DataAnalise', blank=True, null=True)  # Field name made lowercase.
    modificacaoordem = models.DateField(db_column='ModificacaoOrdem', blank=True, null=True)  # Field name made lowercase.
    datafimreal = models.DateField(db_column='DataFimReal', blank=True, null=True)  # Field name made lowercase.
    modificadaaposanalise = models.BooleanField(db_column='ModificadaAposAnalise')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = '[OrdemPesquisa]'

    def __str__(self):
        return self.ordem

    def to_dict_jason(self):
        return {
            'tblsaoid': self.tblsaoid,
            'uep': self.uep,
            'ordem': self.ordem,
            'descricaoordem': self.descricaoordem,
            'observacaoanalista': self.observacaoanalista,
            'resultado': self.resultado,
            'dataanalise': self.dataanalise,
            'modificacaoordem': self.modificacaoordem,
            'datafimreal': self.datafimreal,
        }


class SAO(models.Model):
    tblsaoid = models.AutoField(db_column='tblSAOID', primary_key=True)  # Field name made lowercase.
    dataanalise = models.DateTimeField(db_column='DataAnalise', blank=True, null=True)  # Field name made lowercase.
    analisadopor = models.CharField(db_column='AnalisadoPor', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ordem = models.CharField(db_column='Ordem',  max_length=255)  # Field name made lowercase.
    uep = models.CharField(db_column='UEP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricaoordem = models.CharField(db_column='DescricaoOrdem', max_length=255, blank=True, null=True)  # Field name made lowercase.
    datafimreal = models.DateTimeField(db_column='DataFimReal', blank=True, null=True)  # Field name made lowercase.
    item = models.CharField(db_column='Item', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nota = models.CharField(db_column='Nota', max_length=255, blank=True, null=True)  # Field name made lowercase.
    executadopor = models.TextField(db_column='ExecutadoPor', blank=True, null=True)  # Field name made lowercase.
    confirmadopor = models.TextField(db_column='ConfirmadoPor', blank=True, null=True)  # Field name made lowercase.
    encerradotecnicamentepor = models.TextField(db_column='EncerradoTecnicamentePor', blank=True, null=True)  # Field name made lowercase.
    resultado = models.CharField(db_column='Resultado', max_length=255, blank=True, null=True)  # Field name made lowercase.
    observacaoanalista = models.TextField(db_column='ObservacaoAnalista', blank=True, null=True)  # Field name made lowercase.
    observacaolocal = models.TextField(db_column='ObservacaoLocal', blank=True, null=True)  # Field name made lowercase.
    equipamento = models.CharField(db_column='Equipamento', max_length=255, blank=True, null=True)  # Field name made lowercase.
    databaseinicio = models.DateTimeField(db_column='DataBaseInicio', blank=True, null=True)  # Field name made lowercase.
    necessitaalteracaoplano = models.CharField(db_column='NecessitaAlteracaoPlano', max_length=255, blank=True, null=True)  # Field name made lowercase.
    datacorrecaoefetuada = models.TextField(db_column='DataCorrecaoEfetuada', blank=True, null=True)  # Field name made lowercase.
    possuiaindaalgumapendencia = models.CharField(db_column='PossuiAindaAlgumaPendencia', max_length=255, blank=True, null=True)  # Field name made lowercase.
    verificacaoencerramento = models.CharField(db_column='VerificacaoEncerramento', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dadospreventivosanp = models.BooleanField(db_column='DadosPreventivosANP', blank=True, null=True)  # Field name made lowercase.
    local = models.CharField(db_column='Local', max_length=255, blank=True, null=True)  # Field name made lowercase.
    if_field = models.CharField(db_column='IF', max_length=1, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    tipoordem = models.CharField(db_column='TipoOrdem', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datareferencia = models.DateTimeField(db_column='DataReferencia', blank=True, null=True)  # Field name made lowercase.
    observacaoop = models.TextField(db_column='ObservacaoOp', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = '[tblSAO]'


class SAOResultado(models.Model):
    id = models.AutoField(db_column='tblGravidadeID', primary_key=True)
    categoria = models.CharField(db_column='Categoria1',  max_length=255, null=True)
    item = models.CharField(db_column='Valor',  max_length=255, null=True)
    orientacao = models.CharField(db_column='Orientacao',  max_length=255, null=True)
    item_sel = models.CharField(db_column='Sel', max_length=1)



class Gravidade(models.Model):
    id = models.AutoField(db_column='tblGravidadeID', primary_key=True)
    categoria1 = models.CharField(db_column='Categoria1', max_length=255, blank=True, null=True) 
    categoria2 = models.CharField(db_column='Categoria2', max_length=255, blank=True, null=True) 
    valor = models.CharField(db_column='Valor', max_length=255, blank=True, null=True)
    gravidade = models.CharField(db_column='Gravidade', max_length=255, blank=True, null=True)
    acao = models.CharField(db_column='Acao', max_length=1024, blank=True, null=True)
    orientacao = models.CharField(db_column='Orientacao', max_length=255, blank=True, null=True)
    ativo = models.BooleanField(db_column='Ativo')  
    acaocorretiva = models.CharField(db_column='AcaoCorretiva', max_length=1024, blank=True, null=True)

    class Meta:
        managed = True
        db_table = '[tblGravidade]'

# Checklist

class Modelo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=1024, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Modelo'


class Grupo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=1024, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Grupo'


class Item(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=1024, blank=True, null=True)
    itemtipo = models.CharField(db_column='ItemTipo', max_length=50, blank=True, null=True, choices=ITEM_TIPOS)
    modelo_fk = models.ForeignKey(Modelo, models.DO_NOTHING, db_column="Modelo_FK", blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Item'

class ListaVerificacao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    observacao = models.CharField(db_column='Observacao', max_length=1024, blank=True, null=True)
    criadopor = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)
    criadaem = models.DateTimeField(db_column='CriadoEm', default=now, blank=True, null=True)
    modificadopor = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    modificadoem = models.DateTimeField(db_column='ModificadoEm', default=now, blank=True, null=True)
    modelo_fk = models.ForeignKey(Modelo, models.DO_NOTHING, db_column="Modelo_FK", blank=True, null=True)

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
    resposta = models.CharField(models.DO_NOTHING, db_column="Resposta", max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ListaVerificacaoxItemxResposta'