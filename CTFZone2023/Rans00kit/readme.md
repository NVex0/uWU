Took me very long time to solve :(

![Screenshot (4777)](https://github.com/NVex0/uWU/assets/113530029/a14426a6-2a60-4dea-9539-83ee29c11afb)

Straightly focus on our main works: Bypass the rootkit, write a decryptor and find the flag. 

Since the description said the attacker using `ring-zero rootkit`

> Rootkit - ring0 (Kernel Mode):
> + the “real” rootkits start from this layer. They live in a kernel space, altering behavior of kernel-mode functions.
> + Can run with highest OS privileges.
> + Usually cloaked and hard to detect.

it's very hard to detect which one is malicious. I used [Kaspersky Virus Removal Tool](https://www.kaspersky.com/downloads/free-virus-removal-tool) for scanning virus over the PC. Then i got 2 results:

+ C:\Program Files\VMware\VMware ToolsVMware VGAuth\agony.sys
+ C:\Program Files\VMware\VMware ToolsVMware VGAuth\VGAuthCGI.exe

Went to above path on the PC, i can't see that two suspicious files despite enabling show all the files (include system files, hidden files). 

So i try finding it dynamically. I opened the OVA files with `7z`. Following the path, and finally found them:

![Screenshot (4779)](https://github.com/NVex0/uWU/assets/113530029/76f485f1-4f17-42d0-9e06-7f7deffcbb7c)

Extracted it, using `Virus Total` to know what it is:

![Screenshot (4767)](https://github.com/NVex0/uWU/assets/113530029/fd0dcec8-8f04-4104-884b-90a14832a067)

![Screenshot (4780)](https://github.com/NVex0/uWU/assets/113530029/6242abf7-290e-4a28-b819-1d0407a1c9eb)

See the label? That's the rootkit we looking for. 

But 2 files i got is PE32 Rootkit file, i have no ideas what to do with it. Since the rootkit hides files and processes, when opened OVA with `7z`, i see hidden folder `sys`. The second .config file contains nothing, so i start with the first one. Extract it:

![Screenshot (4791)](https://github.com/NVex0/uWU/assets/113530029/7027360f-0eb4-42a3-801b-de0884d01547)


Now checking what file with [Detect It Easy](https://github.com/horsicq/Detect-It-Easy) or simply `file` in Linux. Yep, it's a `.NET` file, easier for me. Decompiled with `DnSpy`:

K, `Disk_Encoder`, nice one. Seem we get the right ransomware file.

I can summarize whats the main things it does:

+ Genarates a 2048 bytes key from ASCII set.
+ Displays a window to notice the user that all the files is encrypted. Require the user to pay money for recovery key.
+ Encrypt file recursively in it's current directory. Then modified encrypted file name by appending "config".

#### Now is the decryption time. 

Take a look at `__CIPHER` function:

![Screenshot (4781)](https://github.com/NVex0/uWU/assets/113530029/3fd9c9a7-0536-4938-b329-e21907703753)

The encrypting work uses `AES`(rijndael) - `CBC` (rijndaelManaged.Mode = 1) - `256` (Keysize) with key and iv are concatnated from `rfc2898derivebytes`.

`rfc2898derivebytes` takes three parameters: key, salt, iteration.

Key is sha256sum of the value that generated randomly from `__KEYGEN` function:

![Screenshot (4782)](https://github.com/NVex0/uWU/assets/113530029/9422d99b-1138-4fc5-95dd-2582013049fa)

But in the `__Main` function, this value was written to registry path: `Software\Wow6432Node\Microsoft\Active Setup\Status` named `INFO`.

Open `regedit`, following the path and we got the value:

`HF48K!SP%hHudfQrk?*wvYvn*F-$DrooyKUdie0ZcY82OR%bW6$Mbk15hR?E@bLZ/q(TL!IGTmTXm/ZtKtqU0bNNfl(RgwjAMj9uWyQjy7)*QeTo/b)T8+wnc4*x+$wuCTKDF1XjcHs/iY&ASeYF2PPV9WSo9qr7KV9?UPjOEg+0V3ED7!fkpr+!E@Q6i5w8m84Nm=3C(KBVYl=GRO3=LHSqd-)e-z2V7FNj-+o8Hcpfqtlp$KpUCxxfqO6nFYDSe3lTXmHZx%/6p9A7kbo!KiSJe5)6HA25YWA!HSRaCPtH5+@3O=D16PH(kb*ptXSxPJhS8NzSJN8(@Lbn)MsI?B-IOFZ2dz41&&/vgt%AW7rseMGZAXvg2K0NKZD3!&*hgG-/S2HWRs8Mgd0C-A2FDY=9T1lHpONZ&KMYONGUQYPKYn34vB4!R6dHHLwoR=3DeiQWQc*7)i*1J@l2?3jogZIN3EQCopCRsM2$XhoSN&)5%y-Rx%qlnPtFZCpLL8TbguJ?KvenPQbjgZSFF=cu=n1cpxnU+cGb0oZXoBHBmCWW*Kv=7kFMgwc/)4ekIJw9K=6+A(nE/aH&ReofBnkdX%(DMhd7uu)dcjM*a3=*?BUFpfxlQ=isvSmQE22po2hVg1q5SzEUnvgVw$l37/ruLY4K?&7vBhXRr=v**+Tn%OEA9QqOR-4wL9JI&g8V+gSFYP1xRx//vDz?T3Y3dtdDzxF5@n+fG?wl(-ztl/&rG@AIJM*PIE/UCPdxJ&715k9xeOCVE1Rkx9?!x?v0zyWCEbj2sBkpHS8tCZ0(JqKe9fuPSq=MXHCGN7tD2W0CQzceBb7XU0qJn/Pw3TjBBYRAQ1fS3xQ!@INKCPO+5z/un)qVs&Wi!yA/hcOW(pqtk3Tf1FtnFsSZgujXLKx7a4AOHVzxB+&QJVJ7wKqmZ6dSfyj!/+L8+6T23EYgc&mNvCQLkzxArKhqb46g8@4J2LZZBdDs9JKdUPtdiYZQRKR4Z0b-V/unOchk0$JGvEOh=DWLLc?kmn/s%rAYCFW%luO/4I0rOSsM&64VdP9/%KAyj@qI$8Ep4T(c*deDzdWT(2vK!2%9SdAbtnf/or1dODez!bgA86Qn!324QgUK$SWbTr5Y-mlHy)F/X&WiV%AjNjo$7yyIWqm(3DfTsICWUI*%x!gUJ9@&R!N7C/nW!d8IeKLUnC@N+1PFuuP&Se-k1p1)$vQ0s2i$X3mnzL3H&yEmuHMfzqEgeXd@gSd/8MsMTY5+HzUGx+oCkOV6i8BByBj=ZxGg5*V7G/TWYVY=V?5n5bcS?ugALqlR@5ogs*Y9t4(r%-hNjB30S&R-V*iKfUvneChp3+ehw&)Bf7X-NSnK98-)oqL3cNeYIfN/o+hstWDWCPqlok?M3l0tDoBN3xEips/=tfhV8(nn4z$Y=xP/QRrt1r*=$T*&Rr4gXq+ICza7-N*bxzNFhMSXBWVBqhfoGrVM(hBg5H@o+6un3kZOG6lEYhfAU@psT91e+ygPx3WaX1gRy4VFHQiXFR*kBAL/oTUEFQwEEJnZjL4tANZnrjkCbdZx!(Nwse8DhbMiIRA-0I*%jRj*yvYF6R0y+-QJ($4FZ0LwB+fZimZSpeNtiZ-&F3UQxkrJA+C9a5r5F!97Q-tT+hJj8uys/7=tg(=oXVZrkm/6!eounO3GKAZPaHYdPg%p5?ZK!Vk%wB6bpZvdFDF1D)jft7NP?(cEsZA@Fe7R19hIR?xBj%XMaQl@l)oDHU&0w26PY5XyT!=RjaNvKM2DuQ0c!LbL@3Jg$3jmOhz0tv)mQUdL3/)(p)GgBdbNeM8m0qa2$yhzkCg-WNMq4Pf?!O+?xDk7FlVh!d8w)xUEiQimjHJ!R8fO3*zmzdF!Nxu-3-L)bmwH(amt2bkq%wpTGG0-1W?nsh+7tk5k(Pj2MYTcYF6X)m/nHa/xUNOFoImlj1ASs=u1N9G5!XwwmxuFob0SsIP4BdOD94)uFo1)+NZUTJ!?npq+lg&IB4xk6$07vD(FeCr-(1NaBf-iVSRi!Wpc78tX+RJBkpwQ`

Sha256 it, we get the key. 

Next is the salt, it's array in `__CIPHER` function. With Cyberchef, i convert it to hex. But first, you need to swap the `Byte.MaxValue` to `255`:

![Screenshot (4783)](https://github.com/NVex0/uWU/assets/113530029/85597876-8ab8-442a-b2cb-e0441e838bd7)

(That's the notification i said before in summary part)

Convert to hex:

![Screenshot (4784)](https://github.com/NVex0/uWU/assets/113530029/1bb5ead1-1c8e-43a7-ad7a-2f63d0027e84)

Now, deriving `PBKDF2 key` with key, salt we just got - which do the samething as `rfc2898derivebytes` function:

> `rfc2898derivebytes` is a streaming-response object. So when you take first 32 bytes as the key, the following 16 bytes gonna be the iv. By this reason, i will take 48 bytes from Derive Key, which means the length is 384.

![Screenshot (4785)](https://github.com/NVex0/uWU/assets/113530029/d44ba0bc-002c-4315-912c-d0e163494d4f)

Concatnate the result as i describe above, we will get the AES key and iv.

We got only 1 file has "config" extension. 

![image](https://github.com/NVex0/uWU/assets/113530029/3b3764b4-6473-4ecf-be63-1ddae2911da2)

Use as ciphertext and decrypt it, i got a file with MZ header:

![Screenshot (4788)](https://github.com/NVex0/uWU/assets/113530029/36b72fbb-4165-4548-9df8-f942fbec65f4)

Find the flag format in that file, we got the flag:

![Screenshot (4789)](https://github.com/NVex0/uWU/assets/113530029/bf271dd1-d475-4897-b3d1-78b3358fbd37)

Flag: `ctfzone{!R1nG0_r00Tk1T_Ea$Y_byPa$$!}`
