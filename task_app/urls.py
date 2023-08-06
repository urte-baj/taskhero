from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # ----------------- Home page ---------------------- #
    # -------------------------------------------------- #
    path('', views.home, name='index'),

    # ----------------- Register a user ---------------- #
    # -------------------------------------------------- #
    path('register/', views.register, name='register'),

    # ----------------- Log in a user ------------------ #
    # -------------------------------------------------- #
    path('login/', views.user_login, name='login'),

    # ----------------- Log out a user ----------------- #
    # -------------------------------------------------- #
    path('accounts/logout/', views.user_logout, name='user-logout'),

    # ----------------- Dashboard page ----------------- #
    # -------------------------------------------------- #
    path('dashboard/', views.dashboard, name='dashboard'),

    # ----------------- Create a task ------------------ #
    # -------------------------------------------------- #

    path('create-task', views.createTask, name='create-task'),

    # ----------------- View tasks -------------------- #
    # ------------------------------------------------- #

    path('view-tasks', views.viewTask, name='view-tasks'),

    # ----------------- Update a task ------------------ #
    # -------------------------------------------------- #

    path('update-task/<str:pk>/', views.updateTask, name='update-task'),

    # ----------------- Delete a task ------------------ #
    # -------------------------------------------------- #

    path('delete-task/<str:pk>/', views.deleteTask, name='delete-task'),

    # ----------------- User profile ------------------- #
    # -------------------------------------------------- #

    path('profile/', views.profile, name='profile'),

    # ----------------- Update user profile ------------ #
    # -------------------------------------------------- #

    path('update-profile/', views.update_profile, name='update-profile'),

    # ----------------- Search view -------------------- #
    # -------------------------------------------------- #
    path('search/', views.search, name='search'),

    # ----------------- Task calendar ------------------ #
    # -------------------------------------------------- #
    path('get_tasks/', views.get_tasks, name='get_tasks'),

    path('calendar/', views.calendar, name='calendar'),

    # ----------------- Task detail view --------------- #
    # -------------------------------------------------- #

    path('task-detail/<str:pk>/', views.task_detail, name='task-detail'),

    # ----------------- Password reset views ----------- #
    # -------------------------------------------------- #
    path('accounts/', include('django.contrib.auth.urls')),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
