# ALX Backend GraphQL CRM

A Django-based CRM system built following modern Django development standards and best practices with
GraphQL API integration.

## Project Overview

This project demonstrates the integration of GraphQL with Django using `graphene-django`, implementing
a clean, modular architecture leveraging GraphQL's flexible querying capabilities.

---

## Features

### 1. GraphQL API

- **Query** and **mutate** data with a single endpoint
- **Strongly-typed** schema with clear input validations
- **Real-time** data fetching with subscriptions (coming soon)

### 2. Core Models

- **Customers**: Manage customer information with contact details
- **Products**: Track product inventory and pricing
- **Orders**: Handle customer orders with product associations

### 3. Advanced Features

- **Bulk Operations**: Create multiple customers in a single request
- **Data Validation**: Comprehensive input validation and error handling
- **Filtering & Sorting**: Powerful query capabilities with filtering and ordering
- **Pagination**: Efficient data loading with cursor-based pagination
- **Automated Maintenance**: Scheduled cleanup of inactive customers (no orders in the past year)
- **Health Monitoring**: 5-minute heartbeat logging to verify system health
- **Inventory Management**: Automatic restocking of low-inventory products (stock < 10)

## Technology Stack

- **Framework** : Django 5.2+
- **GraphQL** : graphene-django
- **Database** : PostgreSQL (recommended) / SQLite (development)
- **Python** : 3.12
- **Task Scheduling**: django-crontab

---

## Project Structure

```text
alx-backend-graphql_crm/
├── alx_backend_graphql_crm/
│   ├── __init__.py
│   ├── asgi.py
│   ├── schema.py              # GraphQL schema definition
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL configuration
│   └── wsgi.py
├── crm/
│   ├── migrations/
│   ├── cron_jobs/
│   │   ├── clean_inactive_customers.sh    # Script for cleaning up inactive customers
│   │   ├── customer_cleanup_crontab.txt   # Crontab configuration for the cleanup job
│   │   ├── order_reminders_crontab.txt    # Crontab configuration for the reminders job
│   │   └── send_order_reminders.py        # Script for sending order reminders
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── cron.py                            # Scheduled tasks including the heartbeat logger
│   ├── models.py
│   ├── schema.py              # CRM-specific GraphQL schema
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/alx-backend-graphql_crm.git
    cd alx-backend-graphql_crm
    ```

2. Create and activate virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Configure environment variables

    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    ```

5. Run Migrations

    ```bash
    python manage.py makemigrations
    python manage.py migrate

6. Create superuser (optional)

    ```bash
    python manage.py createsuperuser
    ```

7. Start Development Server

    ```bash
    python manage.py runserver
    ```

8. Access GraphiQL interface

    ```bash
    http://localhost:8000/graphql/ or http://127.0.0.1:8000/graphql/
    ```

---

## Automated Maintenance

### Customer Cleanup Job

The system includes an automated maintenance script to clean up inactive customers. This script:

- Runs every Sunday at 2:00 AM (configurable)
- Removes customers who haven't placed any orders in the past year
- Logs all cleanup activities to `/tmp/customer_cleanup_log.txt`

To set up the cron job:

```bash
# Make the script executable
chmod +x crm/cron_jobs/clean_inactive_customers.sh

# Install the crontab (run as the user that will execute the job)
crontab crm/cron_jobs/customer_cleanup_crontab.txt
```

To manually run the cleanup:

```bash
./crm/cron_jobs/clean_inactive_customers.sh
```

### Order Reminder Job

The system includes an automated script to send reminders for recent orders. This script:

- Runs daily at 8:00 AM (configurable)
- Queries the GraphQL API for orders from the past 7 days
- Logs order details to `/tmp/order_reminders_log.txt`
- Can be extended to send email/SMS notifications

To set up the cron job:

```bash
# Install required Python packages
pip install gql requests

# Make the script executable
chmod +x crm/cron_jobs/send_order_reminders.py

# Install the crontab (run as the user that will execute the job)
crontab crm/cron_jobs/order_reminders_crontab.txt
```

### Heartbeat Logger

The system includes a health monitoring feature that:

- Runs every 5 minutes
- Logs system status to `/tmp/crm_heartbeat_log.txt`
- Verifies GraphQL endpoint responsiveness
- Tracks system uptime and health

To set up the heartbeat monitoring:

```bash
# Install the crontab entries
python manage.py crontab add

# Start the cron service (if not already running)
sudo service cron start

# Check active cron jobs
python manage.py crontab show
```

To view the heartbeat log:

```bash
tail -f /tmp/crm_heartbeat_log.txt
```

### Low Stock Alerts & Auto-Restocking

The system includes an automated inventory management feature that:

- Runs every 12 hours
- Identifies products with stock levels below 10
- Automatically restocks these products by adding 10 units
- Logs all restocking activities to `/tmp/low_stock_updates_log.txt`

#### Example Log Entry

```bash
2025-08-27 10:00:00 - Successfully restocked 3 products:

Widget A (New stock: 15)
Widget B (New stock: 12)
Widget C (New stock: 18)
```

#### GraphQL Mutation

The system provides a `updateLowStockProducts` mutation that can be called manually if needed:

```graphql
mutation {
  updateLowStockProducts {
    success
    message
    updatedProducts
  }
}
```

### Log Files

The system maintains several log files for monitoring and debugging:

- `/tmp/crm_heartbeat_log.txt`: System health and uptime monitoring
- `/tmp/low_stock_updates_log.txt`: Product restocking activities
- `/tmp/order_reminders_log.txt`: Order reminder processing logs
- `/tmp/customer_cleanup_log.txt`: Inactive customer cleanup logs

---

## CRM Report Generation with Celery

This document provides instructions for setting up and running the Celery task system for generating
weekly CRM reports.

### Prerequisites

- Python 3.13+
- Redis server
- Django project dependencies

### Installation

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

---

## API Documentation

### Example Queries

#### Get all customers

```graphql
{
  allCustomers {
    edges {
      node {
        id
        name
        email
        phone
      }
    }
  }
}
```

#### Filter products by price range

```graphql
{
  allProducts(filter: { priceGte: 100, priceLte: 1000 }) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Example Mutations

#### Create a new customer

```graphql
mutation {
  createCustomer(input: {
    name: "John Doe",
    email: "<john@example.com>",
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
    }
    message
    success
  }
}
```

#### Create a new order

```graphql
mutation {
  createOrder(input: {
    customerId: "1",
    productIds: ["1", "2"]
  }) {
    order {
      id
      customer {
        name
      }
      products {
        name
        price
      }
      totalAmount
    }
    message
    success
  }
}
```

### Filtering Capabilities

#### Customers

- Filter by name (case-insensitive)
- Filter by email (case-insensitive)
- Filter by creation date range
- Filter by phone number pattern

#### Products

- Filter by name (case-insensitive)
- Filter by price range
- Filter by stock level
- Find low stock items

#### Orders

- Filter by total amount range
- Filter by order date range
- Filter by customer name
- Filter by product name or ID

### Development

#### Running Tests

```bash
python manage.py test
```

---

## Testing the Setup

### 1. Accessing GraphQL

1. **GraphiQL Interface** : Visit <http://localhost:8000/graphql/>
2. **GraphQL Endpoint** : `POST` requests to <http://localhost:8000/graphql/>

### 2. Run Your First Query

In the GraphiQL interface, run:

```graphql
{
  hello
}
```

Expected response:

```json
{
  "data": {
    "hello": "Hello, GraphQL!"
  }
}
```

### CRM Status Query

```graphql
{
  crmStatus
}
```

Expected response:

```json
{
  "data": {
    "crmStatus": "CRM module is ready for GraphQL operations"
  }
}
```

---

## License

This project is developed for educational purposes as part of the ALX Software Engineering Backend
Specialization program.

---
