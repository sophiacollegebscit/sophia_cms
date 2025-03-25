from django.db import models
class Notice(models.Model):
    content = models.TextField()
    link = models.URLField(blank=True, null=True)  # Optional external link
    pdf = models.FileField(upload_to='notices/', blank=True, null=True)  # PDF Upload
    class Meta:
        verbose_name_plural = "Notices"

    def save(self, *args, **kwargs):
        if not self.content:
            self.content = "No content provided"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content[:50]  # Show first 50 characters as string representation

class Preamble(models.Model):
    title = models.CharField(max_length=255, default="Preamble")
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Preamble"
    def __str__(self):
        return self.title
    
class ProgramObjective(models.Model):
    objective = models.TextField()
    class Meta:
        verbose_name_plural = "Program Objectives"
    def __str__(self):
        return self.objective[:50]  # Display first 50 chars in admin panel
    
class Faculty(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, blank=True, null=True)  # Allow empty values
    qualification = models.CharField(max_length=255)
    experience = models.TextField()
    image = models.ImageField(upload_to='faculty/', blank=True, null=True)  # Optional image
    class Meta:
        verbose_name_plural = "Faculty"
    def __str__(self):
        return self.name
    
class AboutPage(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    class Meta:
        verbose_name_plural = "About Page"
    def __str__(self):
        return self.title
    
class AcademicYear(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Syllabus(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="syllabi")
    title = models.CharField(max_length=255)
    semester = models.CharField(max_length=20)
    file = models.FileField(upload_to="syllabus/")


    class Meta:
        verbose_name_plural = "Syllabi"
    def __str__(self):
        return f"{self.title} ({self.academic_year.name})"
    
class Semester(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class EResource(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    url = models.URLField()
    class Meta:
        verbose_name_plural = "E-Resources"

    def __str__(self):
        return f"{self.title} ({self.semester.name})"

class PlacementRecord(models.Model):
    academic_year = models.CharField(max_length=20, unique=True)
    total_students = models.IntegerField()
    students_placed = models.IntegerField()
    higher_studies = models.IntegerField(blank=True, null=True)  # Allow empty values

    def __str__(self):
        return f"{self.academic_year} - {self.total_students} students"
    
class AboutProgram(models.Model):
    title = models.CharField(max_length=255, default="About the Program")
    description = models.TextField()

    def __str__(self):
        return self.title

class PlacementRecord(models.Model):
    academic_year = models.CharField(max_length=20)
    total_students = models.PositiveIntegerField()
    students_placed = models.PositiveIntegerField()
    pursuing_higher_studies = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.academic_year

class JobProfile(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Recruiter(models.Model):
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="recruiter_logos/")

    def __str__(self):
        return self.company_name
    
class Alumni(models.Model):
    name = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="alumni_images/")
    current_position = models.CharField(max_length=255)
    batch = models.CharField(max_length=10)
    review = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class IndustrialVisit(models.Model):
    destination = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    duration = models.CharField(max_length=50)
    batch_size = models.IntegerField()
    
    class Meta:
        verbose_name = "Industrial Visit"
        verbose_name_plural = "Industrial Visits"

    def __str__(self):
        return f"{self.destination} - {self.year}"

class VisitDay(models.Model):
    visit = models.ForeignKey(IndustrialVisit, related_name="days", on_delete=models.CASCADE)
    day_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Day {self.day_number} - {self.title} ({self.visit.destination})"

class VisitImage(models.Model):
    visit = models.ForeignKey(IndustrialVisit, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="industrial_visits/")

    def __str__(self):
        return f"Image for {self.visit.destination}"

class Student(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    reset_token = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'cms_app_student'


class StudentClass(models.Model):
    name = models.CharField(max_length=2, unique=True)  # No predefined choices

    def __str__(self):
        return self.name
    

class LectureTimetable(models.Model):
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="timetables/lecture/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_class} - {self.title}"


class ExamTimetable(models.Model):
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="timetables/exam/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_class} - {self.title}"


class LeaveApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        APPROVED = "Approved", "Approved"
        DENIED = "Denied", "Denied"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="leave_applications")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    proof = models.FileField(upload_to="leave_proofs/", blank=True, null=True)  # Optional proof field
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)
    admin_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.email} - {self.status}"
        
