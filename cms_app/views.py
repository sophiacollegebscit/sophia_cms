from django.shortcuts import render
from itertools import groupby
from operator import attrgetter

from cms_app.models import Notice
from .models import Preamble, ProgramObjective, Faculty
from .models import AboutPage
from .models import AcademicYear
from .models import Semester


def index(request):
    notices = Notice.objects.all()
    preamble = Preamble.objects.first()  # Assuming only one preamble entry
    program_objectives = ProgramObjective.objects.all()
    faculty_members = Faculty.objects.all()

    return render(request, "cms_app/index.html", {
        "notices": notices,
        "preamble": preamble,
        "program_objectives": program_objectives,
        "faculty_members": faculty_members
    })

def about_view(request):
    about_pages = AboutPage.objects.all()
    return render(request, "cms_app/aboutus.html", {"about_pages": about_pages})

def syllabus_view(request):
    academic_years = AcademicYear.objects.prefetch_related("syllabi").all()
    return render(request, "cms_app/syllabi.html", {"academic_years": academic_years})

def e_resources(request):
    semesters = Semester.objects.prefetch_related("resources").all()
    return render(request, "cms_app/e-resources.html", {"semesters": semesters})

def navbar(request):
    return render(request, 'navbar.html')

def navbar_sidebar(request):
    return render(request, 'navbar-sidebar.html')
