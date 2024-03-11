Trace log và trả lời câu hỏi sau khi connect tới instance.

1. What is the IP Address and Port of the SSH Server (IP:PORT)

Dễ thấy nó listen ở port 2221 và khi có connect tới, ta có IP:

![image](https://github.com/NVex0/uWU/assets/113530029/f404b5e9-610b-4d79-867f-a505953d8be7)

> Ans: `100.107.36.130:2221`

2. What time is the first successful Login

![image](https://github.com/NVex0/uWU/assets/113530029/9cabd41c-a7b2-441d-a291-921decffcd20)

> Ans: `2024-02-13 11:29:50`

3. What is the time of the unusual Login

Tại file bash, ta thấy root có add user mới tên softdev và config hệ thống các thứ. Trace lại ở ssh log, có 2 lần login vào root, đặc biệt là lần thứ 2 match với command `whoami` trong bash (sussy :D).

Từ đó ta có time của unusual login:

> Ans: `2024-02-19 04:00:14`

4. What is the Fingerprint of the attacker's public key

Ngay bên cạnh time đó trong log luôn.

> Ans: `OPkBSs6okUKraq8pYo4XwwBg55QSo210F09FCe1-yj4`

5. What is the first command the attacker executed after logging in

Trace theo thời gian như trên ta đã nói thôi, là `whoami`

> Ans: `whoami`

6. What is the final command the attacker executed before logging out

Attacker thoát ssh lúc `2024-02-19 04:38:17`, ta có command cuối cùng gần nhất với time này là:

> Ans: `./setup`

Flag: `HTB{B3sT_0f_luck_1n_th3_Fr4y!!}`
