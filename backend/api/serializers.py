from rest_framework import serializers
from api.models import Chat, chatUsuario, Mensaje
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.serializers import RegisterSerializer


class MensajeSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source="id_usuario.username", read_only=True)

    class Meta:
        model= Mensaje
        fields = ["id", "usuario", "texto", "archivo", "url", "created_at"]
    
    def get_archivo(self, obj):
        return obj.archivo.url if obj.archivo else None


class MensajeCreateSerializer(serializers.Serializer):
    id_chat = serializers.IntegerField()
    texto = serializers.CharField(required=False, allow_blank=True)
    archivo = serializers.FileField(required=False, allow_null=True)
    url = serializers.URLField(required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context.get("user")
        if user is None:
            raise serializers.ValidationError("Usuario no proporcionado")
        
        texto = attrs.get("texto")
        archivo = attrs.get("archivo")
        url = attrs.get("url")

        if not texto and not archivo and not url:
            raise serializers.ValidationError("Debe enviar texto, enlace, o archivo")

        try:
            chat = Chat.objects.get(id=attrs["id_chat"])
        except Chat.DoesNotExist:
            raise serializers.ValidationError({"id_chat": "El chat no existe."})
        
        if not chatUsuario.objects.filter(id_chat=chat, id_usuario=user).exists():
            raise serializers.ValidationError("El usuario no pertenece al chat")
        
        attrs["chat_obj"] = chat
        attrs["user_obj"] = user
        return attrs


class ChatDetalleSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=100)
    usuarios = serializers.SerializerMethodField()
    mensajes = MensajeSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "nombre", "usuarios", "mensajes"]

    def get_usuarios(self, obj):
        qs = chatUsuario.objects.filter(id_chat=obj).select_related("id_usuario")
        return [
            {
                "id": cu.id_usuario.id,
                "username": cu.id_usuario.username
            }
            for cu in qs
        ]

class ChatCreationSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    usuario1 = serializers.IntegerField()
    usuario2 = serializers.IntegerField()

    def validate_nombre(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("El nombre debe tener al menos 6 caracteres.")
        return value

    def validate(self, attrs):
        # Validar existencia de usuarios
        try:
            attrs["usuario_creador_obj"] = User.objects.get(id=attrs["usuario1"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"usuario1": "El usuario creador no existe."})

        try:
            attrs["usuario_seleccionado_obj"] = User.objects.get(id=attrs["usuario2"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"usuario2": "El usuario seleccionado no existe."})

        return attrs
    

class JWTSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.get("user")
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }
    
    def get_token(self, obj):
        user = obj.get("user")
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
    
class UserRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["first_name"] = self.validated_data.get("first_name", "")
        data["last_name"] = self.validated_data.get("first_name", "")
        return data
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.save()
        return user