from Register16bit import Register16bit
from Register8bit import Register8bit

A, B, C, D, E, F, H, L, AF, BC, DE, HL, SP, PC = range(14)


class GB_Registers(list):

    def __init__(self):
        for i in xrange(8):
            self.append(Register8bit())

        self.append(Register16bit(self[A], self[F]))
        self.append(Register16bit(self[B], self[C]))
        self.append(Register16bit(self[D], self[E]))
        self.append(Register16bit(self[H], self[L]))
        self.append(Register16bit())
        self.append(Register16bit())

    def INC_8bit(self, value):
        """Determines flags status after 8-bit INC operation"""
        if value == 0xff:
            self[F].OR(0x80)
        else:
            self[F].AND(0xff - 0x80)
        if value & 0xf == 0xf:
            self[F].OR(0x20)
        else:
            self[F].AND(0xff - 0x20)
        self[F].AND(0xff - 0x40)
        return value + 1

    def DEC_8bit(self, value):
        """Determines flags status after 8-bit DEC operation"""
        if value == 0x1:
            self[F].OR(0x80)
        else:
            self[F].AND(0xff - 0x80)
        if value & 0xf == 0x0:
            self[F].OR(0x20)
        else:
            self[F].AND(0xff - 0x20)
        self[F].OR(0x40)
        return  value - 1

    def RLC_8bit(self, value):
        if value & 0x80 == 0x80:
            self[F].OR(0x10)
        else:
            self[F].AND(0xff - 0x80)

        if value == 0x0:
            self[F].OR(0x80)
        else:
            self[F].AND(0xff - 0x80)

        self[F].AND(0xff - 0x40)
        self[F].AND(0xff - 0x20)
        return (value << 1) | ((self[F].Get() & 0x10) >> 4)

    def ADD_16bit(self, v1, v2):
        if v1 + v2 > 0xffff:
            self[F].OR(0x10)
        else:
            self[F].AND(0xff - 0x10)
        if (v1 & 0xfff) + (v2 & 0xfff) > 0xfff:
            self[F].OR(0x20)
        else:
            self[F].AND(0xff - 0x20)
        self[F].AND(0xff - 0x40)

        return v1 + v2

    def RRC_8bit(self, value):
        if value & 0x80 == 0x80:
            self[F].OR(0x10)
        else:
            self[F].AND(0xff - 0x80)

        if value == 0x0:
            self[F].OR(0x80)
        else:
            self[F].AND(0xff - 0x80)



if __name__ == '__main__':

    reg = GB_Registers()

    reg[A].Set(0x56)
    reg[F].Set(0xf8)
    print hex(reg[AF].Get())

    reg[AF].Set(0x7654)
    print hex(reg[A].Get())
    print hex(reg[F].Get())


    for i in xrange(len(reg)):
        reg[i].Set(i + 1)
        print reg[i].Get()

    print 'ok'

    for i in reg:
        print i.Get()