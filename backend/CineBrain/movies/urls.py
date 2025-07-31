from django.urls import path, include
from .views import MoviesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'all', MoviesViewSet, basename='movie')

urlpatterns = router.urls