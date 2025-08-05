import logging

# Configure root logger (only once)
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Create and expose a shared logger
logger = logging.getLogger("my logger")  


