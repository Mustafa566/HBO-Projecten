from django.contrib import admin
from .models import *


class AddTeacherAdmin(admin.ModelAdmin):
    list_display = (
        "teacher_id",
        "last_name",
        "first_name",
        "email",
    )


class AddClasseAdmin(admin.ModelAdmin):
    list_display = (
        "classe_id",
        "teacher",
    )


class AddStudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "email",
        "classe",
        "last_name",
        "first_name",
        "project_group",
    )


class AddCourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_id",
        "course_name",
        "elective",
    )


class AddStudentScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "schedule_id",
        "student",
        "course",
        "teacher",
        "date",
        "classroom",
    )


class AddTeacherScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "schedule_id",
        "teacher",
        "course",
        "classe",
        "date",
        "classroom",
    )


class AddAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "attendance_id",
        "title",
        "teacher",
        "course",
        "classe",
        "active",
        "start_date",
        "end_date",
    )


class AddHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "history_id",
        "student",
        "attendance",
        "date_joined",
        "is_present",
    )


class PresentAdmin(admin.ModelAdmin):
    list_display = (
        "present_id",
        "student",
        "attendance",
        "date_joined",
        "is_present",
    )


admin.site.register(Attendance, AddAttendanceAdmin)
admin.site.register(Student, AddStudentAdmin)
admin.site.register(Classe, AddClasseAdmin)
admin.site.register(Teacher, AddTeacherAdmin)
admin.site.register(StudentSchedule, AddStudentScheduleAdmin)
admin.site.register(Course, AddCourseAdmin)
admin.site.register(TeacherSchedule, AddTeacherScheduleAdmin)
admin.site.register(History, AddHistoryAdmin)
admin.site.register(Present, PresentAdmin)
