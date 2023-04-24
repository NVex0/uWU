xem TCP stream của file, để ý stream có rất `xml` kèm cả 1 phần signature `50 4B`. Tuy nhiên đầu file lại thiếu signature?. Thêm vào thử signature `50 4B 03 04` và save về, ta có được file excel chưa flag:
![image](https://user-images.githubusercontent.com/113530029/233971331-e7f18483-4306-410e-800a-f305abf88f46.png)
