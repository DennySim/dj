from django.views.generic import ListView

from .models import Student, Teacher


class StudentListView(ListView):
    model = Student
    ordering = 'group'

    def get_context_data(self, **kwargs):

        context = {}

        # context = super(StudentListView, self).get_context_data(**kwargs)
        context['student_list'] = \
            Student.objects.all().prefetch_related('teacher')

        context['teachers'] = Teacher.objects.all().prefetch_related('students')
        return context





