from Registerxbit import Registerxbit

class Register8bit(Registerxbit):
    def __init__(self):
        Registerxbit. __init__(self)
        self.__value = 0

    def Get(self):
        return self.__value

    def Set(self, value):
        self.__value = value & 0xff

    # def Add(self, value):
    #     self.__value += value
    #     self.__value &= 0xff

if __name__ == '__main__':

    a = Register8bit()
    a.Insert(0x56)
    print hex(a.Get())
    print type(a.Get())
