from django.db import models
from django.contrib.auth.models import User

class FusionWheel(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(default="",blank=False)
    photo = models.ImageField()

    def __str__(self):
        return f"{self.nombre}"
class ClearWheel(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(default="",blank=False)
    photo = models.ImageField()

    def __str__(self):
        return f"{self.nombre}"

class SpinTrack(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(default="",blank=False)
    photo = models.ImageField()

    def __str__(self):
        return f"{self.nombre}"
class Tip(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(default="",blank=False)
    photo = models.ImageField()

    def __str__(self):
        return f"{self.nombre}"
class Tipe(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(default="",blank=False)
    photo = models.ImageField()

    def __str__(self):
        return f"{self.nombre}"

class Beyblade(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(default="",blank=False)
    fusion_wheel = models.ForeignKey(FusionWheel, on_delete=models.CASCADE, related_name="beyblade")
    clear_wheel = models.ForeignKey(ClearWheel, on_delete=models.CASCADE, related_name="beyblade")
    spin_track = models.ForeignKey(SpinTrack, on_delete=models.CASCADE, related_name="beyblade")
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, related_name="beyblade")
    tipe = models.ForeignKey(Tipe, on_delete=models.CASCADE, related_name="beyblade")
    color = models.CharField(default="", max_length=100, null=False)
    photo = models.ImageField(upload_to="media/", blank=True, null=True)
    sistem = models.CharField(default="", max_length=200, null=False)
    season = models.CharField(default="", max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.nombre} - {self.tipe}"
    

class Chat(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"nombre: {self.nombre}"

class Mensaje(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes")
    id_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="mensajes")
    texto = models.CharField(max_length=1500, blank=True, null=True)
    archivo = models.FileField(upload_to="chat_archivos/",blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"usuario - {self.id_usuario.first_name}"


class chatUsuario(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('id_chat', 'id_usuario')

    def __str__(self):
        return f"Usuario: {self.id_usuario.first_name}, chat: {self.id_chat.nombre}"

class usuarioBeyblade(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Usuario")
    id_bb = models.ForeignKey(Beyblade, on_delete=models.CASCADE, related_name="Beyblade")
    precio = models.IntegerField()

    def __str__(self):
        return f"Usuario: {self.id_usuario.first_name}, Beyblade: {self.id_bb.nombre}, Precio: {self.precio}"


class Personaje(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    altura = models.CharField(max_length=50, default="", blank=True)
    peso = models.CharField(max_length=50, default="", blank=True)
    personalidad = models.TextField(default="", blank=True)
    historia = models.TextField(default="", blank=True)
    foto = models.ImageField(upload_to="personajes/", blank=True, null=True)
    beyblades = models.ManyToManyField(Beyblade, related_name="personajes", blank=True)

    def __str__(self):
        return f"{self.nombre}"


class Reporte(models.Model):
    ESTADOS = (
        ('pendiente', 'En Revisión'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reportes")
    tipo = models.CharField(max_length=50, default="beyblade")  # 'beyblade' o 'personaje'
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(default="", blank=True)
    opcional = models.TextField(default="", blank=True)  # Info adicional
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    created_at = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Reporte ({self.tipo}) - {self.nombre} - {self.get_estado_display()}"



