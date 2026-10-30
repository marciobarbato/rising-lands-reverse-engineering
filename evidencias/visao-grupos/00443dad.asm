; EnginEstVivant; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00443dad  52                       push edx
00443dae  31d2                     xor edx, edx
00443db0  6689c2                   mov dx, ax
00443db3  89d0                     mov eax, edx
00443db5  c1e004                   shl eax, 4
00443db8  01d0                     add eax, edx
00443dba  c1e002                   shl eax, 2
00443dbd  01d0                     add eax, edx
00443dbf  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00443dc5  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00443dc9  25ff000000               and eax, 0xff
00443dce  7409                     je 0x443dd9
00443dd0  83f804                   cmp eax, 4
00443dd3  7404                     je 0x443dd9
00443dd5  b001                     mov al, 1
00443dd7  5a                       pop edx
00443dd8  c3                       ret
00443dd9  30c0                     xor al, al
00443ddb  5a                       pop edx
00443ddc  c3                       ret
00443ddd  8d4000                   lea eax, [eax]
00443de0  8b4344                   mov eax, dword ptr [ebx + 0x44]
00443de3  008b4344008b             add byte ptr [ebx - 0x74ffbbbd], cl
00443de9  43                       inc ebx
00443dea  44                       inc esp
00443deb  008b4344008b             add byte ptr [ebx - 0x74ffbbbd], cl
00443df1  43                       inc ebx
00443df2  44                       inc esp
00443df3  008b4344008b             add byte ptr [ebx - 0x74ffbbbd], cl
00443df9  43                       inc ebx
00443dfa  44                       inc esp
; 1 trailing bytes are not code (alignment/data): 00
