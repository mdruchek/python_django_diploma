import json
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction

from .models import (
    UserRole,
    UserProfile,
    UserAvatar
)


def sign_in(request: HttpRequest) -> HttpResponse:
    """
    Функция авторизации
    """

    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user: User = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        return HttpResponse(status=401)


def sign_out(request: HttpRequest) -> HttpResponse:
    """
    Функция выхода
    """

    logout(request)
    return HttpResponse(status=200)


def sign_up(request: HttpRequest) -> HttpResponse:
    """
    Функция регистрации
    """

    if request.method == 'POST':
        with transaction.atomic():
            data = json.loads(request.body)
            name = data['username']
            username = data['username']
            password = data['password']
            user = User(first_name=name, username=username)
            user.set_password(password)

            try:
                user.full_clean()
            except ValidationError:
                return HttpResponse(status=401)

            try:
                user.save()
            except IntegrityError:
                return HttpResponse(status=401)

            user_role = UserRole.objects.get(title='Покупатель')
            UserProfile.objects.create(user=user, role=user_role)
            UserAvatar.objects.create(user=user)
        login(request, user)
        return HttpResponse(status=201)
