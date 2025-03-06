from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from cms_app.models import Notice
from .models import Preamble, ProgramObjective, Faculty
from .models import AboutPage
from .models import AcademicYear
from .models import Semester
from .models import AboutProgram, PlacementRecord, JobProfile, Recruiter
from .models import Alumni
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import LectureTimetable, ExamTimetable, StudentClass
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

def student_login(request):
    error_message = None  # Initialize error message

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email:
            error_message = "Please enter your email."
        elif not password:
            error_message = "Please enter your password."
        else:
            try:
                student = Student.objects.get(email=email)
                if check_password(password, student.password):
                    request.session['student_email'] = student.email
                    next_url = request.GET.get('next', '/dashboard/')
                    return redirect(next_url)
                else:
                    error_message = "Invalid password."
            except Student.DoesNotExist:
                error_message = "Invalid email."

    # Render the template and pass the error_message, even if it is None
    return render(request, "cms_app/student_login.html", {"error_message": error_message})
def student_dashboard(request):
    if 'student_email' in request.session:
        try:
            student = Student.objects.get(email=request.session['student_email'])

            # Mapping class_name to numerical values
            class_mapping = {"FY": 1, "SY": 2, "TY": 3}
            student_class = class_mapping.get(student.class_name)  # Get the corresponding number

            # Fetch the exam timetable for the student's class
            exam_timetable = None
            if student_class is not None:
                exam_timetable = ExamTimetable.objects.filter(student_class=student_class).first()

            return render(request, 'cms_app/student_dashboard.html', {
                'student': student,
                'exam_timetable': exam_timetable
            })
        except Student.DoesNotExist:
            return render(request, 'cms_app/student_dashboard.html', {'error': 'Student record does not exist'})
    else:
        return redirect('student_login')

def student_logout(request):
    try:
        del request.session['student_email']
    except KeyError:
        pass
    return redirect('student_login')

def reset_password(request):
    if 'student_email' not in request.session:
        return redirect('student_login')

    student = Student.objects.get(email=request.session['student_email'])

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(old_password, student.password):
            if new_password == confirm_password:
                student.password = make_password(new_password)
                student.save()
                messages.success(request, 'Your password has been updated!')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Incorrect old password.')

    return render(request, 'cms_app/reset_password.html')

def timetables(request):
    classes = StudentClass.objects.all()
    lecture_timetables = LectureTimetable.objects.all()
    exam_timetables = ExamTimetable.objects.all()
    
    context = {
        "classes": classes,
        "lecture_timetables": lecture_timetables,
        "exam_timetables": exam_timetables,
    }
    return render(request, "cms_app/timetables.html", context)