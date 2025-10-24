from django.forms import ModelForm, ValidationError
from apps.empresa.models import Ciudades, Provincias, Empresas
from django import forms

# Clase Formulario Empresa
class EmpresaForm(ModelForm):
    # Atributos
    idprovincia = forms.ModelChoiceField(
        queryset = Provincias.objects.all().order_by('nombre_provincia'), 
        label='Provincia', 
        required=True, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ), 
        empty_label="Seleccione una provincia"
    )
    idciudad = forms.ModelChoiceField(
        queryset=Ciudades.objects.none(), 
        label='Ciudad', 
        required=True, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ), 
        empty_label="Seleccione una ciudad"
    )
    
    # Validación de los campos
    def clean_RUC(self):
        RUC=self.cleaned_data["RUC"]
        if not RUC.isdigit() or len(RUC) != 13:
            raise ValidationError("El RUC debe contener solo 13 dígitos numéricos")
        return RUC

    def clean_cedularepresentantelegal(self):
        ceduRepr=self.cleaned_data["cedularepresentantelegal"]
        if not ceduRepr.isdigit() or len(ceduRepr) != 10:
            raise ValidationError("La cedula debe contener solo 10 dígitos numéricos")
        return ceduRepr
    
    # Inicialización del formulario
    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)

        # Personalización de los widgets
        self.fields['RUC'].widget.attrs.update({'placeholder': 'Ingresa el RUC'})
        self.fields['razonsocial'].widget.attrs.update({'placeholder': 'Ingresa la razón social'})
        self.fields['nombrecomercial'].widget.attrs.update({'placeholder': 'Ingresa el nombre comercial'})
        self.fields['direccion1'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})
        self.fields['direccion2'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})
        self.fields['correo_empresa'].widget.attrs.update({'placeholder': 'Ingresa el correo electrónico'})
        self.fields['telefono_empresa'].widget.attrs.update({'placeholder': 'Ingresa el teléfono'})
        self.fields['celular_empresa'].widget.attrs.update({'placeholder': 'Ingresa el celular'})
        self.fields['cedularepresentantelegal'].widget.attrs.update({'placeholder': 'Ingresa la cédula del representante legal'})
        self.fields['nombrerepresentantelegal'].widget.attrs.update({'placeholder': 'Ingresa el nombre del representante legal'})

        # Configuración de los selectores de provincia y ciudad
        self.fields['idciudad'].queryset = Ciudades.objects.none()
        if 'idprovincia' in self.data:
            try:
                provincia_id = int(self.data.get('idprovincia'))
                self.fields['idciudad'].queryset = (
                    Ciudades.objects
                    .filter(idprovincia=provincia_id)
                    .order_by('nombre_ciudad')
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.idciudad:
            self.fields['idprovincia'].initial = self.instance.idciudad.idprovincia.pk
            self.fields['idciudad'].queryset = (
                Ciudades.objects
                .filter(idprovincia=self.instance.idciudad.idprovincia)
                .order_by('nombre_ciudad')
            )
            self.fields['idprovincia'].widget.attrs['disabled'] = False
    
    # Opciones adicionales
    class Meta:
        model = Empresas
        fields = ['RUC', 'razonsocial', 'nombrecomercial', 'idprovincia', 'idciudad', 'direccion1', 'direccion2', 'correo_empresa', 'telefono_empresa', 'celular_empresa', 'cedularepresentantelegal', 'nombrerepresentantelegal', 'logo']
    
    
class ProvinciaForm(forms.ModelForm):
    nombre_provincia = forms.CharField(
        label="Nombre de la Provincia",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Provincias
        fields = ['nombre_provincia']

# Formulario para registrar una Ciudad
class CiudadForm(forms.ModelForm):
    idprovincia = forms.ModelChoiceField(
        queryset=Provincias.objects.all(),
        label="Provincia",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    nombre_ciudad = forms.CharField(
        label="Nombre de la Ciudad",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Ciudades
        fields = ['idprovincia', 'nombre_ciudad']