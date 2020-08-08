from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'ddt', views.DDTViewSet)
router.register(r'user', views.UserViewSet)
