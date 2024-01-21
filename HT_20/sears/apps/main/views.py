from django.shortcuts import render
from django.views.generic import ListView

from apps.main.models import Task


def index(request):
    return render(request, 'main/index.html', {'title': 'Home Page'})


class TaskListView(ListView):
    model = Task
    template_name = 'main/task.html'
    extra_context = {'title': 'Tasks'}
    context_object_name = 'tasks_list'
# def task(request):
#     return render(request, 'main/task.html', {'title': 'Task'})


def page_not_found(request, exception):
    return render(request, 'main/page_not_found.html')
