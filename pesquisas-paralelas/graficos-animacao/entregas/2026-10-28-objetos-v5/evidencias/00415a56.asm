; AffHangar [0x415a56, 0x415acf)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00415a56  c3                     ret
00415a57  90                     nop
00415a58  41                     inc      ecx
00415a59  40                     inc      eax
00415a5a  3f                     aas
00415a5b  3e3d3c3b3a39           cmp      eax, 0x393a3b3c
00415a61  3837                   cmp      byte ptr [edi], dh
00415a63  1b0b                   sbb      ecx, dword ptr [ebx]
00415a65  0a09                   or       cl, byte ptr [ecx]
00415a67  0807                   or       byte ptr [edi], al
00415a69  06                     push     es
00415a6a  0504030201             add      eax, 0x1020304
00415a6f  380b                   cmp      byte ptr [ebx], cl
00415a71  41                     inc      ecx
00415a72  00555f                 add      byte ptr [ebp + 0x5f], dl
00415a75  41                     inc      ecx
00415a76  00e4                   add      ah, ah
00415a78  5f                     pop      edi
00415a79  41                     inc      ecx
00415a7a  007360                 add      byte ptr [ebx + 0x60], dh
00415a7d  41                     inc      ecx
00415a7e  0001                   add      byte ptr [ecx], al
00415a80  61                     popal
00415a81  41                     inc      ecx
00415a82  0010                   add      byte ptr [eax], dl
00415a84  624100                 bound    eax, qword ptr [ecx]
00415a87  a7                     cmpsd    dword ptr [esi], dword ptr es:[edi]
00415a88  634100                 arpl     word ptr [ecx], ax
00415a8b  25644100b1             and      eax, 0xb1004164
00415a90  6441                   inc      ecx
00415a92  004765                 add      byte ptr [edi + 0x65], al
00415a95  41                     inc      ecx
00415a96  006666                 add      byte ptr [esi + 0x66], ah
00415a99  41                     inc      ecx
00415a9a  00f4                   add      ah, dh
00415a9c  6741                   inc      ecx
00415a9e  003a                   add      byte ptr [edx], bh
00415aa0  5b                     pop      ebx
00415aa1  41                     inc      ecx
00415aa2  00dc                   add      ah, bl
00415aa4  5b                     pop      ebx
00415aa5  41                     inc      ecx
00415aa6  00795c                 add      byte ptr [ecx + 0x5c], bh
00415aa9  41                     inc      ecx
00415aaa  00b45c4100df5c         add      byte ptr [esp + ebx*2 + 0x5cdf0041], dh
00415ab1  41                     inc      ecx
00415ab2  000a                   add      byte ptr [edx], cl
00415ab4  5d                     pop      ebp
00415ab5  41                     inc      ecx
00415ab6  00405d                 add      byte ptr [eax + 0x5d], al
00415ab9  41                     inc      ecx
00415aba  00c5                   add      ch, al
00415abc  5d                     pop      ebp
00415abd  41                     inc      ecx
00415abe  00765e                 add      byte ptr [esi + 0x5e], dh
00415ac1  41                     inc      ecx
00415ac2  00b05e4100e6           add      byte ptr [eax - 0x19ffbea2], dh
00415ac8  5e                     pop      esi
00415ac9  41                     inc      ecx
00415aca  001c5f                 add      byte ptr [edi + ebx*2], bl
00415acd  41                     inc      ecx
