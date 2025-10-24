from django.forms import ModelForm
from apps.categorias.models import Categoriaarticulos, Subcategoriaarticulos

# Clase Formulario Categoria
class CategoriaForm(ModelForm):
    # Inicialización del formulario
    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        
        # Personalización de los widgets
        self.fields['descripcion_categoriaarticulo'].widget.attrs.update({'placeholder': 'Ingresa el nombre'})

    # Opciones adicionales
    class Meta:
        model = Categoriaarticulos
        fields = ['descripcion_categoriaarticulo']

class SubcategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubcategoriaForm, self).__init__(*args, **kwargs)
        self.fields['descripcion_subcategoriaarticulo'].widget.attrs.update({'placeholder': 'Ingresa la subcategoría'})
        self.fields['idcategoriaarticulo'].empty_label = "Seleccione una categoría"

    class Meta:
        model = Subcategoriaarticulos
        fields = ['idcategoriaarticulo', 'descripcion_subcategoriaarticulo']