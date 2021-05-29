from django.urls import include, path

from .services.ecs.router import router as ecs_router

urlpatterns = [
    path('', include(ecs_router.urls)),
]
