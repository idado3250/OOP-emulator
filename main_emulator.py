from sys import argv

if argv[1] == 'chip8':
    import chip8_CPU
    cpu = chip8_CPU.CPU()
elif argv[1] == 'gb':
    from gb.GB_CPU import GB_CPU
    cpu = GB_CPU()
else:
    print('error: Invalid emulator option')
    exit()
cpu.Initialize()
cpu.LoadRom(argv[2])
while True:
    cpu.Cycle()
    cpu.Draw()
    cpu.IfExit()
