from dotenv import load_dotenv
from rich.prompt import Prompt
from src.utils.cowriter_agent import CowriterAgent
from src.utils.display import intro

load_dotenv()


def main():
    intro()
    topic = Prompt.ask(
        f"[bold purple]Type in a topic you are interested to write about 🖊️ [bold purple/]",
        default="python decorators",
    )

    cowriter_agent = CowriterAgent(topic)
    cowriter_agent.run()


if __name__ == "__main__":
    main()
