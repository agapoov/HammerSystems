import time

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AuthCode, User
from .serializers import (AuthCodeSerializer, AuthSerializer,
                          InviteCodeSerializer, ProfileSerializer)

from .schemas import (
    auth_request_schema, auth_response_schema_201, auth_response_schema_400,
    verify_request_schema, verify_response_schema_200, verify_response_schema_400,
    profile_get_response_schema, invite_post_request_schema,
    invite_post_response_schema_200, invite_post_response_schema_400
)


class AuthView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=auth_request_schema,
        responses={
            201: auth_response_schema_201,
            400: auth_response_schema_400,
        }
    )
    def post(self, request):
        serializer = AuthSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            user, _ = User.objects.get_or_create(phone_number=phone_number)
            AuthCode.objects.create(user=user)
            request.session['phone_number'] = phone_number

            time.sleep(2)

            return Response({'message': 'Код отправлен'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthVerifyCodeView(APIView):

    @swagger_auto_schema(
        request_body=verify_request_schema,
        responses={
            200: verify_response_schema_200,
            400: verify_response_schema_400,
        }
    )
    def post(self, request):
        serializer = AuthCodeSerializer(data=request.data)
        if serializer.is_valid():

            phone_number = request.session.get('phone_number')
            code = serializer.validated_data['code']
            if not phone_number:
                return Response({'message': 'Сессия истекла, попробуйте заново'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(phone_number=phone_number)
                auth_code = AuthCode.objects.get(user=user, code=code)
            except (User.DoesNotExist, AuthCode.DoesNotExist):
                return Response({'message': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)

            auth_code.delete()

            user.invite_code = User.generate_invite_code()
            user.save()

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'message': f'Аутентификация прошла успешно. JWT токены созданы',
                'invite_code': f'{user.invite_code}',
                'access_token': str(access_token),
                'refresh_token': str(refresh)}
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: profile_get_response_schema
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=invite_post_request_schema,
        responses={
            200: invite_post_response_schema_200,
            400: invite_post_response_schema_400,
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = InviteCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_code = serializer.validated_data['invite_code']

        if request.user.activated_code:
            return Response({'message': 'Вы уже активировали код'}, status=status.HTTP_400_BAD_REQUEST)

        if invite_code == str(request.user.invite_code):
            return Response({'message': 'Нельзя активировать свой же код'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.activated_code = invite_code
        request.user.save()

        return Response({'message': 'Инвайт-код успешно активирован'}, status=status.HTTP_200_OK)
