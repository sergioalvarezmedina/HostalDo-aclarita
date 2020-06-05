from django.contrib import admin
from .models import HRegion, HComuna, HModulo, HAsistente

admin.site.register(HComuna)
admin.site.register(HAsistente)
admin.site.register(HModulo)
