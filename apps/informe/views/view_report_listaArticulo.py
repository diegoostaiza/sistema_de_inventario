from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from datetime import datetime
from apps.empresa.models import Empresas
from apps.articulos.models import Articulos, Categoriaarticulos
from apps.informe.filters import ReporteArticulosFilter
from django.db.models import Sum, F

# Vista principal del reporte
@login_required
@permission_required('empresa.generar_reportes', raise_exception=True)
def reporte_articulos(request):
    filtro = ReporteArticulosFilter(request.GET, queryset=Articulos.objects.all())
    return render(request, 'informe_informes/reporte_articulos.html', {'filtro': filtro})


# Generador de PDF
def generar_pdf_articulos(self, request):
    articulos = Articulos.objects.values(
        'codigoarticulo', 
        'descripcion_articulo', 
        'idcategoriaarticulo__descripcion_categoriaarticulo', 
        'stock', 
        'stock_minimo', 
        'stock_maximo', 
        'costo'
    ).annotate(
        total=F('stock') * F('costo')
    ).order_by('descripcion_articulo')

    filtro = ReporteArticulosFilter(request.GET, queryset=articulos)
    empresa = Empresas.objects.get(idempresa=100)
    logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    totales = filtro.qs.aggregate(
        total_stock=Sum('stock'),
        total_costo=Sum('costo'),
        total_valor=Sum('total')
    )

    context = {
        'empresa': empresa,
        'articulos': filtro.qs,
        'logo_url': logo_url,
        'now': now,
        'totales': totales,
    }

    template = get_template('informe_pdf/reporte_articulos.html')
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=result)
    if not pdf.err:
        return result.getvalue()
    return None


# Vista clase para servir el PDF
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('empresa.generar_reportes', raise_exception=True), name='dispatch')
class GenerarPDFArticulosView(View):
    def get(self, request, descargar, *args, **kwargs):
        pdf_content = generar_pdf_articulos(self, request)
        if pdf_content:
            filename = "ReporteArticulos.pdf"
            response = HttpResponse(pdf_content, content_type='application/pdf')
            if descargar == 'True':
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'filename="{filename}"'
            return response
        else:
            return HttpResponse("Error al generar el PDF.", status=500)
