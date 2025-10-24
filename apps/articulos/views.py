from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.articulos.models import Articulos
from apps.ventas.models import Detalle_ventas
from apps.compras.models import Detalle_compras
from apps.articulos.forms import ArticulosForm
from apps.articulos.filters import ArticulosFilter
from django.contrib import messages

# Vista Lista de Articulos
@login_required
@permission_required('articulos.ver_productos', raise_exception=True)
def listado_articulos(request):
    articulos = Articulos.objects.all()
    filtro = ArticulosFilter(request.GET, queryset=articulos)
    articulos = filtro.qs

    return render(request, 'listado_articulos.html', {"articulos": articulos, "filtro": filtro})

# Vista Registro de Articulo
@login_required
@permission_required('articulos.crear_productos', raise_exception=True)
def registrar_articulos(request):

    form = ArticulosForm()
    if request.method == "POST":
        form = ArticulosForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro Exitoso!")
            return redirect("articulos:listado_articulos")
    
    return render(request, 'registrar_articulos.html', {"form": form})

# Vista Edición de Articulo
@login_required
@permission_required('articulos.editar_productos', raise_exception=True)
def editar_articulos(request, pk_id):
    articulo=Articulos.objects.get(idarticulo=pk_id)
    form=ArticulosForm(instance=articulo)
    if request.method == "POST":
        form = ArticulosForm(request.POST, request.FILES, instance=articulo)
        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Producto Modificado Correctamente!")
            return redirect("articulos:listado_articulos")
    
    contexto = {"form": form, "articulo": articulo}
    return render(request, 'editar_articulos.html', contexto)

# Vista Eliminación de Articulo
@login_required
@permission_required('articulos.eliminar_productos', raise_exception=True)
def eliminar_articulos(request, pk_id):
    articulo = Articulos.objects.get(idarticulo=pk_id)
    existe_compras = Detalle_compras.objects.filter(codigoarticulo=articulo).exists()
    existe_ventas = Detalle_ventas.objects.filter(codigoarticulo=articulo).exists()
    
    if existe_compras or existe_ventas:
        messages.error(request, "No se puede eliminar el producto. Está asociado a transacciones de compras o ventas.")
    else:
        articulo.delete()
        messages.success(request, "¡Producto Eliminado Correctamente!")
    
    return redirect("articulos:listado_articulos")

# Vista Detalle de Articulo
@login_required
@permission_required('articulos.ver_productos', raise_exception=True)
def detalle_articulos(request, pk_id):
    articulo = Articulos.objects.get(idarticulo=pk_id)
    return render(request, 'detalle_articulos.html', {"articulo_detalle": articulo})


from django.http import JsonResponse
from apps.categorias.models import Subcategoriaarticulos

@login_required
def obtener_subcategorias(request):
    categoria_id = request.GET.get('categoria_id')
    subcategorias = Subcategoriaarticulos.objects.filter(idcategoriaarticulo_id=categoria_id)
    data = [{"id": sub.idsubcategoriaarticulo, "descripcion": sub.descripcion_subcategoriaarticulo} for sub in subcategorias]
    return JsonResponse(data, safe=False)