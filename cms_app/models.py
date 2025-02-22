from django.db import models

class Notice(models.Model):
    content = models.TextField()
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
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience = models.TextField()
    image = models.ImageField(upload_to='faculty_images/')  # Store images in media/faculty_images/
    class Meta:
        verbose_name_plural = "Faculty"
    def __str__(self):
        return self.name