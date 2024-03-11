C2 server, extract Exe từ Pcap ra và phân tích thôi :))

Exe .net, mình dùng dnspy.

Ta có salt của đoạn derive key trong hàm encrypt/decrypt sau khi decode là: `Very_S3cr3t_S`

![image](https://github.com/NVex0/uWU/assets/113530029/5732025d-1e11-49d0-8050-d2dd6fea6d9c)

Derive key, ta có thể tìm thấy password ngay trong code, salt ở bên trên. Ngoài ra còn 1 tham số nữa là Iteration, default value của nó ta có dựa vào đây:

https://referencesource.microsoft.com/#mscorlib/system/security/cryptography/rfc2898derivebytes.cs,78

Value = 1000:

![image](https://github.com/NVex0/uWU/assets/113530029/af05a5b9-13de-4324-8d6e-28b22e70c5ed)

Từ đó ta derive ra bytes sequence như sau:

![image](https://github.com/NVex0/uWU/assets/113530029/6c6f410b-681c-47ab-b46d-f9470ea852eb)

Truncate nó và decrypt thôi, mình decrypt từng cái 1, tại đây mình có part 2 và part 1: _h45_b33n_r357

![image](https://github.com/NVex0/uWU/assets/113530029/91c78c54-f72e-4f56-92cf-860e43295734)

![image](https://github.com/NVex0/uWU/assets/113530029/997fd24a-8173-49b0-8249-5d867b7b6feb)

Tại đây chạy powershell với param encode:

![image](https://github.com/NVex0/uWU/assets/113530029/058e951a-7a58-4fd6-8ab5-1865be55bdd4)


Mình decode nó ra, ta sẽ thấy part 3 được set tên cho new schedule task:

![image](https://github.com/NVex0/uWU/assets/113530029/208290c0-7211-4516-a26b-8be6526a25be)

Flag: `HTB{c0mmun1c4710n5_h45_b33n_r3570r3d_1n_7h3_h34dqu4r73r5}`
