from django.contrib import admin
from django.urls import path
from blog.views import blog
from auth.views import api_auth
from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/", blog)
api.add_router("auth/", api_auth)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls),
]
