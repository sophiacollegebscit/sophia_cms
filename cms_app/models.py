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
    
class Syllabus(models.Model):
    year = models.CharField(max_length=9)  # Example: "2024-2025"
    title = models.CharField(max_length=255)  # Example: "First Year BSc IT NEP Syllabus"
    semester = models.CharField(max_length=20)  # Example: "Semester 1"
    file = models.FileField(upload_to="syllabus/")  # File upload path
    class Meta:
        verbose_name_plural = "Syllabi"
    def __str__(self):
        return f"{self.year} - {self.title} ({self.semester})"