# alx-backend-graphql_crm/crm/cron.py

"""
CRM Cron Jobs

This module contains scheduled tasks for the CRM application.
"""

import logging
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("/tmp/crm_heartbeat_log.txt"),
        logging.StreamHandler(),
    ],
)
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
        logger.info(message)

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


def update_low_stock():
    """
    Update low-stock products via GraphQL mutation.
    Runs every 12 hours.
    """
    try:
        from gql import gql, Client
        from gql.transport.requests import RequestsHTTPTransport
        import logging

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            handlers=[
                logging.FileHandler("/tmp/low_stock_updates_log.txt"),
                logging.StreamHandler(),
            ],
        )
        logger = logging.getLogger(__name__)

        # GraphQL mutation
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    success
                    message
                    updatedProducts
                }
            }
        """)

        # Execute the mutation
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql/")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        result = client.execute(mutation)

        # Log the results
        if result.get("updateLowStockProducts", {}).get("success"):
            updated = result["updateLowStockProducts"]["updatedProducts"]
            logger.info(
                f"Successfully updated {len(updated)} products: {', '.join(updated)}"
            )
        else:
            logger.error(
                f"Failed to update products: {result.get('message', 'Unknown error')}"
            )

    except Exception as e:
        logger.error(f"Error in update_low_stock: {str(e)}")
        raise
