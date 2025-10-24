from django.db import models
from cloudinary.models import CloudinaryField


# Clase Provincia
class Provincias(models.Model):
    # Atributos
    idprovincia = models.AutoField(primary_key=True)
    nombre_provincia = models.CharField(max_length=50, verbose_name="Nombre")

    # Representación del objeto
    def __str__(self):
        return self.nombre_provincia
    
    class Meta:
        db_table="provincias"
        verbose_name="Provincia"
        verbose_name_plural="Provincias"            

# Clase Ciudad
class Ciudades(models.Model):
    # Atributos
    idciudad = models.AutoField(primary_key=True)
    idprovincia = models.ForeignKey(Provincias, on_delete=models.PROTECT, verbose_name="Provincia")
    nombre_ciudad = models.CharField(max_length=50, verbose_name="Nombre")

    # Representación del objeto
    def __str__(self):
        return self.nombre_ciudad
    
    # Opciones adicionales
    class Meta:
        db_table="ciudades"
        verbose_name="Ciudad"
        verbose_name_plural="Ciudades"
    
# Clase Empresa
class Empresas(models.Model):
    # Atributos
    idempresa = models.AutoField(primary_key=True)
    idciudad = models.ForeignKey(Ciudades, on_delete=models.PROTECT, verbose_name="Ciudad")
    RUC = models.CharField(max_length=13, verbose_name="RUC")
    razonsocial = models.CharField(max_length=80, verbose_name="Razón Social")
    nombrecomercial = models.CharField(max_length=80, verbose_name="Nombre Comercial")
    logo = CloudinaryField('imagen', folder='productos/', null=True, blank=True)
    direccion1 = models.CharField(max_length=100, verbose_name="Dirección Matriz")
    direccion2 = models.CharField(max_length=100, verbose_name="Dirección Sucursal")
    correo_empresa = models.EmailField(max_length=80, verbose_name="Correo")
    telefono_empresa = models.CharField(max_length=9, null=True, blank=True, verbose_name="Teléfono")
    celular_empresa = models.CharField(max_length=10, null=True, blank=True, verbose_name="Celular")
    cedularepresentantelegal = models.CharField(max_length=10, verbose_name="Cedula Representante Legal")
    nombrerepresentantelegal = models.CharField(max_length=50, verbose_name="Nombre Representante Legal")
    rutaarchivogenerados = models.CharField(max_length=100, verbose_name="Ruta de Archivos")
    estado_empresa = models.IntegerField(default=1, verbose_name="Estado")

    # Representación del objeto
    def __str__(self):
        return self.nombrecomercial
    
    # Eliminar las imagenes del directorio
    def delete(self, using=None, keep_parents=False):
        self.logo.storage.delete(self.logo.name)
        return super().delete()
    
    # Opciones adicionales
    class Meta:
        db_table="datos_empresa"
        verbose_name="Empresa"
        verbose_name_plural="Empresas"
