"""
URL configuration for iot_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from application.views import get_all_services, get_waiting_time, get_service_providers, get_all_service_providers, \
    get_provider_waiting_time

urlpatterns = [
    path('admin/', admin.site.urls),
    path("services/<str:category>/",get_all_services),
    path("service/<int:service_id>/",get_waiting_time),
    path("service/provider/{int:service_provider_id}/",get_service_providers),
    path("service/provider/",get_all_service_providers),
    path("service/<int:last_frame>/<int:service_provider>/",get_provider_waiting_time),
]
