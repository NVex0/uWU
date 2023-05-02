Tiến hành build 1 file để thoả mãn YARA rules thôi.

## Rule 1:

```
rule rule1 {
    condition:
        uint32(0) == 0x464c457f
}
```

Rule 1 check 4 bytes đầu bằng với giá trị `0x464c457f`, mà convert từ hex ra chính là header ELF. Để làm việc này đầu tiên ta viết 1 script C đơn giản:

```
echo "int main() { return 0; }" > main.c
```

Tiếp theo dùng `gcc` để compile file C thành file executable - hay chính là file có header `.ELF`:

```
gcc -o yarapass main.c
```

## Rule 3 + 7:

> Vì 2 rule này cùng liên quan tới section nên ta gộp vào làm 1 thể luôn.

```
rule rule3 {
    meta:
        description = "Number of sections in a binary"
     condition:
        elf.number_of_sections == 40
}
```
```
rule rule7 {
    condition:
        for any section in elf.sections : (section.name == "poophaha")
}
```

Rule 3 yêu cầu file phải có 40 sections, còn Rule 7 yêu cầu file phải có 1 section tên là `poophaha`. Đầu tiên check section của file ELF ta vừa compile:

`readelf -S yarapass`

![image](https://user-images.githubusercontent.com/113530029/235576040-ee559a74-2c59-41d8-b345-76cddf8c9a90.png)

Tính từ index 0 thì hiện tại file đã có 30 sections, ta sẽ tiến hành thêm 10 sections rỗng nữa, trong đó 1 sections tên là `poophaha`:

> Add 9 sections vào, để chừa 1 sections ra để set tên như rule 7:

`for i in {1..9}; do objcopy --add-section=.new_section$i=/dev/null --set-section-flags=.new_section$i=readonly,noload --change-section-lma=.new_section$i=0 --set-section-alignment=.new_section$i=64 yarapass yarapass; done`

> Thêm section tên "poophaha" vào:

`objcopy --add-section=poophaha=yarapass yarapass yarapass`

Ok, check với `yara`:

![image](https://user-images.githubusercontent.com/113530029/235576980-851c337c-95c0-4c0f-b01e-4377ba0734d8.png)

## Rule 2 + 4 + 6:

```
rule rule2 {
    strings:
        $rocket1 = "jessie"
        $rocket2 = "james"
        $rocket3 = "meowth"

    condition:
        all of ($rocket*)
}
```
```
rule rule4 {
    strings:
        $hex1 = {73 6f 6d 65 74 68 69 6e 67 73 6f 6d 65 74 68 69 6e 67 6d 61 6c 77 61 72 65}
        $hex2 = {5445414d524f434b4554}
        $hex3 = {696d20736f207469726564}
        $hex4 = {736c656570792074696d65}

    condition:
        ($hex1 and $hex2) or ($hex3 and $hex4)
}
```
```
rule rule6 {
    strings:
        $xor = "aqvkpjmdofazwf{lqjm1310<" xor
    condition:
        $xor
}
```
* 3 rule này đều yêu cầu tìm thấy các dãy kí tự nhất định trong file. Ta nhồi nó vào đít file thôi :D

Dùng hxd nhét:

- Để pass rule 2, nhét thêm `jessiejamesmeowth`.
- Để pass rule 4, nhét thêm hex1 + hex2 hoặc hex3 + hex4 vào, ở đây decode hex3+hex4 ra thì text ta cần nhét thêm là `im so tiredsleepy time`.
- Ở rule 6, ta phải brute force ra plain của $xor, bởi rule này yêu cầu sự hiện diện của chuỗi đã xor trong file. Sử dụng cyberchef, tìm ra plain với key(hex) = 03:

![image](https://user-images.githubusercontent.com/113530029/235578065-4cd6c588-6a2c-4958-95ca-2d364bed0a57.png)

Thêm `bruhsinglebytexorin2023?`.

Tổng kết phần này như này:

![image](https://user-images.githubusercontent.com/113530029/235578144-d5440f3c-51d7-441a-982c-05304d91f3ed.png)

## Rule 5 + 8:

```
rule rule5 {
    condition:
        math.entropy(0, filesize) >= 6
}
```
```
rule rule8 {
    condition:
        filesize < 2MB and filesize > 1MB
}
```

Rule 8 yêu cầu file size trong khoảng (1 < file size < 2) MB, còn Rule 5 thì yêu cầu độ ngẫu nhiên các bytes trong file phải đạt 6 đổ lên.

Sau các bước pass rule ở trên, file vẫn khá nhẹ :v (33kb). Nên ta sẽ nhồi thêm bytes vào cho thoả mãn thôi, đương nhiên là nhồi các bytes ngẫu nhiên vào để tăng entropy lên nữa: 

```
import random

with open("yarapass", "rb") as f:
        data = f.read()

for i in data:
        print(i, end = " ")

n = 0
while n < 1500000:
        print(random.randint(0, 255), end = " ")
        n += 1
```

Mở trên Cyberchef với filter sau để check entropy file đó:

![image](https://user-images.githubusercontent.com/113530029/235580830-ce9849b1-3437-4708-9b1f-425be79f911d.png)

Xấp xỉ 8, vậy là ổn rồi. Check xem file pass sạch các rule chưa:

![image](https://user-images.githubusercontent.com/113530029/235580776-6459562e-8ee5-4396-bd42-ac92721154eb.png)

Oke, nhét file lên web rồi đấm thôi:

![image](https://user-images.githubusercontent.com/113530029/235581353-21ddab58-b7ab-4ff8-98a0-a81b52611042.png)

Flag : `UMDCTF{Y0ur3_4_r34l_y4r4_m4573r!}`
