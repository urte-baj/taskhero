from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CreateUserForm, LoginForm, UserUpdateForm, ProfileUpdateForm, CreateTaskForm, TaskFilterForm, \
    CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from .models import Task, Comment
from django.db.models import Q, Max
from datetime import date, timedelta
import logging
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.db import connection


def home(request):
    return render(request, 'index.html')

# --- Register view


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "You have registered successfully!")
            return redirect('login')

    context = {'form': form}

    return render(request, 'registration/register.html', context=context)

# --- Login view


def user_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            # logger = logging.getLogger(__name__)
            # logger.debug(f"Username: {username}, Password: {password}")
            print(f"Received form data - Username: {username}, Password: {password}")

            if user is not None:
                auth.login(request, user)
                messages.success(request, "Login successful.")
                return redirect('dashboard')
            else:
                print(f"Received form data - Username: {username}, Password: {password}")

                messages.error(request, "Invalid username or password.")


    context = {'form': form}
    return render(request, 'registration/login.html', context=context)


# --- Dashboard view

@login_required(login_url='user_login')
def dashboard(request):
    comments = Comment.objects.order_by('-posted_date')[:2]
    tasks = {
        'todo': Task.objects.filter(status='todo'),
        'in_progress': Task.objects.filter(status='in_progress'),
        'done': Task.objects.filter(status='done')
    }
    context = {'tasks': tasks, 'comments': comments}

    return render(request, 'user_profile/dashboard.html', context)


# --- Create task

@login_required(login_url='user_login')
def createTask(request):
    form = CreateTaskForm()

    if request.method == 'POST':
        form = CreateTaskForm(request.POST)

        if form.is_valid():
            print('Form is valid')
            task = form.save(
                commit=False)  # form is ready to be saved but is paused before commiting so we could link the user to the task
            task.user = request.user
            task.save()
            form.save_m2m()

            print(form.cleaned_data['tags'])
            messages.success(request, "Task created successfully!")

            return redirect('view-tasks')

        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'user_profile/create-task.html', context=context)


# --- View all tasks (current user)

@login_required(login_url='user_login')
def viewTask(request):
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks': tasks,
        'user': request.user,
    }

    return render(request, 'user_profile/view-tasks.html', context=context)


# --- Update task

@login_required(login_url='user_login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = CreateTaskForm(instance=task)

    if request.method == "POST":
        form = CreateTaskForm(request.POST, instance=task)

        if form.is_valid():
            print('Form is updated!')
            task = form.save(commit=False)
            task.save()
            form.save_m2m()

            return redirect('view-tasks')

        else:
            form = CreateTaskForm(instance=task)

    context = {'form': form}

    return render(request, 'user_profile/update-task.html', context=context)


# --- Delete task

@login_required(login_url='user_login')
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == "POST":
        task.delete()

        return redirect('view-tasks')

    return render(request, 'user_profile/delete-task.html', {'task': task})


# --- Logout a user

def user_logout(request):
    auth.logout(request)
    messages.success(request, "You have been successfully logged out!")
    return redirect('index')


# --- Profile page

@login_required(login_url='login')
def profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'user_profile/profile.html', context)


# --- Update profile view

@login_required(login_url='login')
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
    }
    return render(request, 'user_profile/update_profile.html', context=context)

# --- Search view

@login_required(login_url='login')
def search(request):
    query = request.GET.get('query')

    # Perform the search query
    tasks = Task.objects.filter(
        Q(content__icontains=query) |
        Q(title__icontains=query) |
        Q(tags__name__icontains=query) |
        Q(assignee__username__icontains=query)
    ).distinct()

    context = {
        'tasks': tasks,
        'query': query
    }
    return render(request, 'user_profile/search_results.html', context)

# --- All tasks (all users) calendar/month view

@login_required(login_url='login')
def calendar(request):
    today = date.today()
    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))

    # Retrieve tasks for the selected month and year
    tasks = Task.objects.filter(
        due_date__year=selected_year,
        due_date__month=selected_month
    ).order_by('due_date')

    context = {
        'tasks': tasks,
        'selected_month': selected_month,
        'selected_year': selected_year,
    }

    return render(request, 'user_profile/calendar.html', context)

def calendar_test(request):
    return render(request, 'test-calendar.html')


def get_tasks(request):
    tasks = Task.objects.all()
    events = []
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
        '#1f78b4', '#ff7f00', '#33a02c', '#e31a1c', '#f781bf',
        '#c51b7d', '#fdbf6f', '#6a3d9a', '#ff7f00', '#b15928'
    ]  # Define a list of colors to choose from

    for idx, task in enumerate(tasks):
        event = {
            'title': task.title,
            'start': task.date_posted.strftime('%Y-%m-%d'),
            'end': task.due_date.strftime('%Y-%m-%d'),
            'color': colors[idx % len(colors)],  # Assign a different color to each task
            # Add other event properties as needed
        }
        events.append(event)

    return JsonResponse(events, safe=False)

# --- Task detail view

def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    comments = Comment.objects.filter(task=task).order_by('-posted_date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(task=task, user=request.user, text=form.cleaned_data['text'])
            comment.save()
            return redirect('task-detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'task': task,
        'comments': comments,
        'form': form
    }
    return render(request, 'user_profile/task-detail.html', context)
