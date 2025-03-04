class Worker:
    def __init__(self, worker_id, image):
        self.worker_id = worker_id
        self.clickingXP = 0
        self.clickingLevel = 0
        self.miningXP = 0
        self.miningLevel = 0
        self.miningBase = 0.1
        self.current_activity = "Mining"
        self.itemLimit = 1
        self.items = []
        self.button = None
        self.name = "John Doe"
        self.icon = "N/A"
        self.image = image

    def calculate_val(self):
        return (self.miningLevel + 1) * self.miningBase

    def page(self):
        return (self.worker_id // 45) + 1

    def update_pos(self, new_rect):
        self.button = new_rect
