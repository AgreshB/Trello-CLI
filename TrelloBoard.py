import requests
import json

#
# Class that has the Trello board an its data 
#
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


    # ALL API END POINTS ARE MARKED AS  @API

    #### @API
    def get_available_board_ID(self):
        # returns list of boards 

    # SETS current board to use
    def set_board_ID(self):
        # sets board id to use for all other requests
        # changes self.auth["idBoard"] to current board id


    #### @API
    def get_available_lists(self):
        # returns list on current board

    # Choose list we wish to add the card into
    def choose_list(self):
        # choose list to add card to
        # returns list id
    

    # Labels : base would be hard coded to start
    def choose_label(self):
        # choose label to add to card
        # returns label id

    
    #### @API
    def post_comment(self,card_id):
        # add comment to card
        # card_id is id of card to add comment to
        #  comment is only signle line comment ???

        # returns comment id

    # add comment to card
    def add_comment(self, card_id):  
        # card_id is id of card to add comment to
        #  comment is only signle line comment ???


    # Main function to create a card
    # using all other helpers to get data
    def create_card(self):
        # create card on current board
        # get list id, card name, card description, card label
        # returns card id

    # Helpers to have

    #### @API
    def delete_single_card(self,card_id):
        # delete signle card

    def print_card(self, card):
        # print card details
        # card is card json object

    def get_all_cards(self):
        # returns all cards on current board


            
    def delete_cards(self):
        # delete one or more cards on current board