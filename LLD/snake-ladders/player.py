class Player():

    def __init__(self, username) -> None:
        self.username = username
        self.position = 0
    
    def get_username(self):
        return self.username
    
    def get_position(self):
        return self.positoin