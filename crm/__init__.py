# crm/__init__.py

"""
CRM Application Package

This package contains the Customer Relationship Management functionality
for the alx_backend_graphql_crm project.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)

default_app_config = "crm.apps.CrmConfig"
