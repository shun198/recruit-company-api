from django.urls import path, include
from rest_framework_nested import routers
from .views import CompanyViewSet


router = routers.DefaultRouter()
# basenameを指定することでテストする際に参照できるようになる
router.register(r"companies",CompanyViewSet,basename="companies")

urlpatterns = [
    path("",include(router.urls))
]


