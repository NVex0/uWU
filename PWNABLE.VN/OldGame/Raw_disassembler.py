#Init
STACK =  [0 for i in range(14)]
digit_trigger = 1
x = 0
final = ""
#9 REG
REGISTER = {
    0x0 : "REG_0",
    0x1 : "REG_1",
    0x2 : "REG_2",
    0x3 : "REG_3",
    0x4 : "REG_4",
    0x5 : "REG_5",
    0x6 : "REG_6",
    0x7 : "REG_7",
    0x8 : "REG_8",
    0x9 : "REG_9",
}
#Instruction
PUSH_IMM = [0xfa, 0xf9, 0x78, 0x94, 0xca, 0x61, 0xce, 0xe4, 0xf7, 0xa8, 0xe0, 0xda, 0x74, 0xd0, 0x7a, 0xb6]
CALL = [0xf0, 0x58, 0x22, 0x39, 0x33, 0x86, 0x34, 0xbd, 0xc1, 0x3, 0x81, 0x8c, 0xb7]
XOR = [0x0, 0x30, 0x40, 0xba, 0x24, 0xe3, 0x2d, 0xd6, 0x1e, 0x36, 0xa6, 0xb0, 0x75, 0xc9, 0x2a]
PUSH_REG = [0xd2, 0x52, 0x9c, 0x2b, 0xc6, 0x54, 0xbe, 0x65, 0xd3, 0x15, 0x8]
POP_REG = [0xe8, 0xaf, 0x9d, 0x87, 0x9e, 0xf2]
CMP = [0x8f, 0x23, 0x5d, 0x80, 0x53, 0x5, 0xb4, 0x3f, 0xd8, 0x5a, 0xfb]
OR = [0xe5, 0xf1, 0x32, 0xf4, 0x57, 0x2f, 0x3c,0x89, 0x10, 0x93, 0x8b,0xa3,0x25,0x6e]
ADD = [0x31, 0x73, 0x63, 0xe6, 0x3b,0x55]
AND = [0xf8, 0xcd,0xa,0x26,0x9b,0x60,0xd,0xe2,0xed,0x29]
SUB = [0x68,0x1d]
DEC_STACK_PTR = [0x41, 0x6a,0xaa,0xa4,0xa9,0x51,0x4a,0xc0,0x44,0x71]
CLONING = [0xa1, 0x3d, 0xb, 0xde, 0x5e, 0xee, 0x19, 0xe7, 0xdc, 0x28, 0x72, 0x7e, 0x16, 0x59]
NEG = [0x4d, 0x97, 0x85, 0x21, 0xb8, 0xad, 0x7c, 0x96, 0x62, 0xd9, 0x1f, 0xcf]
SWAP = [0xcb, 0x4f, 0xe, 0x76, 0x4c, 0x47, 0xb3, 0xf5, 0xbc, 0x7b]
NOT = [0xb5, 0xc8, 0xd4, 0xc4, 0xfd, 0x6, 0x82, 0x56, 0x69, 0x2e, 0xb9, 0xcc, 0xf, 0xa7]
MOV_IDXABSMEM_TOPSTACK = [0xe1, 0x64]
MOV_TOPSTACK_IDXABSMEM = [0xac, 0x4, 0x95]


REG_CONTEXT = [0 for i in range(10)]
ABYSS_MEMORY = [0 for i in range(0xFF)] #0x3000
LICENSE = r"LMAO{I_Br1n9_y0u_Licens3}"    #25 ki tu

for i in range(len(LICENSE)):
    ABYSS_MEMORY[i] = ord(LICENSE[i])


with open(r"D:\ZZZ\CTF-Challenge\PWNABLE_VN\OldGame\resource.txt", "rb") as f:
    data = f.read()

data = data[4:0xFC8]
i = 0
with open("VMCODE_LOG.txt", "w") as f:
    while i < len(data):
        if data[i] == 0x20:
            print("END OF VM")
            break

        # print(f"--------------------------\nCurrent opcode: {hex(data[i])}\nCurrent addr: {hex(i)}\nSTACK: ", end = "")
        
        # for z in STACK:
        #     print(hex(z), end = " ")
        # print()
        # for z in REG_CONTEXT:
        #     print(hex(z), end = " ")
        # print("\n--------------------------")

        f.write(f"Address {hex(i)} - Opcode {hex(data[i])}:")
        if data[i] in PUSH_IMM:
            val = int.from_bytes(data[i + 1 : i + 3], "little")
            string_fmt = hex(val)
            i += 3
            f.write(f"PUSH {string_fmt}\n")
            STACK.append(val)

        elif data[i] in CALL:
            addr = STACK[-1]
            STACK.pop()

            i = addr
            f.write(f"CALL {hex(addr)}\n")

        elif data[i] in XOR:
            i += 1
            STACK[-2] ^= STACK[-1]
            f.write(f"{hex(STACK[-1])} ^ {hex(STACK[-2])}\n")
            STACK.pop()

        elif data[i] in PUSH_REG:
            reg = REGISTER[data[i + 1]]
            reg_val = REG_CONTEXT[data[i + 1]]
            STACK.append(reg_val)
            i += 2
            STACK
            f.write(f"PUSH {reg} value: {hex(reg_val)}\n")

        elif data[i] in POP_REG:
            reg = REGISTER[data[i + 1]]
            REG_CONTEXT[data[i + 1]] = STACK[-1]
            reg_val = STACK[-1]
            STACK.pop()
            i += 2
            f.write(f"POP {hex(reg_val)} to {reg}\n")


        elif data[i] in CMP:
            value1 = STACK[-1]
            value2 = STACK[-2]
            STACK.pop()
            if value1 == value2:
                STACK[-1] = 1
            else:
                STACK[-1] = 0
            i += 1

            f.write(f"CMP {hex(value1)}, {hex(value2)}\n")

        
        #MAINTAINING
        elif data[i] in OR:
            STACK[-2] |= STACK[-1]
            f.write(f"OR {hex(STACK[-1])}, {hex(STACK[-2])}\n")
            STACK.pop()
            i += 1
        
        elif data[i] in ADD:
            STACK[-2] += STACK[-1]
            f.write(f"ADD {hex(STACK[-1])}, {hex(STACK[-2])}\n")
            STACK.pop()
            i += 1
            

        elif data[i] in AND:
            STACK[-2] &= STACK[-1]
            f.write(f"AND {hex(STACK[-1])}, {hex(STACK[-2])}\n")
            STACK.pop()
            i += 1
            

        elif data[i] in SUB:
            STACK[-2] -= STACK[-1]
            f.write(f"SUB {hex(STACK[-1])}, {hex(STACK[-2])}\n")
            STACK.pop()
            i += 1
            

        elif data[i] in DEC_STACK_PTR:
            STACK.pop()
            i += 1
            f.write("Decrease stack ptr\n")

        elif data[i] in [0x6b,0x38,0x98,0x35]:
            STACK[-2] *= STACK[-1]
            f.write(f"MUL {hex(STACK[-1])}, {hex(STACK[-2])}\n")
            STACK.pop()
            i += 1
            
        #END OF DIVIDED INS 7.

        elif data[i] in CLONING:
            Clone = STACK[-1]
            STACK.append(Clone)
            i += 1
            f.write("Cloning\n")

        elif data[i] in NEG:
            STACK[-1] = -STACK[-1]
            i += 1
            f.write(f"NEGATE {hex(STACK[-1])}\n")


        elif data[i] in SWAP:
            i += 1
            temp = STACK[-2]
            STACK[-2] = STACK[-1]
            STACK[-1] = temp
            f.write(f"SWAP {hex(STACK[-1])}, {hex(STACK[-2])}\n")

        elif data[i] in NOT:
            i += 1
            STACK[-1] = ~STACK[-1]
            f.write(f"NOT {hex(STACK[-1])}\n")

        elif data[i] in MOV_IDXABSMEM_TOPSTACK:
            i += 1
            ABYSS_MEMORY[STACK[-2]] = STACK[-1]
            stack_val = STACK[-1]
            
            STACK.pop()
            STACK.pop()
            f.write(f"move indexes abyss mem, {stack_val}\nCURRENT ABYSS_MEM {ABYSS_MEMORY}\n")
        
        elif data[i] in MOV_TOPSTACK_IDXABSMEM:
            i += 1
            mem_val = ABYSS_MEMORY[STACK[-1]]
            mem_idx = STACK[-1]
            STACK[-1] = ABYSS_MEMORY[STACK[-1]]
            f.write(f"mov topstack, indexes abyss mem value {hex(mem_val)} at index {hex(mem_idx)}\nCURRENT ABYSS_MEM {ABYSS_MEMORY}\n")
            if digit_trigger % 2 == 0:
                final += f"x{x}*{mem_val} + "
                x += 1
                if x % 5 == 0:
                    final = final[:-2] + "== "
                    print(final)
                    x = 0
                    final = ""
            digit_trigger += 1

        
        # f.write(f"CURRENT STACK {[hex(z) for z in STACK]}\n")