### 1. What is the full path of the script used by Simon for AWS operations?

Có 2 khu vực ta có thể check, dựa vào 2 file artifact đề cung cấp. Đầu tiên mình check backup file ở `session.xml`:

![image](https://github.com/NVex0/uWU/assets/113530029/0f0c1940-9470-4e8e-9425-bc2618224fc4)

Xem chừng không có gì hot, mình tiếp tục check lịch sử mở file gần đây bằng notepad++ ở `config.xml`, tại đây ta thấy 1 file perl tên là `AWS_objects migration.pl`:

![image](https://github.com/NVex0/uWU/assets/113530029/be55265d-b430-4f41-a0da-089ec7d47b46)

Khả năng cao đây là script của Simon để hoạt động với AWS :))

> Answer: `C:\Users\Simon.stark\Documents\Dev_Ops\AWS_objects migration.pl`

### 2. The attacker duplicated some program code and compiled it on the system, knowing that the victim was a software engineer and had all the necessary utilities. They did this to blend into the environment and didn't bring any of their tools. This code gathered sensitive data and prepared it for exfiltration. What is the full path of the program's source file?

Tại backup, có 1 script java thực hiện gom các file theo các extension xác định, rồi zip lại vào 1 file. Đúng mục tiêu như mô tả `This code gathered sensitive data and prepared it for exfiltration`. Từ đây ta sẽ tìm full path của nó, dễ dàng nhìn thấy trong `session.xml`.

> Answer: `C:\Users\simon.stark\Desktop\LootAndPurge.java`

### 3. What's the name of the final archive file containing all the data to be exfiltrated?

Đọc trong code, nó zip lại với tên `Forela-Dev-Data.zip`.

> Answer: `Forela-Dev-Data.zip`

### 4. What's the timestamp in UTC when attacker last modified the program source file?

Cũng tại session, mình thấy 2 trường `originalFileLastModifTimestamp` và `originalFileLastModifTimestampHigh`. Dựa theo docs này:

![image](https://github.com/NVex0/uWU/assets/113530029/f7ce4f52-ec7b-4143-8010-4dc0b8a4acf0)

Ta làm tương tự và decode LDAP timestamp ra. Ta có kết quả.

> Answer: `2023-07-24 09:53:23`
