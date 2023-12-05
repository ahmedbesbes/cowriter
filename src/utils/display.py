from rich.console import Console

console = Console()


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
- Support for listicles (sections and corresponding prompts)
- Web search to indentify candidate topics
- Data saving to Github Gist

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
