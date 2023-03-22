import requests
import json

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

The class has following methods for creation of cards:
    - choose_list() : returns the ID of the list the user wants to use
    - choose_label() : returns the ID of the label the user wants to use
   
    - add_comment() : adds a comment to the card

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
            print(f"Error with URL : {response.status_code}")

    # SETS current board to use
    # for all other requests
    # changes self.auth["idBoard"] to current board id
    def set_board_ID(self):
        available_boards = self.get_available_board_ID()
        print('Which board would you like to use?')
        for i in range(len(available_boards)):
            print(f'{i + 1}. {list(available_boards.keys())[i]}')
        reply = -1
        total = range(len(available_boards))
        while True:
            reply = int(input('Enter Board number :')) - 1
            if reply not in total:
                print('Please enter an appropriate value.')
            else:
                break
        board_id = available_boards[list(available_boards.keys())[reply]]
        self.auth['idBoard'] = board_id


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
        print('Which list would you like to add a card to? Choose a number below.')
        for i in range(len(lists)):
            print(f'{i + 1}. {lists[i]["name"]}')
        reply = -1
        total = range(len(lists))
        while True:
            reply = int(input('Enter List number :')) - 1
            if reply not in total:
                print('Please enter an appropriate value.')
            else:
                break

        return lists[reply]["id"]
    

    # Labels : base would be hard coded to start
    # choose label to add to card
    # returns label id
    def choose_label(self):
        print('What would you like to label this card as? Please choose a number.\n')
        print("1. General\n")
        print("2. Completed\n")
        print("3. Current\n")
        print("4. Tod Do\n")

        color = ['blue', 'green', 'yellow', 'red']
        reply = -1
        total = range(4)
        while True:
            reply = int(input('Enter Label number :')) - 1
            if reply not in total:
                print('Please enter an appropriate value.')
            else:
                break
        return color[reply]

    
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
            print('Comment Posted Successfully')
        else:
            print(f' Error in Comment : {response.status_code}')
       

    # add Mutiple comments to card
    # card_id is id of card to add comment to
    def add_comment(self, card_id):  
        while True:
            try:
                reply = input('Would you like to add a comment to the card? ( Y/N )\n')
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
        data['idList'] = self.choose_list()

        # enter card details
        card_name = input('Please Enter Card title?\n')
        data['name'] = card_name

        # Any desc ?
        card_desc = input('Please Enter Card Description (Press enter to skip):\n')
        if card_desc:
            data['desc'] = card_desc

        # label for the card
        data['labels'] = [self.choose_label()]

        # create the card
        card_url = self.url + "/cards"   
        response = requests.post(url=card_url, data=data)
        if response.status_code == 200:
            card_id = json.loads(response.text)["id"]
            # if successfull add a comment
            self.add_comment(card_id)
        else:
            print(response.status_code)
        

    # Helpers to have

    #### @API
    def delete_single_card(self,card_id):
        # delete signle card
        return

    def print_card(self, card):
        # print card details
        # card is card json object
        return

    def get_all_cards(self):
        # returns all cards on current board
        return
            
    def delete_cards(self):
        # delete one or more cards on current board 
        return