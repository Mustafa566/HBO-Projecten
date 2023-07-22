from django.views.generic import TemplateView
from django.http import JsonResponse
from attendanceItems.models import Attendance, Present
from django.views.generic.detail import DetailView
from datetime import datetime


class HomePageView(TemplateView):
    template_name = "home.html"
    
    
class attendanceDetailView(DetailView):
    template_name = "attendance/attendance.html"
    model = Attendance
    present_students = []

    def get(self, request, *args, **kwargs):
        # Get the attendance object
        attendance = self.get_object()
        
        # Get the join code parameter from the request
        join_code = request.GET.get('join_code')

        # Check if the join code matches the attendance object's join code
        if join_code == attendance.join_code:
            # The join code is valid, so set checker to True
            self.checker = True
        else:
            self.checker = False
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add the students to the context dictionary
        context['students'] = self.object.classe.student_set.all()
        
        # Add the present students to the context dictionary
        context['present_students'] = self.present_students
        
        # Add the checker to the context dictionary
        context['checker'] = getattr(self, 'checker', False)
        
        return context


class attendanceListPageView(TemplateView):
    template_name = "attendance/attendanceList.html"
    
    def attendance_data(request):
        data = {
            'attendance_id': [],
            'title': [],
            'teacher': [],
            'course': [],
            'classe': [],
            'active': [],
            'join_code': [],
            'start_date': [],
            'end_date': []
        }
        attendances = Attendance.objects.all().order_by('start_date')
        now = datetime.now()
        for attendance in attendances:
            data['attendance_id'].append(attendance.attendance_id)
            data['title'].append(attendance.title)
            data['teacher'].append(attendance.teacher.email)
            data['course'].append(attendance.course.course_id)
            data['classe'].append(attendance.classe.classe_id)
            
            start_date = attendance.start_date.replace(tzinfo=None)
            end_date = attendance.end_date.replace(tzinfo=None)
            if now < start_date or now > end_date:
                attendance.active = False
            else:
                attendance.active = True
            attendance.save()
            
            data['join_code'].append(attendance.join_code)
            data['active'].append(attendance.active)
            data['start_date'].append(start_date.strftime('%d-%m-%Y %H:%M:%S'))
            data['end_date'].append(end_date.strftime('%d-%m-%Y %H:%M:%S'))
        return JsonResponse(data)
    
    
class createAttendancePageView(TemplateView):
    template_name = "attendance/createAttendance.html"
    
    
class attendancePageView(TemplateView):
    template_name = "attendance/attendance.html"
    