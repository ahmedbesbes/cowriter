from rich.console import Console
from rich.prompt import Prompt

console = Console()


def print_ai_message(message: str):
    console.print(f"🤖 : {message}", style="bold red")


def intro():
    console.print(
        """
______________________________________________________________________________________________

 ██████╗ ██████╗ ██╗    ██╗██████╗ ██╗████████╗███████╗██████╗ 
██╔════╝██╔═══██╗██║    ██║██╔══██╗██║╚══██╔══╝██╔════╝██╔══██╗
██║     ██║   ██║██║ █╗ ██║██████╔╝██║   ██║   █████╗  ██████╔╝
██║     ██║   ██║██║███╗██║██╔══██╗██║   ██║   ██╔══╝  ██╔══██╗
╚██████╗╚██████╔╝╚███╔███╔╝██║  ██║██║   ██║   ███████╗██║  ██║
 ╚═════╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝                                                               
    """,
        style="red bold",
    )

    console.print(
        """
Cowriter is your assistant in writing kickass blog post introductions and more :bulb:

How it works? 

- Type in something you're interested to write about
- Configure the Cowriter agent 
- Let the agent write for you

Functionalities:

- Custom prompts
- Interactive or autopilot writing modes
- Data saving to Airtable

This tool is built with Langchain :parrot: and OpenAI :rocket:. It's meant to help you build drafts
quickly. 
        """,
        style="bold",
    )

    console.print(
        """
______________________________________________________________________________________________
    """,
        style="red bold",
    )


def set_temperature():
    is_valid = False
    i = 0
    while not is_valid:
        if i == 0:
            prompt_message = "[bold purple]Set model temperature[bold purple/]"
        else:
            prompt_message = "[bold purple]Set model temperature[bold purple/][bold red] (between 0 and 1)[bold red/]"

        model_temperature = Prompt.ask(
            prompt_message,
            default="0.8",
        )

        try:
            model_temperature = float(model_temperature)
            if model_temperature > 1 or model_temperature < 0:
                is_valid = False
            else:
                is_valid = True
        except ValueError:
            is_valid = False

        i += 1
    return model_temperature
