from rich.console import Console
from rich.prompt import Prompt, Confirm
from src.utils.config import ContentConfig


console = Console()
with console.status(
    "Importing the right packages ...\n",
    spinner="aesthetic",
    speed=1.5,
    spinner_style="red",
):
    from src.utils.llms import generate_topic_from_listicle_sections


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
- Automatic extraction and recommendation of the article sections
- Data saving to Airtable / Github Gist

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


def get_content_config() -> ContentConfig:
    is_listicle = Confirm.ask(
        "[bold purple]Is the article a listicle[bold purple/]",
        default=False,
    )

    if is_listicle:
        load_sections_from_file = Confirm.ask("Load sections from file", default=False)

        if load_sections_from_file:
            file_path = Prompt.ask("Enter path")
            with open(file_path, "r") as f:
                listicle_sections = f.readlines()
                listicle_sections = [section.strip() for section in listicle_sections]

        else:
            listicle_sections = []
            add_listicle_section = True
            section_number = 0
            while add_listicle_section:
                section = Prompt.ask(
                    f"Section {section_number+1} (enter empty string to quit)"
                )
                if section.strip() != "":
                    listicle_sections.append(section)
                    section_number += 1
                else:
                    add_listicle_section = False

        console.print(f"listicle sections : {listicle_sections}")

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
    return content_config
