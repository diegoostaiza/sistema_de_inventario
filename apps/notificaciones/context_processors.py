from apps.notificaciones.models import NotificationCustomUser
from django.utils.timezone import now

def notificaciones(request):
    total_notificaciones = NotificationCustomUser.objects.none()
    notificaciones_base = NotificationCustomUser.objects.none()
    nuevas_notificaciones = False  # Ojo: aquí es `False`, no una queryset

    if request.user.is_authenticated:
        notificaciones_base = NotificationCustomUser.objects.filter(user=request.user, read=False)
        total_notificaciones = notificaciones_base.count()

        primera = notificaciones_base.first()
        if primera:
            diferencia = (now() - primera.created).total_seconds()
            if diferencia <= 5:
                nuevas_notificaciones = True

    return {
        'total_notificaciones': total_notificaciones,
        'notificaciones_base': notificaciones_base,
        'nuevas_notificaciones': nuevas_notificaciones,
    }
