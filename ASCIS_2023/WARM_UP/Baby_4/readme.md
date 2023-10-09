![image](https://github.com/NVex0/uWU/assets/113530029/d4fe283e-2352-4f1e-b61c-23fa8a6c24aa)

#### File đề: https://drive.google.com/file/d/1VbGL1Xvx6PEFiUDAgSgXpMU6YqtLPk16/view?usp=drive_link

Đề cho chúng ta 1 file minidump của 1 chương trình đang chạy mà đề bài nói là "malicious". Mình sử dụng `windbg` để bắt đầu phân tích dump này.

Trên CLI của windbg, ta có thể tìm xem tên process gốc của dump này bằng command `!analyze -v`:

![image](https://github.com/NVex0/uWU/assets/113530029/627bfb0c-c75c-44ca-b629-c17509ebb74b)

Tiếp tới, để xem cái "malicious" mà process này đang làm là gì, mình dùng command `lm` để xem toàn bộ module được load vào process:

![image](https://github.com/NVex0/uWU/assets/113530029/0d5575b5-c14e-448e-bb29-fd2e22ec1eac)

Để ý module đầu tiên được load vào là CobaltStrike, chính là file thực thi khởi chạy tạo thành process này. Bởi khi file thực thi khởi chạy thì tiến trình sẽ load nó vào đầu tiên, sau đó mới load các dll cần thiết mà file đó gọi tới.

Có thể dễ dàng nhìn thấy full path của module đầu tiên:

![image](https://github.com/NVex0/uWU/assets/113530029/3725d688-2826-4ffa-80a1-2a8b1439e6b6)

Mình sẽ extract file thực thi ra khỏi dump để phân tích:

- Đầu tiên nhìn offset của module CobaltStrike, mình extract dãy bytes theo offset đó bằng command `.writemem C:\Users\theon\OneDrive\Desktop\CobaltStrike.exe 00460000 L?00467000-00460000`:

![image](https://github.com/NVex0/uWU/assets/113530029/33145de1-9320-4f15-b8a1-17a0a91c6cf9)

- Tiếp theo, dùng [PE Dump Fixer](https://github.com/skadro-official/PE-Dump-Fixer) để áp offset ban đầu của module trong virtual space vào file ta dump ra ở trên:

![image](https://github.com/NVex0/uWU/assets/113530029/b49014b5-82f2-45b4-9e5c-51229d85b638)

- Cuối cùng là unmap địa chỉ ảo khỏi file bằng [PE Unmapper](https://github.com/hasherezade/pe_unmapper):

![image](https://github.com/NVex0/uWU/assets/113530029/62efcbff-9d5c-4956-90e6-298c8000d746)

Ta đã dump thành công file thực thi từ minidump, load vào ida:

![image](https://github.com/NVex0/uWU/assets/113530029/993e6cf3-250a-429a-ae53-5fd3ca475230)

Đại khái là code sẽ thực hiện decrypt AES-ECB-128 với key là `pbBinary`:

![image](https://github.com/NVex0/uWU/assets/113530029/a0f6a401-3a1c-403a-af02-21e2920d1a4a)

Và ciphertext là `byte_4643f8`:

![image](https://github.com/NVex0/uWU/assets/113530029/22eb88e1-ad68-46de-8f38-c7360cc7cc1c)

Mình decrypt bằng Cyberchef:

![image](https://github.com/NVex0/uWU/assets/113530029/ac69a0eb-927c-4609-8265-744e1f6ea055)

Flag: `ASCIS{H4v3_Y0u_7ri3d_u5ing_57RINg5_0N_M3M0RY_dUmp}`


