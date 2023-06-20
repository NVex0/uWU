![Screenshot (4296)](https://github.com/NVex0/uWU/assets/113530029/cdd6a816-0cde-4ae4-9638-ff7279c1e9cd)

Tóm tắt cách giải :( 
> Src: kakuja

![image](https://github.com/NVex0/uWU/assets/113530029/31141fbd-31f3-4371-85be-be67dbc2223b)

## Solve:

Mình thử build profile cho máy, nhưng nhận được hint "nghĩ đơn giản thôi" thì mình quyết định strings grep.

Sau 1 hồi mò thử từng kiểu flag không được thì mình quyết định mò theo extension, và thấy được file tên `fl4c.txt`.

Grep theo `fl4c.txt`, mình tìm thấy 2 dòng encrypt fl4c.txt sử dụng openssl:

![Screenshot (4298)](https://github.com/NVex0/uWU/assets/113530029/5b2fdb9c-a6da-49bf-b56f-01a41497d140)

![Screenshot (4299)](https://github.com/NVex0/uWU/assets/113530029/70530717-68f7-45b5-a404-0b01a11aeaf5)

để ý tới option `-pdkdf2`, khi thêm option này vào openssl, key mà ta set ở option `-k` sẽ không lấy làm key mã hoá trực tiếp, mà nó chỉ là pass để dẫn xuất khoá dựa trên thuật toán pdkdf2. Nên dù có dùng key như nào thì phần `KMACTF` (phần đầu đã biết - flag format) của flag sẽ luôn trả về 1 kết quả.
