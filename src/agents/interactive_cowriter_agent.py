from rich.prompt import Confirm, Prompt
from src import logger
from src.utils.config import ContentConfig
from src.utils.llms import get_chain
from src.agents.base_cowriter_agent import BaseCowriterAgent


class InteractiveCowriterAgent(BaseCowriterAgent):
    def __init__(
        self,
        content_config: ContentConfig,
        model_name="gpt3.5",
        model_temperature=0.8,
        output_folder="data/answers/",
    ):
        super().__init__(
            content_config,
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

    def write_section(
        self,
        section_type,
        return_response,
        section_data,
    ):
        if section_type == "intro":
            input_query = self._prepare_query_for_introduction()
            section_topic = None
        elif section_type == "conclusion":
            input_query = self._prepare_query_for_conclusion()
            section_topic = None
        else:
            if self.is_listicle:
                section_topic = section_data["section_topic"]
                section_prompt = section_data["section_prompt"]
            else:
                section_topic = section_data
                section_prompt = section_data

            input_query = Prompt.ask(
                "What do you want to write in the next section?",
                default=section_prompt,
            )

        self._log_section_title(
            section_type=section_type,
            title=section_topic,
        )

        response = self._run_chain_on_query(input_query)
        response = self._format_section(
            section_type=section_type,
            text=response,
            header=section_topic,
        )

        is_happy = Confirm.ask(
            "[bold red]\n\nAre you happy with the answer?[bold red]",
            default=True,
        )
        while not is_happy:
            refine_query = Prompt.ask(
                "[bold red]\n\nTell us how to improve it[bold red/]"
            )
            response = self._run_chain_on_query(refine_query)
            response = self._format_section(
                section_type=section_type,
                text=response,
                header=section_topic,
            )

            is_happy = Confirm.ask(
                "[bold red]\n\nAre you happy with the answer?[bold red/]",
                default=True,
            )

        save = Confirm.ask(
            "[bold red]\n\nGreat, would you like to save this answer to a file?[bold red/]",
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
            section_data=None,
        )

        if self.listicle_sections is None:
            sections = self._generate_sections(introduction)
        else:
            sections = self.listicle_sections

        add_section = Confirm.ask("[bold red]Add a section ?[bold red/]", default=True)
        section_number = 0
        while add_section:
            if self.is_listicle and section_number >= len(sections):
                logger.info("Done writing the sections")
                break

            self.write_section(
                section_data=sections[section_number]
                if section_number < len(sections)
                else None,
                section_type="section",
                return_response=False,
            )
            add_section = Confirm.ask(
                "[bold red]Add a section ?[bold red/]",
                default=True,
            )
            section_number += 1

        self.write_section(
            section_type="conclusion",
            return_response=False,
            section_data=None,
        )
