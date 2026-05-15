class HashEntry:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

        # Флаги
        self.C = 0
        self.U = 0
        self.T = 0
        self.L = 0
        self.D = 0

    def clear(self):
        self.key = None
        self.value = None

        self.C = 0
        self.U = 0
        self.T = 0
        self.L = 0
        self.D = 0