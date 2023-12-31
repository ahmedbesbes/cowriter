import logging
import click
from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()

LOGGER_NAME = "cowriter"
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])],
)
logger = logging.getLogger(LOGGER_NAME)
logging.getLogger("numexpr").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
