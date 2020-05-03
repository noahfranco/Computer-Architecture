"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0# the pointer
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        # LS-8 flag below
        self.fl = 0b00000000

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
            # for sprint challenge
            0b10100111: "CMP",
            0b01010100: "JMP",
            0b01010101: "JEQ",
            0b01010110: "JEQ",
        }

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

    #  For Sprint
    def CMP(self, reg_a, reg_b):
        
        if self.ram[reg_a] == self.ram[reg_b]:
            self.fl = "HLT"
        elif self.ram[reg_a] > self.ram[reg_b]:
            self.fl = 0b00000010
        else:
            self.fl = 0b00000100



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

            # Sprint challenge below // CMP, JMP, JEQ, JNE

             if opcode == "CMP": # if they place were we in our memior is equal to the CMP
               self.CMP(operand_a, operand_b)
               self.pc += 3
            #    print("Is this running", self.pc)

             if opcode == "JMP":
                self.pc = self.ram_read(operand_a)
            
             if opcode == "JEQ":
                if self.fl == "HLT":
                    self.pc = self.ram_read(operand_a)
                else:
                    self.pc += 2

             if opcode == "JNE":
                 if self.fl != "HLT":
                     self.pc = self.ram_read(operand_a)
                 else:
                    self.pc += 2









            #  if self.ram[self.pc] == "CMP": # if they place were we in our memior is equal to the CMP
            #    self.CMP(operand_a, operand_b)
            #    self.pc += 3
            #    print("Is this running", self.pc)

            #  if self.ram[self.pc] == "JMP":
            #     self.pc = self.ram_read(operand_a)
            
            #  if self.ram[self.pc] == "JEQ":
            #     if self.fl == "HLT":
            #         self.pc = self.ram_read(operand_a)
            #     else:
            #         self.pc += 2

            #  if self.ram[self.pc] == "JNE":
            #      if self.fl != "HLT":
            #          self.pc = self.ram_read(operand_a)
            #      else:
            #         self.pc += 2