import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from pyairtable import Table
from src import logger
from src.utils.llms import generate_sections_from_introduction


class BaseCowriterAgent(object):
    def __init__(
        self,
        topic,
        model_name="gpt3.5",
        model_temperature=0.8,
        output_folder="src/answers/",
    ):
        self.topic = topic
        self.model_name = model_name
        self.model_temperature = model_temperature
        self.total_cost = 0
        self.console = Console()
        self.creation_date = str(datetime.now().replace(microsecond=0))
        self.output_folder = output_folder
        self.file_name = os.path.join(
            output_folder,
            f"{self.topic}_{self.creation_date}.md",
        )
        self.saved_data = {
            "topic": self.topic,
            "date": self.creation_date,
        }

    def _prepare_query_for_introduction(self):
        prompt_introduction = PromptTemplate(
            input_variables=["topic"],
            template=Path("src/prompts/introduction.prompt").read_text(),
        )
        input_query = prompt_introduction.format(topic=self.topic)
        return input_query

    def _generate_sections(self, introduction: str):
        with self.console.status(
            "Extracting the sections of the article ... \n",
            spinner="aesthetic",
            speed=1.5,
            spinner_style="red",
        ):
            with get_openai_callback() as cb:
                sections = generate_sections_from_introduction(introduction)
                self.total_cost += cb.total_cost
        return sections

    def _log_section_title(self, section_type: str, default_value: str):
        if section_type == "intro":
            logger.info("generating introduction")
        else:
            logger.info(f"generating the following section: {default_value}")

    def _add_section_to_saved_data(self, section_type, response):
        if section_type == "intro":
            self.saved_data["introduction"] = response
            self.saved_data["full_content"] = response + "\n"
        else:
            self.saved_data["full_content"] = (
                self.saved_data["full_content"] + "\n" + response
            )

    def write_to_airtable(self):
        logger.info("Saving to Airtable ... 💾 ")
        self.saved_data["cost"] = self.total_cost
        api_key = os.environ["AIRTABLE_API_KEY"]
        base_id = os.environ["AIRTABLE_BASE_ID"]
        table = Table(
            api_key=api_key,
            base_id=base_id,
            table_name="articles",
        )
        table.create(self.saved_data)
        logger.info("Data saved to Airtable ... ✅")