from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import Form, Router

from auth.jwt import create_token

api_auth = Router()


@api_auth.post('login')
def login(request, username: str = Form(...), password: str = Form(...)):
    user = get_object_or_404(User, username=username)
    if check_password(password, user.password):
        return create_token(user.id)
