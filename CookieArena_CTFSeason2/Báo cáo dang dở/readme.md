![Screenshot (4462)](https://github.com/NVex0/uWU/assets/113530029/8b655ef1-9e86-431e-8d62-9bf0285993d0)

#### Solve:

Đề cho ta 1 file dump, mình dùng `volatility3` để phân tích dump này.

Đầu tiên check các process hiện hành:

![image](https://github.com/NVex0/uWU/assets/113530029/54d827db-c5a6-4cdc-b2f0-5432027b7ffa)

Dựa vào mô tả của bài, dễ nhận thấy process `WinWord.exe` chính là cái ta cần nhắm vào, từ đây mình biết bài tập lớn mà Hoà làm ở trên Word. 

File Word khi chưa lưu sẽ tạo ra file backup nằm trong `AppData\Roaming\Microsoft\Word` hoặc `AppData\Local\Microsoft\Office\UnsavedFiles`. Mình thử scan file với từ `Word` trước:

![Screenshot (4465)](https://github.com/NVex0/uWU/assets/113530029/6aeed601-9b1f-4aba-89f7-4bd37d35f1c9)

Ta có thể thấy file Autorecover đuôi asd - là extension của bản nháp của văn bản chưa lưu. Mình dump nó về, move vào đúng path như trên nhưng ở máy mình và mở ra:

![Screenshot (4466)](https://github.com/NVex0/uWU/assets/113530029/6b346e63-52b7-42e0-94c2-fd1a4aff0300)

Gotcha!

![image](https://github.com/NVex0/uWU/assets/113530029/a45f56f8-905f-4af3-9d45-92f7135cbe1f)

Flag: `CHH{4ut0R3c0v3r_s4v3_my_l1f3}`
