from Registerxbit import Registerxbit
from Register8bit import Register8bit


class Register16bit(Registerxbit):
    def __init__(self, h=None, l=None):
        Registerxbit. __init__(self)
        self.h = h
        if not h:
            self.h = Register8bit()

        self.l = l
        if not l:
            self.l = Register8bit()

    def Get(self):
        return (self.h.Get() << 8) | self.l.Get()

    def Set(self, value):
        self.l.Set(value)
        self.h.Set((value >> 8))



    # def Add(self, value):
    #     if self.l.Get() + (0xff & value) > 0xff:
    #         value += 0x100
    #     self.l.Add(value)
    #     self.h.Add(value >> 8)

if __name__ == '__main__':
    a = Register16bit()
    a.Set(0xf856)
    print hex(a.Get())
    print hex(a.h.Get())
    print hex(a.l.Get())
    a.Add(0xffff)
    print hex(a.Get())