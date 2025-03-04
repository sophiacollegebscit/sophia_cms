from django.shortcuts import render

from cms_app.models import Notice
from .models import Preamble, ProgramObjective, Faculty
from .models import AboutPage
from .models import AcademicYear
from .models import Semester
from .models import AboutProgram, PlacementRecord, JobProfile, Recruiter
from .models import Alumni




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

def placement_page(request):
    about = AboutProgram.objects.first()  # Fetch About Program
    placements = PlacementRecord.objects.all().order_by("-academic_year")  # Fetch all Placement Records
    job_profiles = JobProfile.objects.all()  # Fetch Job Profiles
    recruiters = Recruiter.objects.all()  # Fetch Recruiters

    return render(request, "cms_app/placement.html", {
        "about": about,
        "placements": placements,
        "job_profiles": job_profiles,
        "recruiters": recruiters,
    })

def alumni_page(request):
    alumni = Alumni.objects.all()
    return render(request, "cms_app/alumni.html", {"alumni": alumni})

def navbar(request):
    return render(request, 'navbar.html')

def navbar_sidebar(request):
    return render(request, 'navbar-sidebar.html')



