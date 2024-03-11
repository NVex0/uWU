Đề cho 1 file mft. Sử dụng tool `MFTecmd` để parse thành csv:

![image](https://github.com/NVex0/uWU/assets/113530029/a068783c-9738-43a9-abd9-a8d42179426e)

1. Files are related to two years, which are those? (for example: 1993,1995)

Dễ thấy 2 năm đó luôn:

![image](https://github.com/NVex0/uWU/assets/113530029/e8e6303d-b98b-44ee-ab0d-e24a6f38aeb1)

> Ans: 2023,2024

2. There are some documents, which is the name of the first file written? (for example: randomname.pdf)

> Ans: Final_Annual_Report.xlsx

3. Which file was deleted? (for example: randomname.pdf)

Ta thấy Marketing_Plan.xlsx có trường `Inuse` là False, tức là đã bị xóa:

![image](https://github.com/NVex0/uWU/assets/113530029/77aae891-ca1e-476b-8feb-3eac0707e6dd)

> Ans: Marketing_Plan.xlsx

4. How many of them have been set in Hidden mode? (for example: 43)

Trừ các file hệ thống ra, thì có duy nhất file `credentials.txt` ở Hidden mode.

> Ans: 1

5. Which is the filename of the important TXT file that was created? (for example: randomname.txt)

> Ans: credentials.txt

6. A file was also copied, which is the new filename? (for example: randomname.pdf)

Check trường IsCopied xem cái nào True, ta được đáp án:

> Ans: Financial_Statement_draft.xlsx

7. Which file was modified after creation? (for example: randomname.pdf)

Ta check time Created với LastRecordChange, chỉ có 1 file là có thời gian LastRecordChange mới hơn.

> Ans: Project_Proposal.pdf

8. What is the name of the file located at record number 45? (for example: randomname.pdf)

> Ans: Annual_Report.xlsx

9. What is the size of the file located at record number 40? (for example: 1337)

> Ans: 57344

Flag: `HTB{p4rs1ng_mft_1s_v3ry_1mp0rt4nt_s0m3t1m3s}`
