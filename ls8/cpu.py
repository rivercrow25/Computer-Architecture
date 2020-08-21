"""CPU functionality."""

import sys
from switch import Switcher


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7
        self.running = False
        self.op_size = 0
        self.switch = Switcher(self)
        self.FL = 0b00000000

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                # store val in memory
                    self.ram[address] = val

                    address += 1

                # print(f"{x:08b}: {x:d}")

        except:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MULTIPLY":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.FL = self.FL & 0b00000010
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = self.FL & 0b00000100
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = self.FL & 0b00000001
            if self.reg[reg_a] != self.reg[reg_b]:
                self.FL = self.FL & 0b00000000

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        value = self.ram[address]
        return value

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            cmd = self.ram[self.pc]
            self.op_size = (cmd >> 6) + 1
            self.switch.command(format(cmd, '08b'))
            self.pc += self.op_size
