from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from src.utils.llms import get_chain


class CowriterAgent(object):
    def __init__(self, topic):
        self.total_cost = 0
        self.topic = topic
        self.chain = get_chain(use_streaming=True)
        self.console = Console()
        self.file_name = (
            f"src/answers/{self.topic}_{str(datetime.now().replace(microsecond=0))}.md"
        )

    def generate_section(
        self,
        input_query: str,
    ):
        with get_openai_callback() as cb:
            response = self.chain.run(input_query)
            self.total_cost += cb.total_cost
        return response

    def write_section(self, section_type=None):
        if section_type == "intro":
            prompt_introduction = PromptTemplate(
                input_variables=["topic"],
                template=Path("src/prompts/introduction.prompt").read_text(),
            )
            input_query = prompt_introduction.format(topic=self.topic)
            spinner_message = "Generating introduction ..."
        else:
            input_query = Prompt.ask("What do you want to write in the next section?")
            spinner_message = "Generating section ..."

        response = self.generate_section(input_query)

        is_happy = Confirm.ask(
            "\n\nAre you happy with the answer?",
            default=True,
        )
        while not is_happy:
            refine_query = Prompt.ask("Tell us how to improve it")
            response = self.generate_section(refine_query)
            is_happy = Confirm.ask(
                "Are you happy with the answer?",
                default=True,
            )

        save = Confirm.ask(
            "Great, would you like to save this answer to a file?",
            default=True,
        )

        if save:
            with open(self.file_name, "a") as f:
                f.write(response)

    def run(self):
        self.write_section(section_type="intro")
        add_section = Confirm.ask("Add a section ?", default=True)
        while add_section:
            self.write_section()
            add_section = Confirm.ask("Add a section ?", default=True)
