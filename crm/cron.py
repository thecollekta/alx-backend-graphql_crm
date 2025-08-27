# alx-backend-graphql_crm/crm/cron.py

"""
CRM Cron Jobs

This module contains scheduled tasks for the CRM application.
"""

import logging
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)


def log_crm_heartbeat():
    """
    Log a heartbeat message and verify GraphQL endpoint is responsive.
    This function is called every 5 minutes by django-crontab.
    """
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

        # Log heartbeat
        message = f"{timestamp} CRM is alive"
        print(message)  # This will be captured by the cron log

        # Verify GraphQL endpoint
        try:
            transport = RequestsHTTPTransport(
                url="http://localhost:8000/graphql/"
            )
            client = Client(
                transport=transport, fetch_schema_from_transport=True
            )

            # Simple query to verify GraphQL is working
            query = gql("""
                query {
                    __schema {
                        types {
                            name
                        }
                    }
                }
            """)

            # Execute the query
            result = client.execute(query)
            if result:
                logger.info("GraphQL endpoint is responsive")

        except Exception as e:
            logger.error(f"Error connecting to GraphQL endpoint: {str(e)}")

    except Exception as e:
        logger.error(f"Error in heartbeat logging: {str(e)}")
        raise
