from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'detail': 'Пожалуйста, укажите имя пользователя и пароль'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({
            'detail': 'Неверное имя пользователя или пароль'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Получаем или создаем токен
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'username': user.username
    })

@api_view(['POST'])
def logout(request):
    try:
        # Удаляем токен для текущего пользователя
        request.user.auth_token.delete()
        return Response({'detail': 'Успешный выход из системы'})
    except (AttributeError, ObjectDoesNotExist):
        return Response({'detail': 'Неверный токен'}, status=status.HTTP_400_BAD_REQUEST)
