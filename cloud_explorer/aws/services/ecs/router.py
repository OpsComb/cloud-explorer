from aws.views import ECSClusterViewSet, ECSServiceViewSet, ECSTaskViewSet
from rest_framework_nested import routers


def __get_all_routes():
    router = routers.SimpleRouter()

    router.register(r'clusters', ECSClusterViewSet, basename='clusters')

    cluster_router = routers.NestedSimpleRouter(router, r'clusters', lookup='cluster')
    cluster_router.register(r'services', ECSServiceViewSet, basename='services')

    service_router = routers.NestedSimpleRouter(cluster_router, r'services', lookup='services')

    cluster_router.register(r'tasks', ECSTaskViewSet, basename='tasks')

    combined_router = routers.SimpleRouter()
    for router in (router, cluster_router, service_router):
        combined_router.registry.extend(router.registry)

    return combined_router


router = __get_all_routes()
