Cate: `reverse`

Đề cho 1 con ELF, chắc cũng như bao con crackme khác, enter password -> done.

Mình decompile sử dụng `pyinstxtractor` và 3 tool luân phiên :)) `pycdc`, `Uncompyle6`, `Decompyle3`.

Ta được chương trình gốc nhìn khá hoa mắt. Đại khái là obfuscate xor key, sau đó thực hiện 1 loạt decode base64, decompress các thứ lên  `globals().[__doc__]`. Sau đó code sử dụng `marshal` để load phần ta vừa làm 1 loạt thao tác lên `globals().[__doc__]`. Load lên xong thì nó exec object này. Thêm vào đó, mình thấy có thêm 1 class con V gọi tới Z, nhưng nó không được define ở đâu cả:

![image](https://github.com/user-attachments/assets/e3d57133-4e1b-4b52-9709-5ff6f447930f)

Hiển nhiên rồi, ta sẽ đào sâu vào serialize object mà marshal đã load kia lên. Ở đây nó đang là bytecode (Ae có thể dùng `compile()` để xem output thử). Vì marshal chạy không đúng env đúng phiên bản python thì bytecode sẽ không đọc được. Ở đây ta có thông tin khi thực hiện decompile lần đầu tiên, compiler của con file này ver 3.7.0:

![image](https://github.com/user-attachments/assets/8a33c9ba-a120-4607-b2cc-a010d07e14b3)

Khá ảo ma khi mình thử load trên env python 3.7.0 báo lỗi bad marshal data liên tọi 💀, nên mình đã đi tìm hiểu cách khác.

Tại blog này: https://www.cnblogs.com/jzking121/p/15312628.html. Mình biết được là chỉ cần thêm header từ `struct.pyc` vào để biến bytecode object kia thành 1 file pyc phù hợp và chạy ngon ơ.

Nhờ vậy, mình decompile và đã đục được vào bên trong nó. Tuy nhiên lại là sử dụng `globals().[__doc__]`, khác với đoạn đầu, global doc hiện tại là raw bytecode luôn, được encode `raw_unicode_escape` trước khi marshal load nó vào tiếp. Bên dưới nó define thêm 1 attribute con của class V như mình đề cập ở đoạn đầu.

Khi nhìn vào mớ bytecode còn lại, mình thấy rất nhiều string `raw_unicode_escape`, tức là mình đã đoán là sẽ bắt ta lôi đầu lên rất nhiều đoạn bytecode bị marshal lại, khi decompile ra phần con tiếp theo thì đúng thế thật 😃

Thế nên mình viết script sau để đục tới gốc nó, đồng thời lưu lại dòng attribute mới của V mỗi lần decompile:

```
from base64 import b64decode
from zlib import decompress
import os

data = """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"""
#Stage1
# print(True.__class__.__name__[1] + [].__class__.__name__[2])
# print(().__class__.__eq__.__class__.__name__[5:7][::-1],end="")
# print(().__class__.__eq__.__class__.__name__[2],end="")
# print(().__class__.__eq__.__class__.__name__[8],end="") -> os.read()

k1 = b"viblo"
k2 = b"\x7f\x45\x4c\x46"
b64d = b64decode(data)
msobj = [(b64d[i] ^ k1[i % len(k1)]) for i in range(len(b64d))]
msobj = b"".join([int.to_bytes(msobj[i] ^ k2[i % len(k2)], 1, 'big') for i in range(len(msobj))])
msobj = decompress(b64decode(decompress(msobj)))

#py3.7 - struct.pyc
byte_string = b'\x42\x0d\x0d\x0a\x00\x00\x00\x00\x70\x79\x69\x30\x01\x01\x00\x00'
msobj = byte_string + msobj
with open('Stage.pyc', 'wb') as pyc:
    pyc.write(msobj)
     
######################
#Stage2
os.system("uncompyle6 Stage.pyc > decompiled.txt")
sw = 0
while True:
    try:
        if sw != 0:
            with open("decompiled.txt", "rb") as f:
                msobj = f.read()
                msobj = byte_string + msobj
            with open(f"temp_mso{str(sw)}.pyc", "wb") as f:
                f.write(msobj)
            with open('Stage.pyc', 'wb') as pyc:
                pyc.write(msobj)
                
            os.system("uncompyle6 Stage.pyc > decompiled.txt")
                          
        with open("decompiled.txt", "r") as f:
            fd = f.readlines()

        leftover_code = fd[-3] #dong code thua append vao 1 file moi
        proc_py = ".encode('raw_unicode_escape')\
                \nwith open('decompiled.txt', 'wb') as f:\
                    \n\tf.write(globals()['__doc__'])"
        fd = "".join(fd[5:-4])[:-1]  #globals()[.__doc__]
        
        with open("leftover_code.txt", "a") as lc:
            lc.write(leftover_code)

        with open("dat_proc.py", "w") as f:
            f.write(fd + proc_py)

        os.system('python dat_proc.py')
        sw += 1
    except:
        os.system("del /f decompiled.txt dat_proc.py Stage.pyc")
        break
```

Khi này, mình có thể nói là đã có toàn bộ code không bị serialize. Tại vòng lặp cuối, code không theo format global doc + V.attribute nữa nên nó lỗi, mình nhặt con `temp_mso18.pyc` (18, 19 gì đấy) ra decompile tay.

Khi này, ta có full script như sau:

```
"""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"""
from itertools import cycle as d
import marshal as m
import dis
from sys import argv as w
from zlib import decompress as z
import sys as y, string as s
c = chr
i = int
o = ord
l = s.ascii_lowercase
u = s.ascii_uppercase
p = print
v = eval
p("Enter key")
j = 16
from base64 import b64decode as b
e = print
x = lambda h, e, n: "".join([chr(int("".join([str(n.index(o)) for o in f]), e) - j) for f in h.split(n[e])]).encode() #b'viblo'
g = lambda p, q: b''.join([bytes([p ^ q]) for p, q in zip(p, d(q))])
t = b"\x7f\x45\x4c\x46"
for _ in range(256)[::(-1)]:
    try:
        (e(m.loads(z(b(z(g(g(b(globals()['__doc__']), b"viblo"), t)))))), V.Z(getattr(__import__(True.__class__.__name__[1] + [].__class__.__name__[2]), ().__class__.__eq__.__class__.__name__[5:7][::-1] + ().__class__.__eq__.__class__.__name__[2] + ().__class__.__eq__.__class__.__name__[8])(1, j))) #os.read() 16 bytes -> get input, cũng là len flag.
    except:
        pass

class V:
    pass
V.S = lambda x: 4 * x[4] - 3 * x[5] - 1 * x[6] == o(l[17])
V.R = lambda x: 2 * x[4] - 3 * x[5] + 2 * x[6] == o(l[9])
V.Q = lambda x: x[4] + x[5] - x[6] == o(l[13])
V.P = lambda x: x[9] ^ x[0] == x.index(x[-1])   #16 ký tự -> x.index(x[-1]) = 15
V.O = lambda x: x[14] ^ x[9] == 62
V.N = lambda x: x[13] ^ x[14] == 33
V.M = lambda x: x[12] ^ x[13] == 39
V.L = lambda x: x[11] ^ x[12] == 28
V.K = lambda x: x[10] ^ x[11] == 13
V.J = lambda x: x[9] ^ x[10] == 41
V.I = lambda x: x[1] == x[15] ^ 85
V.H = lambda x: x[3] == x[2] % 256
V.G = lambda x: not i(c(x[2]))
V.F = lambda x: y.version[2] == c(x[2] + 7)    #sys.version trả về 3.7.0 -> y.version[2] = 7, y.version[0] = 3
V.E = lambda x: y.version[0] == c(x[15] + 1)
V.D = lambda x: x[7] == x[15] + 1
V.C = lambda x: x[0] == x[8]
V.B = lambda x: x[0] == ord(__name__[0])        #__main__ -> x[0] = "_"
V.Y = "Nope"
V.X = "Correct"
#V.Z = lambda x: p(V.X) if all([getattr(V, k)(x) for k in u[1:19]]) else p(V.Y)        
```

Phần Class V, nó sẽ check điều kiện của từng ký tự trong flag, thỏa mãn mớ tính toán kia, all True thì print Correct. Việc của ta là ngồi tính toán đơn giản lại mớ đấy là ra flag thôi.

Tuy nhiên phần phương trình 3 nghiệm của mình có vẻ có vấn đề, sẽ update sau :/

> Why `dJ@`? why not `dBy`?
