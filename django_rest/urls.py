from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meeting.urls import routes as meeting_routes
from location.urls import routes as location_routes

router = DefaultRouter()
for (route, view) in meeting_routes + location_routes:
    router.register(route, view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
