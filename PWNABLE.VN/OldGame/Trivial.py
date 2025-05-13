with open(r"D:\ZZZ\CTF-Challenge\PWNABLE_VN\OldGame\resource.txt", "rb") as f:
    data = f.read()

def bytes_to_int(numb):
    return int.from_bytes(numb, 'little')
start = data[0:4]
start = bytes_to_int(start)
start += 4
# Cipher length - Key - index of cipher
list_1 = [[0, 0 ,0] for i in range(256)]
index = 0

while True:
    v10 = data[start : start + 4]
    v10 = bytes_to_int(v10)
    list_1[index][0] = hex(v10)

    list_1[index][2] = hex(start + 8)

    v12 = data[start + 4 : start + 8]
    v12 = bytes_to_int(v12)
    list_1[index][1] = hex(v12)

    v8 = data[start + 8 : start + 12]
    v8 = bytes_to_int(v8)
    
    v8 = data[start + v10 + 8 : start + v10 + 12]
    v8 = bytes_to_int(v8)
    
    start = start + v10 + 8
    if v8 == 0:
        break
    
    index += 1
    # print(hex(v8))
want_to = 0
from capstone import *
from Crypto.Cipher import ARC4
import os

md = Cs(CS_ARCH_X86, CS_MODE_32)

with open("D:\ZZZ\CTF-Challenge\PWNABLE_VN\OldGame\OPCODE.txt", "rb") as f:
    opcode = f.read()

is_exist = []
for i in opcode:
    if i in is_exist:
        continue
    else:
        is_exist.append(i)


for want_to in is_exist:
    try:
        with open("Disassembly_Shellcode.txt", "a") as f:
            f.write(f"##################################\n########## BLOCK {hex(want_to)}")
            idx = int(list_1[want_to][2], 16)
            cipher = data[idx : idx + int(list_1[want_to][0], 16)]
            key = bytes.fromhex(list_1[want_to][1][2:].zfill(8))[::-1]
            # swap endianess
            s = list_1[want_to][1][2:].zfill(8)
            parts = [s[i:i+2] for i in range(0, len(s), 2)]
            flipped = ''.join(reversed(parts))
            
            f.write(f", LENGTH {len(cipher)}, INDEX {hex(idx)}, KEY 0x{flipped} ###########\n##################################\n")
            cip = ARC4.new(key)
            plain = cip.decrypt(cipher)
            with open ("temp.txt", "wb") as fi:
                fi.write(plain)
            os.system("python CTF-Challenge\PWNABLE_VN\OldGame\msynth\scripts\symbolic_simplification.py temp.txt 0x0 CTF-Challenge\PWNABLE_VN\OldGame\msynth\oracle.pickle > output.txt")
            with open("output.txt", "r") as fi:
                dat = fi.read()
                f.write(dat)
            # break
            # for insn in md.disasm(plain, 0x1000):
            #     # print("0x%x:\t%s\t%s" % (insn.address, insn.mnemonic, insn.op_str))
            #     to_write = f"{insn.address}:\t{insn.mnemonic}\t{insn.op_str}\n"
            #     f.write(to_write)
    except:
        print("Error at " + str(want_to))
        print(list_1[want_to])

### breakpoints spec addr ###
# BREAK_EA_CALL = 0x00C813B6
# BREAK_EA_READ_VMCODE = 0x00C81385
# BASE_FUNC = 0x0019EB40
# MEMORY_INDEX_PTR_0x3E14 = 0
# MEMORY_0x3A00 = 0
# VM_FILE_PTR_0x3E16 = 0

# def bytes_to_int(numb):
#     return int.from_bytes(numb, 'little')

# class Tracer(idaapi.DBG_Hooks):
#     def dbg_bpt(self, tid, ea):
#         if ea == BREAK_EA_CALL:
#             esi = get_reg_value("esi")
#             ebx = get_reg_value("ebx")
#             addr = esi + ebx * 4 + 0x30
#             func_index = int((addr - BASE_FUNC - 8) / 12)
#             if func_index > 0xFF:
#                 idaapi.suspend_process()
#             # func_addr = get_bytes(addr, 4)
#             # func_addr = bytes_to_int(func_addr)
#             print(f"[+] Current func at 0x{func_index:X}")
#             with open("OPCODE.txt", "ab") as f:
#                 f.write(int.to_bytes(func_index, 1, 'big'))
#             # Continue execution automatically
#             idaapi.continue_process()
#         elif ea == BREAK_EA_READ_VMCODE:
#             edx = get_reg_value("edx")
#             print(f"VMCODE {hex(edx)}: ")


#         return 0
# tracer = Tracer()
# tracer.hook()