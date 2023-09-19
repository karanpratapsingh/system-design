class Level():

    def __init__(self, name = 'Default', board_size = '30', music_theme = 'Fresh') -> None:
	    self.name = name
	    self.board_size = board_size
	    self.music_theme = music_theme

    def get_board_size(self):
        return self.board_size
    
    def get_name(self):
        return self.name

    def get_music_theme(self):
        return self.music_theme