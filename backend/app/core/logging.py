import logging
import sys

# Configure logging
def setup_logging(log_level=logging.INFO):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

# Create a logger
logger = logging.getLogger(__name__)

# Example usage
if __name__ == "__main__":
    setup_logging()
    logger.info("Logging is set up.")