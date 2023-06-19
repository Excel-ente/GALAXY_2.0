from django import forms
from django.db import models
from django.contrib import admin
from .models import *
from .Funciones import Actualizar,Entregar,Aceptar
from import_export.admin import ImportExportModelAdmin
import pytz
from .AceptacionPresupuesto import generar_reporte
from .Reporte import generar_reporte_cliente,generar_presupuesto

admin.site.site_header = "GALAXY 2.0"
admin.site.site_title = "GALAXY 2.0"

class IngredienteRecetaInline(admin.TabularInline):
    model = ingredientereceta
    extra = 1
    fields = ('producto', 'cantidad',)
    #readonly_fields =('medida_uso','subtotal',)
    autocomplete_fields = ('producto',)

class gastosAdicionalesInline(admin.TabularInline):
    model = adicionalreceta
    extra = 1
    fields = ('adicional', 'precio',)

@admin.register(PedidosEntregados)
class PedidosEntregadosAdmin(ImportExportModelAdmin):
    list_display = ('CLIENTE','FECHA_ENTREGA','DIAS_DE_TRABAJO','PRECIO','INGREDIENTES',)
    exclude=('COSTO_RECETA','MANO_DE_OBRA','ARTICULO',)
    actions=[generar_reporte,]

    def PRECIO_VENTA(self, obj):
        return "💲{:,.2f}".format(obj.PRECIO)
    
@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    list_display = ('NOMBRE_Y_APELLIDO','DIRECCION','EMAIL','TELEFONO',)
  
@admin.register(Proveedor)
class ProveedorAdmin(ImportExportModelAdmin):
    list_display = ('EMPRESA', 'NOMBRE','DIRECCION', 'EMAIL','TELEFONO',)
    ordering = ('EMPRESA',)

@admin.register(gastosFijos)
class gastosFijosAdmin(ImportExportModelAdmin):
    list_display = ('DETALLE', 'IMPORTE',)
    ordering = ('DETALLE',)

    def IMPORTE(self, obj):
        return "💲{:,.2f}".format(obj.TOTAL)

@admin.register(gastosAdicionales)
class gastosAdicionalesAdmin(ImportExportModelAdmin):
    list_display = ('PRODUCTO',)
    ordering = ('PRODUCTO',)

@admin.register(Insumo)
class InventarioAdmin(ImportExportModelAdmin):
    list_display = ('PRODUCTO','PROVEEDOR','UNIDAD_MEDIDA_COMPRA', 'CANTIDAD', 'PRECIO__COMPRA', 'UNIDAD_MEDIDA_USO', 'COSTO__UNITARIO',)
    ordering = ('PRODUCTO',)
    list_filter=()
    exclude=('COSTO_UNITARIO','STOCK',)
    search_fields = ('PRODUCTO',)
    list_per_page = 25
    list_display_links = ('PRODUCTO',)

    def PRECIO__COMPRA(self, obj):
        return "💲{:,.2f}".format(obj.PRECIO_COMPRA)
    
    def COSTO__UNITARIO(self, obj):
        return "💲{:,.2f}".format(obj.COSTO_UNITARIO)

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    inlines = [
        gastosAdicionalesInline,
        IngredienteRecetaInline,
    ]
    
    list_display = ('Presupuesto','NOMBRE','Estado','DIAS_DE_TRABAJO','Precio','Fecha_de_entrega',)
    readonly_fields = ('Precio','Gastos_adicionales,')
    ordering = ('RENTABILIDAD',)
    exclude = ('ADICIONALES','GASTOS_ADICIONALES','ARTICULOS','STOCK', 'INGREDIENTES', 'ULTIMA_ACTUALIZACION', 'PRECIO_VENTA', 'RENTABILIDAD', 'COSTO_FINAL', 'ESTADO',)
    search_fields = ('NOMBRE',)
    list_per_page = 25
    list_display_links = ('Presupuesto', 'NOMBRE',)
    actions = [Actualizar, Aceptar, Entregar,generar_reporte_cliente,generar_presupuesto]

    formfield_overrides = {
        models.DecimalField: {'widget': forms.TextInput},  # Ejemplo de personalización para DecimalField
    }

    def Gastos_adicionales(self, obj):
        formateo = "💲{:,.0f}".format(obj.GASTOS_ADICIONALES)
        return formateo
    
    def Presupuesto(self,obj):
        presup = obj.pk
        return f'# {presup}'

    def Precio(self, obj):
        formateo = "💲{:,.0f}".format(obj.PRECIO_VENTA)
        return formateo

    def Ultima_Actualizacion(self, obj): 
        hora_buenos_aires = pytz.timezone('America/Argentina/Buenos_aires')
        fecha_hora = obj.ULTIMA_ACTUALIZACION.astimezone(hora_buenos_aires)
        formateo = fecha_hora.strftime("%H:%M %d/%m/%Y")

        formateo = "📆 " +formateo
        return formateo

    def Estado(self,obj):
        if obj.ESTADO=="Pendiente":
            return "🔴 Pendiente"
        elif obj.ESTADO=="Aceptado":
            return "🟢 Aceptado"
        else:
            return "🔵 Entregado"

    def Fecha_de_entrega(self, obj):
        formateo = "📆 " + str(obj.FECHA_ENTREGA)
        return formateo
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if 'entregado' in request.GET:
            return queryset  # No aplicar ningún filtro si el filtro 'entregado' está activo
        else:
            return queryset.exclude(ESTADO='Entregado')


