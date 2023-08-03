from pathlib import Path
from rich.prompt import Confirm, Prompt
from src import logger
from src.utils.llms import get_chain
from src.agents.base_cowriter_agent import BaseCowriterAgent


class InteractiveCowriterAgent(BaseCowriterAgent):
    def __init__(
        self,
        topic,
        model_name="gpt3.5",
        model_temperature=0.8,
        output_folder="src/answers/",
        listicle_sections=None,
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
        self.listicle_sections = listicle_sections
        logger.info("Starting CowriterAgent in interactive mode")

    def _run_chain_on_query(self, input_query: str):
        response = self.chain.run(input_query)
        return response

    def write_section(
        self,
        section_type,
        return_response,
        default_value,
    ):
        if section_type == "intro":
            input_query = self._prepare_query_for_introduction()
        elif section_type == "conclusion":
            input_query = self._prepare_query_for_conclusion()
        else:
            input_query = Prompt.ask(
                "What do you want to write in the next section?",
                default=default_value,
            )

        self._log_section_title(section_type, input_query)

        response = self._run_chain_on_query(input_query)
        response = self._format_section(
            section_type,
            response,
            input_query,
        )

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

    def run(self):
        introduction = self.write_section(
            section_type="intro",
            return_response=True,
            default_value=None,
        )

        if self.listicle_sections is None:
            sections = self._generate_sections(introduction)
        else:
            sections = self.listicle_sections

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

        self.write_section(
            section_type="conclusion",
            return_response=False,
            default_value=None,
        )
