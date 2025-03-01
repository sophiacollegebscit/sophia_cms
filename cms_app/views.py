from django.shortcuts import render
from itertools import groupby
from operator import attrgetter

from cms_app.models import Notice
from .models import Preamble, ProgramObjective, Faculty
from .models import AboutPage
from .models import Syllabus
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

def syllabi_view(request):
    syllabi = Syllabus.objects.all().order_by('-year')  # Fetch syllabus by year
    grouped_syllabi = {}
    for key, group in groupby(syllabi, key=attrgetter('year')):
        grouped_syllabi[key] = list(group)
    return render(request, "cms_app/syllabi.html",  {'grouped_syllabi': grouped_syllabi})


def navbar(request):
    return render(request, 'navbar.html')

def navbar_sidebar(request):
    return render(request, 'navbar-sidebar.html')
