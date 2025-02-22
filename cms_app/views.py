from django.shortcuts import render
from cms_app.models import Notice
from .models import Preamble, ProgramObjective, Faculty

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

def navbar(request):
    return render(request, 'navbar.html')

def navbar_sidebar(request):
    return render(request, 'navbar-sidebar.html')
