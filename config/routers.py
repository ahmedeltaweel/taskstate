from rest_framework.routers import DefaultRouter

from taskstate.tasks.views import TasksViewSet

router_v1 = DefaultRouter('v1')
router_v1.register('tasks', TasksViewSet)


urlpatterns = router_v1.urls
