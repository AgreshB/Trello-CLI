from TrelloBoard import TrelloBoard
from TrelloBoard import console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table

key = ''
token = ''


console.clear()
console.print(Panel(" [bold red] WELCOME TO TRELLO [/]", title="Welcome", title_align="center", border_style="bold purple" , highlight=True,expand= False, padding=(1, 10)))
print("\n\n")
trello = TrelloBoard(key, token)


# need to create menu
table = Table("Select Action to Perform", expand = False ,padding = (0,3))
table.add_row("1. Create Card")
table.add_row("2. Delete Card")


while True:
    console.clear()
    console.print(Panel(" [bold red] WELCOME TO TRELLO [/]", title="Welcome", title_align="center", border_style="bold purple" , highlight=True,expand= False, padding=(1, 10)))
    console.print(table)

    option = Prompt.ask("Enter Option (q to exit)", choices = ["1","2","q"], default = "1" , show_default = False)
    if option == "q":
        break
    elif option == "1":
        console.clear()
        trello.create_card()
    elif option == "2":
        console.clear()
        trello.delete_cards()

console.clear()
console.print(Panel(" [bold red] CLOSING TRELLO CLI :wave: [/]", title="Thank you", title_align="center", border_style="bold purple" , highlight=True,expand= False, padding=(1, 10)))
