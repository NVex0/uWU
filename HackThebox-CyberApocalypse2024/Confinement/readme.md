Đề cho 1 file ad1, load bằng `FTK Imager` và phân tích. Trong các folder Document thì file bị encrypt, 1 số file bị sửa mỗi byte đầu nên lúc đó mình chưa hiểu là ransomware kiểu gì:v Trôn VN.

Recent các thứ cũng không có gì, nên mình chuyển qua đọc log.

Tại log `Microsoft-Windows-Powershell-Operational`, event id 4104 (common:v), mình trace được command:

![image](https://github.com/NVex0/uWU/assets/113530029/7c6bb614-9381-4ad9-bb4b-194d8523bacd)

Sussy XD, sau whoami là 1 loạt các command như sau:

![image](https://github.com/NVex0/uWU/assets/113530029/5ffac6b9-d7e6-4cb1-a38b-ec917c21c52c)

![image](https://github.com/NVex0/uWU/assets/113530029/b71e9cff-a606-4e9e-b9ce-a2faf4843ec7)

![image](https://github.com/NVex0/uWU/assets/113530029/94e42263-d393-43c2-8676-db92224d8916)

![image](https://github.com/NVex0/uWU/assets/113530029/9f4ce401-8e71-49df-bdb6-56f1a5143fe9)

![image](https://github.com/NVex0/uWU/assets/113530029/eddb2e90-820f-4ff8-b084-c118afec9a17)

![image](https://github.com/NVex0/uWU/assets/113530029/a28a9beb-b98d-4e04-a0f8-7dd0062aaf72)

![image](https://github.com/NVex0/uWU/assets/113530029/d84dd819-5cd0-409d-bee3-51ac016a1741)

![image](https://github.com/NVex0/uWU/assets/113530029/3e63ed5f-7f70-47b1-8f90-092ad5e97db8)

![image](https://github.com/NVex0/uWU/assets/113530029/c90858e5-fc9b-405b-b18a-dda93bbbbec8)

![image](https://github.com/NVex0/uWU/assets/113530029/9a0d3813-37e3-464c-bc9e-48919f25c622)

![image](https://github.com/NVex0/uWU/assets/113530029/0aeeb95d-bbb7-4678-b025-cdf4c4175d6f)

![image](https://github.com/NVex0/uWU/assets/113530029/b63d1b22-53d1-490e-a773-e3b1fabf7759)

![image](https://github.com/NVex0/uWU/assets/113530029/9ecb5bf4-5477-476e-ab65-8264449b0907)

![image](https://github.com/NVex0/uWU/assets/113530029/dd8f211a-4053-4565-abc1-7a783f42081d)

![image](https://github.com/NVex0/uWU/assets/113530029/f1b587b3-801e-4715-911c-21ea48196bfa)

![image](https://github.com/NVex0/uWU/assets/113530029/9606eae5-3bbe-4540-bae3-658bae26f6f6)

![image](https://github.com/NVex0/uWU/assets/113530029/ca3037d2-f4c5-4013-ad02-33669ea74e91)

![image](https://github.com/NVex0/uWU/assets/113530029/6397ff21-ebaf-4704-a0e1-3c38a3af4b23)

![image](https://github.com/NVex0/uWU/assets/113530029/b90cebfc-844b-47e4-828f-a192c4c6028b)

![image](https://github.com/NVex0/uWU/assets/113530029/f49b6adf-60ae-46b8-badd-22fe658ed825)

![image](https://github.com/NVex0/uWU/assets/113530029/51091f2d-325a-4285-a4af-5ea941c4d800)

![image](https://github.com/NVex0/uWU/assets/113530029/b0a1d8b0-41cd-4084-8df4-58690dd3b7c3)

![image](https://github.com/NVex0/uWU/assets/113530029/8ae53a7a-b009-4077-a74f-94f5c30f5a9f)

Tổng kết lại là sau khi có shell, attacker check info domain, ip,... tải về zip chứa 1 mớ các exe gì gì đó. Ta có thể xem đầy đủ trong prefetch của 7z:

![image](https://github.com/NVex0/uWU/assets/113530029/9566e75a-5571-4138-8195-8ee5679176f6)

Attacker chạy 1 số con exe trong đấy, sau đó gỡ Windows Defender đi.

Sau khi chạy 1 số exe trong này, attacker đã xóa file zip và các exe liên quan trong Documents, nên lúc đấy mình không nghĩ ra hướng nào nữa.

Tuy nhiên, attacker chạy xong exe mới gỡ Windows Defender bằng Dism 🐸, điều này hướng mình tới Log Firewall có thể còn thông tin gì đó.

Chính đây là thời điểm `Dism` Defender:

![image](https://github.com/NVex0/uWU/assets/113530029/d11344e8-a748-4928-a31f-87387d081a93)

Ta trace ngược lại 1 ít thời gian:

![image](https://github.com/NVex0/uWU/assets/113530029/88b7c6db-fa94-423b-99d3-9e6863e544db)

Ở đây ta thấy con `intel.exe` trước đó đã bị detect và quarantined. Củng cố hơn cho việc đây là con ransom, tại Powershell log ban nãy, ta có thấy con intel.exe chạy bị lỗi gì đó, Werfault được gọi lên và ghi lại report, tại path `Program Data\Microsoft\Windows\WER` ta có thể tìm thấy crash folder của intel.exe, tại đó chứa wer report của nó. Original filename là Encrypter.exe =))

![image](https://github.com/NVex0/uWU/assets/113530029/84edd137-26e8-4bd1-bbaa-bc70a30324ff)

Sau khi dạo quanh google 1 đêm, mình đọc được 1 bài này:

![image](https://github.com/NVex0/uWU/assets/113530029/2842fcb7-3d75-4286-bd97-e821513affaa)

Tức là vẫn còn cách để khôi phục. Mình nhận ra tiềm năng từ đây :)), mình bắt đầu google 1 số thứ liên quan và tìm hiểu được rằng, file bị detect sẽ được quarantine vào folder `/Program Data/Windows Defender/Quarantine`, từ đó người dùng có thể tùy chọn allow hoặc restore file đó.

Mình tìm được tool sau: https://github.com/knez/defender-dump/tree/master

Tiến hành khôi phục thử thôi:

![image](https://github.com/NVex0/uWU/assets/113530029/934cdec6-7459-455f-aa26-abf4c393c5bd)

Ngon =)). Tiến hành RE thôi nào.
----

![image](https://github.com/NVex0/uWU/assets/113530029/d7553592-c438-47be-8184-89d4f816c57e)

DotNet enjoyer!

Đầu tiên với hàm Main:

![image](https://github.com/NVex0/uWU/assets/113530029/ebd1c85e-0156-4aba-9f07-43e11fe31a6e)

Vì là ransomware, mình sẽ tập trung vào các phần liên quan tới mã hóa thôi. Ta thấy nó tạo 1 object CoreEncrypter với param `(passwordHasher.GetHashCode(Program.UID, Program.salt), alert.ValidateAlert(), Program.alertName, Program.email)`

Tiếp tục đi vào class passwordHasher, nó nối password và salt vào:

![image](https://github.com/NVex0/uWU/assets/113530029/e8268eb0-fe94-4dfc-9dbf-0ec8921edbb1)

Password ở đây là UID và Salt từ class Program:

+ Salt:

  ![image](https://github.com/NVex0/uWU/assets/113530029/080fc068-6bfa-4ef5-876b-0d2036ac36ff)
  
+ Password:
  Nó đang được set giá trị là null, nhưng nếu đọc kỹ thì tại hàm Main, biến này cũng được gọi lên để hàm GenerateUserID() gen giá trị rồi assign vào biến đó.

  GenerateUserID():

  ![image](https://github.com/NVex0/uWU/assets/113530029/8629b796-5dd5-4aca-9259-6be633e1886d)

  Hàm này gen ra 1 chuỗi 14 ký tự xen kẽ chuỗi và kí tự thôi.

  Sau khi gen xong, ta thấy nó được truyền vào object Alert với vai trò là AttackID, khi reference, ta dễ dàng AttackID này được nhồi vào Html chứa thông báo tống tiền:

  ![image](https://github.com/NVex0/uWU/assets/113530029/fbc28490-1961-40a6-b9db-ee417df991aa)

  Vào folder bất kì có file bị encrypt rồi mở file HTA lên xem là ta có AttackID, đồng nghĩa với việc ta đã có password :v :

  ![image](https://github.com/NVex0/uWU/assets/113530029/e8afe1ff-b208-4f6b-b902-69c28c6b2ccd)

Quay trở lại passwordHasher, nó gọi đến Hasher:

![image](https://github.com/NVex0/uWU/assets/113530029/2133da4e-28b8-4d1c-b10b-1ba89a1fc5ed)

Thực hiện concat 2 cái trên ta vừa tìm được, sha512 lại rồi encode base64. Làm tương tự và mình có chuỗi sau:

`A/b2e5CdOYWbfxqJxQ/Y4Xl4yj5gYqDoN0JQBIWAq5tCRPLlprP2GC87OXq92v1KhCIBTMLMKcfCuWo+kJdnPA==`

Sau khi khởi tạo Object CoreEncrypter xong, tại Main, ta thấy nó gọi tới hàm Enc, và Enc lại gọi tới EncryptFile trong CoreCrypter. Ta cùng xem qua:

![image](https://github.com/NVex0/uWU/assets/113530029/3b425841-fef8-4c8b-a6af-abd2166d6c7f)


Đầu tiên nó derive key nhận vào 3 params:

+ Key: chính là param 1 truyền vào Object CoreEncrypter, cụ thể là chuỗi base64 ta tính được từ pass và salt ở trên:

> A/b2e5CdOYWbfxqJxQ/Y4Xl4yj5gYqDoN0JQBIWAq5tCRPLlprP2GC87OXq92v1KhCIBTMLMKcfCuWo+kJdnPA==

+ Salt: là byte array trong code kia, mình convert sang hex:

> 0001010001010000

+ Iterations:

> 4953

> ###### Ngoài lề, sau khi đọc hết code, mình biết được các file vượt quá size mà nó xác định kia (đoạn if), thì nó chỉ mã hóa byte đầu thôi, điều này cũng clear cho mình hơn tại sao lại có ransomware troll thế :v

Derive key thôi!

![image](https://github.com/NVex0/uWU/assets/113530029/f51b1688-900f-4cc8-a7d4-32901c69899f)

Sau đó truncate nó thành 2 phần là key với iv, decrypt aes:

![image](https://github.com/NVex0/uWU/assets/113530029/a53065e9-1d5c-415d-9b0d-4f3ec604230a)

Header PK, decrypt xong rồi. Mở ra và ẵm flag thôi:

![image](https://github.com/NVex0/uWU/assets/113530029/5f5bd532-2095-4d7b-adb2-926c5ff7f3ef)

Flag: `HTB{2_f34r_1s_4_ch01ce_322720914448bf9831435690c5835634}`



