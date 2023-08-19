1 misc duy nhat.

Đầu tiên, đề cho 1 file text toàn hex.
Decode nó ra.

![Screenshot (4859)](https://github.com/NVex0/uWU/assets/113530029/1e828dbd-4429-47e2-99e1-7896f4c017f7)

Để ý dòng được bôi xanh nhé, ngoài ra magic number của nó rất giống với magic number của 1 file gif, ta sửa magic number của nó:

`87 89 46 38 89 61` > `47 49 46 38 39 61`.

Ta nhận được file gif chuẩn. Mở lên xem thử giống như từng phần của 1 cái QR, extract từng frame của gif ra với `ffmpeg`:

`ffmpeg -i file.gif frame_%d.png`

lúc này ta sẽ nhận được 9 cái png, tương ứng 9 frame của gif, sau 1 hồi ngồi nghịch linh tinh thì mình để ý nó ghép vào nhau theo thứ tự 0 -> 9 sẽ ra 1 cái QR chuẩn, vì thế mình viết script sau để merge lại thành 1 con QR:

```
from PIL import Image
new = Image.new("RGB", (1200, 1200))
pix = new.load()
startx = 0
starty = 0
orgx = 0
orgy = 0
for i in range(1, 10):
    img = Image.open("frame_{0}.png".format(str(i)))
    for x in range(startx, startx + 400):
        for y in range(starty, starty + 400):
            r, g, b, a = img.getpixel((orgx, orgy))
            if r > 128 and g > 128 and b > 128:
                pix[x, y] = 0, 0, 0
            else:
                pix[x, y] = 255, 255, 255
            orgy += 1
        orgy = 0
        orgx += 1

    startx += 400
    orgx = 0
    orgy = 0
    if startx >= 1200:
        startx = 0
        starty += 400

new.save("QR.png")
```

Kết quả của cái ảnh merge rồi như này:

![whatisit](https://github.com/NVex0/uWU/assets/113530029/36ff9ec4-a902-474b-88e8-b6500e9088f7)

Quét ra và ta được text sau:
> Nếu cảm thấy mệt quá, em cho mượn: https://drive.google.com/file/d/1xebJa87ARLdgYgYmR-5aLB1lu5ckZxRH, thì thầm em nói nhỏ: "https://www.youtube.com/watch?v=9ar6S2wHZA8 never die"

Cái link youtube dẫn tới 1 vid bị xoá, sau khi solve mình cũng không dùng tới cái link đó nên mình cũng không quan tâm :v
---

Drive cho ta 1 file wave của bài Hurricaneger Sanjou, nostalgic XD. Nghe tới đoạn giữa thì mình thấy rè rè nên mình ném vào Sonic Visualizer để xem Spectrogram. Mình thấy được:

+ 1 link pastebin
+ 1 cái QR bị ọp ẹp phần dưới :D

#### Link pastebin:

  ![image](https://github.com/NVex0/uWU/assets/113530029/464a8100-69b9-46d8-b660-d264c415a2b7)

Link paste bị thọt mất 1 kí tự đầu. Mình dùng script sau để bruteforce kí tự đó:

```
import requests
guess = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for char in guess:
    response = requests.get('https://pastebin.com/'+char+'Wwx9n8N')
    print(char, ": ", response.status_code)
```

Tìm char có code 200 rồi lấy thôi :v, ta được link chuẩn: `https://pastebin.com/mWwx9n8N`

Link này dẫn tới 1 text bị encode:

![Screenshot (4861)](https://github.com/NVex0/uWU/assets/113530029/d193f3ce-0b17-407d-89fa-e6f3037aad99)

Mình ném text lên: https://www.dcode.fr/cipher-identifier, nhận diện được là base32 và decode, mình có được flag với 1 phần bị khuyết, lấp bằng format như sau:

`BKSEC{1_l0v3_xxxxxx-xxx-xxxxx}`

#### QR:

![image](https://github.com/NVex0/uWU/assets/113530029/19e04ca5-b82a-4aee-89af-4377ae0688e6)


Tới đây, mình đoán chắc chắn QR sẽ là text để lấp vào format kia, tuy nhiên cái QR này bị khuyết tật :D, mình cũng không có cách nào để máy scan được. Nên mình quyết định zoom spectrogram lên, dùng sức người để mô phỏng lại cái QR này với [QRazyBox](https://merri.cx/qrazybox/)


Khá là chật vật, mình khôi phục tương đối và nhận được text như sau từ QR:

![Screenshot (4862)](https://github.com/NVex0/uWU/assets/113530029/9af07e83-36e4-470f-a716-e3c428761a79)

Dựa vào format trên kia cùng với việc đoán từ gì có ngữ nghĩa 1 tí, mình sửa lại cho khớp như sau: `h1dd3n-w4v-4ud1o`

Và ta có được flag : `BKSEC{1_l0v3_h1dd3n-w4v-4ud1o}`
