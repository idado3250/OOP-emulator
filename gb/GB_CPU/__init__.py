from CPU import CPU
from GB_Registers import *
from msvcrt import *
from Memory import Memory


class GB_CPU(CPU):

    def __init__(self):
        self.__memory = Memory(0xffff)
        self.__reg = GB_Registers()
        self.__clock = {'cc': 0, 'mc': 0}  # clock cycles and machine cycles, 1 mc = 4 cc.
        self.__opcode = None

        self.__opcodeDict = {  # opcode lenght, cycles taken, function. All opcodes are documented in the GB manual.
            # 0x00:
            0x00: (1, 4, lambda: None),  # NOP
            0x01: (3, 12, lambda: self.__reg[BC].Set(self.__memory.rw(self.__reg[PC].Get()))),  # LD BC, nn
            0x02: (1, 8, lambda: self.__memory.wb(self.__reg[BC].Get(), self.__reg[A].Get())),  # LD (BC), A
            0x03: (1, 8, lambda: self.__reg[BC].Add(1)),  # INC BC
            0x04: (1, 4, lambda x=self.__reg[B]: x.Set(self.__reg.INC_8bit(x.Get()))),  # INC B
            0x05: (1, 4, lambda x=self.__reg[B]: x.Set(self.__reg.DEC_8bit(x.Get()))),  # DEC B
            0x06: (2, 8, lambda: self.__reg[B].Set(self.__memory[self.__reg[PC].Get()])),  # LD B, n
            0x07: (1, 4, lambda x=self.__reg[A]: x.Set(self.__reg.RLC_8bit(x.Get()))),  # RLCA
            0x08: (3, 20, lambda x=self.__memory, y=self.__reg[PC]: x.ww(x.rw(y.Get()), y.Get())),  # LD (nn), SP
            0x09: (1, 8, lambda x=self.__reg[HL]: x.Set(self.__reg.ADD_16bit(x.Get(), self.__reg[BC].Get()))),  # ADD HL, BC
            0x0a: (1, 8, lambda: self.__reg[A].Set(self.__memory[self.__reg[BC].Get()])),  # LD A, (BC)
            0x0b: (1, 8, lambda: self.__reg[BC].Add(-1)),  # DEC BC
            0x0c: (1, 4, lambda x=self.__reg[C]: x.Set(self.__reg.INC_8bit(x.Get()))),  # INC C
            0x0d: (1, 4, lambda x=self.__reg[C]: x.Set(self.__reg.DEC_8bit(x.Get()))),  # DEC C
            0x0e: (2, 8, lambda: self.__reg[C].Set(self.__memory[self.__reg[PC].Get()])),  # LD C, n
            0x0f: (1, 4),  # RRCA

            # 0x10:
            0x7e: (1, 8, lambda: self.__reg[A].Set(self.__memory[self.__reg[HL].Get()])),  # LD A, (HL)
            0xc3: (3, 12, lambda x=self.__reg[PC]: x.Set(self.__memory.rw(x.Get())) or True),  # JP nn
            0xcb: ()
        }

        self.__CBDict = {
            0x00: (1, 4, lambda: None)
        }

    def Initialize(self):
        self.MachineParts()
        self.IO()
        self.__reg[PC].Set(0x100)

    def LoadRom(self, path):
        #Supports ROM only cartridges
        binary = open(path, 'rb').read()
        for i in xrange(len(binary)):
            self.__memory[i] = ord(binary[i])

    def Cycle(self):
        self.__opcode = self.__memory[self.__reg[PC].Get()]

        try:
            print hex(self.__opcode)

            shouldJump = self.__opcodeDict[self.__opcode][2]()  # call the associated function
            if not shouldJump:
                self.__reg[PC].Add(self.__opcodeDict[self.__opcode][0])

            self.__clock['cc'] += self.__opcodeDict[self.__opcode][1]
            self.__clock['mc'] += self.__opcodeDict[self.__opcode][1] / 4
        except:
            print "Unknown instruction: {0}".format(hex(self.__opcode))
            exit()


    def IfExit(self):
        if kbhit():
            exit()

    def Draw(self):
        pass

#-----------------------------------------------------opcodes----------------------------------------------------------
    def doit(self):
        self.__memory[0x80] = 0x55
        self.__reg[HL].Set(0x80)

        self.__opcodeDict[0x7e][2]()

        print hex(self.__reg[A].Get())

if __name__ == '__main__':

    cpu = GB_CPU()
    cpu.doit()
    cpu.doit()