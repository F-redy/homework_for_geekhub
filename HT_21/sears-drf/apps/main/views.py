from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from apps.main.models import Task


def index(request):
    return render(request, 'main/index.html', {'title': _('Home Page')})


class TaskListView(ListView):
    model = Task
    template_name = 'main/task.html'
    extra_context = {'title': _('Tasks')}
    context_object_name = 'tasks_list'


def page_not_found(request, exception):
    return render(request, 'main/page_not_found.html', context={'message': _('Page Not Found')})
