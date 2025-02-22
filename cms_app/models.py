from django.db import models

class Notice(models.Model):
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.content:
            self.content = "No content provided"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content[:50]  # Show first 50 characters as string representation

class Preamble(models.Model):
    title = models.CharField(max_length=255, default="Preamble")
    description = models.TextField()

    def __str__(self):
        return self.title
    
class ProgramObjective(models.Model):
    objective = models.TextField()

    def __str__(self):
        return self.objective[:50]  # Display first 50 chars in admin panel