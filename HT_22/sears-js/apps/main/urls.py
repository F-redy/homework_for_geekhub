from apps.main import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('task/', views.TaskListView.as_view(), name='task'),
]
