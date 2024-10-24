import typing
import requests


#if player name cannot be found, set name
PLAYER_UNKNOWN_NAME = "MISSING DATA"


class Player:
    def __init__(self, link):

        #player's unique id
        self.id = None
        
        #player's tournament seed
        #set later
        self.seed = None
        
        #link to player's AI
        if link[-1] != '/':
            link = link + "/"
        self.link = link
        
        #player score for tournament
        self.points = 0
        
        #name to use if name == None
        self.standin_name = PLAYER_UNKNOWN_NAME
        self.name = self.get_name()
    
    def __repr__(self):
        string = "Player: " + self.name + ". ID = " + str(self.id)
        return string
        
        
    #function that gets move player will make with game_state
    def get_move(self, game_state : typing.Dict):
        
        
        #try to get name
        if self.name == None:
            self.name = self.get_name()
        

        # Send the request
        try:
            
            response = requests.post(self.link+"move", json=game_state, headers={'Content-Type': 'application/json'}, timeout=2)
            
            # Check if the response is successful
            if response.status_code == 200:
                return response.json().get('move')
            else:
                #upon request rejection, return a move of 0
                return 0
            
        #upon request failure, return a move of 1
        except requests.exceptions.RequestException as e:
            return 1

        #upon request timeout, return a move of 2
        except requests.exceptions.Timeout as e:
            return 2
        
    def get_name(self):
        # Send the request
        try:
            response = requests.get(self.link, headers={'Content-Type': 'application/json'}, timeout=0.5)
            
            # Check if the response is successful
            if response.status_code == 200:
                return response.json().get('name')
            else:
                #upon request rejection, return a move of 0
                return None
            
        #upon request failure, return a move of 1
        except requests.exceptions.RequestException as e:
            return None

        #upon request timeout, return a move of 2
        except requests.exceptions.Timeout as e:
            return None