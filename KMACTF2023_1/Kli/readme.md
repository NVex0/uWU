![Screenshot (4296)](https://github.com/NVex0/uWU/assets/113530029/cdd6a816-0cde-4ae4-9638-ff7279c1e9cd)

Tóm tắt cách giải :( 
> Src: kakuja

![image](https://github.com/NVex0/uWU/assets/113530029/31141fbd-31f3-4371-85be-be67dbc2223b)

Đại khái là biết Flag format rồi :v (KMACTF)

Ta sẽ tiến hành encrypt "KMACTF" bằng dòng openssl grep được từ  `strings chall.vmem | grep fl4c.txt -A 10 -B 10`. 

Sau đó grep đoạn đầu của dãy base64 thôi (8 bytes), là có được encrypted_txt.

Decrypt ngược lại với các thông số đã biết -> Flag.
