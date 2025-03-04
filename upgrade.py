# upgrade.py

class Upgrade:
    def __init__(self, cost, name, blurb, execute, image):
        self.cost = cost
        self.name = name
        self.blurb = blurb  # List of strings for extra details.
        self.execute = execute  # A function that modifies the game state.
        self.button_pos = None  # To be set by the UI during drawing.
        self.image = image

    def update_pos(self, new_rect):
        self.button_pos = new_rect
