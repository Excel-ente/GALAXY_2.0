from administracion.models import Receta
from django.contrib import messages


def Actualizar(modeladmin, request, queryset):
    for receta in Receta.objects.filter(ESTADO="Pendiente"):
        if receta.ESTADO == "Pendiente":
            costo_receta = 0

            for ingrediente in receta.ingredientes.all():
                costo_receta += ingrediente.COSTO_UNITARIO * ingrediente.CANTIDAD

            receta.COSTO_RECETA = costo_receta
            receta.COSTO_FINAL = costo_receta
            receta.save()

    messages.success(request, "Recetas actualizadas con éxito.")

Actualizar.short_description = "Actualizar Presupuestos"

