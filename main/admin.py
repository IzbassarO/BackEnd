from django.contrib import admin
from .models import Main
from .models import Student
from .models import Department
from.models import Course
from .models import FacultyMember
from .models import NewsArticle

# Register your models here.

admin.site.register(Main)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(FacultyMember)
admin.site.register(NewsArticle)