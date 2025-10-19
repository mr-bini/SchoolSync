from django.contrib import admin
from .models import CustomUser, HomeworkNote
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('school_year', 'subjects')}),
    )

admin.site.register(HomeworkNote)
from .models import StudyGroup, Message

admin.site.register(StudyGroup)
admin.site.register(Message)
