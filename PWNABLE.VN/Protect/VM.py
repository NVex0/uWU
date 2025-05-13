with open(r"D:\ZZZ\CTF-Challenge\PWNABLE_VN\Protect\vm_code.txt", "rb") as f:
    vm_stub = f.read()

index = 0
Origin = 0
Tinh_toan_cac_thu = []
# test = True
Start_capture = False
def Emulator(List_tinh_toan):
    result = List_tinh_toan[-1][2]
    reg = [0 ,0, 0, 0, 0, 0, 0]
    reg_to_brute = List_tinh_toan[0] - 1
    List_tinh_toan.pop(-1)
    List_tinh_toan.pop(0)
    for Origin in range(0, 0xFF):
        reg[reg_to_brute] = Origin
        for line in List_tinh_toan:
            ins = line[0]
            if ins == 'MOV_REG_VAL':
                reg[line[1] - 1] = line[2]
            elif ins == 'MOV_REG_REG':
                reg[line[1] - 1] = reg[line[2] - 1]
            elif ins == 'SUB':
                reg[line[1] - 1] -= reg[line[2] - 1]
            elif ins == 'ADD':
                reg[line[1] - 1] += reg[line[2] - 1]
            elif ins == 'XOR':
                reg[line[1] - 1] ^= reg[line[2] - 1]
        if reg[reg_to_brute] == result:
            print(chr(Origin), end = "")
            
with open("Disassem.txt", "a") as f:
    while index < len(vm_stub): #0x320e
        f.write(f"ADDRESS: {hex(index)[2:].zfill(8)} - ")
        curr = vm_stub[index:index+5]
        if curr[0] == 0:
            index += 2
            f.write("NOP\n")

        elif curr[0] == 0x10:
            index += 2
            f.write(f"JMP {hex(index + curr[1])}\n")

        elif curr[0] == 0x11:
            index += 2
            f.write(f"JZ {hex(index + curr[1])}\n")

        elif curr[0] == 0x12:
            index += 2
            f.write(f"JMP REG_{curr[1]}\n")

        elif curr[0] == 0x13:
            index += 2
            f.write(f"JNZ {hex(index + curr[1])}\n")

        elif curr[0] == 0x20:
            index += 3
            f.write(f"CMP REG_{curr[1]}, REG_{curr[2]}\n")
            try:
                Emulator(Tinh_toan_cac_thu)
            except:
                pass
            Tinh_toan_cac_thu = []
            Start_capture = False

        elif curr[0] == 0x30:
            index += 3
            f.write(f"XOR REG_{curr[1]}, REG_{curr[2]}\n")
            if Start_capture:
                Tinh_toan_cac_thu.append(('XOR', curr[1], curr[2]))

        elif curr[0] == 0x31:
            index += 3
            f.write(f"SUB REG_{curr[1]}, REG_{curr[2]}\n")
            if Start_capture:
                Tinh_toan_cac_thu.append(('SUB', curr[1], curr[2]))

        elif curr[0] == 0x32:
            index += 3
            f.write(f"ADD REG_{curr[1]}, REG_{curr[2]}\n")
            if Start_capture:
                Tinh_toan_cac_thu.append(('ADD', curr[1], curr[2]))

        elif curr[0] == 0x40:
            index += 3
            f.write(f"AND REG_{curr[1]}, REG_{curr[2]}\n")
            if Start_capture:
                Tinh_toan_cac_thu.append(('AND', curr[1], curr[2]))

        elif curr[0] == 0x41:
            index += 3
            f.write(f"SHL REG_{curr[1]}, nREG_{curr[2]}\n")

        elif curr[0] == 0x42:
            index += 3
            f.write(f"SHR REG_{curr[1]}, nREG_{curr[2]}\n")

        elif curr[0] == 0x60:
            index += 2
            f.write(f"PUSH_VM REG_{curr[1]}\n")

        elif curr[0] == 0x61:
            index += 2
            f.write(f"POP_VM REG_{curr[1]}\n")
            pass
        elif curr[0] == 0x62:
            index += 3
            f.write(f"READ_TOP_STACK maybeIndexes {hex(curr[2])}, REG_{curr[1]}\n")
            pass
        elif curr[0] == 0x63:
            index += 2
            f.write(f"PUSH REG_{curr[1]}\n")

        elif curr[0] == 0x64:
            index += 2
            f.write(f"POP REG_{curr[1]}\n")

        elif curr[0] == 0xA0:
            index += 3
            f.write(f"MOV  REG_{curr[1]}, REG_{curr[2]}\n")
            if Start_capture:
                Tinh_toan_cac_thu.append(('MOV_REG_REG', curr[1], curr[2]))

        elif curr[0] == 0xA1:
            index += 3
            f.write(f"MOV REG_{curr[1]}, {hex(curr[2])}\n")
            if Start_capture:
                Tinh_toan_cac_thu.append(('MOV_REG_VAL', curr[1], curr[2]))

        elif curr[0] == 0xA2:
            index += 4
            f.write(f"MOV BYTE PTR REG_{curr[1]}, [REG_{curr[2]} + REG_{curr[3]}]\n")
            if index not in range(0x3210, 0x3262):
                Start_capture = True
                Tinh_toan_cac_thu.append(curr[1])
            else:
                print("?", end="")

        elif curr[0] == 0xA3:
            index += 4
            f.write(f"MOV DWORD PTR REG_{curr[1]}, [REG_{curr[2]} + REG_{curr[3]}]\n")

        elif curr[0] == 0xCA:
            index += 2
            f.write(f"CALL REG_{(curr[1])}\n")

        elif curr[0] == 0xCB:
            index += 2
            f.write(f"MOV EAX, REG_{curr[1]}\n")

        else:
            index += 1
            f.write("NOT DEFINED OPCODE!!!!!!\n")




