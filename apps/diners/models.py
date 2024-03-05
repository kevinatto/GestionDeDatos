from django.db import models

# Create your models here.

class diners_emision(models.Model):
    CEDULA_SOCIO                 = models.CharField(max_length=500)
    D8FAXT                       = models.CharField(max_length=500)
    D8H9NB                       = models.IntegerField()
    D8KINR                       = models.IntegerField()
    D8B0TX                       = models.CharField(max_length=500)
    D8GLNB                       = models.IntegerField()
    D8GKNB                       = models.IntegerField()
    D8CLTX                       = models.CharField(max_length=500)
    D8GJNB                       = models.IntegerField()
    D8GNNB                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8GWNB                       = models.IntegerField()
    D8GZNB                       = models.IntegerField()
    D8DIEC                       = models.CharField(max_length=500)
    D8X1XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8X2XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8X3XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8XTXT                       = models.CharField(max_length=500)
    D8O5XT                       = models.CharField(max_length=500)
    D8OLST                       = models.CharField(max_length=500)
    D8ABCD                       = models.IntegerField()
    D8AECD                       = models.IntegerField()
    TOTAL_FACTURADO_DC           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_DC            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_DC                      = models.DecimalField(max_digits=12, decimal_places=2)
    TOTAL_FACTURADO_VS           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_VS            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_VS                      = models.DecimalField(max_digits=12, decimal_places=2)
    TOTAL_FACTURADO_DI           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_DI            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_DI                      = models.DecimalField(max_digits=12, decimal_places=2)
    BASE                         = models.CharField(max_length=500)
    TOTAL_FACTURADO_MC           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_MC            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_MC                      = models.DecimalField(max_digits=12, decimal_places=2)
    FECHA_AFILIACION             = models.DateTimeField()
    SUMA_ASEGURADA               = models.DecimalField(max_digits=12, decimal_places=2)
    PRIMA_NETA                   = models.DecimalField(max_digits=12, decimal_places=2)
    PRIMA_TOTAL                  = models.DecimalField(max_digits=12, decimal_places=2)
    VALOR_MAXIMO                 = models.DecimalField(max_digits=12, decimal_places=2)
    PRIORIDAD                    = models.CharField(max_length=500)
    PROCESADO_EL                 = models.DateTimeField()
    
class diners_excluidos(models.Model):
    CEDULA_SOCIO                 = models.CharField(max_length=500)
    D8FAXT                       = models.CharField(max_length=500)
    D8H9NB                       = models.IntegerField()
    D8KINR                       = models.IntegerField()
    D8B0TX                       = models.CharField(max_length=500)
    D8GLNB                       = models.IntegerField()
    D8GKNB                       = models.IntegerField()
    D8CLTX                       = models.CharField(max_length=500)
    D8GJNB                       = models.IntegerField()
    D8GNNB                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8GWNB                       = models.IntegerField()
    D8GZNB                       = models.IntegerField()
    D8DIEC                       = models.CharField(max_length=500)
    D8X1XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8X2XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8X3XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8XTXT                       = models.CharField(max_length=500)
    D8O5XT                       = models.CharField(max_length=500)
    D8OLST                       = models.CharField(max_length=500)
    D8ABCD                       = models.IntegerField()
    D8AECD                       = models.IntegerField()
    TOTAL_FACTURADO_DC           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_DC            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_DC                      = models.DecimalField(max_digits=12, decimal_places=2)
    TOTAL_FACTURADO_VS           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_VS            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_VS                      = models.DecimalField(max_digits=12, decimal_places=2)
    TOTAL_FACTURADO_DI           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_DI            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_DI                      = models.DecimalField(max_digits=12, decimal_places=2)
    BASE                         = models.CharField(max_length=500)
    TOTAL_FACTURADO_MC           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_MC            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_MC                      = models.DecimalField(max_digits=12, decimal_places=2)
    FECHA_AFILIACION             = models.DateTimeField()
    SUMA_ASEGURADA               = models.DecimalField(max_digits=12, decimal_places=2)
    PRIMA_NETA                   = models.DecimalField(max_digits=12, decimal_places=2)
    PRIMA_TOTAL                  = models.DecimalField(max_digits=12, decimal_places=2)
    VALOR_MAXIMO                 = models.DecimalField(max_digits=12, decimal_places=2)
    PRIORIDAD                    = models.CharField(max_length=500)
    PROCESADO_EL                 = models.DateTimeField()
    
class diners_prima_cero(models.Model):
    CEDULA_SOCIO                 = models.CharField(max_length=500)
    D8FAXT                       = models.CharField(max_length=500)
    D8H9NB                       = models.IntegerField()
    D8KINR                       = models.IntegerField()
    D8B0TX                       = models.CharField(max_length=500)
    D8GLNB                       = models.IntegerField()
    D8GKNB                       = models.IntegerField()
    D8CLTX                       = models.CharField(max_length=500)
    D8GJNB                       = models.IntegerField()
    D8GNNB                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8GWNB                       = models.IntegerField()
    D8GZNB                       = models.IntegerField()
    D8DIEC                       = models.CharField(max_length=500)
    D8X1XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8X2XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8X3XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8XTXT                       = models.CharField(max_length=500)
    D8O5XT                       = models.CharField(max_length=500)
    D8OLST                       = models.CharField(max_length=500)
    D8ABCD                       = models.IntegerField()
    D8AECD                       = models.IntegerField()
    TOTAL_FACTURADO_DC           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_DC            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_DC                      = models.DecimalField(max_digits=12, decimal_places=2)
    TOTAL_FACTURADO_VS           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_VS            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_VS                      = models.DecimalField(max_digits=12, decimal_places=2)
    TOTAL_FACTURADO_DI           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_DI            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_DI                      = models.DecimalField(max_digits=12, decimal_places=2)
    BASE                         = models.CharField(max_length=500)
    TOTAL_FACTURADO_MC           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_MC            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_MC                      = models.DecimalField(max_digits=12, decimal_places=2)
    FECHA_AFILIACION             = models.DateTimeField()
    SUMA_ASEGURADA               = models.DecimalField(max_digits=12, decimal_places=2)
    PRIMA_NETA                   = models.DecimalField(max_digits=12, decimal_places=2)
    PRIMA_TOTAL                  = models.DecimalField(max_digits=12, decimal_places=2)
    VALOR_MAXIMO                 = models.DecimalField(max_digits=12, decimal_places=2)
    PRIORIDAD                    = models.CharField(max_length=500)
    PROCESADO_EL                 = models.DateTimeField()
    
class diners_cobro_cero(models.Model):
    CEDULA_SOCIO                 = models.CharField(max_length=500)
    D8FAXT                       = models.CharField(max_length=500)
    D8H9NB                       = models.IntegerField()
    D8KINR                       = models.IntegerField()
    D8B0TX                       = models.CharField(max_length=500)
    D8GLNB                       = models.IntegerField()
    D8GKNB                       = models.IntegerField()
    D8CLTX                       = models.CharField(max_length=500)
    D8GJNB                       = models.IntegerField()
    D8GNNB                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8GWNB                       = models.IntegerField()
    D8GZNB                       = models.IntegerField()
    D8DIEC                       = models.CharField(max_length=500)
    D8X1XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8X2XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8X3XT                       = models.DecimalField(max_digits=12, decimal_places=2)
    D8XTXT                       = models.CharField(max_length=500)
    D8O5XT                       = models.CharField(max_length=500)
    D8OLST                       = models.CharField(max_length=500)
    D8ABCD                       = models.IntegerField()
    D8AECD                       = models.IntegerField()
    TOTAL_FACTURADO_DC           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_DC            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_DC                      = models.DecimalField(max_digits=12, decimal_places=2)
    TOTAL_FACTURADO_VS           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_VS            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_VS                      = models.DecimalField(max_digits=12, decimal_places=2)
    TOTAL_FACTURADO_DI           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_DI            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_DI                      = models.DecimalField(max_digits=12, decimal_places=2)
    BASE                         = models.CharField(max_length=500)
    TOTAL_FACTURADO_MC           = models.DecimalField(max_digits=12, decimal_places=2)
    DIF_X_FACTURAR_MC            = models.DecimalField(max_digits=12, decimal_places=2)
    NETO_MC                      = models.DecimalField(max_digits=12, decimal_places=2)
    FECHA_AFILIACION             = models.DateTimeField()
    SUMA_ASEGURADA               = models.DecimalField(max_digits=12, decimal_places=2)
    PRIMA_NETA                   = models.DecimalField(max_digits=12, decimal_places=2)
    PRIMA_TOTAL                  = models.DecimalField(max_digits=12, decimal_places=2)
    VALOR_MAXIMO                 = models.DecimalField(max_digits=12, decimal_places=2)
    PRIORIDAD                    = models.CharField(max_length=500)
    PROCESADO_EL                 = models.DateTimeField()