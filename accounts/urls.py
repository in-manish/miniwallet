from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^obtain-token$', view=views.ObtainTokenAPIView.as_view(), name='obtain token'),

    url(r'^register$', view=views.ObtainTokenAPIView.as_view(), name='obtain token'),
]
