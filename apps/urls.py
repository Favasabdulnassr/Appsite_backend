from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'apps',views.AndroidAppViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'tasks', views.CompletedTaskViewSet)


urlpatterns = [
    path('',include(router.urls))
]


