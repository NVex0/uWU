netcat vào, ta thấy đề yêu cầu ghép 3 chữ đầu của con vật đầu tiên với 3 chữ sau của con vật thứ 2.

Quick script như sau để làm việc đó:

```
import socket

HOST = "challs.actf.co"
PORT =  31402

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    rec = s.recv(1024).decode("utf8")
    print(rec)
    msg = ""
    tmp = rec.split()
    print(tmp)
    msg = tmp[6][:3] + tmp[13][-3:] +"\n"
    print(msg)
    s.send(msg.encode("utf8"))
```

Get flag:
![Screenshot (3714)](https://user-images.githubusercontent.com/113530029/233971932-fba006a6-0a80-4767-9062-9837e3b07b10.png)
