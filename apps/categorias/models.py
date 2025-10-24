from django.db import models

# Clase Categoria de Articulos
class Categoriaarticulos(models.Model):
    # Atributos
    idcategoriaarticulo = models.AutoField(primary_key=True)
    descripcion_categoriaarticulo =models.CharField(max_length=100, verbose_name="Descripción")

    # Representación del objeto
    def __str__(self):
        return self.descripcion_categoriaarticulo
    
    # Opciones adicionales
    class Meta:
        ordering = ['descripcion_categoriaarticulo']
        db_table="categoriaarticulos"
        verbose_name="Categoría Artículo"
        verbose_name_plural="Categoría Artículos"
    
    

class Subcategoriaarticulos(models.Model):
    idsubcategoriaarticulo = models.AutoField(primary_key=True)
    
    idcategoriaarticulo = models.ForeignKey(
        Categoriaarticulos,
        on_delete=models.CASCADE,
        verbose_name="Categoría asociada",
        related_name="subcategorias"
    )
    
    descripcion_subcategoriaarticulo = models.CharField(
        max_length=100,
        verbose_name="Descripción de la subcategoría"
    )
    
    def __str__(self):
        return f"{self.descripcion_subcategoriaarticulo} ({self.idcategoriaarticulo.descripcion_categoriaarticulo})"

    class Meta:
        ordering = ['descripcion_subcategoriaarticulo']
        db_table = "subcategoriaarticulos"
        verbose_name = "Subcategoría Artículo"
        verbose_name_plural = "Subcategorías Artículos"
        
        
        
