from django.shortcuts import render, redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from apps.categorias.models import Categoriaarticulos
from apps.articulos.models import Articulos
from apps.categorias.forms import CategoriaForm,SubcategoriaForm
from django.contrib import messages

# Vista Lista de Categorias
@login_required
@permission_required('categorias.ver_categorias', raise_exception=True)
def listado_categorias(request):
    categorias=Categoriaarticulos.objects.all()
    return render(request, 'listado_categorias.html', {"categorias":categorias})

# Vista regristro de Categoria
@login_required
@permission_required('categorias.crear_categorias', raise_exception=True)
def registrar_categorias(request):
    form = CategoriaForm()
    if request.method=="POST":
        form=CategoriaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro Exitoso!")
            return redirect("categorias:listado_categorias")
    
    return render(request, 'registrar_categorias.html', {"form": form})

# Vista Edición de Categoria
@login_required
@permission_required('categorias.editar_categorias', raise_exception=True)
def editar_categorias(request, pk_id):
    categoria = Categoriaarticulos.objects.get(idcategoriaarticulo=pk_id)
    form = CategoriaForm(instance=categoria)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Categoría Modificada Correctamente!")
            return redirect("categorias:listado_categorias")
    
    return render(request, 'editar_categorias.html', {"form": form, 'pk':pk_id})

# Vista Eliminación de Categoria
@login_required
@permission_required('categorias.eliminar_categorias', raise_exception=True)
def eliminar_categorias(request, pk_id):
    categoria=Categoriaarticulos.objects.get(idcategoriaarticulo=pk_id)
    
    if Articulos.objects.filter(idcategoriaarticulo=categoria).exists():
        messages.error(request, "No se puede eliminar la categoría. Existen productos asociados a esta categoría.")
    else:
        categoria.delete()
        messages.success(request, "¡Categoría Eliminada Correctamente!")
    
    return redirect("categorias:listado_categorias")



@login_required
@permission_required('categorias.crear_subcategoria', raise_exception=True)
def registrar_subcategorias(request, pk_id):
    categoria = Categoriaarticulos.objects.get(idcategoriaarticulo=pk_id)

    if request.method == "POST":
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            subcat = form.save(commit=False)
            subcat.idcategoriaarticulo = categoria  # Asignar la categoría seleccionada
            subcat.save()
            messages.success(request, "¡Subcategoría registrada con éxito!")
            return redirect("categorias:listado_categorias")
    else:
        form = SubcategoriaForm()
        form.fields["idcategoriaarticulo"].initial = categoria
        form.fields["idcategoriaarticulo"].widget.attrs['readonly'] = True  # para que no se pueda cambiar

    return render(request, "registrar_subcategorias.html", {
        "form": form,
        "categoria": categoria,
        "pk": categoria.idcategoriaarticulo  # aquí pasas el valor
    })



@login_required
@permission_required('categorias.ver_subcategoriaarticulos', raise_exception=True)
def ver_subcategorias(request, pk_id):
    categoria = get_object_or_404(Categoriaarticulos, idcategoriaarticulo=pk_id)
    subcategorias = categoria.subcategorias.all()  # gracias al related_name="subcategorias"
    return render(request, 'detalle_subcategorias.html', {
        'categoria': categoria,
        'subcategorias': subcategorias
    })