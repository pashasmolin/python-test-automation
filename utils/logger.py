import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("my logger")  


