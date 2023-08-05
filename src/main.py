from rich.prompt import Prompt, Confirm
from rich.console import Console
from src import logger
from src.utils.config import ContentConfig
from src.utils.display import intro, set_temperature

intro()

console = Console()
with console.status(
    "Importing the right packages ...\n",
    spinner="aesthetic",
    speed=1.5,
    spinner_style="red",
):
    from src.utils.llms import generate_topic_from_listicle_sections
    from src.agents.auto_cowriter_agent import AutoCowriterAgent
    from src.agents.interactive_cowriter_agent import InteractiveCowriterAgent


def main():
    is_listicle = Confirm.ask(
        "[bold purple]Is the article a listicle[bold purple/]",
        default=False,
    )

    if is_listicle:
        topic = None
        listicle_sections = []
        add_listicle_section = True
        section_number = 0
        while add_listicle_section:
            listicle_section = Prompt.ask(f"Section {section_number+1}")
            listicle_sections.append(listicle_section)
            section_number += 1
            add_listicle_section = Confirm.ask(
                "[bold purple]Add a listicle section [bold purple/]",
                default=True,
            )

        with console.status(
            "Generating topic from this list",
            spinner="aesthetic",
            speed=1.5,
            spinner_style="red",
        ):
            topic = generate_topic_from_listicle_sections(listicle_sections)

        console.print(f"[red bold]Generated topic: {topic}[red bold/]")

    else:
        topic = Prompt.ask(
            f"[bold purple]Type in a topic you are interested to write about 🖊️ [bold purple/]",
        )
        listicle_sections = None

    content_config = ContentConfig(
        is_listicle=is_listicle,
        topic=topic,
        listicle_sections=listicle_sections,
    )

    model_name = Prompt.ask(
        "[bold purple]Pick a model[bold purple/]",
        choices=["gpt3.5", "gpt4"],
        default="gpt3.5",
    )

    model_temperature = set_temperature()

    autopilot = Confirm.ask(
        "[bold purple]Use autopilot mode[bold purple/]",
        default=False,
    )

    if autopilot:
        cowriter_agent = AutoCowriterAgent(
            content_config=content_config,
            model_name=model_name,
            model_temperature=model_temperature,
            save_to_disk=True,
        )
    else:
        cowriter_agent = InteractiveCowriterAgent(
            content_config=content_config,
            model_name=model_name,
            model_temperature=model_temperature,
        )

    cowriter_agent.run()

    save_as_gist = Confirm.ask(
        "[bold purple]Save as Github Gist[bold purple/]",
        default=True,
    )
    if save_as_gist:
        cowriter_agent.save_as_gist()

    write_to_airtable = Confirm.ask(
        "[bold purple]Write to Airtable[bold purple/]",
        default=True,
    )
    if write_to_airtable:
        cowriter_agent.write_to_airtable()

    logger.info("Exiting Cowriter 👋")


if __name__ == "__main__":
    main()
