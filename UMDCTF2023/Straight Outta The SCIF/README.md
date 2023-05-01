Đề cho ta 1 file PDF. Khi mở file PDF ta thấy các trang PDF chứa rất nhiều text bị redacted. Mà khi extract ra để đọc thì không có gì đáng chú ý lắm. (Lyrics của Never Gonna Give You Up và hội thoại các nhân vật trong Bee Movie).

Kiểu như vậy:

![image](https://user-images.githubusercontent.com/113530029/235313428-eea57fff-753e-444b-97d2-41619e4aba2f.png)

Nhưng nếu nhìn kĩ hơn, ta sẽ thấy các chấm vàng nằm trên trang PDF. Có thể xem trên bit plane 5 của trang pdf đó để nhìn rõ hơn các chấm này:

![image](https://user-images.githubusercontent.com/113530029/235314015-1313971c-697b-478c-95d8-2f7770960b06.png)

Các chấm này hướng ta tới 1 kiểu stego gọi là `printer steganography`, hay còn gọi là `MIC (Machine Identification Code)`, hay `Yellow Dots`.

> Các thông tin sử dụng loại stego này thường là Serial Number của máy in, ngày giờ bản in được xuất ra,...vân vân.

Để extract các thông tin này, mình sử dụng https://github.com/dfd-tud/deda - là 1 tool để extract các dots đó ra và đưa ra thông tin mình đã nêu trên.

Đầu tiên, để lấy các trang pdf dưới dạng ảnh, mình sử dụng `pdftoppm`:

`pdftoppm top-secret-team-rocket.pdf scan -png`

Tiếp tới là extract thông tin bằng `deda_parse_print`:

`deda_parse_print scan-01.png`

cho ra được các thông tin như thế:

![image](https://user-images.githubusercontent.com/113530029/235314655-d8305211-9f9a-40aa-a643-8bad5ab434b0.png)

Để ý phần serial (hoặc printer) khá sus, ta lấy hết serial của toàn bộ 15 ảnh trang PDF ra với command:

`for i in {01..15`}; do deda_parse_print scan-$i.png | grep serial; done`

![image](https://user-images.githubusercontent.com/113530029/235420589-66dcae07-bb64-421c-a8eb-aa6b0260d447.png)
