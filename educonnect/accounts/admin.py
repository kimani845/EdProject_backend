from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TutorProfile, StudentProfile, Course, CourseEnrollment, CourseMaterial, CourseReview, CourseRating, CourseComment

# Register your models here.
class TutorProfileInline(admin.StackedInline):
    model = TutorProfile
    can_delete = False
    
class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    
class UserAdmin(BaseUserAdmin):
    inlines = (TutorProfileInline, StudentProfileInline)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
    list_filter = ['role','is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'avatar', 'bio')}),
        )
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        
        inlines = []
        if obj.role == 'TUTOR':
            inlines.append(TutorProfileInline(self.model, self.admin_site))
        elif obj.role == 'STUDENT':
            inlines.append(StudentProfileInline(self.model, self.admin_site))
            
        return inlines
    
admin.site.register(User, UserAdmin)
admin.site.register(TutorProfile)
admin.site.register(StudentProfile)