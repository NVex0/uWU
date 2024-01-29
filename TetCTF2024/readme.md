Misc/Forensics - Author troll 🐸

![image](https://github.com/NVex0/uWU/assets/113530029/0e24a4d6-5fc7-487e-aa80-6cb76661acad)

Chall: https://mega.nz/file/U20TCS7Z#dXWlXyL4MKVx5J5RahJRpC3uB_oUJrH1IlPdRhmrNvA

Vì author ra đề troll, chưa check nên tồn tại nhiều unintended solution, ở đây mình sẽ làm theo hướng mà mình nghĩ là intended 🐧.

## 1. Find the malicious code and tell me the IP and Port C2
----

Đầu tiên, ta load file `Backup.ad1` vào `FTK Imager`.

Vì description có nói tới việc đọc rules xong thì máy bị infected. Đầu tiên mình check trong `Recent` folder:

![image](https://github.com/NVex0/uWU/assets/113530029/5eb2e3c8-f4d7-4a98-9baa-8cd658859750)

Ta thấy file lnk tới 1 file Rules, lướt binary xuống xem ta sẽ có file path nó trỏ đến:

![image](https://github.com/NVex0/uWU/assets/113530029/fe2cf0d9-5c45-421b-af99-57164cafad9f)

Mình sẽ dump file docx này ra từ memdump mà đề bài đã cho bằng `Volatility3`:

![image](https://github.com/NVex0/uWU/assets/113530029/22790b83-4390-4341-9f5e-bf7b984d427f)

Và vì là Docx, mình tiếp tục check `Recent` folder của Office:

![image](https://github.com/NVex0/uWU/assets/113530029/ad6c44f9-2145-4df1-bdb6-d7b371f68e7e)

Như ta thấy, recent opened file có file Rule, ngoài ra nó load cả Template của file docx lên. Tuy nhiên khi mình check trên file docx thì không có dấu hiệu nào là malicious template cả 💀. Vì thế mình tiếp tục check trong `Template`:

![image](https://github.com/NVex0/uWU/assets/113530029/1d807350-82f2-4d7d-8783-154ce6e96175)

Template có enable macro (dotm), khá khả nghi. Mình extract file `Normal.dotm` và kiểm tra macro của nó bằng `olevba`:

![image](https://github.com/NVex0/uWU/assets/113530029/da02281f-65e2-41d6-b1f4-874322cc7239)

Sau khi đọc qua code, ta tạm hiểu được là nó khởi tạo socket, connect tới c2 server, gọi reverseshell bằng createproc cmd. 

Và tại code, ta có luôn IP và Port của C2 Server:

![image](https://github.com/NVex0/uWU/assets/113530029/8295653a-1b48-4027-bc0e-71ab8793f22b)

## 2. What was the first flag you found? 
----

Tại đây, dưới cùng của code, ta thấy có 1 comment được encode base64:

![image](https://github.com/NVex0/uWU/assets/113530029/ec754fe6-8009-4d68-834a-b1383e96aaa0)

Sau khi decode 5 lần ra thì ta có part1 của flag:

![image](https://github.com/NVex0/uWU/assets/113530029/cc268610-7c3f-4bc4-ba16-12d82d2897b9)

## 3. After registering an account, I no longer remember anything about my account. Can you help me find and get the second flag? 
----

:v Tác giả chưa check đề nên History vẫn chứa info về flag này, nhưng mình sẽ làm theo 2 cách khác:

- Cách 1: Dựa vào bài viết này: https://systemweakness.com/extracting-saved-passwords-from-web-browser-1444dbfb6551. Đầu tiên mình extract file `Login Data` ra và view bằng tool xem sql online. Ta thấy được 1 account pastebin được lưu pass có user name là `tecij23311`:
  ![image](https://github.com/NVex0/uWU/assets/113530029/a4038486-2f3d-41d5-a9f9-bac257c24a67)
  
  Sau đó mình dump proc của chrome ra, sau đó dùng combo tối thượng `string` `grep` tương tự cách họ demo trong đó:

  ![image](https://github.com/NVex0/uWU/assets/113530029/f2b6fd8d-8cee-41f8-a0f2-449c69bf1c90)

  Ta có được password là `tecij23311Pass`. Login pastebin bằng tài khoản đó và ta có được part2.

- Cách 2: Painful, nhưng nghe chắc chắn hơn. Mình sử dụng công cụ `MemprocFS`. Ở đây mình load thêm plugin `pym_regscrets` vào tool:

  ![image](https://github.com/NVex0/uWU/assets/113530029/be08b6f7-5d47-4fbe-98cd-04098601540a)

  Sau đó load mem vào:

  ![image](https://github.com/NVex0/uWU/assets/113530029/cc61220e-37b9-4011-b102-c45a9831a134)

  Check kết quả parse được từ plugin chúng ta thêm vào, mình lấy được windows default password:

  ![image](https://github.com/NVex0/uWU/assets/113530029/7716c212-7489-4ecf-91dc-9522e4478795)

  Sau khi có lsa pass, mình sử dụng `mimikatz` để lấy masterkey:

  ![image](https://github.com/NVex0/uWU/assets/113530029/48e25375-b22c-4e7b-9452-b3bf637d45c9)

  Tiếp theo, tại file `Local State`, ta lấy trường `encrypted_key` ra decode base64 và xóa phần `DPAPI` ở đầu file đi:

  ![image](https://github.com/NVex0/uWU/assets/113530029/a19ced76-51e2-4124-b3c5-77edda4ddf34)

  Đây là key dùng để encrypt password ở file `Login Data`, nó đã được mã hóa bởi masterkey. Ở trên ta đã có được masterkey, mình dùng `mimikatz` cùng masterkey này để decrypt ra aes key cần tìm:

  ![image](https://github.com/NVex0/uWU/assets/113530029/11eae174-b5c4-40a3-8ce4-adac677363a0)

  Ta có được aeskey là: `aa b6 83 b4 8a f4 52 76 f7 44 48 5a 2c 95 ba 15 2f c3 ae 2a ff 00 5b 1d d7 ba 19 b1 e2 f0 77 29`.

  Cuối cùng mình sử dụng script sau để decrypt password trong `Login Data`:

```
# Decrypt Chromium Passwords
import argparse
import base64
import os
import re
import shutil
import sqlite3
import sys
from Cryptodome.Cipher import AES

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    
def get_db_connection(chromium_path_login_db):
    try:
        shutil.copy2(chromium_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome database cannot be found")
        return None

# Main Function
def main():
    chromium_path = os.path.normpath('Login Data')
    secret_key = bytes.fromhex('aab683b48af45276f744485a2c95ba152fc3ae2aff005b1dd7ba19b1e2f07729')

    try:
        chromium_path_login_db = chromium_path
        conn = get_db_connection(chromium_path_login_db)
        if(secret_key and conn):
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for index,login in enumerate(cursor.fetchall()):
                url = login[0]
                username = login[1]
                ciphertext = login[2]
                decrypted_password = decrypt_password(ciphertext, secret_key)
                if (decrypted_password != ""):
                    print("Sequence: %d"%(index))
                    print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                    print("*"*50)
            # Close database connection
            cursor.close()
            conn.close()
            # Delete temp login db
            os.remove("Loginvault.db")
    except Exception as e:
        print("[ERR] %s"%str(e))
 
if __name__ == '__main__':
    main()
```

Và ta có được password:

![image](https://github.com/NVex0/uWU/assets/113530029/e4c2a406-03b3-417d-b413-b1ec47f15987)

Tiếp tới là login như cách 1 và lấy part 2 thôi.

![image](https://github.com/NVex0/uWU/assets/113530029/bdf78274-c681-4e4c-9280-8405447f986e)

Flag: `TetCTF{172.20.25.15:4444_VBA-M4cR0_R3c0v3rry_34sy_R1ght?}`
