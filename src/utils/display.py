from rich.console import Console


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
        """,
        style="bold",
    )

    console.print(
        """
______________________________________________________________________________________________
    """,
        style="red bold",
    )
