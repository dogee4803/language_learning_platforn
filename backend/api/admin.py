from django.contrib import admin

# Register your models here.
from .models import Customer, Teacher, Language, Course, CustomerCourse, TeacherCourse, TeacherLanguage

# Регистрация моделей
admin.site.register(Customer)
admin.site.register(Teacher)
admin.site.register(Language)
admin.site.register(Course)
admin.site.register(CustomerCourse)
admin.site.register(TeacherCourse)
admin.site.register(TeacherLanguage)
