from django.db import models
from apps.articulos.models import Articulos
from apps.compras.models import Compras, Detalle_compras
from django.utils import timezone

# Clase Estado de Lote
class Estado_lotes(models.Model): # nuevo
    # Atributos
    idestado_lote = models.AutoField(primary_key=True)
    code_estado_lote = models.CharField(max_length=30, unique=True)
    descripcion_estado_lote = models.CharField(max_length=30, verbose_name="Descripción")

    # Representación del objeto
    def __str__(self):
        return self.descripcion_estado_lote
    
    # Opciones adicionales
    class Meta:
        db_table="estado_lotes"
        verbose_name="Estado Lote"
        verbose_name_plural="Estado Lotes"

# Clase Lotes
class Lotes(models.Model): # nuevo
    # Atributos
    idlote = models.AutoField(primary_key=True)
    idestado_lote = models.ForeignKey(Estado_lotes, on_delete=models.RESTRICT, verbose_name="Estado Lote")
    codigoarticulo = models.ForeignKey(Articulos, on_delete=models.RESTRICT, verbose_name="Producto")
    numero_lote = models.CharField(max_length=15, verbose_name="Número de Lote")
    fecha_fabricacion = models.DateField(null=True, blank=True, verbose_name="Fecha Fabricación")
    fecha_caducidad = models.DateField(null=True, blank=True, verbose_name="Fecha Caducidad")
    cantidad = models.IntegerField(default=0, verbose_name="Cantidad")

    # Momento de creación
    def save(self, *args, **kwargs):

        # Validación de fechas
        if not self.fecha_caducidad:  # Si no hay fecha de caducidad
            self.idestado_lote = Estado_lotes.objects.get(code_estado_lote='no_vence')
        else:
            dias_restantes = (self.fecha_caducidad - timezone.now().date()).days
            if dias_restantes <= 0:
                self.idestado_lote = Estado_lotes.objects.get(code_estado_lote='vencido')
            elif dias_restantes <= 15:  # Por vencer si quedan 15 días o menos (ajustable)
                self.idestado_lote = Estado_lotes.objects.get(code_estado_lote='por_vencer')
            else:
                self.idestado_lote = Estado_lotes.objects.get(code_estado_lote='vigente')
        
        # Si la cantidad es 0, se considera como consumido
        if self.cantidad == 0:
            self.idestado_lote = Estado_lotes.objects.get(code_estado_lote='consumido')

        # Guardar el objeto        
        super(Lotes, self).save(*args, **kwargs)

    # Representación del objeto
    def __str__(self):
        return self.numero_lote
    
    # Opciones adicionales
    class Meta:
        ordering = ['codigoarticulo', 'fecha_caducidad']
        db_table="lotes"
        verbose_name="Lote"
        verbose_name_plural="Lotes"

# Clase Detalle Compra del Lote
class Detalle_compra_lotes(models.Model): # nuevo
    # Atributos
    iddetalle_compra_lote = models.AutoField(primary_key=True)
    iddetalle_compra = models.ForeignKey(Detalle_compras, on_delete=models.RESTRICT, verbose_name="Detalle Compra Lote")
    idlote = models.ForeignKey(Lotes, on_delete=models.RESTRICT, verbose_name="Lote")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor")

    # Representación del objeto
    def __str__(self):
        return f'{self.iddetalle_compra_lote} - {self.iddetalle_compra}'
    
    # Opciones adicionales
    class Meta:
        db_table="detalle_compra_lotes"
        verbose_name="Detalle Compra Lote"
        verbose_name_plural="Detalle Compra Lotes"
