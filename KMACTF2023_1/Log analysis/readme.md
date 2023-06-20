![Screenshot (4288)](https://github.com/NVex0/uWU/assets/113530029/4cf16ae0-57d0-42c0-a369-0c578f129639)

Đề bài đề cập đến máy của chị mewlody bị hack, và ta cần thông tin về máy chủ C2 của kẻ tấn công. Khi máy bị hack, nó sẽ cố gắng tìm tới C2 server để tải xuống các lệnh mới nhất từ kẻ tấn công. Vì thế mình kiểm tra kiểm tra log `Microsoft-Windows-PowerShell%4Operational.evtx` là log chứa thông tin về hoạt động của Powershell trên hệ thống.

Khi mở ra, ta xem các event level `Warning` - là level cảnh báo trước về các vấn đề tiềm ẩn:

![Screenshot (4290)](https://github.com/NVex0/uWU/assets/113530029/60bf0889-94d1-467b-bd85-efb97f9a11dd)

Ta thấy `revshell.ps1` được gọi lên,  bypass execution policies để thực thi. Sau đó, với event kế tiếp, ta thấy powershell sau được thực thi:

![Screenshot (4289)](https://github.com/NVex0/uWU/assets/113530029/0759ca82-66d0-4add-ba17-e73c6b643cc9)

Dễ nhìn thấy code ps này khởi tạo IP và Port để connect tới, gửi đi Flag và đi vào 1 vòng lặp để nhận lệnh từ máy chủ từ xa -> Đây chính là thông tin liên quan về C2 Server ta cần tìm. 

Ta tập trung vào phần Flag thôi :v 

Bây giờ mình sẽ mổ xẻ phần flag:

 `KMACTF{$(([System.BitConverter]::ToString(([System.Security.Cryptography.MD5]::Create()).ComputeHash(([System.Text.Encoding]::UTF8.GetBytes(((Get-Process -Id $PID).Id.ToString()+[System.Security.Principal.WindowsIdentity]::GetCurrent().Name+(Get-Date).ToString())))))).Replace('-', '').ToLower())}`

Phần Content của Flag là 1 md5 hash của 1 chuỗi ghép bởi:  
+ PID của tiến trình chạy ps script này.
+ Tên người dùng hiện tại của phiên làm việc.
+ Thời gian hiện tại - lúc log được tạo.

Dễ thấy ngay bên dưới phần general của event, ta có được thời gian của nó:   ![Screenshot (4289)](https://github.com/NVex0/uWU/assets/113530029/05b29957-3b9d-49af-9cfc-9577e161e309)

Nhìn ngay các event trước là event record khi khởi tạo process, ta có được PID của process này: ![Screenshot (4291)](https://github.com/NVex0/uWU/assets/113530029/cc5bb7c9-8451-4302-bade-c9916f82348a)

Sử dụng log Security.evtx, tra vào khoảng thời gian khởi gian xung quanh lúc khởi tạo process (sai số 1s gì đó :v), ta có được tên người dùng (lấy tên đầy đủ, DOMAIN or WORKGROUP + \USERNAME):

![Screenshot (4292)](https://github.com/NVex0/uWU/assets/113530029/c7ceee71-9fcc-4ce3-aa89-af8f7c6d7bb2)

vậy content của Flag là: `4144KMA\long5/22/2023 5:09:58 PM`

Md5 hash content, và ta được Flag: `KMACTF{0da4ab044b8e929ec9c75bc44d24777e}`
