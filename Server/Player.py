import typing
import requests

#track number of players created and give them a unique number id
player_id = 0

class Player:
    def __init__(self, link):
        global player_id
        
        #player's unique id
        self.id = player_id
        
        #link to player's AI
        self.link = link
        
        #increment player_id for next player created
        player_id += 1
        
        self.name = self.get_name()
    
    #function that gets move player will make with game_state
    def get_move(self, game_state : typing.Dict):
        
        
        #try to get name
        if self.name == None:
            self.name = self.get_name()
        

        # Send the request
        try:
            response = requests.post(self.link+"move", json=game_state, headers={'Content-Type': 'application/json'}, timeout=0.5)
            
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
