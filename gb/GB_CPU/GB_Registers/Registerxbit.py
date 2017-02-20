
class Registerxbit():
    def __init__(self):
        pass

    def Get(self):
        pass

    def Set(self, value):
        pass

    def Add(self, value):
        self.Set(self.Get() + value)

    def XOR(self, value):
        self.Set(self.Get() ^ value)

    def OR(self, value):
        self.Set(self.Get() | value)

    def AND(self, value):
        self.Set(self.Get() & value)

