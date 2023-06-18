
import datetime
from urllib import request
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import messages,admin



UnidadDeMedida = [
    ("Unidades","Unidades"),
    ("Kilogramos","Kilogramos"),
    ("Litros","Litros"),
    ("Onzas","Onzas"),
    ("Libras","Libras"),
]

Estado = [
    ("Pendiente","Pendiente"),
    ("Aceptado","Aceptado"),
    ("Entregado","Entregado"),
]

UnidadDeMedidaSalida = [
    ("Unidades","Unidades"),
    ("Gramos","Gramos"),
    ("Mililitros","Mililitros"),
    ("Onzas","Onzas"),
    ("Libras","Libras"),
]

class Cliente(models.Model):
    NUMERO_CLIENTE= models.AutoField(primary_key=True)
    NOMBRE_Y_APELLIDO=models.CharField(max_length=120,null=False,blank=False)
    DIRECCION=models.CharField(max_length=255,null=False,blank=False)
    EMAIL=models.CharField(max_length=120,null=True,blank=True)
    TELEFONO =models.CharField(max_length=15,null=False,blank=False)
                   
    def __str__(self):
        return self.NOMBRE_Y_APELLIDO

class Proveedor(models.Model):
    EMPRESA=models.CharField(max_length=120,null=False,blank=False) 
    NOMBRE=models.CharField(max_length=120,null=False,blank=False) 
    DIRECCION=models.CharField(max_length=120,null=True,blank=True)
    EMAIL=models.EmailField(null=True,blank=True)
    TELEFONO=models.CharField(max_length=120,null=False,blank=False)

    def __str__(self):
        return self.EMPRESA
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural ='Proveedores' 

class Insumo(models.Model):
    PRODUCTO = models.CharField(max_length=120, null=False, blank=False,unique=True)
    PROVEEDOR=models.ForeignKey(Proveedor,on_delete=models.CASCADE,blank=True,null=True)
    DETALLE = models.TextField(null=True, blank=True)
    STOCK = models.IntegerField(default=0,null=True,blank=True)
    CANTIDAD = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    UNIDAD_MEDIDA_COMPRA = models.CharField(max_length=10, choices=UnidadDeMedida, default="Unidades", null=False, blank=False)
    PRECIO_COMPRA = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    UNIDAD_MEDIDA_USO = models.CharField(max_length=10, choices=UnidadDeMedidaSalida, default="Unidades", null=False, blank=False)
    COSTO_UNITARIO = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural ='Materiales' 

    def __str__(self):
        return f'{self.PRODUCTO} | ${self.COSTO_UNITARIO}'

    def clean(self):

        if self.UNIDAD_MEDIDA_COMPRA == "Unidades" and self.UNIDAD_MEDIDA_USO != "Unidades":
            raise ValidationError("Si selecciona 'Unidades' en el campo Unidad de compra, solo puede utilizar 'Unidades' como Unidad de Uso.")
        elif self.UNIDAD_MEDIDA_COMPRA == "Kilogramos" and self.UNIDAD_MEDIDA_USO != "Kilogramos" and self.UNIDAD_MEDIDA_USO != "Gramos":
            raise ValidationError("Si selecciona 'Kilogramos' en el campo Unidad de compra, solo puede seleccionar 'Gramos' como Unidad de Uso.")
        elif self.UNIDAD_MEDIDA_COMPRA == "Litros" and self.UNIDAD_MEDIDA_USO != "Litros" and self.UNIDAD_MEDIDA_USO != "Mililitros":
            raise ValidationError("Si selecciona 'Litros' en el campo Unidad de compra, solo puede seleccionar 'Mililitros' como Unidad de Uso.")
        elif self.UNIDAD_MEDIDA_COMPRA == "Onzas" and self.UNIDAD_MEDIDA_USO != "Onzas":
            raise ValidationError("Si selecciona 'Onzas' en el campo Unidad de compra, solo puede seleccionar 'Onzas'")
        elif self.UNIDAD_MEDIDA_COMPRA == "Libras" and self.UNIDAD_MEDIDA_USO != "Libras" and self.UNIDAD_MEDIDA_USO != "Onzas":
            raise ValidationError("Si selecciona 'Libras' en el campo Unidad de compra, solo puede seleccionar 'Libras' u 'Onzas' como Unidad de Uso.")
    
        super().clean()

    def save(self, *args, **kwargs):
        if self.PRECIO_COMPRA > 0:
            if str(self.UNIDAD_MEDIDA_COMPRA) == str(self.UNIDAD_MEDIDA_USO):
                self.COSTO_UNITARIO = self.PRECIO_COMPRA / self.CANTIDAD
            elif str(self.UNIDAD_MEDIDA_COMPRA) == "Kilogramos" or str(self.UNIDAD_MEDIDA_COMPRA) == "Litros":
                self.COSTO_UNITARIO = self.PRECIO_COMPRA / self.CANTIDAD / 1000
            elif str(self.UNIDAD_MEDIDA_COMPRA) == "Libras":
                self.COSTO_UNITARIO = self.PRECIO_COMPRA / self.CANTIDAD / 16

        super(Insumo, self).save(*args, **kwargs)

class gastosAdicionales(models.Model):
    PRODUCTO  = models.CharField(max_length=255,blank=False,null=False,unique=True)

    def __str__(self):
        return self.PRODUCTO
    
    
    

class Receta(models.Model):
    CODIGO=models.AutoField(primary_key=True)
    ESTADO= models.CharField(choices=Estado,max_length=20,default="Pendiente",blank=False,null=False)
    CLIENTE = models.ForeignKey(Cliente, on_delete=models.CASCADE,blank=True,null=True)
    FECHA_ENTREGA = models.DateField(null=True, blank=False)
    NOMBRE=models.CharField(verbose_name='PRODUCTO',max_length=120,null=False,blank=False) 
    DETALLE=models.TextField(null=True,blank=True) 
    DIAS_DE_TRABAJO=models.DecimalField(max_digits=4,decimal_places=2,default=1,blank=False,null=False)
    RENTABILIDAD = models.DecimalField(max_digits=12,decimal_places=2,default=0,blank=True,null=True)
    PRECIO_VENTA = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    ADICIONALES = models.ManyToManyField(gastosAdicionales, blank=True)
    INGREDIENTES = models.ManyToManyField(Insumo)
    COSTO_FINAL = models.DecimalField(max_digits=22,decimal_places=2,default=0,blank=True,null=True)
    VALIDO_HASTA = models.DateField(blank=True,null=True)
    ULTIMA_ACTUALIZACION = models.DateTimeField(blank=True,null=True,auto_now=True)
    ARTICULOS = models.TextField(blank=True,null=True)
    GASTOS_ADICIONALES = models.DecimalField(verbose_name="TOTAL ADICIONALES",max_digits=22,decimal_places=2,default=0,blank=True,null=True)

    def __str__(self):
        return f'{self.NOMBRE} - $ {self.PRECIO_VENTA}'
    
    def clean(self):
        if self.DIAS_DE_TRABAJO <= 0:
            raise ValidationError("La cantidad de dias de trabajo debe ser superior a 0.")
        if self.pk:
            if self.ESTADO == "Entregado" or self.ESTADO == "Aceptado":
                raise ValidationError("No se puede modificar un pedido Aceptado/Entregado")
        super().clean()

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural ='Presupuestos' 

    def save(self, *args, **kwargs):
        
        if not self.pk:
            super().save(*args, **kwargs)
            
        costo_receta = 0
        self.COSTO_FINAL = 0

        #Capturar el costo de los insumos
        for ingrediente in self.ingredientereceta_set.all():
            costo_receta += ingrediente.cantidad * ingrediente.producto.COSTO_UNITARIO

        #Capturar el costo de los gastos adicionales
        total_gastos_adicionales = 0
        for gasto in self.adicionalreceta_set.all():
            total_gastos_adicionales += gasto.precio

        self.GASTOS_ADICIONALES = float(total_gastos_adicionales)

        #Capturar el costo de los dias de trabajo
        dias_trabajo = self.DIAS_DE_TRABAJO
        gastos_fijos = gastosFijos.objects.aggregate(models.Sum('TOTAL'))['TOTAL__sum'] or 0
        costo_diario = gastos_fijos / 25

        #Capturar costo final de la receta
        costo_final = float(costo_diario) * float(dias_trabajo)


        self.COSTO_FINAL = costo_final + float(total_gastos_adicionales)
        self.PRECIO_VENTA = float(costo_final) + float(costo_receta) + float(total_gastos_adicionales) #costo con todos los insumos,gastos y dias de trabajo

        if costo_final > 0:
            rentabilidad = float(((self.PRECIO_VENTA - costo_final) / costo_final) * 100)
            self.RENTABILIDAD = rentabilidad

        insumos_receta = self.ingredientereceta_set.all()

        self.ARTICULOS = ", ".join([f"{ingrediente.producto.PRODUCTO.split(' | $')[0]} ({ingrediente.cantidad})" for ingrediente in insumos_receta])

        super().save(*args, **kwargs)



class ingredientereceta(models.Model):

    producto  = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    costo_unitario = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    medida_uso = models.CharField(max_length=255,blank=True,null=True)
    subtotal = models.DecimalField(max_digits=20,decimal_places=2,default=0,blank=False,null=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural ='Productos incluidos en presupuesto' 

    def __str__(self):
        return self.receta.NOMBRE
    
    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("Por favor ingrese una cantidad superior a 0.")
        super().clean()

    def save(self, *args, **kwargs):
        self.costo_unitario = self.producto.COSTO_UNITARIO
        self.medida_uso = self.producto.UNIDAD_MEDIDA_USO
        self.subtotal = self.costo_unitario * self.cantidad
        super().save(*args, **kwargs)


class adicionalreceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    adicional  = models.ForeignKey(gastosAdicionales, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)


class gastosFijos(models.Model):
    DETALLE  = models.CharField(max_length=255,blank=False,null=False)
    TOTAL = models.DecimalField(max_digits=20, decimal_places=2,blank=False,null=False)
    
    def clean(self):
        if self.TOTAL and self.TOTAL < 0:
            raise ValidationError("Por favor ingrese un monto superior a 0.")
        super().clean()

    class Meta:
        verbose_name = 'Gasto fijo'
        verbose_name_plural ='Gastos fijos' 

class PedidosEntregados(models.Model):
    CODIGO = models.CharField(max_length=10)
    CLIENTE = models.ForeignKey(Cliente, on_delete=models.CASCADE,blank=True,null=True)
    FECHA_ENTREGA = models.DateField(null=True, blank=True,default=datetime.date.today)
    ARTICULO=models.TextField() 
    DETALLE=models.CharField(max_length=120,null=True,blank=True) 
    DIAS_DE_TRABAJO=models.DecimalField(max_digits=4,decimal_places=2,default=1,blank=False,null=False)
    COSTO_RECETA = models.DecimalField(verbose_name="Costo articulos",max_digits=22,decimal_places=2,default=0,blank=True,null=True)
    MANO_DE_OBRA = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    PRECIO = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    INGREDIENTES = models.TextField(blank=True,null=True)
    GASTOS_ADICIONALES = models.DecimalField(verbose_name="TOTAL ADICIONALES",max_digits=22,decimal_places=2,default=0,blank=True,null=True)
    
