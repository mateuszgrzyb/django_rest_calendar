from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meeting.urls import routes as meeting_routes
from location.urls import routes as location_routes
from user.urls import routes as user_routes

router = DefaultRouter()
for router_data in meeting_routes + location_routes + user_routes:
    router.register(*router_data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include(router.urls)),
]
