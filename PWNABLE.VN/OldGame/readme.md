`DUMPed_address.txt`: Set breakpoint vào mỗi lúc nó call VM handler, từ đó ta có được list các giá trị nào được gọi (174 opcode).

Script dump opcode:

```
BREAK_EA_CALL = 0x00C813B6
BREAK_EA_READ_VMCODE = 0x00C81385
BASE_FUNC = 0x0019EB40
MEMORY_INDEX_PTR_0x3E14 = 0
MEMORY_0x3A00 = 0
VM_FILE_PTR_0x3E16 = 0

def bytes_to_int(numb):
    return int.from_bytes(numb, 'little')

class Tracer(idaapi.DBG_Hooks):
    def dbg_bpt(self, tid, ea):
        if ea == BREAK_EA_CALL:
            esi = get_reg_value("esi")
            ebx = get_reg_value("ebx")
            addr = esi + ebx * 4 + 0x30
            func_index = int((addr - BASE_FUNC - 8) / 12)
            if func_index > 0xFF:
                idaapi.suspend_process()
            # func_addr = get_bytes(addr, 4)
            # func_addr = bytes_to_int(func_addr)
            print(f"[+] Current func at 0x{func_index:X}")
            with open("OPCODE.txt", "ab") as f:
                f.write(int.to_bytes(func_index, 1, 'big'))
            # Continue execution automatically
            idaapi.continue_process()
        elif ea == BREAK_EA_READ_VMCODE:
            edx = get_reg_value("edx")
            print(f"VMCODE {hex(edx)}: ")


        return 0
tracer = Tracer()
tracer.hook()
```

`Trivial.py`: Tiến hành đọc từ resource ra giống chương trình, ta có từng part handler VM. Deobfuscate MBA từng handler shellcode này với `msynth`. Ta được `Disassembly_Shellcode.txt`, sửa script của msynth để lấy các vùng nhớ quan trọng trong shellcode ra. Ở đây ta nắm qua được đoạn relative mem sau:
```
3E16: VM EIP.
3E14: VM ESP.
3A00: STACK.
3000: Ta tạm gọi là Abyss mem, tại 3000 chứa input utf16.
3E00: Vùng này chứa các giá trị cho tính toán sau này.
```

Khi này ta sẽ được file disassembly shellcode như trên.

`Filtering.py`: Khi này các đoạn shellcode có chức năng tương ứng sẽ có 1 cái pattern tương tự nhau khi chúng nó tương tác với các vùng nhớ ở trên. (Có and or các thứ là pattern na ná nhau quá, làm tay =)).)

Khi đã gộp thành công các opcode có chức năng như nhau vào từng nhóm, ta ngồi đọc chức năng 1 opcode là xong.

`Raw_disassembler.py`: Sau khi đã có chức năng của từng nhóm VMcode, code 1 cái disassembler để đọc progress của nó. Ra được cái `VMCODE_LOG.txt`. Nếu theo dõi luồng thực thi, ta thấy nó dùng 5 kí tự 1, nhân từng cái với 1 byte trong dãy 25 byte digit trong 0x3E00 kia. Sau đó cộng hết vào rồi CMP => phương trình 5 ẩn cơ bản. Có 5 cái phương trình như thế, và chung format với toàn bộ kí tự còn lại.

(Ngu z3)
```
from z3 import *
fin = ""
#CHUNK 1
vars = [Int(f'x{i}') for i in range(5)]
x0, x1, x2, x3, x4 = vars
s = Solver()

s.add(x0*3 + x1*4 + x2*3 + x3*7 + x4*5 == 0x6d9)
s.add(x0*5 + x1*4 + x2*0 + x3*8 + x4*0 == 0x589)
s.add(x0*1 + x1*6 + x2*3 + x3*2 + x4*0 == 0x387)
s.add(x0*8 + x1*0 + x2*3 + x3*5 + x4*9 == 0x8da)
s.add(x0*0 + x1*8 + x2*8 + x3*0 + x4*4 == 0x600)

if s.check() == sat:
    m = s.model()
    for i in range(5):
        res = m[vars[i]].as_long()
        fin += chr(res)
else:
    print("Vo nghiem")

#CHUNK 2
vars = [Int(f'x{i}') for i in range(5)]
x0, x1, x2, x3, x4 = vars
s = Solver()
s.add(x0*3 + x1*4 + x2*3 + x3*7 + x4*5 == 0x84a)
s.add(x0*5 + x1*4 + x2*0 + x3*8 + x4*0 == 0x678)
s.add(x0*1 + x1*6 + x2*3 + x3*2 + x4*0 == 0x465)
s.add(x0*8 + x1*0 + x2*3 + x3*5 + x4*9 == 0x9bc)
s.add(x0*0 + x1*8 + x2*8 + x3*0 + x4*4 == 0x720)

if s.check() == sat:
    m = s.model()
    for i in range(5):
        res = m[vars[i]].as_long()
        fin += chr(res)
else:
    print("Vo nghiem")

#CHUNK 3
vars = [Int(f'x{i}') for i in range(5)]
x0, x1, x2, x3, x4 = vars
s = Solver()
s.add(x0*3 + x1*4 + x2*3 + x3*7 + x4*5 == 0x6e4)
s.add(x0*5 + x1*4 + x2*0 + x3*8 + x4*0 == 0x475)
s.add(x0*1 + x1*6 + x2*3 + x3*2 + x4*0 == 0x408)
s.add(x0*8 + x1*0 + x2*3 + x3*5 + x4*9 == 0x7ad)
s.add(x0*0 + x1*8 + x2*8 + x3*0 + x4*4 == 0x778)

if s.check() == sat:
    m = s.model()
    for i in range(5):
        res = m[vars[i]].as_long()
        fin += chr(res)
else:
    print("Vo nghiem")

#CHUNK 4
vars = [Int(f'x{i}') for i in range(5)]
x0, x1, x2, x3, x4 = vars
s = Solver()
s.add(x0*3 + x1*4 + x2*3 + x3*7 + x4*5 == 0x77f)
s.add(x0*5 + x1*4 + x2*0 + x3*8 + x4*0 == 0x6ab)
s.add(x0*1 + x1*6 + x2*3 + x3*2 + x4*0 == 0x44d)
s.add(x0*8 + x1*0 + x2*3 + x3*5 + x4*9 == 0x89c)
s.add(x0*0 + x1*8 + x2*8 + x3*0 + x4*4 == 0x64c)

if s.check() == sat:
    m = s.model()
    for i in range(5):
        res = m[vars[i]].as_long()
        fin += chr(res)
else:
    print("Vo nghiem")

#CHUNK 5
vars = [Int(f'x{i}') for i in range(5)]
x0, x1, x2, x3, x4 = vars
s = Solver()
s.add(x0*3 + x1*4 + x2*3 + x3*7 + x4*5 == 0x8f6)
s.add(x0*5 + x1*4 + x2*0 + x3*8 + x4*0 == 0x79a)
s.add(x0*1 + x1*6 + x2*3 + x3*2 + x4*0 == 0x511)
s.add(x0*8 + x1*0 + x2*3 + x3*5 + x4*9 == 0x9ba)
s.add(x0*0 + x1*8 + x2*8 + x3*0 + x4*4 == 0x7a0)

if s.check() == sat:
    m = s.model()
    for i in range(5):
        res = m[vars[i]].as_long()
        fin += chr(res)
else:
    print("Vo nghiem")

print(fin)
```
