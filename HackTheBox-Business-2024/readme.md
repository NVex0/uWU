# Counter Defensive

Đi thẳng vào câu hỏi luôn nhé:

### 1.  What time did the victim finish downloading the Black-Myth-Wukong64bit.exe file? Please, submit the epoch timestamp. (ie: 168061519)

+ Đề chỉ cấp cho disk folder của `Users`, điều này dẫn đến khá ít thứ để trace. Tuy nhiên dựa vào câu hỏi, ta có thể suy đoán rằng file này được download từ trình duyệt về, mình extract `History` của Brave về:

  Tại table `download_url_chains`, ta có url download của con exe như câu hỏi:

  ![image](https://github.com/NVex0/uWU/assets/113530029/203ffc36-7fd2-4337-ab46-0c83c76d5f25)

  Lấy end time khi tải xong con exe, convert từ webkit time sang epoch:

  ![image](https://github.com/NVex0/uWU/assets/113530029/70426ab4-d3a1-4ca0-9310-c38dcf0fbdcf)

  ![image](https://github.com/NVex0/uWU/assets/113530029/94e9110d-5188-431f-8d2c-5f8bb1bb2296)

> Ans: 1713451126

### 2. What is the full malicious command which is run whenever the user logs in? (ignore explorer.exe, ie: nc.exe 8.8.8.8 4444)

+ Câu hỏi hướng ta đến tìm persistence từ malware, tuy nhiên src malware đã bị xóa sạch :v, không thể đọc src mà tìm được. Ở đây mình chọn cách trace theo list common persistence path trong registry của user này:

```
Software\Microsoft\Windows\CurrentVersion\Runonce
Software\Microsoft\Windows\CurrentVersion\policies\Explorer\Run
Software\Microsoft\Windows\CurrentVersion\Run
SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
```

+ Tại `SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon` ta thấy key `shell` có value tham chiếu đến `explorer.exe`, ngoài ra còn chạy song song command bên cạnh: 

  ![image](https://github.com/NVex0/uWU/assets/113530029/0142385e-e213-4c59-80dd-0ae74be352e3)

  `%PWS%` ở đây là Powershell:

  ![image](https://github.com/NVex0/uWU/assets/113530029/f1382282-284e-44bb-a653-9e195eab8b90)

  chạy kèm tham số `noprofile` và `-windowstyle hidden` nữa thì chắc cú rồi :v. Dựa vào example, ta có answer:

> %PWS% -nop -w h "start "$env:temp\wct98BG.tmp""

### 3. What is the first process that starts when the malicious file is opened? (ie: svhost.exe) 

+ Dựa vào command persistence, mình tìm tới tmp file:

  ![image](https://github.com/NVex0/uWU/assets/113530029/430da6a1-c283-470a-9630-a15491168179)

+ Không phải 1 file powershell, 1 mớ byte khá random. Ngoài ra extension `.tmp` cũng không phải default ext của Windows, mình tiếp tục check cách nó handle đuôi này từ `UsrClass.dat`:

  ![image](https://github.com/NVex0/uWU/assets/113530029/a15a9ba5-42a0-4023-a097-9f8e7ebcc77f)

+ Key này được reg bởi malware, khi gọi đến file tmp sẽ dùng handler là value của key `.tmp`, handler sẽ gọi `mshta.exe` lên để chạy con Js:

  ![image](https://github.com/NVex0/uWU/assets/113530029/0ee6353a-bff0-42bb-a24c-b7051ca944ab)

> Ans: mshta.exe

### 4. What is the value of the variable named **cRkDgAkkUElXsDMMNfwvB3** that you get after decoding the first payload? (ie: randomvalue)

+ Mình dùng `de4js` để clean lại js:

  ![image](https://github.com/NVex0/uWU/assets/113530029/edb620de-4749-464c-ae10-0fc3053971f0)

  Script này lấy value từ key `HKCU\\software\\Classes\\Directory\\DisplayName` ra, đảo chuỗi rồi decode hex:

  ![image](https://github.com/NVex0/uWU/assets/113530029/cc171e02-05b4-4a14-bde4-434523c76f56)

  ![image](https://github.com/NVex0/uWU/assets/113530029/aefec5fa-66e2-4812-a6ac-fbf49c9291bf)

  Tiếp tục clean code bằng `de4js`, từ script này, ta có đáp án:

> CbO8GOb9qJiK3txOD4I31x553g

### 5. What algorithm/encryption scheme is used in the final payload? (ie: RC4)

+ Hầu như các variable được assign value nhìn base64 đều là rác, ở đây mình tập trung vào các hàm tính toán:

  Decode hex cái biến được assign to đùng ở trên đầu:

  ![image](https://github.com/NVex0/uWU/assets/113530029/53b29da5-06c4-4889-807a-f4db5b89192c)

  Read value từ key như trong hình, xor với biến đã decode ở trên:

  ![image](https://github.com/NVex0/uWU/assets/113530029/71440053-c8a4-46d1-aea5-89d9c2694065)

  ![image](https://github.com/NVex0/uWU/assets/113530029/2d47bde9-a8de-4a3a-b347-f3d5896d4044)

  Cuối cùng eval result ở trên. Thực hiện tương tự với cyberchef, ta được script kế như này:

  ![image](https://github.com/NVex0/uWU/assets/113530029/a5686256-87fd-42ca-9fbc-7445988aa9a7)
  
  Decode base64:

  ![image](https://github.com/NVex0/uWU/assets/113530029/58033ced-5fdc-4c0c-9635-e0d8cca41638)

  Sau khi clean, dễ thấy script gọi `AesManaged`. Từ đó ta có đáp án.

> Ans: AES

### 6. What is the full path of the key containing the password to derive the encryption key? (ie: HKEY_LOCAL_MACHINE\SAM\SAM\LastSkuUpgrade)


  
  

  

  




