import logging

# Configure the logging
logging.basicConfig(level=logging.DEBUG,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
                    handlers=[logging.StreamHandler()])  # Output to console (you can add FileHandler for file output)

# Create a logger instance
logger = logging.getLogger(__name__)

# Logging different levels of messages
#logger.debug("This is a debug message")
#logger.info("This is an info message")
#logger.warning("This is a warning message")
#logger.error("This is an error message")
#logger.critical("This is a critical message")
