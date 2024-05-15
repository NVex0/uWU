## Official wu for `Jumper In Disguise`

Đề là 1 file docm (macro enabled). Ta sẽ check macro bằng `olevba`:

![image](https://github.com/NVex0/uWU/assets/113530029/3eedb32e-3559-4c79-9e80-1cae2beef013)

Khá nhiêu khê, đại khái là malicious macro. Ta đá qua code trước, tóm tắt lại là nó regex theo pattern để lấy đoạn binary ra, sau đó xor đoạn binary với 1 key để tạo thành 1 con exe. Cuối cùng chạy con exe với param là 1 string được xor với key tiếp.

Ở đây khi xor với key `4444` hoặc dùng 1 cách khác như chạy thẳng thì không ra được exe. Vì sao nhỉ?

Như ở trên ta thấy, nó bị nghi dùng VBA Stomping (pcode và vba source không khớp nhau).

Dùng `pcodedmp` để check pcode, dễ thấy biến bbb (hay xor key) đã modified và khác với vba source:

![image](https://github.com/NVex0/uWU/assets/113530029/17553ee8-12fe-4173-ba5d-17254385802f)

![image](https://github.com/NVex0/uWU/assets/113530029/921e78f9-f4a3-4b50-add5-2618b164132b)

Từ đó, mình dùng quick script sau lấy con exe:

```
import re

pattern = b"SUPERNOVAOVERLOAD"
bina = open("ThongBao.docm", "rb").read()

idx = re.search(pattern, bina)
idx = idx.start()
st = idx + len(pattern)
data = bina[st:st+4296811]
with open("Acheron.exe", "wb") as f:
    for i in range(len(data)):
        f.write(int.to_bytes(data[i] ^ b"1337"[i % 4]))
```

> Note: Việc chạy thẳng ra hay không tùy thuộc version office để VBA stomping có thể trigger effect được. Nếu đúng version office, nó sẽ check pcode và vba source, nếu 2 cái này không match thì nó sẽ load lại pcode lên để overwrite vba source, từ đó chạy ra `Acheron.exe` đẹp (vì xor với đúng key mà mình intended, hay đúng hơn là malware chạy bình thường :v), còn không thì sẽ ra binary xor với key sai, buộc bạn phải phân tích tĩnh như trên.

Tiếp với DIE, ta thấy nó compiled bằng pyinstaller. Từ đây có thể decompile về python source:

```
"""nR9aRuepXAGTojNrgfy3ai8iY5vq86RrJVwkOPRl5ne9vqd2b38dWd650pxpK/OMwkl1qcOeY/Bf+GYqKR7UG/0stVv2AfMjCYyb9CGSnZHqeaXLEd/2rhrni1+oyqqKuuQbawVTNY7ZcFJqejDjyw+1i2TSCgTuj1N7RZb9paxVlWZ/xLxz8pxrfhdtStZPVflTB24X1yQ/mZNfYWepk2zblSmsnq6sPRGr+50EeB0E+1j1igDuVTv0Ym1cS45QNMymjP0hFY5DjvR0W0EraJdEoXR6dQvgBPKSwdJ0JI87iPkesR3M7I77mtKtmNv5ydm3eo5TYzmbnXL42rZnLrhmgmNFzXa3gDYxnYBtmzgLTB3PQ3qVnSPVI2mr1GD7hCLQDeHm1HFEwx3dPvBwKhLSWqQw7Crw37OTaJCYOCLDlPzE1GZc2sOITPq2xckalHsjzXJMZ83u4FPSW31LS4hvdLb1LNl6vOgEMkUgaGqtfVO7AHPMwHFY7wO+1ggzJubH1MlX3UAtqS8DtskzeeSrHaS1GNyr5Pp6cVbUJLqSREHrmqJ/pi/3637Fyjsj374laynjrsJA8txeUD5GoNVIgB82rftGPNE6JR46JnBx0o8koHkXuKySWrPGkPV/IS2tZIb0O9qinGRQWI/hxm5q1qPVloqtVn644DVaeM9K4NGCU6VS2YDhEMlADOht5T3U2KbfoQD9HPta5W82HfaKv2/yJs+UfVd9xKfTQ/k4q3ob9nVupqiwTNgPWgaHPS36LZtGL3lEQTLaNRX3BQVDGuFY4s3RZQk/Oq9MkD5ZUVQlEJCQDezT40pbvWJRn+2OaKZizb3fbnKM0ggUbDKEU1gsI2OPrdqq3W/8Zel5NwC/7fdhiL+2zuO58JamssKdTc7e8CcwKhVRBFGs6Q0uYCx+VKXgnO7dn+ojW6RiQGeDb6w4IufhEvJxH56fgWcO52ZnvhOYymHKtztJSWLDn5H6hyEvCS48UPFW3SrCqxOXVadzcl4OOJkOoRBQ09PRfJd1mN92rF0kH23AyRvJWjQXXJ78uxeNoaRDmK6zDPS1R0LR40J0dPwJGnZYEeWyPw=="""
import sys
from base64 import b64decode as d
S = [i for i in range(256)]
j = 0
out = []
for i in range(256):
    j = (j + S[i] + ord(sys.argv[1][i % len(sys.argv[1])])) % 256
    S[i] , S[j] = S[j] , S[i]
i = j = 0
for char in d(globals()['__doc__']):
    i = ( i + 1 ) % 256
    j = ( j + S[i] ) % 256
    S[i] , S[j] = S[j] , S[i]
    out.append(char ^ S[(S[i] + S[j]) % 256])
exec("".join([chr(out[i] ^ open(sys.argv[0], "rb").read(4)[i % 4]) for i in range(len(out))]))
```

Code này thực hiện RC4 với param truyền vào từ vba như mình đã nói trước, sau đó xor với 4 byte đầu của `sys.argv[0]` (ở đây là 4 byte của exe).

Ta retrieve lại param:

![image](https://github.com/NVex0/uWU/assets/113530029/95c6b089-7496-4ad6-a3e2-c8c687b32b4d)

Decrypt dựa theo xor key và param đã có:

![image](https://github.com/NVex0/uWU/assets/113530029/ed816d31-f64d-4b8c-8c50-c35054678e8b)

Flag: `KCSC{I_@m_daStomp_dat_1z_4Ppr0/\ch1n9!}`
