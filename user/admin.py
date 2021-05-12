from django.contrib import admin
from user.models import User, Manager, Participant, Owner

admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Participant)
admin.site.register(Owner)
