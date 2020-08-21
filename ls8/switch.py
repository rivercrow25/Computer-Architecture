class Switcher():
    def __init__(self, obj):
        self.obj = obj

    def command(self, argument):
        """Dispatch method"""
        method_name = 'cmd_' + str(argument)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid command")
        # Call the method as we return it
        return method()

    def cmd_00000001(self):
        self.obj.running = False

    def cmd_10000010(self):
        indx = self.obj.ram[self.obj.pc+1]
        value = self.obj.ram[self.obj.pc+2]
        self.obj.reg[indx] = value

    def cmd_01000111(self):
        indx = self.obj.ram[self.obj.pc+1]
        print(self.obj.reg[indx])

    def cmd_0b10100010(self):
        self.obj.alu(
            "MULTIPLY", self.obj.ram[self.obj.pc + 1], self.obj.ram[self.obj.pc + 2])

    def cmd_0b10100000(self):
        self.obj.alu(
            "ADD", self.obj.ram[self.obj.pc + 1], self.obj.ram[self.obj.pc + 2])

    def cmd_0b1000101(self):
        reg_index = self.obj.ram[self.obj.pc+1]
        val = self.obj.reg[reg_index]

        self.obj.reg[self.obj.sp] -= 1

        self.obj.ram[self.obj.reg[self.obj.sp]] = val

    def cmd_0b1000110(self):
        reg_index = self.obj.ram[self.obj.pc + 1]
        val = self.obj.ram[self.obj.reg[self.obj.sp]]

        self.obj.reg[reg_index] = val
        self.obj.reg[self.obj.sp] += 1

    def cmd_0b1010000(self):
        self.obj.reg[self.obj.sp] -= 1
        self.obj.ram[self.obj.reg[self.obj.sp]] = self.obj.pc + 2

        reg_index = self.obj.ram[self.obj.pc + 1]
        self.obj.pc = self.obj.reg[reg_index]
        self.obj.op_size = 0

    def cmd_0b10001(self):
        self.obj.pc = self.obj.ram[self.obj.reg[self.obj.sp]]
        self.obj.reg[self.obj.sp] += 1
        self.obj.op_size = 0

    def cmd_10100111(self):
        self.obj.alu(
            "CMP", self.obj.ram[self.obj.pc + 1], self.obj.ram[self.obj.pc + 2])
        print(self.obj.reg[self.obj.ram[self.obj.pc + 1]],
              self.obj.reg[self.obj.ram[self.obj.pc + 2]], self.obj.reg[3])

    def cmd_01010100(self):
        self.obj.pc = self.obj.ram[self.obj.pc + 1]

    def cmd_01010101(self):
        if self.obj.FL == 0b00000001:
            self.obj.pc = self.obj.reg[self.obj.ram[self.obj.pc + 1]]
            self.obj.op_size = 0

    def cmd_01010110(self):
        if self.obj.FL != 0b00000001:
            self.obj.pc = self.obj.reg[self.obj.ram[self.obj.pc + 1]]
            self.obj.op_size = 0
