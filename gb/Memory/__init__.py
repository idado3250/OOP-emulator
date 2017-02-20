
class Memory(bytearray):
    def __init__(self, size):
        bytearray.__init__(self, size)

    def rb(self, address):
        return self[address]

    def rw(self, address):
        return (self[address] | (self[address + 1] << 8))

    def wb(self, address, value):
        self[address] = value

    def ww(self, address, value):
        self[address] = value & 0xff
        self[address + 1] = (value >> 8) & 0xff


if __name__ == '__main__':
    a = Memory(0xffff)
    a.wb(0x7f09, 0x30)
    a.wb(0x7f0a, 0x41)
    print hex(a.rw(0x7f09))
    a.ww(0x7f09, 0x3344)
    print hex(a.rw(0x7f09))
    print hex(a[0x7f09])
    print type(a[3])