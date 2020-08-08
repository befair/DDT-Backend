from django.urls import include, path
from .api import router

urlpatterns = [
    path('', include(router.urls)),
]
