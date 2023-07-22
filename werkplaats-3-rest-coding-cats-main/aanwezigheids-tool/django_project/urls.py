"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login.views import HomePageView, attendanceListPageView, attendanceDetailView
from attendanceItems.views import StudentTableView, AddStudentsView, AddTeachersView, AddattendanceView, \
    student_agenda, teacher_agenda, StudentFilterView, StudentEditView, StudentDeleteView, mark_attendance, \
    get_all_presents, StudentDetailView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path("attendanceListData/", attendanceListPageView.attendance_data, name="attendanceListData"),
    path("attendanceList/", attendanceListPageView.as_view(), name="attendanceList"),
    path('attendance/<pk>/', attendanceDetailView.as_view(), name="attendance"),
    path("createAttendance/", AddattendanceView.as_view(), name="createAttendanceList"),
    path("auth/", include("django.contrib.auth.urls")),
    path("addstudents/", AddStudentsView.as_view(), name="newstudent"),
    path("students/", StudentTableView.as_view(), name="student_db"),
    path("filtered/", StudentFilterView.as_view(), name="students_filtered"),
    path("students/<int:pk>/edit/", StudentEditView.as_view(), name="student-edit"),
    path("students/<int:pk>/delete/", StudentDeleteView.as_view(), name="delete-student"),
    path("newteacher/", AddTeachersView.as_view(), name="newteacher"),
    path("student_agenda/", student_agenda, name="student_agenda"),
    path("teacher_agenda/", teacher_agenda, name="teacher_agenda"),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('presents/', get_all_presents, name='presents'),
    path('students/<int:pk>/detail/', StudentDetailView.as_view(), name='student-detail')
]
