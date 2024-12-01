from rest_framework import serializers

from .models import AuthCode, User


class AuthCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthCode
        fields = ('code',)


class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class ProfileSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()
    activated_code = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_code', 'referred_users']

    def get_referred_users(self, obj):
        referred_users = User.objects.filter(activated_code=obj.invite_code)
        return [user.phone_number for user in referred_users]


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate_invite_code(self, value):
        if not User.objects.filter(invite_code=value).exists():
            raise serializers.ValidationError('Инвайт-код не найден.')
        return value
