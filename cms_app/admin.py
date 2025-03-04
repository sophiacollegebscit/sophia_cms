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

class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')  # Display fields in admin panel
