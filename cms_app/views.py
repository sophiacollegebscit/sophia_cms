from django.shortcuts import render
from cms_app.models import Notice
from .models import Preamble, ProgramObjective

def index(request):
    notices = Notice.objects.all()
    preamble = Preamble.objects.first()  # Assuming only one preamble entry
    program_objectives = ProgramObjective.objects.all()
    
    # Debugging output
    print("Notices:", notices)
    print("Preamble:", preamble)
    print("Program Objectives:", program_objectives)

    return render(request, "cms_app/index.html", {
        "notices": notices,
        "preamble": preamble,
        "program_objectives": program_objectives
    })

def navbar(request):
    return render(request, 'navbar.html')

def navbar_sidebar(request):
    return render(request, 'navbar-sidebar.html')
