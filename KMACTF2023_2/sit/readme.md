![image](https://github.com/NVex0/uWU/assets/113530029/ebbb6b58-bf26-4e85-8079-a2c5071c4c60)

Dựa theo description, ta biết được ta phải đi tìm 1 con ransomware autostart. Mình thử kiểm tra trong registry và scheduler task đều không thấy, và tới Startup thì mình thấy 2 file shortcut:

![image](https://github.com/NVex0/uWU/assets/113530029/f86d4165-1b51-4af0-93c5-1de7b2b56381)

Mình thử parse bằng LECmd:

![image](https://github.com/NVex0/uWU/assets/113530029/4b84f0e8-7a61-42ef-97f6-fdbf8653692d)

file shortcut đầu thì không có gì đáng chú ý, còn shortcut unikey này thì siêu khả nghi:

+ Shortcut unikey nhưng gọi tới 1 path khá kì quặc: `C:\Users\admin\AppData\LocalLow\Microsoft\CryptnetUrlCache\Content\datahost.exe`. Con exe đi kèm cũng sus không kém.

+ Hoạt động trên file xác định: cụ thể là `C:\Program Files\Common Files\Microsoft Shared\TextConv\tailieu`.

Từ đây ta có thể đoán được đây chính là con ransomware mà ta cần tìm.

Mình check thử xem nó compile bằng gì:

![image](https://github.com/NVex0/uWU/assets/113530029/dfb93a85-c016-4f3e-bfbe-f20c7214c24a)

Ok, là python. Mình tiến hành sử dụng `Pyinxtractor` và `Uncompyle6` để reverse. Và ta lấy được python source code:

```
import os, sys, random, platform
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256, MD5

def encryption(file, key, iv):
    with open(file, 'rb') as (enc):
        data = enc.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        write = ciphertext
    enc.close()
    with open(file + '.huhu', 'wb') as (data):
        data.write(write)
    data.close()


while True:
    filename = sys.argv[1]
    sed_ = int(os.path.getctime(filename))
    random.seed(sed_)
    key = SHA256.new(str(random.randint(1, 13374953)).encode('utf-8')).digest()
    iv = MD5.new((platform.node() + '-' + os.path.dirname(os.path.abspath(filename))).encode('utf8')).digest()
    encryption(filename, key, iv)
    os.remove(filename)
    break
```

Có thể thấy nó encrypt bằng AES và append extension `huhu` vào sau file sau khi encrypt. Tại path của `tailieu`, ta có thể tìm thấy `tailieu.huhu` ở đó.

- Đầu tiên là key, key lấy sha256 của 1 giá trị random trong khoảng chỉ định như trên code, dựa trên seed là creation time của filename, cụ thể là `tailieu`.

  Mình dùng `MFTECmd` để parse $MFT file ra, và tìm create time của `tailieu` (time này ở GMT sẵn nhé, không cần đổi về local):

  ![image](https://github.com/NVex0/uWU/assets/113530029/c5bd035a-c4dc-4bdd-8eb3-9ec931822b2e)

  -> Epoch timestamp ta có được là: 1692896933.

- Kế đến là iv, là md5 hash của computername-dir path của `tailieu`. computername dễ dàng tìm được trong registry:

  ![image](https://github.com/NVex0/uWU/assets/113530029/0ced2f0c-bea6-4132-9651-5cce9757b5a2)

  dir path của `tailieu` là `C:\Program Files\Common Files\Microsoft Shared\TextConv`.

Toàn bộ dữ kiện cần thiết đã có đủ, mình decrypt thôi:

```
import random
from Crypto.Hash import SHA256, MD5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

random.seed(1692896933)
key = SHA256.new(str(random.randint(1, 13374953)).encode('utf-8')).digest()
iv = MD5.new(('KTMM-C:\Program Files\Common Files\Microsoft Shared\TextConv').encode('utf8')).digest()

with open('tailieu.huhu', 'rb') as f:
        data = f.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.decrypt(data)
        final = unpad(ciphertext, AES.block_size)
with open('outfile', 'wb') as f:
        f.write(final)
```

Outfile là 1 file pdf chứa 1 mã QR, scan QR ta sẽ được flag.

Flag: `KMACTF{Wh3n_Pl4y1n9_CTF,_pl@Y_w1tH_4ll_Ur_h34r7}`
