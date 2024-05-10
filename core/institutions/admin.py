from django.contrib import admin

# Register your models here.
from .models import Institution, Domain, Course, Instructor, TeachingAssistant, UserEmail


admin.site.register(Institution)
admin.site.register(Domain)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(TeachingAssistant)
admin.site.register(UserEmail)
