import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from pyairtable import Table
from src import logger
from src.utils.llms import generate_sections_from_introduction, get_chain


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


class InteractiveCowriterAgent(BaseCowriterAgent):
    def __init__(
        self,
        topic,
        model_name="gpt3.5",
        model_temperature=0.8,
        output_folder="src/answers/",
    ):
        super().__init__(
            topic,
            model_name,
            model_temperature,
            output_folder,
        )
        self.chain = get_chain(
            self.model_name,
            temperature=self.model_temperature,
            use_streaming=True,
        )
        logger.info("Starting CowriterAgent in interactive mode")

    def _run_chain_on_query(self, input_query: str):
        response = self.chain.run(input_query)
        return response

    def run(self):
        introduction = self.write_section(
            section_type="intro",
            return_response=True,
            default_value=None,
        )
        sections = self._generate_sections(introduction)

        add_section = Confirm.ask("Add a section ?", default=True)
        section_number = 0
        while add_section:
            self.write_section(
                default_value=sections[section_number]
                if section_number < len(sections)
                else None,
                section_type="section",
                return_response=False,
            )
            add_section = Confirm.ask(
                "Add a section ?",
                default=True,
            )
            section_number += 1

    def write_section(
        self,
        section_type,
        return_response,
        default_value,
    ):
        if section_type == "intro":
            input_query = self._prepare_query_for_introduction()
        else:
            input_query = Prompt.ask(
                "What do you want to write in the next section?",
                default=default_value,
            )

        self._log_section_title(section_type, default_value)

        response = self._run_chain_on_query(input_query)

        is_happy = Confirm.ask(
            "\n\nAre you happy with the answer?",
            default=True,
        )
        while not is_happy:
            refine_query = Prompt.ask("\n\nTell us how to improve it")
            response = self._run_chain_on_query(refine_query)
            is_happy = Confirm.ask(
                "\n\nAre you happy with the answer?",
                default=True,
            )

        save = Confirm.ask(
            "\n\nGreat, would you like to save this answer to a file?",
            default=True,
        )

        if save:
            with open(self.file_name, "a") as f:
                f.write(response)

        self._add_section_to_saved_data(section_type, response)

        if return_response:
            return response


class AutoCowriterAgent(BaseCowriterAgent):
    def __init__(
        self,
        topic,
        model_name,
        model_temperature,
        save_to_disk,
        output_folder="src/answers/",
    ):
        super().__init__(
            topic,
            model_name,
            model_temperature,
            output_folder,
        )
        self.chain = get_chain(
            self.model_name,
            temperature=self.model_temperature,
            use_streaming=True,
        )
        self.save_to_disk = save_to_disk
        self.chain = get_chain(
            self.model_name,
            temperature=self.model_temperature,
            use_streaming=False,
        )
        logger.info("Starting CowriterAgent in autopilot mode")

    def _run_chain_on_query(self, input_query: str):
        with self.console.status(
            "Writing :pen: ...\n",
            spinner="aesthetic",
            speed=1.5,
            spinner_style="red",
        ):
            with get_openai_callback() as cb:
                response = self.chain.run(input_query)
                self.total_cost += cb.total_cost

        logger.info(f"TOTAL COST : {self.total_cost}")
        return response

    def run(self):
        introduction = self.write_section(
            section_type="intro",
            return_response=True,
            default_value=None,
        )
        sections = self._generate_sections(introduction)
        for section in sections:
            self.write_section(
                default_value=section,
                return_response=False,
                section_type="section",
            )

    def write_section(
        self,
        section_type,
        return_response,
        default_value,
    ):
        if section_type == "intro":
            input_query = self._prepare_query_for_introduction()
        else:
            input_query = default_value

        self._log_section_title(section_type, default_value)
        response = self._run_chain_on_query(input_query)

        if self.save_to_disk:
            with open(self.file_name, "a") as f:
                f.write(response)

        self._add_section_to_saved_data(section_type, response)

        if return_response:
            return response
