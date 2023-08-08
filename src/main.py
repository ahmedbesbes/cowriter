from rich.prompt import Prompt, Confirm
from src import logger
from src.utils.display import get_content_config, intro, set_temperature
from src.agents.auto_cowriter_agent import AutoCowriterAgent
from src.agents.interactive_cowriter_agent import InteractiveCowriterAgent

intro()


def main():
    content_config = get_content_config()

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
