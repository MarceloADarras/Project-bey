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


# Create your models here.
