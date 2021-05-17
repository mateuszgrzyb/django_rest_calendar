from rest_framework.permissions import IsAuthenticated


class EventPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view)
