from drf_yasg import openapi

# Request AuthView
auth_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example='79087777777'),
    },
    required=['phone_number']
)

# Response AuthView
auth_response_schema_201 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Код отправлен'),
    }
)

auth_response_schema_400 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example='Некорректный номер телефона'),
    }
)

# Request AuthVerifyCodeView
verify_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'code': openapi.Schema(type=openapi.TYPE_INTEGER, example=1234),
    },
    required=['code']
)

# Response AuthVerifyCodeView
verify_response_schema_200 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Аутентификация прошла успешно. JWT токены созданы'),
        'invite_code': openapi.Schema(type=openapi.TYPE_STRING, example='987654'),
        'access_token': openapi.Schema(type=openapi.TYPE_STRING, example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'),
        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, example='dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4uLi4u'),
    }
)

verify_response_schema_400 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Неверный код'),
    }
)

# GET response ProfileView
profile_get_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example='79087777777'),
        'invite_code': openapi.Schema(type=openapi.TYPE_STRING, example='777777'),
    }
)

invite_post_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'invite_code': openapi.Schema(type=openapi.TYPE_STRING, example='123456'),
    },
    required=['invite_code']
)

invite_post_response_schema_200 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Инвайт-код успешно активирован'),
    }
)

invite_post_response_schema_400 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Нельзя активировать свой же код'),
    }
)
