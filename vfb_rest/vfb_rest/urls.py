from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from vfb_server import views

router = DefaultRouter()
router.register(r'dataset', views.datasetViewSet)
router.register(r'neuron', views.neuronViewSet)
router.register(r'person', views.personViewSet)


schema_view = get_swagger_view(title='Snippets API')

urlpatterns = [
    url('^$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    #url(r'^requestid/', views.requestId),
]
