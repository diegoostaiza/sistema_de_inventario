from django.db import models
from apps.categorias.models import Categoriaarticulos,Subcategoriaarticulos
from cloudinary.models import CloudinaryField
# Clase Graba Iva
class Givas(models.Model):
    # Atributos
    idgiva = models.AutoField(primary_key=True)
    descripcion_giva = models.CharField(max_length=30, verbose_name="Descripción")
    valoriva = models.IntegerField(verbose_name="Valor Iva")

    # Representación del objeto
    def __str__(self):
        return self.descripcion_giva

    # Opciones adicionales
    class Meta:
        db_table="givas"
        verbose_name="Graba Iva"
        verbose_name_plural="Graba Ivas"






class Talla(models.Model):
    idtalla = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=5, unique=True, verbose_name="Talla")  # Ej: S, M, L, XL

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "tallas"
        verbose_name = "Talla"
        verbose_name_plural = "Tallas"


# Clase Articulos
class Articulos(models.Model):
    # Atributos
    idarticulo = models.AutoField(primary_key=True)
    codigoarticulo = models.CharField(max_length=10, unique=True, verbose_name="Código de Producto")
    idcategoriaarticulo = models.ForeignKey(Categoriaarticulos, on_delete=models.PROTECT, verbose_name="Categoría")
    idsubcategoriaarticulo = models.ForeignKey(Subcategoriaarticulos, on_delete=models.PROTECT, verbose_name="Subcategoría", null=True, blank=True)
    idgiva = models.ForeignKey(Givas, on_delete=models.PROTECT, verbose_name="Iva")
    imagen = CloudinaryField('imagen', folder='productos/', null=True, blank=True)
    descripcion_articulo = models.CharField(max_length=100, verbose_name="Descripción")
    tallas = models.ManyToManyField(Talla, verbose_name="Tallas Disponibles", related_name='articulos')
    stock = models.IntegerField(default=0, verbose_name="Stock")
    stock_minimo = models.IntegerField(default=0, verbose_name="Stock Mínimo")
    stock_maximo = models.IntegerField(default=1, verbose_name="Stock Máximo")
    costo = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Costo")
    utilidad = models.IntegerField(verbose_name="Utilidad")
    precioventa = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Precio Venta")
    estado_articulo = models.IntegerField(default=1, verbose_name="Estado")

    # Representación del objeto
    def __str__(self):
        return self.descripcion_articulo
    
    # Obtener el valor del IVA
    def get_valor_iva(self):
        return self.idgiva.valoriva

    # Eliminar las imagenes del directorio
    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        return super().delete(using, keep_parents)
    
    # Opciones adicionales
    class Meta:
        ordering = ['-estado_articulo', 'descripcion_articulo']
        db_table="articulos"
        verbose_name="Artículo"
        verbose_name_plural="Artículos"
    