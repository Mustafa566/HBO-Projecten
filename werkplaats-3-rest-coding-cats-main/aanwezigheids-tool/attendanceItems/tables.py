import django_tables2 as tables
from django_tables2 import A
from .models import Student


class StudentTable(tables.Table):
    student_id = tables.LinkColumn('student-detail',
                                   args=[A('pk')])
    email = tables.Column(linkify=False)
    edit = tables.TemplateColumn(template_name="admin/student_edit_table_view.html",
                                 extra_context={"pk": tables.A('pk')},
                                 verbose_name="",
                                 )
    delete = tables.TemplateColumn(template_name="admin/delete_student.html",
                                   verbose_name="",
                                   extra_context={"pk": tables.A("pk")},
                                   orderable=False
                                   )

    class Meta:
        model = Student
        fields = ('student_id', 'email', 'classe', 'last_name', 'first_name', 'project_group')
