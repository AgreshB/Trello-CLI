import requests
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

#
# Class that has the Trello board an its data 
#

'''
# ALL API END POINTS ARE MARKED AS  @API
The class has the following API:
    - get_available_board_ID() : returns a dictionary of all the boards the user has access to
    - set_board_ID() : sets the board ID to use for the rest of the API
    - get_available_lists() : returns a list of all the lists in the board
    - post_comment() : posts a comment to the card
    - delete_single_card() : deletes a single card
    - get_all_cards() : returns a list of all the cards in the board

The class has following methods for creation of cards:
    - choose_list() : returns the ID of the list the user wants to use
    - choose_label() : returns the ID of the label the user wants to use
    - add_comment() : add one or more comments to the card
    - create_card() : creates a card in the board

'''
class TrelloBoard:
    def __init__(self, key, token, board_id = None):
        # set auth data for all requests
        self.auth = {'key': key, 'token': token}
        self.url = "https://api.trello.com/1"
        self.headers = {
            'type': "type",
            'content-type': "application.json"
        }
        # first need to choose which board to use
        self.board_name = None
        self.set_board_ID()

    #### @API
    # returns list of boards 
    def get_available_board_ID(self):
        board_url = self.url + '/members/me/boards'
        board_data = {}
        data = self.auth.copy()
        response = requests.get(url=board_url, data=data)
        if response.status_code == 200:
            board_json = json.loads(response.text)
            for board in board_json:
                board_data[board['name']] = board['id']
            return board_data
        else:
            console.print(f"{response.status_code} : No board found or all boards are closed")

    # SETS current board to use
    # for all other requests
    # changes self.auth["idBoard"] to current board id
    def set_board_ID(self):
        available_boards = self.get_available_board_ID()
        if available_boards == None:
            console.print("Please create a board first and then run this program again ! Bye :wave:")
            exit(0)
            return


        # Table to display all the boards
        table = Table(title="Which board would you like to use?" , expand = False ,padding = (0,3))
        table.add_column("Board Number" , style="bold cyan" , justify="right") 
        table.add_column("Board Name" , justify="center")

        for i in range(len(available_boards)):
            table.add_row(f'{i + 1}', f'{list(available_boards.keys())[i]}')

        console.print(table)

        reply = Prompt.ask("Enter Board number" , choices = [str(i) for i in range(1,len(available_boards)+1)] , show_choices = False)
        reply = int(reply) -1
        console.clear()
        
        board_name = list(available_boards.keys())[reply]
        self.auth['idBoard'] = available_boards[board_name]
        self.board_name = board_name


    #### @API
    # returns list on current board
    def get_available_lists(self):
        data = self.auth.copy()
        list_url = self.url + '/boards/' + self.auth["idBoard"] + '/lists'
        response = requests.get(url=list_url, data=data)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(response.status_code)
    
    # Choose list we wish to add the card into
    # returns list id
    def choose_list(self):
        lists = self.get_available_lists()
        # Table of Options
        table = Table(title="Which list would you like to add a card to?" , expand = False ,padding = (0,3))
        table.add_column("List No." , style="bold cyan" , justify="right") 
        table.add_column("List Name" , justify="center")
        for i in range(len(lists)):
            table.add_row(f'{i + 1}', f'{lists[i]["name"]}')
        console.print(table)
        
        # Using promt to get user input
        reply = Prompt.ask("Enter List number" , choices = [str(i) for i in range(1,len(lists)+1)] , show_choices = False)
        reply = int(reply) -1
        return lists[reply]["id"] , lists[reply]["name"]


    def get_available_labels(self):
        data = self.auth.copy()
        label_url = self.url + '/boards/' + self.auth["idBoard"] + '/labels'
        response = requests.get(url=label_url, data=data)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(response.status_code)

    
    # Labels : Now dynamically generated
    # choose label to add to card
    # returns label id
    def choose_label(self):
        labels = self.get_available_labels()
        table = Table(title="Which label would you like to add to this card?" , expand = False ,padding = (0,3))
        table.add_column("Label No." , style="bold cyan" , justify="right")
        table.add_column("Label" , justify="center")

        if len(labels) == 0:
            table.add_row("[blue]1", "General")
            table.add_row("[green]2", "Completed")
            table.add_row("[yellow]3", "Current")
            table.add_row("[red]4", "To Do")
            console.print(table)

            color = ['blue', 'green', 'yellow', 'red']
            total = 4
        else:
            total = len(labels)
            for i in range(total):
                table.add_row(f'{i + 1}', f'[{labels[i]["color"]}]{labels[i]["color"]} {labels[i]["name"]}')
            color = []
            for i in range(len(labels)):
                color.append(labels[i]["color"])

        console.print(table)

        reply = -1
        result = []
        while True:
            reply = input('Enter Label number(s) (Enter mutiple labels seperated by ,)')
            result = [int(x) -1 for x in str(reply).split(',')]
            if any(x < 0 or x > total for x in result):
                console.print('Please enter an appropriate value.')
                continue
            else:

                break
        return [color[x] for x in result]


    #### @API
    # add comment to card
    # card_id is id of card to add comment to
    # currently only signle line comment
    def post_comment(self,card_id):
        data = self.auth.copy()
        text = input('Please enter your comment text (Press enter to post):\n')
        data['text'] = text
        comment_url = self.url + "/cards/" + card_id + "/actions/comments"
        response = requests.post(url=comment_url, params=data)
        if response.status_code == 200:
            console.print('Comment Posted Successfully :thumbs_up: \n\n')
        else:
            console.print(f' Error in Comment : {response.status_code}')
    
    # add Mutiple comments to card
    # card_id is id of card to add comment to
    def add_comment(self, card_id):  
        while True:
            try:
                reply = input('Would you like to add a any comments to the card? (Y/N)\n')
                if reply.lower() == 'y' or reply.lower() == 'yes':
                    self.post_comment(card_id)
                elif reply.lower() == 'n' or  reply.lower() == 'no':
                    return
            except EOFError:
                break

    # Main function to create a card on Current board
    # using all other helpers to get data
    def create_card(self):
        data = self.auth.copy()
        # choose the list to add the card to
        data['idList'] , list_name = self.choose_list()

        console.clear()
        console.print(Panel(f"[red] Adding Card to Board : [underline bold white]{self.board_name}[/] \n list : [underline bold white]{list_name}[/] [/]", border_style="bold purple" , highlight=True,expand= False, padding=(1, 10)))

        # enter card details
        card_name = input('Please Enter Card title?\n')
        data['name'] = card_name

        # Any desc ?
        card_desc = input('Please Enter Card Description (Press enter to skip):\n')
        if card_desc:
            data['desc'] = card_desc

        # label for the card
        data['labels'] = self.choose_label()

        # create the card
        card_url = self.url + "/cards"   
        response = requests.post(url=card_url, data=data)
        if response.status_code == 200:
            card_id = json.loads(response.text)["id"]
            console.clear()
            console.print('Card Created Successfully  :D')
            # if successfull add a comment
            self.add_comment(card_id)
        else:
            print(response.status_code)


    # Helpers Nice to have

    #### @API
    # delete signle card
    def delete_single_card(self,card_id):
        url = self.url + "/cards/" + card_id
        data = self.auth.copy()
        response = requests.request("DELETE", url, params=data)
        if response.status_code != 200:
            console.print(f'Error in deleting card : {response.status_code}')
            return False
        return True

    # print card details
    # card is card json object
    def print_card(self, card):
        all_labels = [lab["color"] for  lab in card["labels"]]
        return f'Card ID : {card["id"]}', f'Name : {card["name"]}  Label: {all_labels}'

    #### @API
    # returns all cards on current board
    def get_all_cards(self):
        data = self.auth.copy()
        card_url = self.url + "/boards/" + self.auth["idBoard"] + "/cards"
        response = requests.get(url=card_url, data=data)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(response.status_code)
    

    # delete one or more cards on current board 
    def delete_cards(self):
        #need to make sur eit is called after choosing a board
        cards = self.get_all_cards()
        if not cards:
            console.print('No cards found')
            return

        table = Table(title=f"Cards on given Board {self.board_name}" , expand = False ,padding = (0,3))
        table.add_column("Card no." , style="bold cyan" , justify="right")
        table.add_column("Card id."  , justify="center")
        table.add_column("Card details" , justify="center")
        for i in range(len(cards)):
            c_id , c_dets = self.print_card(cards[i])
            table.add_row(f'{i + 1}', c_id, c_dets)

        table.add_row(f'{i+2}', 'Delete All Cards')
        console.print(table)

        reply = -1
        total = range(len(cards)+ 1)
        while True:
            reply = int(input('Enter Card number to delete (Or 0 to exit):')) - 1

            if reply == -1:
                return
            if reply not in total:
                console.print('Please enter an appropriate value.')
            else:
                break

        if reply == len(cards):
            for card in cards:
                self.delete_single_card(card["id"])
        else:
            self.delete_single_card(cards[reply]["id"])
        
        console.print('Card Deleted Successfully')