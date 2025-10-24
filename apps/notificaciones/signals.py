from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from apps.articulos.models import Articulos
from apps.usuarios.models import CustomUser
from apps.notificaciones.models import Notification, NotificationCustomUser
from apps.compras.models import Detalle_compras
from apps.ventas.models import Detalle_ventas

def enviar_notificacion_stock(articulo):
    """ Verificar el stock y enviar notificaciones """
    content_type = ContentType.objects.get_for_model(Articulos)


@receiver(post_save, sender=Detalle_compras)
def verificar_stock_compra(sender, instance, **kwargs):
    """ Enviar notificación cuando se registra una compra """
    articulo = instance.codigoarticulo
    enviar_notificacion_stock(articulo)

@receiver(post_save, sender=Detalle_ventas)
def verificar_stock_compra(sender, instance, **kwargs):
    """ Enviar notificación cuando se registra una venta """
    articulo = instance.codigoarticulo
    enviar_notificacion_stock(articulo)