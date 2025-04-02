import logging # flexible framework for emitting log messages from Python programs
import sys # provides access to some variables used or maintained by the interpreter

print(f"2. working in file /discord/app/utils/logging.py)")

# Function to set up logging configuration
def setup_logging():
    logging.basicConfig(
        level=logging.INFO, # Set the logging level to INFO
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)], # Output logs to stdout (console)
    )

# Create a logger instance with the name "chat_api"
logger = logging.getLogger("chat_api")
