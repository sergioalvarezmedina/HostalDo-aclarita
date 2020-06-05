# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HAsistente(models.Model):
    asistente_id = models.FloatField(primary_key=True)
    contenido = models.CharField(max_length=4000)
    vigencia_flag = models.FloatField()
    modulo = models.ForeignKey('HModulo', models.DO_NOTHING)
    vigencia = models.FloatField()

    class Meta:
        managed = False
        db_table = 'h_asistente'


class HComuna(models.Model):
    comuna_id = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey('HRegion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'h_comuna'


class HHabitacion(models.Model):
    habitacion_id = models.FloatField(primary_key=True)
    rotulo = models.CharField(max_length=20, blank=True, null=True)
    habitacion_tipo = models.ForeignKey('HHabitacionTipo', models.DO_NOTHING)
    habitacion_estado = models.ForeignKey('HHabitacionEstado', models.DO_NOTHING)
    camas = models.CharField(max_length=4000, blank=True, null=True)
    accesorios = models.CharField(max_length=4000, blank=True, null=True)
    precio = models.FloatField()
    vigencia = models.FloatField()

    class Meta:
        managed = False
        db_table = 'h_habitacion'


class HHabitacionEstado(models.Model):
    habitacion_estado_id = models.FloatField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    usable = models.FloatField()

    class Meta:
        managed = False
        db_table = 'h_habitacion_estado'


class HHabitacionTipo(models.Model):
    habitacion_tipo_id = models.FloatField(primary_key=True)
    descriptor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_habitacion_tipo'


class HHuespedHabitacion(models.Model):
    huesped_habitacion = models.OneToOneField('HOcHuesped', models.DO_NOTHING, primary_key=True)
    huesped = models.ForeignKey('HOcHuesped', models.DO_NOTHING, related_name="+")
    habitacion = models.ForeignKey(HHabitacion, models.DO_NOTHING, related_name="+")

    class Meta:
        managed = False
        db_table = 'h_huesped_habitacion'
        unique_together = (('huesped_habitacion', 'huesped', 'habitacion'),)


class HMenu(models.Model):
    menu_id = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=100)
    registro_fecha = models.DateField()
    vigencia = models.FloatField()

    class Meta:
        managed = False
        db_table = 'h_menu'


class HMinuta(models.Model):
    minuta_id = models.FloatField(primary_key=True)
    fecha = models.FloatField()
    plato = models.ForeignKey('HPlato', models.DO_NOTHING)
    menu = models.ForeignKey(HMenu, models.DO_NOTHING)
    vigencia = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'h_minuta'


class HModulo(models.Model):
    modulo_id = models.FloatField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'h_modulo'


class HOcHuesped(models.Model):
    oc_huesped_id = models.FloatField(primary_key=True)
    orden_compra = models.ForeignKey('HOrdenCompra', models.DO_NOTHING)
    persona = models.ForeignKey('HPersona', models.DO_NOTHING)
    recepcion_flag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_oc_huesped'
        unique_together = (('oc_huesped_id', 'orden_compra'),)


class HOcItems(models.Model):
    op_item_id = models.FloatField(primary_key=True)
    cantidad = models.FloatField()
    orden_pedido = models.ForeignKey('HOrdenPedido', models.DO_NOTHING)
    proveedor_documento_numero = models.CharField(max_length=100, blank=True, null=True)
    proveedor_entrega_fecha = models.DateField(blank=True, null=True)
    producto = models.ForeignKey('HProducto', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'h_oc_items'


class HOrdenCompra(models.Model):
    orden_compra_id = models.FloatField(primary_key=True)
    servicio_inicio = models.DateField()
    servicio_fin = models.DateField()
    organismo = models.ForeignKey('HOrganismo', models.DO_NOTHING, related_name="+")
    revision_fecha = models.DateField(blank=True, null=True)
    revision_usuario = models.ForeignKey('HUsuario', models.DO_NOTHING, related_name="+")
    visacion_fecha = models.DateField(blank=True, null=True)
    visacion_usuario = models.ForeignKey('HUsuario', models.DO_NOTHING, related_name="+")
    factura_numero = models.CharField(max_length=100, blank=True, null=True)
    factura_emision_flag = models.BooleanField(blank=True, null=True)
    factura_usuario = models.ForeignKey('HUsuario', models.DO_NOTHING, related_name="+")
    usuario = models.ForeignKey('HUsuario', models.DO_NOTHING, related_name="+")
    registro_fecha = models.DateField()
    nulo_fecha = models.DateField(blank=True, null=True)
    nulo_usuario = models.ForeignKey('HUsuario', models.DO_NOTHING, related_name="+")

    class Meta:
        managed = False
        db_table = 'h_orden_compra'


class HOrdenPedido(models.Model):
    orden_pedido_id = models.FloatField(primary_key=True)
    proveedor_organismo = models.ForeignKey('HOrganismo', models.DO_NOTHING, related_name="+")
    documento_numero = models.CharField(max_length=100, blank=True, null=True)
    documento_fecha = models.DateField(blank=True, null=True)
    observacion = models.CharField(max_length=4000, blank=True, null=True)
    usuario = models.ForeignKey('HUsuario', models.DO_NOTHING, related_name="+")
    registro_fecha = models.DateField()
    revision_fecha = models.DateField(blank=True, null=True)
    revision_usuario_id = models.FloatField(blank=True, null=True)
    nulo_fecha = models.DateField(blank=True, null=True)
    nulo_usuario = models.ForeignKey('HUsuario', models.DO_NOTHING, related_name="+")

    class Meta:
        managed = False
        db_table = 'h_orden_pedido'


class HOrganismo(models.Model):
    organismo_id = models.FloatField(primary_key=True)
    razon_social = models.CharField(max_length=1000)
    rut = models.CharField(max_length=20, blank=True, null=True)
    nombre_fantasia = models.CharField(max_length=1000, blank=True, null=True)
    giro = models.CharField(max_length=1000, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    cuenta_datos = models.CharField(max_length=2000, blank=True, null=True)
    persona = models.ForeignKey('HPersona', models.DO_NOTHING)
    usuario = models.ForeignKey('HUsuario', models.DO_NOTHING)
    registro_fecha = models.DateField()
    proveedor_flag = models.FloatField(blank=True, null=True)
    comuna = models.ForeignKey(HComuna, models.DO_NOTHING)
    vigencia = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'h_organismo'


class HPersona(models.Model):
    persona_id = models.FloatField(primary_key=True)
    rut = models.CharField(max_length=30, blank=True, null=True)
    nombres = models.CharField(max_length=100)
    paterno = models.CharField(max_length=100, blank=True, null=True)
    materno = models.CharField(max_length=50, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_persona'


class HPersonaDireccion(models.Model):
    persona_direccion_id = models.FloatField(primary_key=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    persona = models.ForeignKey(HPersona, models.DO_NOTHING)
    usuario = models.ForeignKey('HUsuario', models.DO_NOTHING)
    registro_fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_persona_direccion'


class HPlato(models.Model):
    plato_id = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ingredientes = models.CharField(max_length=1000, blank=True, null=True)
    valor = models.FloatField()
    registro_fecha = models.DateField()
    vigencia = models.FloatField()

    class Meta:
        managed = False
        db_table = 'h_plato'


class HProducto(models.Model):
    producto_id = models.FloatField(primary_key=True)
    codigo = models.CharField(max_length=100)
    producto_familia = models.ForeignKey('HProductoFamilia', models.DO_NOTHING)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000, blank=True, null=True)
    costo_ultimo = models.FloatField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    usuario = models.ForeignKey('HUsuario', models.DO_NOTHING)
    registro_fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'h_producto'


class HProductoFamilia(models.Model):
    producto_familia_id = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_producto_familia'


class HRegion(models.Model):
    region_id = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    orden = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_region'


class HUsuario(models.Model):
    usuario_id = models.FloatField(primary_key=True)
    persona = models.ForeignKey(HPersona, models.DO_NOTHING)
    username = models.CharField(max_length=100, blank=True, null=True)
    contrasena = models.CharField(max_length=1000)
    registro_fecha = models.DateField()
    usuario_perfil = models.ForeignKey('HUsuarioPerfil', models.DO_NOTHING)
    vigencia = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'h_usuario'


class HUsuarioPerfil(models.Model):
    usuario_perfil_id = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'h_usuario_perfil'
