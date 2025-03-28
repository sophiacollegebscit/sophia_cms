import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import LeaveApplication
from datetime import date
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse
from .models import Student
from cms_app.models import Notice
from .models import Preamble, ProgramObjective, Faculty
from .models import AboutPage
from .models import AcademicYear
from .models import Semester
from .models import AboutProgram, PlacementRecord, JobProfile, Recruiter
from .models import Alumni
from .models import IndustrialVisit
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import LectureTimetable, ExamTimetable, StudentClass
from django.core.mail import send_mail
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


def industrial_visits(request):
    visits = IndustrialVisit.objects.prefetch_related("days", "images").all()
    return render(request, "cms_app/industrial_visits.html", {"visits": visits})

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

            # Mapping class_name (text) to numerical values
            class_mapping = {"FY": 1, "SY": 2, "TY": 3}
            student_class_id = class_mapping.get(student.class_name)  # Convert class name to ID

            # Fetch both timetables based on student class
            exam_timetable = ExamTimetable.objects.filter(student_class=student_class_id).first()
            lecture_timetable = LectureTimetable.objects.filter(student_class=student_class_id).first()

            return render(request, 'cms_app/student_dashboard.html', {
                'student': student,
                'exam_timetable': exam_timetable,
                'lecture_timetable': lecture_timetable
            })
        except Student.DoesNotExist:
            return render(request, 'cms_app/student_dashboard.html', {'error': 'Student record does not exist'})
    
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

        # Strong password pattern: At least 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*().?])[A-Za-z\d!@#$%^&*().?]{8,}$"


        # Validate old password
        if not check_password(old_password, student.password):
            messages.error(request, 'Incorrect old password.')
            return redirect('reset_password')

        # Validate new password strength
        if not re.match(password_pattern, new_password):
            messages.error(request, "Password must be at least 8 characters long and include: "
                                    "one uppercase letter, one lowercase letter, one number, and one special character.")
            return redirect('reset_password')

        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('reset_password')

        # Update password
        student.password = make_password(new_password)
        student.save()
        return redirect('student_dashboard')

    return render(request, 'cms_app/reset_password.html')

def student_password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()

        # Check if student exists
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("student_password_reset_request")

        # Generate and store reset token
        token = get_random_string(30)
        student.reset_token = token
        student.save()

        # Create reset link
        reset_link = request.build_absolute_uri(reverse("student_password_reset_confirm", args=[token]))

        # Send reset email
        try:
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                "website.bscit@sophiacollege.edu.in",  # Must match EMAIL_HOST_USER in settings.py
                [email],
                fail_silently=False,
            )
            messages.success(request, "A password reset link has been sent to your email.")
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")  # Logs any email errors

    return render(request, "cms_app/student_password_reset_request.html")


def student_password_reset_confirm(request, token):
    try:
        student = Student.objects.get(reset_token=token)
    except Student.DoesNotExist:
        return render(request, "cms_app/student_password_reset_confirm.html", {"error": "Invalid reset link"})

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            student.password = make_password(new_password)  # Hash the password manually
            student.reset_token = None  # Clear the reset token after use
            student.save()
            return redirect("student_login")
        else:
            return render(request, "cms_app/student_password_reset_confirm.html", {"error": "Passwords do not match"})

    return render(request, "cms_app/student_password_reset_confirm.html")

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


def apply_leave(request):
    student = Student.objects.get(email=request.session.get("student_email"))  # Adjust based on your auth system
    success_message = None  # Store success message without redirecting

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")
        proof = request.FILES.get("proof")

        leave = LeaveApplication(student=student, start_date=start_date, end_date=end_date, reason=reason, proof=proof)
        leave.save()

        # Email proof details (if available)
        proof_text = f"Proof attached: {request.build_absolute_uri(leave.proof.url)}" if leave.proof else "No proof attached."

        # Notify student
        student_email = student.email
        student_subject = "Leave Application Submitted"
        student_message = f"""
        Dear {student.first_name},

        Your leave application has been submitted successfully.

        Details:
        Start Date: {leave.start_date}
        End Date: {leave.end_date}
        Reason: {leave.reason}
        Status: Pending
        {proof_text}

        You will be notified once your leave status is updated.

        Regards,
        Admin Team
        """
        send_mail(student_subject, student_message, settings.EMAIL_HOST_USER, [student_email])

        # Notify admin
        admin_email = "website.bscit@sophiacollege.edu.in"  # Replace with actual admin email
        admin_subject = "New Leave Application Submitted"
        admin_message = f"""
        A new leave application has been submitted by {student.email}.

        Details:
        Start Date: {leave.start_date}
        End Date: {leave.end_date}
        Reason: {leave.reason}

        {proof_text}

        Please review and update the leave status in the admin panel.

        Regards,
        System Notification
        """
        send_mail(admin_subject, admin_message, settings.EMAIL_HOST_USER, [admin_email])

        success_message = "Leave application submitted successfully."

    return render(request, "cms_app/apply_leave.html", {"success_message": success_message})




def leave_history(request):
    student = Student.objects.get(email=request.session.get("student_email"))
    leave_applications = LeaveApplication.objects.filter(student=student).order_by("-applied_at")
    return render(request, "cms_app/leave_history.html", {"leave_applications": leave_applications})
