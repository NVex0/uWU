![image](https://github.com/NVex0/uWU/assets/113530029/7e3bd8ba-44ce-47d2-900c-718c0fa2e975)

Đề cho ta access log của web server. Mục đích là đi tìm incident.

Mình đoán là lại nhồi payload trong link, nên grep thẳng luôn tìm link chứa các ký tự urlencode bằng command `cat access.log | grep -E "%*%"`:

![image](https://github.com/NVex0/uWU/assets/113530029/56c2da2c-627f-4498-8af3-33e6f078ed81)

Có vẻ ta đã đúng :v, trong các payload, mình để ý dòng bôi đen lên như kia (vì có sử dụng `echo`, biết đâu là cat flag). Decode ra:

![image](https://github.com/NVex0/uWU/assets/113530029/c4eabfd9-e3c0-4424-bda8-c0050cd1d092)

Nó thực hiện decode bas64 các phần data kia ghép lại, sau đó reverse rồi ghi vào cron làm persistence.

Lại lấy data ra coding thôi:

```
data = """Nz=Eg1n;az=5bDRuQ;Mz=fXIzTm;Kz=F9nMEx;Oz=7QlRI;Tz=4xZ0Vi;Vz=XzRfdDV;echo $Mz$Tz$Vz$az$Kz$Oz"""
data = data.replace("=","='").replace(";", "'\n").replace("echo $", "print(").replace("$", "+") + ")"
exec(data)
```

![Screenshot (335)](https://github.com/NVex0/uWU/assets/113530029/020117f0-b2d7-4b13-8d7c-c41ed9c85a19)

Flag: `HTB{L0g_@n4ly5t_4_bEg1nN3r}`
