import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from src import logger
from src.utils.llms import generate_sections_from_introduction, get_chain


class CowriterAgent(object):
    def __init__(self, topic, output_folder="src/answers/", autopilot=False):
        self.topic = topic
        self.autopilot = autopilot
        self.chain = get_chain(use_streaming=True)
        self.console = Console()
        self.file_name = os.path.join(
            output_folder,
            f"{self.topic}_{str(datetime.now().replace(microsecond=0))}.md",
        )
        if self.autopilot:
            logger.info("starting CowriterAgent in autopilot mode")

    def run_chain_on_query(
        self,
        input_query: str,
    ):
        with get_openai_callback() as cb:
            response = self.chain.run(input_query)
            self.total_cost += cb.total_cost
        return response

    def write_section(
        self,
        section_type=None,
        return_response=True,
        default_value=None,
    ):
        if section_type == "intro":
            prompt_introduction = PromptTemplate(
                input_variables=["topic"],
                template=Path("src/prompts/introduction.prompt").read_text(),
            )
            input_query = prompt_introduction.format(topic=self.topic)
        else:
            if self.autopilot:
                if default_value is not None:
                    input_query = default_value
                else:
                    raise ValueError("`default_value` must be set in autopilot mode")
            else:
                input_query = Prompt.ask(
                    "What do you want to write in the next section?",
                    default=default_value,
                )

        if self.autopilot:
            if section_type == "intro":
                logger.info("generating introduction")
            else:
                logger.info(f"generating the following section: {default_value}")

        response = self.run_chain_on_query(input_query)

        if self.autopilot:
            is_happy = True
        else:
            is_happy = Confirm.ask(
                "\n\nAre you happy with the answer?",
                default=True,
            )
            while not is_happy:
                refine_query = Prompt.ask("Tell us how to improve it")
                response = self.run_chain_on_query(refine_query)
                is_happy = Confirm.ask(
                    "Are you happy with the answer?",
                    default=True,
                )

        if self.autopilot:
            save = True
        else:
            save = Confirm.ask(
                "Great, would you like to save this answer to a file?",
                default=True,
            )

        if save:
            with open(self.file_name, "a") as f:
                f.write(response)

        if return_response:
            return response

    def run(self):
        introduction = self.write_section(section_type="intro", return_response=True)

        with self.console.status(
            "Extracting the sections of the article ... \n",
            spinner="aesthetic",
            speed=1.5,
            spinner_style="red",
        ):
            with get_openai_callback() as cb:
                sections = generate_sections_from_introduction(introduction)
                self.total_cost += cb.total_cost

        if self.autopilot:
            for section in sections:
                self.write_section(default_value=section)

        else:
            add_section = Confirm.ask("Add a section ?", default=True)
            section_number = 0
            while add_section:
                self.write_section(
                    default_value=sections[section_number]
                    if section_number < len(sections)
                    else None
                )
                add_section = Confirm.ask(
                    "Add a section ?",
                    default=True,
                )
                section_number += 1
