![image](https://github.com/NVex0/uWU/assets/113530029/71e6b8da-92cc-4a94-bdd8-61c11a283d51)Đề cấp 1 file pcap, đại khái là nó truyền file bằng cách zip, set password rồi base64 lại. Khá troll vì không đọc được trường :(. Mình code quick script sau để dump data ra:

```
import os
from base64 import b64decode
os.system('strings phreaky.pcap | grep Password > password')
os.system('tshark -nr phreaky.pcap -Y "smtp && imf" -T fields -e media.type | tr -d "\n" | xxd -r -p > data.txt')
with open("data.txt", "r") as f:
    data = f.readlines()
password = open("password", "r").readlines()
password= [i[42:-1] for i in password]
trigger = 0
seq = ""
j = 0
for i in range(len(data)):
    if len(data[i]) == 77:
        seq += data[i].replace("\n", "")
    else:
        seq += data[i].replace("\n", "")
        print(b64decode(seq))
        with open("temp.zip", "wb") as f:
            print(password[j])
            f.write(b64decode(seq))
        os.system(f'unzip -P "{password[j]}" temp.zip')
        j += 1
        seq = ""

with open("final.pdf", "wb") as f:
    for i in range(1, 16):
        data = open(f"phreaks_plan.pdf.part{i}", "rb").read()
        f.write(data)
```

Result: 

![image](https://github.com/NVex0/uWU/assets/113530029/2a4f1924-ffa8-4775-9f8c-ae62469c3e8f)

Flag: `HTB{Th3Phr3aksReadyT0Att4ck}`
