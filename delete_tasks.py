from task_app.models import Task
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskhero.settings')
django.setup()

def delete_all_tasks():
    Task.objects.all().delete()
    print('All tasks have been deleted.')

if __name__ == '__main__':
    delete_all_tasks()
