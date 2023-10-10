from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'trucks', views.TruckViewSet)
router.register(r'cargos', views.CargoViewSet)

urlpatterns = router.urls
