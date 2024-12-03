from django.contrib import admin

# Register your models here.
from .models import Customer, Teacher, Language, Course, Payment, TeacherLanguage

# Регистрация моделей
admin.site.register(Customer)
admin.site.register(Teacher)
admin.site.register(Language)
admin.site.register(Course)
admin.site.register(Payment)
admin.site.register(TeacherLanguage)
