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
