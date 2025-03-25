from django.contrib import admin
from .models import Notice
from .models import Preamble
from .models import ProgramObjective
from .models import Faculty
from .models import AboutPage
from .models import AcademicYear, Syllabus
from .models import Semester, EResource
from .models import AboutProgram, PlacementRecord, JobProfile, Recruiter
from .models import Alumni
from import_export import resources
from import_export.admin import ExportMixin, ImportMixin 
from .models import Student
from django.contrib.auth.hashers import make_password
from .resources import StudentResource
from .models import StudentClass, LectureTimetable, ExamTimetable, LeaveApplication
from .models import IndustrialVisit, VisitDay, VisitImage

admin.site.site_header = "BScIT Admin Panel"
admin.site.site_title = "BScIT Admin"
admin.site.index_title = "Site administration"

admin.site.register(Notice)
admin.site.register(Preamble)
admin.site.register(ProgramObjective)
admin.site.register(Faculty)
admin.site.register(AboutPage)
admin.site.register(AcademicYear)
admin.site.register(Syllabus)
admin.site.register(Semester)
admin.site.register(EResource)
admin.site.register(AboutProgram)
admin.site.register(PlacementRecord)
admin.site.register(JobProfile)
admin.site.register(Recruiter)
@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ("name", "batch", "current_position")
    search_fields = ("name", "batch", "current_position")


class VisitDayInline(admin.TabularInline):
    model = VisitDay
    extra = 1

class VisitImageInline(admin.TabularInline):
    model = VisitImage
    extra = 1

@admin.register(IndustrialVisit)
class IndustrialVisitAdmin(admin.ModelAdmin):
    list_display = ("destination", "year", "batch_size")
    inlines = [VisitDayInline, VisitImageInline]
    
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        exclude = ('id',)  # Exclude 'id' from import since it is auto-generated
        import_id_fields = ('email',)  # You can import based on email (unique)

    def before_import_row(self, row, **kwargs):
        # Ensure password is set to 'student@BSCIT' before import if it's not provided
        if 'password' not in row or not row['password']:
            row['password'] = 'student@BSCIT'
        # Hash the password (you can use Django's make_password method for hashing)
        row['password'] = make_password(row['password'])
        return row

# Customize the StudentAdmin class to add the import/export functionality
class StudentAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):  # Both ImportMixin and ExportMixin
    resource_class = StudentResource
    list_display = ('email', 'first_name', 'last_name', 'class_name', 'roll_no')
    search_fields = ('email', 'first_name', 'last_name', 'class_name', 'roll_no')

# Register the Student model with the admin interface
admin.site.register(Student, StudentAdmin)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')  # Display fields in admin panel

@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(LectureTimetable)
class LectureTimetableAdmin(admin.ModelAdmin):
    list_display = ("title", "student_class", "uploaded_at")
    search_fields = ("title",)
    list_filter = ("student_class",)

@admin.register(ExamTimetable)
class ExamTimetableAdmin(admin.ModelAdmin):
    list_display = ("title", "student_class", "uploaded_at")
    search_fields = ("title",)
    list_filter = ("student_class",)

@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "start_date", "end_date", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("student__email", "reason")
