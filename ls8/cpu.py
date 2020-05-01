"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = 256,  
        self.pc = 0,# the pointer
        self.reg = [0] * 8,

    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        self.ram.append(address)
        return address

    def ram_write(self, address, value):
        #should accept a value to write, and the address to write it to.
        self.ram[address] = value

    def load(self, filename):

        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010

        memory = [
            LDI,
            0b00000000,
            0b00001000,
            PRN,
            0b00000000,
            HLT,
        ]

        for instruction in memory:
            self.ram[address] = instruction
            address += 1

        #  load an .ls8 file given the filename passed in as an argument
        address = 0
        with open(filename) as file:
            for line in file:
                file_split = line.split("#")
                number_string = comment_split[0].strip()

                if number_string == "":
                    continue

                num = int(number_string)
                memory[address] = num
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
       pass
