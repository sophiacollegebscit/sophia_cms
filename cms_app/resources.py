from django.contrib.auth.hashers import make_password
from import_export import resources
from .models import Student

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('id', 'email', 'first_name', 'last_name', 'class_name', 'roll_no', 'password')

    def before_import_row(self, row, **kwargs):
    # Ensure password is set to 'student@BSCIT' before import if it's not provided
        if 'password' not in row or not row['password']:
            row['password'] = 'student@BSCIT'
    # Hash the password
        row['password'] = make_password(row['password'])

    # Strip any leading/trailing whitespace from email and ensure it's not empty
        if row.get('email'):
            row['email'] = row['email'].strip()

        return super().before_import_row(row, **kwargs)
