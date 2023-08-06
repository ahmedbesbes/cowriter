from pathlib import Path
from langchain.callbacks import get_openai_callback
from src import logger
from src.utils.config import ContentConfig
from src.utils.llms import get_chain
from src.agents.base_cowriter_agent import BaseCowriterAgent


class AutoCowriterAgent(BaseCowriterAgent):
    def __init__(
        self,
        content_config: ContentConfig,
        model_name,
        model_temperature,
        save_to_disk,
        output_folder="answers/",
        write_intro_only=False,
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
        self.save_to_disk = save_to_disk
        self.write_intro_only = write_intro_only
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
        response = self._format_section(
            section_type,
            response,
            default_value,
        )

        if self.save_to_disk:
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
        if not self.write_intro_only:
            if self.listicle_sections is None:
                sections = self._generate_sections(introduction)
            else:
                sections = self.listicle_sections

            for section in sections:
                self.write_section(
                    default_value=section,
                    return_response=False,
                    section_type="section",
                )

        self.write_section(
            default_value=Path("src/prompts/conclusion.prompt").read_text(),
            return_response=False,
            section_type="conclusion",
        )
