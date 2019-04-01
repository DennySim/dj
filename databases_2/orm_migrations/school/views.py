from django.views.generic import ListView

from .models import Student, Teacher


class StudentListView(ListView):
    model = Student
    ordering = 'group'

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all()
        return context


