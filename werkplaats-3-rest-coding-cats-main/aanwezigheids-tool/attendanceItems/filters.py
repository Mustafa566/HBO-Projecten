import django_filters
from .models import Student, Classe
from django.db.models import Q
from django.forms import CheckboxSelectMultiple


class StudentFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_filter')

    class Meta:
        model = Student
        fields = ['q']

    @staticmethod
    def custom_filter(queryset, x, value):
        return queryset.filter(
            Q(last_name__icontains=value) |
            Q(first_name__icontains=value) |
            Q(student_id__startswith=value)
        )


class ClasseFilter(django_filters.FilterSet):
    classe = django_filters.MultipleChoiceFilter(
        field_name='classe__classe_id',
        label="",
        widget=CheckboxSelectMultiple,
        choices=Classe.objects.all().values_list('classe_id', 'classe_id')
    )

    class Meta:
        model = Student
        fields = ['classe']
