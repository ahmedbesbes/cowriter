from dotenv import load_dotenv
from rich.prompt import Prompt, Confirm
from src.utils.display import intro, set_temperature
from src.utils.cowriter_agent import AutoCowriterAgent, InteractiveCowriterAgent

load_dotenv()


def main():
    intro()
    topic = Prompt.ask(
        f"[bold purple]Type in a topic you are interested to write about 🖊️ [bold purple/]",
        default="python decorators",
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
            topic=topic,
            model_name=model_name,
            model_temperature=model_temperature,
            save_to_disk=True,
        )
    else:
        cowriter_agent = InteractiveCowriterAgent(
            topic=topic,
            model_name=model_name,
            model_temperature=model_temperature,
        )

    cowriter_agent.run()

    write_to_airtable = Confirm.ask(
        "[bold purple]Write to Airtable[bold purple/]",
        default=True,
    )
    if write_to_airtable:
        cowriter_agent.write_to_airtable()


if __name__ == "__main__":
    main()
