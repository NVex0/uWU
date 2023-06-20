![Screenshot (4293)](https://github.com/NVex0/uWU/assets/113530029/8e282382-8afc-44f5-977e-308a0a5f36c6)

1. *Tên của máy tính là gì?*

Load file SYSTEM theo path `DFIR\config\SYSTEM` - file hệ thống lưu trữ cấu hình, vào Registry Viewer, tiếp tục tìm theo path: `ControlSet001\Control\ComputerName`. Data của `ComputerName` chính là tên máy:

`DESKTOP-AL3DV8F`

2. *Anna đã xem một video về hack trên youtube, cung cấp dấu thời gian lúc đó (UTC)*

Load folder vào Autospy:

Trong `Web History`, ta thấy 1 link youtube với title `Metasploit For Beginners - How To Scan And Pwn A Computer | Learn From A Pro Hacker`. Trừ nó ra thì còn lại là nhà báo Flex với xem video gái thôi :v. Ta lấy time của nó, nhớ đổi từ UTC +7 về UTC:

`21/05/2023-09:04:13`

3. *Thời gian lần cuối cùng người dùng đăng nhập thất bại (UTC)*

Load file SAM theo path `DFIR\config\SAM` - file hệ thống lưu trữ thông tin người dùng, vào Registry Viewer, tìm theo path `SAM\Domains\Account\Users\000003E8`, ta có được last failed login time (ở UTC sẵn):

`09/05/2023-08:17:51`

Flag: `KMACTF{DESKTOP-AL3DV8_21/05/2023-09:04:13_09/05/2023-08:17:51}`
