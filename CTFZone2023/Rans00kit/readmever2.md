Took me very long time to solve :(

![Screenshot (4777)](https://github.com/NVex0/uWU/assets/113530029/a14426a6-2a60-4dea-9539-83ee29c11afb)

Straightly focus on our main works: Bypass the rootkit, write a decryptor and find the flag. 

Since the description said the attacker using `ring-zero rootkit`

> Rootkit - ring0 (Kernel Mode):
> + the “real” rootkits start from this layer. They live in a kernel space, altering behavior of kernel-mode functions.
> + Can run with highest OS privileges.
> + Usually cloaked and hard to detect.

With running [Autoruns](https://download.sysinternals.com/files/Autoruns.zip), i found there are 2 files that look sussy:

`C:\Program Files\VMware\VMware ToolsVMware VGAuth\agony.sys`

`C:\Program Files\VMware\VMware ToolsVMware VGAuth\aliasStore\Update\UpdateService.exe`

Now checking with [Detect It Easy](https://github.com/horsicq/Detect-It-Easy).

`agony.sys` gaves no information than a PE32 file. But `UpdateService.exe` is a bit different:

![Screenshot (4804)](https://github.com/NVex0/uWU/assets/113530029/347cae11-4f5b-43e4-ab94-a8913f220049)

A `packed executable`. Following my Aidoru's guide (Translate it yourself XD):

![Screenshot (4805)](https://github.com/NVex0/uWU/assets/113530029/4bf47c7c-1cc3-4456-b9e7-bcf4b360fbc3)

We know that `UpdateService.exe` is a bat originated.

Now unpack with [UPX](https://upx.github.io/), we will get the original bat from it:

> 2 Lazy to install, image supported by BuiHuyThang

![image](https://github.com/NVex0/uWU/assets/113530029/1b51207e-9bee-4e2a-8e3a-749343ed5233)

Yeahh, as you can see, it calls `VGAuthCGI.exe` with some parameters look like options, i wonder if it was a tool or something like this.

There're 2 ways here to know:

+ First is, the `VGAuthCGI.exe` has been called and executes the `agony.sys`, no directory specified in `agony.sys`. Gotcha, they are at the same directory. Open `cmd` in that path, execute `VGAuthCGI.exe` (still appears when you enter its name and tab for choosing file), you will see it displays help table, and when you execute with `-h` option, you will know what the batch did.

+ Second and the last way, reverse it. I dont think that a good point in a forensics challenge. But why not, trying loses nothing. As i told above, since they're at the same dir, go find and extract it. But i see no file like that in `VMware ToolsVMware VGAuth` dir. Yep, cuz rootkit hid it right? The only way to take it is to using `7z` on the OVA file, and now we can see and extract it. Open in `IDA`, provides us a lot of things:

![image](https://github.com/NVex0/uWU/assets/113530029/9deb46d3-6bb3-43ac-93e6-d5735c111fd4)

I dont have a good reversing knowledge, but still can figure out it uses `strcmp` compare with `argv[1]` to display several things like we expected: a tool with options.

Now, we know what `VGAuthCGI.exe` does. Provide an option with a file will do "something". "something"?, type `-h` XD. jk

We know all the dirs and files related to `VGAuthCGI.exe` now, go find and analyze them.

![image](https://github.com/NVex0/uWU/assets/113530029/9bd1efd2-95c4-4870-acb6-0dde20c8954e)

`7z` with OVA again, get in the path and, what we got?:

- `sys`, `binary` are directory. Nothing special.

- `Wow6432Node` is a registry key. It's not important now, but not later :>

- `.config` looks like a pack of random bytes, i have no ideas with it.

- And the last one, `aliasStore`. Yep, it's a `.NET` file. Decompile it with `DnSpy`:

K, `Disk_Encoder`, nice one. Seem we get the right ransomware file.

I can summarize whats the main things it does:

+ Genarates a 2048 bytes key from ASCII set.
+ Displays a window to notice the user that all the files is encrypted. Require the user to pay money for recovery key.
+ Encrypt file recursively in its current directory. Then modified encrypted file name by appending "config".

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

Next is the salt, it's array in `__CIPHER` function. With Cyberchef, i convert the array to hex. But first, you need to swap the `Byte.MaxValue` with `255`:

![Screenshot (4783)](https://github.com/NVex0/uWU/assets/113530029/85597876-8ab8-442a-b2cb-e0441e838bd7)

(That's the notification i said before in summary part)

Convert to hex:

![Screenshot (4784)](https://github.com/NVex0/uWU/assets/113530029/1bb5ead1-1c8e-43a7-ad7a-2f63d0027e84)

Now, deriving `PBKDF2 key` - which do the samething as `rfc2898derivebytes` function with key, salt we just got:

> `rfc2898derivebytes` is a streaming-response object. So when you take first 32 bytes as the key, the following 16 bytes gonna be the iv. By this reason, i will take 48 bytes from Derive Key, which means the length (or key size) is 384.

![Screenshot (4785)](https://github.com/NVex0/uWU/assets/113530029/d44ba0bc-002c-4315-912c-d0e163494d4f)

Concatnate the result as i described above, we will get the AES key and iv.

We have only 1 file has "config" extension. 

![image](https://github.com/NVex0/uWU/assets/113530029/3b3764b4-6473-4ecf-be63-1ddae2911da2)

Use as ciphertext and decrypt it, i got a file with MZ header:

![Screenshot (4788)](https://github.com/NVex0/uWU/assets/113530029/36b72fbb-4165-4548-9df8-f942fbec65f4)

Find the flag format in that file, we will get the flag:

![Screenshot (4789)](https://github.com/NVex0/uWU/assets/113530029/bf271dd1-d475-4897-b3d1-78b3358fbd37)

Flag: `ctfzone{!R1nG0_r00Tk1T_Ea$Y_byPa$$!}`
