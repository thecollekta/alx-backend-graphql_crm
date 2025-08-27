# CRM Report Generation with Celery

This document provides instructions for setting up and running the Celery task system for generating
weekly CRM reports.

## Prerequisites

- Python 3.13+
- Redis server
- Django project dependencies

## Installation

1. **Install Redis**
   - On Ubuntu/Debian:

     ```bash
     sudo apt update
     sudo apt install redis-server
     ```

   - On macOS (using Homebrew):

     ```bash
     brew install redis
     brew services start redis
     ```

   - On Windows:
     - Download Redis for Windows from: <https://github.com/tporadowski/redis/releases>
     - Follow the installation instructions

2. **Install Python Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Database Migrations**

   ```bash
   python manage.py migrate
   ```

## Running the Application

1. **Start Redis Server**
   - Linux/macOS:

     ```bash
     redis-server
     ```

   - Windows: Start the Redis service or run `redis-server.exe`

2. **Start Celery Worker**
   In a new terminal window:

   ```bash
   celery -A crm worker -l info
   ```

3. **Start Celery Beat**
   In another terminal window:

   ```bash
   celery -A crm beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

4. **Start Django Development Server**
   In a separate terminal window:

   ```bash
   python manage.py runserver
   ```

## Verifying the Setup

1. The Celery worker should show a message indicating it's ready to accept tasks.
2. The Celery Beat should show the schedule for the CRM report task.
3. The report will be generated every Monday at 6:00 AM and logged to `/tmp/crm_report_log.txt`

## Manually Triggering the Report

To manually trigger the report generation, you can use the Django shell:

```bash
python manage.py shell
```

Then run:

```python
from crm.tasks import generate_crm_report
generate_crm_report.delay()

# Results
# <AsyncResult: 3d94cd66-a424-4930-84d1-4ae154ca997d>
```

## Viewing Logs

Check the report logs at:

```bash
/tmp/crm_report_log.txt
```

## Troubleshooting

- If the worker doesn't start, ensure Redis is running.
- Check for any error messages in the terminal where the worker is running.
- Verify that all dependencies are installed correctly.
- Ensure the log directory (`/tmp/`) is writable by the application.
