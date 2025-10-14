from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, groups_list_create, groups_join, group_messages, groups_delete, groups_edit, message_detail, groups_leave, frontend_homework, frontend_homework_preview, homework_list_create, homework_detail, homework_like, homework_comment_create, homework_comment_delete, quizzes_folders_list_create, quizzes_folder_detail, quizzes_in_folder, quizzes_list_create, quizzes_detail, quizzes_in_folder_v2, quiz_submit_attempt, quiz_leaderboard, my_quiz_attempts, schedule_list_create, schedule_detail, notifications_list, notification_mark_read
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('users/<int:pk>', ProfileView.as_view(), name='profile'),
    # Groups
    path('groups', groups_list_create, name='groups_list_create'),
    path('groups/<int:pk>/join', groups_join, name='groups_join'),
    path('groups/<int:pk>/delete', groups_delete, name='groups_delete'),
    path('groups/<int:pk>/edit', groups_edit, name='groups_edit'),
    path('groups/<int:pk>/leave', groups_leave, name='groups_leave'),
    path('groups/<int:pk>/messages', group_messages, name='group_messages'),
    path('messages/<int:pk>', message_detail, name='message_detail'),
    # Homework
    path('homework', homework_list_create, name='homework_list_create'),
    path('homework/<int:pk>', homework_detail, name='homework_detail'),
    path('homework/<int:pk>/like', homework_like, name='homework_like'),
    path('homework/<int:pk>/comments', homework_comment_create, name='homework_comment_create'),
    path('homework/comments/<int:pk>', homework_comment_delete, name='homework_comment_delete'),
    # Dev preview (unauthenticated) for visual styling checks only
    path('homework/preview/', frontend_homework_preview, name='homework_preview'),
    # Quizzes: folders and quizzes within a folder
    path('quizzes/folders', quizzes_folders_list_create, name='quizzes_folders_list_create'),
    path('quizzes/folders/<int:pk>', quizzes_folder_detail, name='quizzes_folder_detail'),
    path('quizzes/folders/<int:pk>/quizzes', quizzes_in_folder_v2, name='quizzes_in_folder_v2'),
    # quizzes
    path('quizzes', quizzes_list_create, name='quizzes_list_create'),
    path('quizzes/<int:pk>', quizzes_detail, name='quizzes_detail'),
    path('quizzes/<int:pk>/attempt', quiz_submit_attempt, name='quiz_submit_attempt'),
    path('quizzes/<int:pk>/leaderboard', quiz_leaderboard, name='quiz_leaderboard'),
    path('quizzes/my-activity', my_quiz_attempts, name='my_quiz_attempts'),

    # Schedule events
    path('schedule/', schedule_list_create, name='schedule_list_create'),
    path('schedule/<int:pk>/', schedule_detail, name='schedule_detail'),
    # Notifications
    path('notifications', notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/read', notification_mark_read, name='notification_mark_read'),
]
