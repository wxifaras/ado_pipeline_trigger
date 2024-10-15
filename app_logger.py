import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

instrumentation_key = os.getenv('APP_INSIGHTS_INSTRUMENTATION_KEY')

# Function to set up and return the logger
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Ensure the handler is not added multiple times
        logger.setLevel(logging.INFO)
        handler = AzureLogHandler(connection_string=f'InstrumentationKey={instrumentation_key}')
        logger.addHandler(handler)
    return logger