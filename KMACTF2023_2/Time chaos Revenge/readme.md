![image](https://github.com/NVex0/uWU/assets/113530029/46327415-6f9a-43f0-b16b-d5683a86a352)

Đề cung cấp cho mình toàn bộ file folder của 1 máy. Theo mặc định mình cứ tìm bash_history trước:

```
sudo poweroff
nano
ls -la
cat .bash_history
ls
remina
ls -la
sudo apt update
sudo apt install python3-pip
sudo apt install python3-pip --fix-missing
pip3 install scapy
python3 -m pip install scapy
sudo apt install pipx
sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old
python3 -m pip install scapy
python3 pcapgen.py
ls -la /tmp/
rm -rf /tmp/temp.pcap
rm -rf fl.kma
```

Ở home này mình cũng thấy source code của pcapgen.py luôn, nhưng đại khái là code này shuffle packet và mình sort lại theo time giống [Times chao](https://github.com/NVex0/uWU/tree/main/KMACTF2023_1/Time%20Chaos) là được :v.

File pcap đó sẽ locate ở directory /tmp như trên bash, mình lấy data đã sort ra bằng script sau:

```
import os
os.system("tshark -nr chaos.pcap -T fields -e data.data | xxd -r -p > data.txt")
os.system("tshark -nr chaos.pcap -T fields -e frame.time_epoch > time.txt")
data = open("data.txt", "rb").read()
time = open('time.txt', 'r').readlines()
timelist = []
datalist = []
for i in time:
    timelist.append(float(i))
for j in data:
    datalist.append(j)
sorted_pairs = sorted(zip(timelist, datalist))

with open('fl.kma','wb') as f:
    for z in sorted_pairs:
        f.write(z[1].to_bytes(1, 'little'))
```

Tuy nhiên các bytes mình lấy ra nhìn khá vô nghĩa. Ban đầu mình nghĩ nó là shellcode và debug thử thì không thấy gì :(

Lúc sau, để ý tới bash_history có 1 command là `remina`. Vì folder hiện hành (current directory của bash_history ấy), không chứa file gì liên quan `remina`, nên mình check thử trong /bin và /sbin (Đại khái là folder hệ thống và người dùng chứa chương trình thực thi mà khi dùng command tương ứng thì nó gọi tới ấy.) Khi strings thử bin file remina, mình thấy 1 số thứ khá thú vị:

![image](https://github.com/NVex0/uWU/assets/113530029/ec3093c0-fc43-4c07-b023-ac9ac5fc4d9c)

Xem ra chúng ta còn có cả 1 file `fl.png` đi cùng `fl.kma`. Theo mình tìm hiểu thì `remina` là tool để remote desktop, tại sao lại thực thi với các file của người dùng 1 cách cụ thể như vậy?, nên mình ném vào IDA xem thử:

![image](https://github.com/NVex0/uWU/assets/113530029/28511ed7-20c1-4912-91f5-8d280b2b3eac)

Rất rõ ràng :v, `remina` này thực hiện 1 vài phép encrypt bằng xor lên fl.png và cho đầu ra là fl.kma. Mình sẽ đi chi tiết vào như này:

- Đầu tiên, thực hiện lấy hostname set cho biến name. Hostname dễ dàng tìm được từ path /etc/hostname:

  ![image](https://github.com/NVex0/uWU/assets/113530029/b4e7d826-366b-4e7a-84c3-71135893f98c)

  - Tiếp theo là xor bytestream đọc từ file ra với xor key chính là hostname ta vừa có được: `debian`.

  - Cuối cùng là xor với key là 1 số được lấy từ hàm random, với random seed là currenttime tức lúc file thực thi, sau đó modulo cho 256. Não mình ngưng hoạt động lúc đó nên cố gắng tìm bằng được timestamp thực thi của file. Sau đấy mình nhận ra modulo 256 thì bruteforce 256 kí tự là được :(
 
Bắt đầu làm ngược lại thôi:

  - Đầu tiên mình bruteforce key cho bước 2 như đã nói trên. Ta đã biết file gốc là PNG. Vậy nên bruteforce với byte đầu đến khi nó trả về đúng 0x89 là được. Và mình được key cho bước 2 là `137` ở dạng decimal.

  - Kế tiếp là xor với `debian`.

Mình dùng cyberchef để thực hiện. (Lúc decode tới bước 2 thì mình dùng magic, nó tự read QR luôn:v):

![image](https://github.com/NVex0/uWU/assets/113530029/d59d25d3-b99f-430b-93a1-117229df4edb)

Flag: `KMACTF{Dun9_leak_de_nhe_anh_em_:((}`
