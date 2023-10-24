# TaskHero Project

TaskHero is a web application that helps you manage and track your and your team's tasks and projects efficiently. This README provides an overview of the project structure, installation steps, and usage instructions.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Technologies](#technologies)
- [License](#license)

## Introduction

TaskHero is a project management tool that allows you to create, manage, and track tasks and projects. It provides features such as task creation, task assignment, due dates, tags, comments, and more.

## Features

- User authentication and registration
- Dashboard view to track overall tasks
- Task creation, editing, and deletion
- Assigning tasks to different users
- Adding due dates and tags to tasks
- Commenting on tasks for collaboration
- Calendar view for a visual representation of tasks
- Profile management and settings

## Getting Started

### Prerequisites

- Python (3.6 or higher)
- Django (3.0 or higher)
- SQLite or other database backend
- Git (for version control)
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/urte-baj/taskhero.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
python manage.py migrate
```

4. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the application at http://localhost:8000 in your web browser.

## Technologies

* Django: Web framework for building the application.
* Bootstrap: Front-end framework for styling.
* SQLite: Database management system for storing data.
* Python: Programming language used for server-side logic.
* HTML, CSS, JavaScript: Languages for building user interfaces.

## License

This project is licensed under the MIT License.
