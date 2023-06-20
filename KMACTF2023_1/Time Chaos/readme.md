![Screenshot (4287)](https://github.com/NVex0/uWU/assets/113530029/989dd4c3-b9ba-44d4-b926-5b07732e35fd)

Dựa theo đề, ta có thể hiểu các packet được capture không đúng trình tự, có 1 sự sai sót ở đây, cụ thể là thời gian. Tiến hành sort packet theo thời gian, để ý các trường data của ICMP ghép thành các từ có nghĩa :v. Nhưng mà quá nhiều packet, extract bằng tay thì khá tốn thời gian. Mình làm như sau:

Đầu tiên mình lấy 2 trường thời gian và data của IMCP ra:

> `tshark -nr Time_chaos.pcap -T fields -e data.data | xxd -r -p > data.txt` #Lấy trường data ra.

> `tshark -nr Time_chaos.pcap -T fields -e frame.time_epoch > time.txt` #Lấy trường thời gian đến của packet.

Sau đó mình viết script python sau để sort data theo time và có được flag:

```
data = open("data.txt", "r").read()

time = open('time.txt', 'r').readlines()

timelist = []
datalist = []
for i in time:
    timelist.append(float(i))
for j in data:
    datalist.append(j)


sorted_pairs = sorted(zip(timelist, datalist))
sorted_list1, sorted_list2 = zip(*sorted_pairs)

for i in sorted_list2:
    print(i, end = "")
```

Chạy script và được flag:

![Screenshot (4286)](https://github.com/NVex0/uWU/assets/113530029/096afb0c-4d6d-4f26-b947-9558fa32addd)

Flag: `KMACTF{C0d3_cun9_du0c_t0Ol_Cun9_DuOc_nHun9_h1_v0n9_b4n_kh0n9_l@m_m0t_c4cH_tHu_C0nG}`
