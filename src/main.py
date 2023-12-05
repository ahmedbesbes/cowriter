from rich.prompt import Confirm
from src import logger
from src.utils.display import intro
from src.utils.menu import get_content_config, get_model_name, get_temperature
from src.agents.auto_cowriter_agent import AutoCowriterAgent
from src.agents.interactive_cowriter_agent import InteractiveCowriterAgent

intro()


def main():
    content_config = get_content_config()
    model_name = get_model_name()
    model_temperature = get_temperature()

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

    logger.info("Exiting Cowriter 👋")


if __name__ == "__main__":
    main()
