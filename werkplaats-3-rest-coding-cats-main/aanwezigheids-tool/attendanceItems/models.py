from django.db import models
from django.urls import reverse


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=150, verbose_name='Achternaam')
    first_name = models.CharField(max_length=150, verbose_name='Voornaam')
    email = models.EmailField(max_length=250, verbose_name='E-mailadres')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Classe(models.Model):
    classe_id = models.CharField(primary_key=True, max_length=2, verbose_name='Klas')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default="", verbose_name='SLC\'er',
                                null=True, blank=True)

    def __str__(self):
        return self.classe_id


class Student(models.Model):
    student_id = models.IntegerField(primary_key=True, verbose_name='Studentnummer', unique=True)
    email = models.EmailField(max_length=250, verbose_name='E-mailadres')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, default="", verbose_name='Klas')
    last_name = models.CharField(max_length=150, verbose_name='Achternaam')
    first_name = models.CharField(max_length=150, verbose_name='Voornaam')
    project_group = models.CharField(max_length=255, verbose_name='Projectgroep')

    def __str__(self):
        return f'{self.student_id}, {self.first_name} {self.last_name}'


class Course(models.Model):
    course_id = models.CharField(max_length=150, primary_key=True, verbose_name='Cursuscode')
    course_name = models.CharField(max_length=150, verbose_name='Cursusnaam')
    elective = models.BooleanField(null=True, verbose_name='Keuzevak')

    def __str__(self):
        return self.course_name


class StudentSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Studentnummer', default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Cursusnaam', default="")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Docent', default="")
    date = models.DateTimeField(null=True, verbose_name='Datum')
    classroom = models.CharField(max_length=150, verbose_name='Leslocatie')

    def __str__(self):
        return self.classroom


class TeacherSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Docent', default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default="", verbose_name="Cursusnaam")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, default="", verbose_name='Klas')
    date = models.DateTimeField(null=True, verbose_name='Datum')
    classroom = models.CharField(max_length=150, verbose_name='Leslocatie')

    def __str__(self):
        return self.classroom


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name='Naam bijeenkomst')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Docent', default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Cursusnaam', default="")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, default="", verbose_name='Klas')
    join_code = models.CharField(max_length=200, verbose_name='Toegangscode', default="",
                                 help_text='Verzin een code die studenten kunnen gebruiken om toegang tot de les te '
                                           'krijgen.')
    active = models.BooleanField(default=True, verbose_name='Actief')
    start_date = models.DateTimeField(null=True, verbose_name='Begint')
    end_date = models.DateTimeField(null=True, verbose_name='Eindigt')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("attendance", kwargs={"pk": self.pk})


class History(models.Model):
    history_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Studentnummer')
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, verbose_name='Bijeenkomst')
    date_joined = models.DateTimeField(default="", null=True, verbose_name='Datum aangemeld')
    is_present = models.BooleanField(default=False, verbose_name='Aanwezig')

    def __str__(self):
        return f'{self.student} - {self.attendance}'


class Present (models.Model):
    present_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Studentnummer')
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, verbose_name='Bijeenkomst')
    date_joined = models.DateTimeField(default="", null=True, verbose_name='Datum aangemeld')
    is_present = models.BooleanField(default=False, verbose_name='Aanwezig')

    def __str__(self):
        return f'{self.student} - {self.attendance}'
