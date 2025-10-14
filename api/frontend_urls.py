from django.urls import path
from .views import frontend_login, dashboard, frontend_groups, frontend_homework, frontend_quizzes, frontend_quizzes_folder, frontend_quiz_take, frontend_schedule

urlpatterns = [
    path('', frontend_login, name='frontend_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('groups/', frontend_groups, name='frontend_groups'),
    path('homework/', frontend_homework, name='frontend_homework'),
    path('quizzes/', frontend_quizzes, name='frontend_quizzes'),
    path('quizzes/<int:pk>/', frontend_quizzes_folder, name='frontend_quizzes_folder'),
    path('quizzes/<int:pk>/take/', frontend_quiz_take, name='frontend_quiz_take'),
    path('schedule/', frontend_schedule, name='frontend_schedule'),
]
