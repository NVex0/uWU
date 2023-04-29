mở file pcap lên, export theo ftp ta được 4 file:

![image](https://user-images.githubusercontent.com/113530029/235311462-2f32136d-c9ff-4a5f-8720-f5cddf9d05ef.png)

Trong đó có 1 file dung lượng lớn hơn hẳn 3 file còn lại:

![image](https://user-images.githubusercontent.com/113530029/235312089-dca806fb-e5b8-4815-93cc-a4277b956d92.png)

Check bằng HxD. Thấy ở phần đầu có magic number `50 4b 03 04`. Vậy nên ta thêm extension `zip` vào file `secret` đó.

Mở ra thì thấy có 1 file mp4 nhưng đã bị khoá. Crack với `john` và được pass là `pika`. Mở vid ra và có được flag:

`UMDCTF{its_n0t_p1kachu!!}`
