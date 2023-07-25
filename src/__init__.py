import logging
import click
from dotenv import load_dotenv
from rich.logging import RichHandler
from src.utils.display import intro

load_dotenv()

LOGGER_NAME = "cowriter"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])],
)
logger = logging.getLogger(LOGGER_NAME)
logging.getLogger("numexpr").setLevel(logging.ERROR)

intro()
