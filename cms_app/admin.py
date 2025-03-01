from django.contrib import admin
from .models import Notice
from .models import Preamble
from .models import ProgramObjective
from .models import Faculty
from .models import AboutPage
from .models import Syllabus
admin.site.site_header = "BScIT Admin Panel"
admin.site.site_title = "BScIT Admin"
admin.site.index_title = "Site administration"

admin.site.register(Notice)
admin.site.register(Preamble)
admin.site.register(ProgramObjective)
admin.site.register(Faculty)
admin.site.register(AboutPage)
admin.site.register(Syllabus)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')  # Display fields in admin panel
