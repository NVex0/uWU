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

Mặc định khi mã hoá bằng openssl, luôn có 1 đoạn base64 ở đầu kèm theo là `U2FsdGVkX1` hay ở Ascii là `Salted_`, đi sau đó là 8 random bytes của Salt. Openssl yêu cầu như thế để có thể tương tác được với Encrypted file. 

Ta grep để xem có bất kì đoạn encrypted nào không:

![Screenshot (4303)](https://github.com/NVex0/uWU/assets/113530029/a16aabf4-a8f1-473b-8ad7-46afa4d85c08)

:v Vậy là có Encrypted text rồi, decrypt thử theo 2 lệnh openssl ở trên, tuy nhiên chỉ có 1 cái là thành công. Và sau khi decrypt, ta có được flag:

![Screenshot (4304)](https://github.com/NVex0/uWU/assets/113530029/114bcea7-283f-4c10-9541-d3b2fd15f007)

Flag: `KMACTF{5tr1n9_15_$1mply_too_0v3r_p0w3r}`
