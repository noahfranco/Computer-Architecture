"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0# the pointer
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4

        self.sp = 7

        self.opcodes = {
            0b00000001: "HLT",
            0b01000111: "PRN",
            0b10000010: "LDI",
            0b10100010: "MUL", # 00001000
            0b01000101: "PUSH", # for stack
            0b01000110: "POP", # for stack
            0b01010000: "CALL", 
            0b10100000: "ADD",
            0b00010001: "RET",
        }   

        # self.branchtable = {
        #     "HLT": self.hlt,
        #     "LDI": self.ldi,
        #     "PRN": self.prn,
        #     "CALL": self.call,
        #     "RET": self.ret, 
        #     "PUSH": self.push, # for stack 
        #     "POP": self.pop, # for stack
        #     "ADD": self.add,
        #     "MUL": self.mul
        # }

    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        return self.ram[address]

    def ram_write(self, address, value):
        #should accept a value to write, and the address to write it to.
        self.ram[address] = value

    def load(self, filename): 
        address = 0
        try:
            with open(filename) as file:
                for line in file:
                    file_split = line.split("#")
                    number_string = file_split[0].strip()

                    if number_string == "":
                        continue

                    num = int(number_string, 2)
                    self.ram[address] = num
                    address += 1
        

        except FileNotFoundError:
            # print(f"{sys.argv[0]}: could not find {sys.argv[1]}")
            sys.exit(2)
    # # load(sys.argv[1])

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
            # self.pc += 3
        elif op == "MUL":
            self.registers[reg_a] += self.registers[reg_b]
            # self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")



    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.registers[i], end='')

    #     print()

    def run(self):
        """Run the CPU."""
        self.running = True 
        while self.running:
             IR = self.ram_read(self.pc)
            #  print("This is what's not working", IR)
             operand_a = self.ram_read(self.pc + 1)
             operand_b = self.ram_read(self.pc + 2)
             opcode = self.opcodes[IR]
             if opcode == "HLT":
                self.running = False
             if opcode == "PRN":
                print(self.registers[operand_a])
                self.pc += 2

            

            #  if not sets_pc:
            #     self.pc += 1 + num_operands
            
             if opcode == "LDI":
                self.registers[operand_a] = operand_b
                self.pc += 3

             if opcode == "CALL":
                return_address = self.pc + 2
                self.registers[self.sp] -= 1
                self.ram[self.registers[self.sp]] = return_address
                reg_num = self.ram[self.pc + 1]
                sub_address = self.registers[reg_num]
                self.pc = sub_address

             if opcode == "ADD":
                 self.registers[operand_a] += self.registers[operand_b]
                 self.pc += 3

             if opcode == "MUL":
                self.registers[operand_a] * self.registers[operand_b]
                self.pc += 3

             if opcode == "RET":
                return_address = self.ram[self.registers[self.sp]]
                self.registers[self.sp] +=1
                self.pc = return_address

             if opcode == "PUSH":
                self.registers[self.sp] -= 1
                operand_a = self.ram[self.pc + 1]
                value = self.registers[operand_a]
                self.ram[self.registers[self.sp]] = value
                self.pc +=2

             if opcode == "POP":
                operand_a = self.ram[self.pc + 1]
                value = self.ram[self.registers[self.sp]]
                self.registers[operand_a] = value 
                self.registers[self.sp] += 1
                self.pc += 2


    # def hlt(self, _, __):
    #     self.running = False
    
    # def prn(self, op_a, _):
    #     print(self.registers[op_a])

    # def ldi(self, op_a, op_b):
    #     self.registers[op_a] = op_b
    #     self.pc += 3

    # Task Four
    # def call(self, op_a, _):
    #     # self.registers[7] -= 1
    #     # sp = self.registers[7]
    #     # self.ram_write(sp, self.pc + 2)

    #     # self.pc = self.registers[op_a]
    #     return_address = self.pc + 2
    #     self.registers[self.sp] -= 1
    #     self.ram[self.registers[self.sp]] = return_address
    #     reg_num = self.ram[self.pc + 1]
    #     sub_address = self.registers[reg_num]
    #     self.pc = sub_address

    # def add(self, op_a, op_b):
    #     self.registers[op_a] += self.registers[op_b]
    #     self.pc += 3

    
    # def mul(self, op_a, op_b):
    #     self.registers[op_a] * self.registers[op_b]
    #     self.pc += 3


    # def ret(self, op_a, _):
    #     # sp =self.registers[7]
    #     # return_address = self.ram_read(sp)
    #     return_address = self.ram[self.registers[self.sp]]
    #     self.registers[self.sp] +=1
    #     self.pc = return_address

    # def push(self, op_a, _):
    #     self.registers[self.sp] -= 1
    #     sp = self.registers[7]
    #     value = self.registers[op_a]

    #     self.ram_write(sp, value)

    # def pop(self, op_a, _):
    #     sp = self.registers[7]
    #     value = self.ram_read(sp)

    #     self.registers[op_a] = value

    #     self.registers[7] += 1

