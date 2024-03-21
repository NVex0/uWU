Đoạn sau của bài mình solve khá randomly, nên wu này mình có điều chỉnh sau khi đọc official wu của giải 🐸

Đề cho ta 1 file Hiberfil.sys - file lưu thông tin tất tần tật các thứ trên máy ở trạng thái hiện tại khi nó bắt đầu vào mode ngủ đông 💤

Và vì thế nó cũng na ná memdump thôi <("), mình convert qua dạng raw mem trước. Mình sử dụng bản volatility 3 branch build này để lấy thêm 2 plugin hibernation:

https://github.com/forensicxlab/volatility3

Convert:

![image](https://github.com/NVex0/uWU/assets/113530029/48ecd17a-55d3-4243-a72a-92b93ddafad5)

Sau đó load vào xem pslist, dễ thấy 1 sus proc tên `TheGame.exe`, cũng phù hợp với mô tả của bài :)) :

![image](https://github.com/NVex0/uWU/assets/113530029/9a59a13a-058a-4456-a353-c1bc470b66c5)

Sau khi filescan string grep, ngoài ra cũng có thể dùng dlllist lên proc này, ta thấy rất nhiều dll cùng nằm trong folder chứa exe. Ngoài ra trong đó còn có coreclr.dll, mà dựa theo docs trong repo đã archived của Microsoft, define như này:

`CoreCLR is the runtime for .NET Core. It includes the garbage collector, JIT compiler, primitive data types and low-level classes.`

Vì thế nên đây là 1 .NET project, vì nó chứa core runtime, JIT compiler,..tự làm tự ăn. Ngoài ra, Coreclr như ta biết ở trên, là "runtime for .NET Core". .NET Core là cross-platform của .NET: https://learn.microsoft.com/en-us/archive/msdn-magazine/2016/april/net-core-net-goes-cross-platform-with-net-core. Thì theo đó, thông thường con exe sẽ là executable của project luôn, tuy nhiên trong cross-platform, nó chỉ là loader cho con dll. Hoặc ta dump cả 2 con ra rồi check file type cũng được :v :

![image](https://github.com/NVex0/uWU/assets/113530029/6592b8d9-2421-4bf5-9292-472f97696771)

Phân tích .NET bằng DNSpy, tuy nhiên hàm main lại không decompile ra gì được, lỗi. Khi đổi sang Intermediate language, ta thấy 1 mớ dài nop opcode:

![image](https://github.com/NVex0/uWU/assets/113530029/440ebb1d-2397-46c8-a34c-89ec09014ad2)

Ngoài ra dựa vào hint từ đề bài và từ 1 người bạn, ngoài ra check structure của TheGame.dll, ta cũng có thể thấy ReadyToRun header, mình biết được đây là R2R stomping, nó giấu code bằng cách thay các opcode về nop trước các trình decompile như dnspy, ilspy. Thế thì mình đã làm như thế nào? Mình load PE vào IDA và F5 :v 
Nó thực hiện xor 2 array, mà khi ta xor xong, sẽ được 1 command có kèm flag.

