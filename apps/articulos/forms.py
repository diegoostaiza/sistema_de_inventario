from django import forms
from django.forms import ModelForm, ValidationError
from decimal import Decimal
from apps.articulos.models import Articulos,Talla
from django.forms import CheckboxSelectMultiple
# Clase Formulario Articulo
class ArticulosForm(ModelForm):
    # Atributos
    ESTADO_CHOICES = ((0, 'Inactivo'), (1, 'Activo'),)
    estado_articulo = forms.ChoiceField(choices=ESTADO_CHOICES, label="Estado", initial=1)
    tallas = forms.ModelMultipleChoiceField(
        queryset=Talla.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',  # importante para el estilo base
            'id': 'multiple-select-field',
            'data-placeholder': 'Elige las tallas',
        }),
        required=False,
        label="Tallas disponibles"
    )
    # Inicialización del formulario
    def __init__(self, *args, **kwargs):
        super(ArticulosForm, self).__init__(*args, **kwargs)

        # Personalización de los widgets
        self.fields['idcategoriaarticulo'].empty_label = "Seleccione una categoría"
        self.fields['idsubcategoriaarticulo'].empty_label = "Seleccione una subcategoria"
   
        self.fields['idgiva'].empty_label = "Seleccione un tipo"
        self.fields['descripcion_articulo'].widget.attrs.update({'placeholder': 'Ingresa el nombre de la prenda'})
        
      
        
        self.fields['codigoarticulo'].widget.attrs.update({'placeholder': 'Ingresa el código de la prenda'})
       
        self.fields['utilidad'].widget.attrs.update({'min': '0', 'max': '100', 'placeholder': 'Ingresa la utilidad'})
        self.fields['costo'].widget.attrs.update({'placeholder': 'Ingresa el costo'})
        self.fields['precioventa'].widget.attrs.update({'readonly': 'readonly', 'style': 'cursor: not-allowed;'})
        self.fields['stock_minimo'].widget.attrs.update({'placeholder': 'Ingresa un stock mínimo'})
        self.fields['stock_maximo'].widget.attrs.update({'placeholder': 'Ingresa un stock máximo'})

    # Validación de los campos
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_utilidad(self):
        utilidad = self.cleaned_data.get('utilidad')
        if int(utilidad) < 0:
            raise ValidationError("El porcentaje de utilidad no puede ser negativo")
        if int(utilidad) > 100:
            raise ValidationError("El porcentaje de utilidad no puede ser mayor que 100")
        return utilidad

    def clean_costo(self):
        costo = self.cleaned_data.get('costo')
        if Decimal(costo) < Decimal('0.00'):
            raise ValidationError("El costo no puede ser negativo")
        return costo
    
    def clean_precioventa(self):
        precioventa = self.cleaned_data.get('precioventa')
        if Decimal(precioventa) < Decimal('0.00'):
            raise ValidationError("El precio de venta no puede ser negativo")
        return precioventa
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        max_size = 4 * 1024 * 1024  # 3 MB en bytes
        if imagen and imagen.size > max_size:
            raise ValidationError("El tamaño máximo de la imagen debe ser de 4 MB.")
        return imagen
    
   
    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo")
        return stock_minimo

    def clean_stock_maximo(self):
        stock_maximo = self.cleaned_data.get('stock_maximo')
        stock_minimo = self.cleaned_data.get('stock_minimo')
        errors = []
        if stock_maximo is not None and stock_minimo is not None:
            if stock_maximo <= stock_minimo:
                errors.append("El stock máximo debe ser mayor que el stock mínimo")
        if stock_maximo < 0:
            errors.append("El stock máximo no puede ser negativo")
        if errors:
            raise ValidationError(errors)
        return stock_maximo

    # Opciones adicionales
    class Meta:
        model = Articulos
        fields = ['codigoarticulo', 'idcategoriaarticulo' ,'idsubcategoriaarticulo','imagen', 'descripcion_articulo','tallas', 'costo', 'precioventa', 'stock_minimo', 'stock_maximo', 'idgiva', 'utilidad', 'estado_articulo']
    
       