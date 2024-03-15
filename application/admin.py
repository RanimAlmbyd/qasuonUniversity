from django.contrib import admin
from .models import User,Department,AddressOne,AddressTwo,Student,Empolyee,Buses,Lines,Trips
# Register your models here.
admin.site.register(User)
admin.site.register(Department)
admin.site.register(AddressOne)
admin.site.register(AddressTwo)
admin.site.register(Student)
admin.site.register(Empolyee)
admin.site.register(Lines)
admin.site.register(Trips)
admin.site.register(Buses)