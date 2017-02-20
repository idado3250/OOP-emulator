import pygame
from random import randint
from logging import log
from time import time


class CPU():
    def __init__(self):
        self.__register = None
        self.__vx = None
        self.__vy = None
        self.__pc = None
        self.__opcode = None
        self.__I = None
        self.__memory = None
        self.__displayBuffer = None
        self.__soundTimer = None
        self.__delayTimer = None
        self.__clockTimers = None
        self.__clock = None
        self.__stack = None
        self.__sp = None
        self.__shouldDraw = None
        self.__fonts = None
        self.__keyDict = None
        self.__reversedKeyDict = None
        self.__opcodeDict = None
        self.__screen = None
        self.__pixel = None
        self.__buzz = None
        self.__timeCounter = None


    def Initialize(self):
        self.__register = bytearray(16)
        self.__vx = 0
        self.__vy = 0
        self.__I = 0
        self.__memory = bytearray(4096)
        self.__displayBuffer = [0]*32*64
        self.__stack = []
        self.__sp = 0

        self.__soundTimer = 0
        self.__delayTimer = 0
        self.__clockTimers = time()
        self.__clock = self.__clockTimers

        pygame.init()
        self.__shouldDraw = False
        self.__screen = pygame.display.set_mode((640, 320))
        self.__pixel = pygame.Surface((10, 10))
        self.__pixel.fill((255, 255, 255))

        pygame.mixer.init()
        self.__buzz = pygame.mixer.Sound('beep-03.wav')

        self.__opcode = 0
        self.__pc = 0x200

        self.__opcodeDict = {
            0x0000: self._0ZZZ,
            0x00e0: self._00E0,
            0x00ee: self._00EE,
            0x1000: self._1nnn,
            0x2000: self._2nnn,
            0x3000: self._3xkk,
            0x4000: self._4xkk,
            0x5000: self._5xy0,
            0x6000: self._6xkk,
            0x7000: self._7xkk,
            0x8000: self._8ZZZ,
            #self._8xy0() is implemented in _8ZZZ() because 0x8xy0 & 0xf00f == 0x8000
            0x8001: self._8xy1,
            0x8002: self._8xy2,
            0x8003: self._8xy3,
            0x8004: self._8xy4,
            0x8005: self._8xy5,
            0x8006: self._8xy6,
            0x8007: self._8xy7,
            0x800e: self._8xyE,
            0x9000: self._9xy0,
            0xa000: self._Annn,
            0xb000: self._Bnnn,
            0xc000: self._Cxkk,
            0xd000: self._Dxyn,
            0xe000: self._EZZZ,
            0xe09e: self._Ex9E,
            0xe0a1: self._ExA1,
            0xf000: self._FZZZ,
            0xf007: self._Fx07,
            0xf00a: self._Fx0A,
            0xf015: self._Fx15,
            0xf018: self._Fx18,
            0xf01e: self._Fx1E,
            0xf029: self._Fx29,
            0xf033: self._Fx33,
            0xf055: self._Fx55,
            0xf065: self._Fx65
        }

        self.__keyDict = {
            0x1: pygame.K_1,
            0x2: pygame.K_2,
            0x3: pygame.K_3,
            0xc: pygame.K_4,
            0x4: pygame.K_q,
            0x5: pygame.K_w,
            0x6: pygame.K_e,
            0xd: pygame.K_r,
            0x7: pygame.K_a,
            0x8: pygame.K_s,
            0x9: pygame.K_d,
            0xe: pygame.K_f,
            0xa: pygame.K_z,
            0x0: pygame.K_x,
            0xb: pygame.K_c,
            0xf: pygame.K_v
        }

        self.__reversedKeyDict = {self.__keyDict[key]: key for key in self.__keyDict.keys()}

        self.__fonts = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, #0
            0x20, 0x60, 0x20, 0x20, 0x70, #1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, #2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, #3
            0x90, 0x90, 0xF0, 0x10, 0x10, #4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, #5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, #6
            0xF0, 0x10, 0x20, 0x40, 0x40, #7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, #8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, #9
            0xF0, 0x90, 0xF0, 0x90, 0x90, #A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, #B
            0xF0, 0x80, 0x80, 0x80, 0xF0, #C
            0xE0, 0x90, 0x90, 0x90, 0xE0, #D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, #E
            0xF0, 0x80, 0xF0 ,0x80 ,0x80, #F
        ]

        for i in xrange(80):
            self.__memory[i] = self.__fonts[i]


    def LoadRom(self, path):
        log(__debug__, "Loading " + path)
        binary = open(path, 'rb').read()
        for i in xrange(len(binary)):
            self.__memory[i + 0x200] = ord(binary[i])


    def Cycle(self):
        currentTime = time()
        if currentTime - self.__clock >= 1.0/500: #Determines the CPU's clock speed (1/hz = seconds)
            self.__clock = currentTime

            self.__opcode = (self.__memory[self.__pc] << 8) | self.__memory[self.__pc + 1]
            # print 'memory location:' + hex(self.__pc)
            # print 'opcode: ' + hex(self.__opcode)
            # print self.__delayTimer

            #process opcode
            self.__vx = (self.__opcode & 0x0f00) >> 8
            self.__vy = (self.__opcode & 0x00f0) >> 4
            self.__pc += 2

            #check ops, lookup and execute
            try:
                self.__opcodeDict[self.__opcode & 0xf000]() # call the associated method
            except:
                 print "Unknown instruction: {0}".format(hex(self.__opcode))

        currentTime = time()
        if currentTime - self.__clockTimers >= 1.0/60: #Timers are decremented at a frequency of 60hz
            self.__clockTimers = currentTime
            if self.__delayTimer > 0:
                self.__delayTimer -= 1
            if self.__soundTimer > 0:
                self.__soundTimer -= 1
                self.__buzz.play()


    def Draw(self):
        # if self.__shouldDraw:
        self.__screen.fill((0, 0, 0))
        for i in xrange(32):
            for j in xrange(64):
                if self.__displayBuffer[j + (i * 64)] == 1:
                    self.__screen.blit(self.__pixel, (j * 10, i * 10))
        pygame.display.flip()
        self.__shouldDraw = False


    def IfExit(self):
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            exit()


    def _0ZZZ(self):
         try:
            self.__opcodeDict[self.__opcode]()
         except:
             print 'Unknown instruction: {0}'.format(self.__opcode)


    def _00E0(self):
        """Clears the screen"""
        for i in xrange(2048):
            self.__displayBuffer[i] = 0
        self.__shouldDraw = True

    def _00EE(self):
        """Return from function"""
        try:
            self.__pc = self.__stack.pop()
        except:
            self.__pc = 0

    def _1nnn(self):
        """Jmp to address at nnn"""
        self.__pc = self.__opcode & 0x0fff

    def _2nnn(self):
        """Call function at nnn"""
        self.__stack.append(self.__pc)
        self.__pc = self.__opcode & 0x0fff

    def _3xkk(self):
        """Skip the next instruction if Vx equals kk"""
        if self.__register[self.__vx] == self.__opcode & 0x00ff:
            self.__pc += 2

    def _4xkk(self):
        """Skip the next instruction if Vx doesn't equals kk"""
        if self.__register[self.__vx] != self.__opcode & 0x00ff:
            self.__pc += 2

    def _5xy0(self):
        """Skip the next instruction if Vx equals Vy"""
        if self.__register[self.__vx] == self.__register[self.__vy]:
            self.__pc += 2

    def _6xkk(self):
        """Sets Vx to kk"""
        self.__register[self.__vx] = self.__opcode & 0x00ff

    def _7xkk(self):
        """Adds kk to Vx"""
        self.__register[self.__vx] = (self.__register[self.__vx] + (self.__opcode & 0x00ff)) & 0xff

    def _8ZZZ(self):
        if self.__opcode & 0xf00f == 0x8000:
            self._8xy0()
        else:
            try:
                self.__opcodeDict[self.__opcode & 0xf00f]()
            except:
                print "Unknown instruction: {0}".format(self.__opcode)

    def _8xy0(self):
        """Sets Vx to Vy"""
        self.__register[self.__vx] = self.__register[self.__vy]

    def _8xy1(self):
        """Sets Vx to Vx OR Vy"""
        self.__register[self.__vx] |= self.__register[self.__vy]

    def _8xy2(self):
        """Sets Vx to Vx AND Vy"""
        self.__register[self.__vx] &= self.__register[self.__vy]

    def _8xy3(self):
        """Sets Vx to Vx XOR Vy"""
        self.__register[self.__vx] ^= self.__register[self.__vy]

    def _8xy4(self):
        """Sets Vx to Vx + Vy, sets VF to 1 if there is a carry, if not set VF to 0"""
        if self.__register[self.__vx] + self.__register[self.__vy] >= 0x100:
            self.__register[0xf] = 1
        else:
            self.__register[0xf] = 0
        self.__register[self.__vx] = (self.__register[self.__vx] + self.__register[self.__vy]) & 0xff

    def _8xy5(self):
        """Sets Vx to Vx - Vy, sets VF to 1 is there isn't a borrow, if there is set VF to 0"""
        if self.__register[self.__vx] > self.__register[self.__vy]:
            self.__register[0xf] = 1
        else:
            self.__register[0xf] = 0
        self.__register[self.__vx] = (self.__register[self.__vx] - self.__register[self.__vy]) & 0xff

    def _8xy6(self):
        """Sets Vx to Vx shifted by 1 to the right, sets VF to the rightmost bit."""
        self.__register[0xf] = self.__register[self.__vx] & 0b00000001
        self.__register[self.__vx] >>= 1

    def _8xy7(self):
        """Sets Vx to Vy - Vx, sets VF to 1 is there isn't a borrow, if there is set VF to 0"""
        if self.__register[self.__vy] > self.__register[self.__vx]:
            self.__register[0xf] = 1
        else:
            self.__register[0xf] = 0
        self.__register[self.__vx] = (self.__register[self.__vy] - self.__register[self.__vx]) & 0xff

    def _8xyE(self):
        """Sets Vx to Vx shifted by 1 to the left, sets VF to the leftmost bit."""
        self.__register[0xf] = (self.__register[self.__vx] & 0b10000000) >> 7
        self.__register[self.__vx] = (self.__register[self.__vx] << 1) & 0xff

    def _9xy0(self):
        """Skip next instruction if Vx != Vy."""
        if self.__register[self.__vx] != self.__register[self.__vy]:
            self.__pc += 2

    def _Annn(self):
        """Sets the I register to address nnn"""
        self.__I = self.__opcode & 0x0fff

    def _Bnnn(self):
        """Jump to address at V0 + nnn"""
        self.__pc = self.__register[0x0] + (self.__opcode & 0x0fff)

    def _Cxkk(self):
        """Generates a random number from 0 to 255, which is then ANDed with the value kk. The results are stored in Vx."""
        self.__register[self.__vx] = randint(0, 255) & (self.__opcode & 0xff)

    def _Dxyn(self):
        self.__register[0xf] = 0
        x = self.__register[self.__vx]
        y = self.__register[self.__vy]
        height = self.__opcode & 0x000f #Get "n"
        for row in xrange(height):
            currentRow = self.__memory[row + self.__I]
            for byteSpot in xrange(8):
                if (y + row) < 32 and (x + byteSpot) < 64:
                    location = x + byteSpot + ((y + row) * 64)
                    mask = 1 << 7 - byteSpot
                    currentPixel = (currentRow & mask) >> 7 - byteSpot
                    oldPixel = self.__displayBuffer[location]
                    self.__displayBuffer[location] ^= currentPixel
                    if oldPixel == currentPixel and currentPixel == 1:
                        self.__register[0xf] = 1
        self.__shouldDraw = True

    def _EZZZ(self):
        try:
            self.__opcodeDict[self.__opcode & 0xf0ff]()
        except:
            print "Unknown instruction: {0}".format(self.__opcode)

    def _Ex9E(self):
        #Skip next instruction if key with the value of Vx is pressed.
        pygame.event.pump()
        if pygame.key.get_pressed()[self.__keyDict[self.__register[self.__vx]]] == True:
            self.__pc += 2
        pass

    def _ExA1(self):
        #Skip next instruction if key with the value of Vx is not pressed.
        pygame.event.pump()
        if pygame.key.get_pressed()[self.__keyDict[self.__register[self.__vx]]] == False:
            self.__pc += 2

    def _FZZZ(self):
        try:
            self.__opcodeDict[self.__opcode & 0xf0ff]()
        except:
            print "Unknown instruction: {0}".format(self.__opcode)

    def _Fx07(self):
        """The value of the delay timer is placed into Vx."""
        self.__register[self.__vx] = self.__delayTimer

    def _Fx0A(self):
        """Wait for a key press, store the value of the key in Vx."""
        pressed = False
        while not pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in self.__reversedKeyDict.keys():
                        self.__register[self.__vx] = self.__reversedKeyDict[event.key]
                        pressed = True
                        break

    def _Fx15(self):
        """The delay timer is set to the value of Vx."""
        self.__delayTimer = self.__register[self.__vx]

    def _Fx18(self):
        """The sound timer is set to the value of Vx."""
        self.__soundTimer = self.__register[self.__vx]

    def _Fx1E(self):
        """The values of I and Vx are added, and the results are stored in I."""
        self.__I += self.__register[self.__vx]

    def _Fx29(self):
        """The value of I is set to the location for the hexadecimal sprite corresponding to the value of Vx."""
        if self.__register[self.__vx] <= 0xf:
            self.__I = 5 * self.__register[self.__vx]
        else:
            print 'operand too big'

    def _Fx33(self):
        """The interpreter takes the decimal value of Vx, and places the hundreds digit in memory at location in I, the tens digit at location I+1, and the ones digit at location I+2."""
        self.__memory[self.__I] = self.__register[self.__vx] / 100
        self.__memory[self.__I + 1] = self.__register[self.__vx] % 100 / 10
        self.__memory[self.__I + 2] = self.__register[self.__vx] % 10

    def _Fx55(self):
        """Store registers V0 through Vx in memory starting at location I."""
        for i in xrange(self.__vx + 1):
            self.__memory[self.__I + i] = self.__register[i]

    def _Fx65(self):
        """Read registers V0 through Vx from memory starting at location I."""
        for i in xrange(self.__vx + 1):
            self.__register[i] = self.__memory[self.__I + i]