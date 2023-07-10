![Screenshot (4468)](https://github.com/NVex0/uWU/assets/113530029/eddf12be-de51-4e7d-9acd-4d153163be6f)

#### Solve:

Truyền tải tập tin qua TFTP, ta đi thẳng vào breakdown phần data trên UDP luôn :v cụ thể là ở udp stream 25:

![Screenshot (4470)](https://github.com/NVex0/uWU/assets/113530029/de8f2839-b066-4e48-a592-dffc6f315a16)

Ta thấy được các thông số của giao thức tftp này: 

> Opcode 1 - Read Request: `192.168.25.1` gửi yêu cầu đọc file lên `192.168.25.135`.

> File name: Flag.pdf.

> Transfer mode: TFTP hỗ trợ 3 transfer mode: `octet`, `netascii`, `mail`. Ở đây là netascii.

Tiếp với udp stream tiếp theo, `192.168.25.135` trả về message với :
> 2 bytes opcode. Opcode = `00 03` ở đây khai báo message này là data message.

> 2 bytes block number. Khai báo thứ tự của data trong stream.

> Cuối cùng là phần data.

![Screenshot (4471)](https://github.com/NVex0/uWU/assets/113530029/193b40e5-9f33-4f03-a0ff-d47fb2f68aba)

Kế đó, `192.168.25.1` gửi lại acknowledgement message tới data mà nó nhận được:

> Opcode = `00 04`. Khai báo cho acknowledgement message.

> 2 bytes block number. Như bạn thấy thì nó là block number của gói tin ngay đằng trước gói này.

  ![Screenshot (4473)](https://github.com/NVex0/uWU/assets/113530029/23d634a4-82d4-4456-a97a-7043d720db49)

Tương tự theo sequence, các gói sau cũng y vậy thôi :v, bây giờ mình tiến hành dump data mà `192.168.25.135` gửi trả `192.168.25.1`, sau đó mình loại bỏ 2 field là opcode và block number của từng gói đi:

`tshark -nr arenas2-forensics-trivialFTP/TrivialFTP.pcapng -Y 'udp.stream eq 26 && ip.src == 192.168.25.135' -T fields -e data.data > data.txt`
```
with open("data.txt", "r") as f:
    data = f.readlines()
fin = open("fin.txt", "w")
for i in data:
    fin.write(i[8:-1])
```

Netascii Transfer mode sẽ encode `Line Feed` -> `Carriage Return/Line Feed` và `Carriage Return -> Carriage Return/Null`. Tương ứng với hex là `0a`-> `0d0a` và `0d` -> `0d00`. Giờ ta làm ngược lại thôi :v :

![image](https://github.com/NVex0/uWU/assets/113530029/f4813793-2218-4a09-adda-f863575ab517)

Tải file pdf đã decode về và mở:

![Screenshot (4475)](https://github.com/NVex0/uWU/assets/113530029/0e24ca2a-4ae2-4aae-972b-3c02380a7dda)

Flag: `CHH{FTP_4nd_TFTP_4r3_b0th_un$af3}`
