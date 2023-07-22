from django import forms
from .models import Student, Teacher, Attendance
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class AddStudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = (
            "student_id",
            "email",
            "classe",
            "first_name",
            "last_name",
            "project_group",
        )

    def save(self, commit=True):
        # Save the student object
        student = super().save(commit=False)

        # Save the user object
        user = User.objects.create_user(
            username=self.cleaned_data['student_id'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        student.user = user

        if commit:
            student.save()
        return student


class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_id',
                  'email',
                  'classe',
                  'last_name',
                  'first_name',
                  'project_group')


class AddTeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = (
            "email",
            "first_name",
            "last_name",
        )

    def save(self, commit=True):
        # Save the student object
        teacher = super().save(commit=False)

        # Save the user object
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )

        teacher.user = user

        if commit:
            teacher.save()
        return teacher


# Datetime widget inspired by:
# https://ordinarycoders.com/blog/article/using-django-form-fields-and-widgets
#
# Date validation inspired by:
# https://stackoverflow.com/questions/7355409/validate-end-date-is-bigger-than-start-date-in-django-model-form
class AttendanceForm(forms.ModelForm):
    start_date = forms.DateTimeField(label="Begint", widget=NumberInput(attrs={
        'type': 'datetime-local'
    }))
    end_date = forms.DateTimeField(label="Eindigt", widget=NumberInput(attrs={
        'type': 'datetime-local'
    }))

    class Meta:
        model = Attendance
        fields = (
            "title", 
            "teacher", 
            "course", 
            "classe",
            "start_date",
            "end_date",
            "join_code",
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise ValidationError(
                _("De einddatum moet na de startdatum plaatsvinden.")
            )
