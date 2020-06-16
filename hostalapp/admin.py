from django.contrib import admin
from .models import HRegion, HComuna, HModulo, HAsistente

class AsistenteAdmin(admin.ModelAdmin):
	readonly_fields = ('vigencia_flag','vigencia')
	list_display = ('asistente_id','contenido',)
	search_fields = ('asistente_id','contenido')

class ComunasAdmin(admin.ModelAdmin):
	list_display = ('comuna_id','nombre')
	search_fields = ('region','nombre')

class ModulosAdmin(admin.ModelAdmin):
	list_display = ('modulo_id','descripcion')
	search_fields = ('modulo_id','descripcion')

admin.site.register(HAsistente, AsistenteAdmin)
admin.site.register(HComuna, ComunasAdmin)
admin.site.register(HModulo, ModulosAdmin)
