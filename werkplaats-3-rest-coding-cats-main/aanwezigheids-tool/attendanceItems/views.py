from django.shortcuts import get_object_or_404, render, redirect
from .forms import AddStudentForm, AddTeacherForm, AttendanceForm, EditStudentForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DeleteView
from .models import Attendance, Student, History, Teacher, Present
from .filters import StudentFilter, ClasseFilter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_tables2 import SingleTableView, LazyPaginator, RequestConfig
from .tables import StudentTable
from django_filters.views import FilterView
from django.views.generic.detail import DetailView


class AddStudentsView(CreateView):
    form_class = AddStudentForm
    success_url = reverse_lazy("student_db")
    template_name = "registration/addstudents.html"


def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddStudentForm()
    return render(request, 'addstudents.html', {'form': form})


class AddTeachersView(CreateView):
    form_class = AddTeacherForm
    success_url = reverse_lazy("newteacher")
    template_name = "registration/addteachers.html"


def add_teacher(request):
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddTeacherForm()
    return render(request, 'addteachers.html', {'form': form})


class StudentTableView(SingleTableView):
    model = Student
    table_class = StudentTable
    template_name = "admin/student_view.html"
    filter_class = ClasseFilter
    paginator_class = LazyPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classe_filter = ClasseFilter(self.request.GET, queryset=Student.objects.all())
        context['classe_filter'] = classe_filter
        filtered_data = classe_filter.qs
        table = StudentTable(filtered_data)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(table)
        context['table'] = table
        return context


class StudentFilterView(FilterView):
    model = Student
    filterset_class = StudentFilter
    table_class = StudentTable
    template_name = 'admin/students_filtered.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = self.table_class(self.filterset.qs)
        return context


class StudentEditView(FormView):
    template_name = 'admin/student_edit.html'
    form_class = EditStudentForm
    success_url = reverse_lazy('student_db')

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['pk'])
        student.email = form.cleaned_data['email']
        student.classe = form.cleaned_data['classe']
        student.last_name = form.cleaned_data['last_name']
        student.first_name = form.cleaned_data['first_name']
        student.project_group = form.cleaned_data['project_group']
        student.save()
        return redirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = get_object_or_404(Student, pk=self.kwargs['pk'])
        return kwargs


class StudentDeleteView(DeleteView):
    model = Student
    template_name = "admin/student_confirm_delete.html"
    success_url = reverse_lazy('student_db')


class AddattendanceView(CreateView):
    form_class = AttendanceForm
    success_url = reverse_lazy("attendanceList")
    template_name = "attendance/createAttendance.html"


def student_agenda(request):
    user = request.user
    if user.is_authenticated and user.username.isdigit:
        student = Student.objects.get(student_id=user.username)
        class_attendance = Attendance.objects.filter(classe=student.classe)
        return render(request, 'student_agenda.html', {'class_attendance': class_attendance})
    else:
        return render(request, 'home.html')


def teacher_agenda(request):
    user = request.user
    if user.is_authenticated and "@" in user.username:
        teacher = Teacher.objects.get(email=user.username)
        class_attendance = Attendance.objects.filter(teacher=teacher)
        return render(request, 'teacher_agenda.html', {'class_attendance': class_attendance})
    else:
        return render(request, 'home.html')


def add_student_attendance(request, attendance_id):
    # Get the attendance object
    attendance = get_object_or_404(Attendance, pk=attendance_id)

    if request.method == 'POST':
        # Get the student object
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, pk=student_id)

        # Add the student to the attendance
        attendance.students.add(student)

        # Create a history object
        history = History.objects.create(student=student, attendance=attendance)

        # Redirect to the attendance detail page
        return redirect('attendance_detail', attendance_id=attendance_id)

    # Render the add student attendance form
    return render(request, 'add_student_attendance.html', {'attendance': attendance})


@csrf_exempt
@require_POST
def mark_attendance(request):
    username = request.user.username
    student_id = request.POST.get('student_id')
    attendance_id = request.POST.get('attendance_id')
    date_joined = request.POST.get('date_joined')
    present = Present(student_id=username, attendance_id=attendance_id, date_joined=date_joined, is_present=True)
    present.save()

    print(request.user.username)

    return JsonResponse({'status': 'success'})


class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'
    context_object_name = 'student'


def get_all_presents():
    presents = Present.objects.all()

    # Call the get_all_presents() function to retrieve all Present instances
    # present_instances = presents

    print(presents)

    # Example of iterating through the Present instances and accessing field values
    # for present in present_instances:
    #     print(present.student)  # Access the student field of the Present instance
    #     print(present.attendance)  # Access the attendance field of the Present instance
    #     print(present.date_joined)  # Access the date_joined field of the Present instance
    #     print(present.is_present)  # Access the is_present field of the Present instance
    #     # Perform other actions with the retrieved field values as needed

    return presents
