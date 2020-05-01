"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] = 256,  
        self.pc = 0,# the pointer
        self.registers = [0] * 8,
        self.registers[7] * 0xF4,

        self.opcodes = {
            0b00000001: "HLT",
            0b01000111: "PRN",
            0b10000010: "LDI",
            0b00001000:"MUL", # 00001000
            0b01000101: "PUSH", # for stack
            0b01000110: "POP", # for stack
            0b01010000: "CALL", 
            0b10100000: "ADD",
            # add RET here
        }

        self.branchtable = {
            # Task Three below
              "HLT": self.hlt,
              "LDI": self.ldi,
              "PRN": self.prn,
            # Task Four below
             "CALL": self.call,
              "RET": self.ret, 
        }


    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        return self.ram[address]

    def ram_write(self, address, value):
        #should accept a value to write, and the address to write it to.
        self.ram[address] = value

    def load(self, filename):
        #  load an .ls8 file given the filename passed in as an argument
        address = 0
        try:
            with open(filename) as file:
                for line in file:
                    file_split = line.split("#")
                    number_string = comment_split[0].strip()

                    if number_string == "":
                        continue

                    num = int(number_string, 2)
                    memory[address] = num
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: could not find {sys.argv[1]}")
            sys.exit(2)
    load_memory(sys.argv[1])

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.registers[reg_a] += self.registers[reg_a]
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
        self.running = True 

        while self.running:
             IR = self.ram_read(self.pc)
             operand_a = self.ram_read(self.pc +1)
             operand_b = self.ram_read(self.pc + 2)

             num_operands = (IR >> 6)

             sets_pc = (IR >> 4) & 0b0001 == 1 # IR is shifted to the right 4 times 
             
             is_alu_operation = (IR >> 5 & 0b001) == 1

             opcode = self.opcodes[IR]

             if not sets_pc:
                self.pc += 1 + num_operands

             if is_alu_operation:
                 self.alu(opcode, operand_a, operand_b)
             else: 
                self.branchtable[opcode](operand_a, operand_b)

    def hlt(self, _, __):
        self.running = False
    
    def prn(self, op_a, _):
        print(self.registers[op_a])

    def ldi(self, op_a, op_b):
        self.registers[op_a] = op_b


    # Create stack here

    # Task Four
    def call(self, op_a, _):
        self.registers[7] -= 1
        sp = self.registers[7]
        self.ram_write(sp, self.pc + 2)

        self.pc = self.registers[op_a]

    def ret(self, op_a, _):
        sp =self.registers[7]
        return_address = self.ram_read(sp)

