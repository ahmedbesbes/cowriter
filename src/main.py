from dotenv import load_dotenv
from rich.prompt import Prompt, Confirm
from src.utils.cowriter_agent import CowriterAgent
from src.utils.display import intro

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

    autopilot = Confirm.ask(
        "[bold purple]Use autopilot mode[bold purple/]",
        default=False,
    )

    cowriter_agent = CowriterAgent(
        topic,
        model_name=model_name,
        autopilot=autopilot,
    )
    cowriter_agent.run()


if __name__ == "__main__":
    main()
