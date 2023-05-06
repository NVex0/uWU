Với file PCAP của đề, mở lên xem nhánh protocol thì 100% usb:
![image](https://user-images.githubusercontent.com/113530029/236618516-1f00d6be-6eba-4d95-a68d-342d8bb72826.png)

Để ý phần leftover của các packet source `1.13.2`. Phần này lưu dữ liệu của các event trong suốt quá trình kết nối USB. Extract nó ra và lưu vào file `data`:

`tshark -nr cheat.pcapng -Y 'usb.capdata' -T fields -e usb.capdata > data`

`cat` file ra, ta thấy được các dòng data không đều:

![image](https://user-images.githubusercontent.com/113530029/236618878-fa1a750f-7ffc-4be4-8a1f-926bbe939a54.png)

Thông thường các dòng data này sẽ chỉ 8 bytes (khi thao tác với bàn phím) hoặc 4 bytes (khi thao tác với chuột). Tuy nhiên data này lại lên tới 48 bytes :v.

Sau khi hint được release là 1 video quảng cáo full set Xbox S, mình nghĩ ngay tới việc data này từ controller mà ra, nên nó mới lạ thế :v.

Google 1 hồi thì mình tìm hiểu được hầu hết về từng bytes trong dãy data:

Với bytes đầu là type của event. Trong đó `0x20` là khi có thay đổi liên quan tới Button, để ý thì tất cả các dòng nào mà 48 bytes đều có byte đầu là `0x20` hết, nên ta bỏ qua.

Bytes tiếp theo là 1 hằng số?, Bytes 2 là cho id và Bytes 3 là độ dài phần phía sau byte này.

Nói chung 4 bytes đầu không cần để ý lắm, đi tiếp vào Bytes 4 đổ lên, nó là phần data ta cần tập trung vào, ta map phần data đó để lấy các button tương ứng với quick script sau:

```
#MAP CONTROLLER.
#Nó bao gồm cả phần joystick và toạ độ joystick nữa, nhưng Cheat code GTA thì không xài đến joystick nên ta có thể bỏ qua :)
#Start from index 0.

##Map của các bytes thứ 4.
fourth = {
    0x10 : 'gamepad -> a',
    0x20 : 'gamepad -> b',
    0x40 : 'gamepad -> x',
    0x80 : 'gamepad -> y',
    0x01 : 'gamepad -> sync',
    0x04 : 'gamepad -> menu',
    0x08 : 'gamepad -> view',
}

##Map của các bytes thứ 5.
fifth = {
    0x10 : 'lbumper',
    0x20 : 'rbumper',
    0x40 : 'lstick',
    0x80 : 'rstick',
    0x01 : 'dpad_up',
    0x02 : 'dpad_down',
    0x04 : 'dpad_left',
    0x08 : 'dpad_right',
}

##########
with open('data', 'r') as f:
    data = f.readlines()
    for line in data:
        if len(line) == 97:
            fourthbytes = line[8:10]
            fifthbytes = line[10:12]

            left_trigger = line[12:14]
            right_trigger = line[16:18]


            if int(fourthbytes, 16) in fourth:
                print(fourth[int(fourthbytes, 16)])

            if int(fifthbytes, 16) in fifth:
                print(fifth[int(fifthbytes, 16)])

            if int(left_trigger, 16) != 0x00:
                print('l_trigger')
            
            if int(right_trigger, 16) != 0x00:
                print('r_trigger')
```
Run code ta được kết quả như này:

![Screenshot (3861)](https://user-images.githubusercontent.com/113530029/236621250-e8640612-e078-4ffb-8d2f-6d0be0f5f37e.png)

Dựa vào dãy trên, lên mạng mò cheat code GTA thôi.

Đầu tiên với đoạn:

```
dpad_left
dpad_left
lbumper
rbumper
lbumper
dpad_right
dpad_left
lbumper
dpad_left
```

Sẽ tương ứng với cheat code : `Moon Gravity`

Với đoạn kế tiếp:

```
gamepad -> y
dpad_left
dpad_right
dpad_right
gamepad -> x
r_trigger
r_trigger
r_trigger
r_trigger
r_trigger
r_trigger
r_trigger
rbumper
```

Mình grep được 5 bước đầu khớp với 1 cheat code duy nhất : `Slow Motion`. 

> Tuy nhiên phần right_trigger mình chưa rõ lắm, không rõ là author hold nút này hay thế nào mà ra 1 đống như kia.

Với phần còn lại, grep ra cheat code: `Drunk Mode`.

Flag không space, không uppercase, vậy nên ta lấy được flag:

Flag : `shellmates{moongravity_slowmotion_drunkmode}`
