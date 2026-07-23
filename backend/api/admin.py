from django.contrib import admin
from api.models import Personaje, Beyblade, FusionWheel, ClearWheel, SpinTrack, Tip, Tipe, usuarioBeyblade, Chat, chatUsuario, Mensaje

@admin.register(Personaje)
class PersonajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'altura', 'peso', 'get_beyblades_count')
    search_fields = ('nombre', 'historia', 'personalidad')
    filter_horizontal = ('beyblades',)

    def get_beyblades_count(self, obj):
        return obj.beyblades.count()
    get_beyblades_count.short_description = 'Cant. Beyblades'


@admin.register(Beyblade)
class BeybladeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'season', 'color')
    search_fields = ('nombre', 'season')
    list_filter = ('season', 'tipe')


admin.site.register(FusionWheel)
admin.site.register(ClearWheel)
admin.site.register(SpinTrack)
admin.site.register(Tip)
admin.site.register(Tipe)
admin.site.register(usuarioBeyblade)
admin.site.register(Chat)
admin.site.register(chatUsuario)
admin.site.register(Mensaje)
