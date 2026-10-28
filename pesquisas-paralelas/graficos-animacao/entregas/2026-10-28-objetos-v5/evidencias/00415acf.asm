; AffVeget [0x415acf, 0x416864)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00415acf  51                     push     ecx
00415ad0  56                     push     esi
00415ad1  57                     push     edi
00415ad2  55                     push     ebp
00415ad3  83ec0c                 sub      esp, 0xc
00415ad6  50                     push     eax
00415ad7  89d6                   mov      esi, edx
00415ad9  895c2408               mov      dword ptr [esp + 8], ebx
00415add  0fb7eb                 movzx    ebp, bx
00415ae0  31d2                   xor      edx, edx
00415ae2  30e4                   xor      ah, ah
00415ae4  8a1541805000           mov      dl, byte ptr [0x508041]
00415aea  8864240c               mov      byte ptr [esp + 0xc], ah
00415aee  89e8                   mov      eax, ebp
00415af0  e8fb0b0600             call     0x4766f0 ; TerrainEstDecouvert
00415af5  84c0                   test     al, al
00415af7  0f843bb0ffff           je       0x410b38
00415afd  31d2                   xor      edx, edx
00415aff  89e8                   mov      eax, ebp
00415b01  8a1541805000           mov      dl, byte ptr [0x508041]
00415b07  e82e0e0600             call     0x47693a ; CaseEstIlluminee
00415b0c  84c0                   test     al, al
00415b0e  0f8405000000           je       0x415b19
00415b14  c644240c01             mov      byte ptr [esp + 0xc], 1
00415b19  0fb76c2408             movzx    ebp, word ptr [esp + 8]
00415b1e  a1747d5000             mov      eax, dword ptr [0x507d74]
00415b23  b918000000             mov      ecx, 0x18
00415b28  bf585a4100             mov      edi, 0x415a58
00415b2d  8a0428                 mov      al, byte ptr [eax + ebp]
00415b30  f2ae                   repne scasb al, byte ptr es:[edi]
00415b32  2eff248d6f5a4100       jmp      dword ptr cs:[ecx*4 + 0x415a6f]
00415b3a  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
00415b40  30e4                   xor      ah, ah
00415b42  8a042b                 mov      al, byte ptr [ebx + ebp]
00415b45  05c5230000             add      eax, 0x23c5
00415b4a  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
00415b50  31d2                   xor      edx, edx
00415b52  25ffff0000             and      eax, 0xffff
00415b57  88ca                   mov      dl, cl
00415b59  89442404               mov      dword ptr [esp + 4], eax
00415b5d  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00415b63  81e2ff000000           and      edx, 0xff
00415b69  bf02000000             mov      edi, 2
00415b6e  89d0                   mov      eax, edx
00415b70  c1fa1f                 sar      edx, 0x1f
00415b73  f7ff                   idiv     edi
00415b75  fec1                   inc      cl
00415b77  880d181d4e00           mov      byte ptr [0x4e1d18], cl
00415b7d  b901000000             mov      ecx, 1
00415b82  31c0                   xor      eax, eax
00415b84  0fbffe                 movsx    edi, si
00415b87  8a042b                 mov      al, byte ptr [ebx + ebp]
00415b8a  8b7424fe               mov      esi, dword ptr [esp - 2]
00415b8e  29d0                   sub      eax, edx
00415b90  89fa                   mov      edx, edi
00415b92  8b5c2404               mov      ebx, dword ptr [esp + 4]
00415b96  29c2                   sub      edx, eax
00415b98  c1fe10                 sar      esi, 0x10
00415b9b  0fbfd2                 movsx    edx, dx
00415b9e  89f0                   mov      eax, esi
00415ba0  e87e5e0400             call     0x45ba23 ; PasteEclairCmp
00415ba5  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00415baa  31d2                   xor      edx, edx
00415bac  8a1428                 mov      dl, byte ptr [eax + ebp]
00415baf  83c203                 add      edx, 3
00415bb2  bb10000000             mov      ebx, 0x10
00415bb7  89d0                   mov      eax, edx
00415bb9  c1fa1f                 sar      edx, 0x1f
00415bbc  f7fb                   idiv     ebx
00415bbe  b901000000             mov      ecx, 1
00415bc3  81c2c5230000           add      edx, 0x23c5
00415bc9  31db                   xor      ebx, ebx
00415bcb  89f0                   mov      eax, esi
00415bcd  6689d3                 mov      bx, dx
00415bd0  89fa                   mov      edx, edi
00415bd2  e84c5e0400             call     0x45ba23 ; PasteEclairCmp
00415bd7  e95cafffff             jmp      0x410b38 ;
00415bdc  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
00415be2  30e4                   xor      ah, ah
00415be4  8a042b                 mov      al, byte ptr [ebx + ebp]
00415be7  05c5230000             add      eax, 0x23c5
00415bec  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
00415bf2  31d2                   xor      edx, edx
00415bf4  25ffff0000             and      eax, 0xffff
00415bf9  88ca                   mov      dl, cl
00415bfb  89442404               mov      dword ptr [esp + 4], eax
00415bff  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00415c05  81e2ff000000           and      edx, 0xff
00415c0b  bf02000000             mov      edi, 2
00415c10  89d0                   mov      eax, edx
00415c12  c1fa1f                 sar      edx, 0x1f
00415c15  f7ff                   idiv     edi
00415c17  fec1                   inc      cl
00415c19  880d181d4e00           mov      byte ptr [0x4e1d18], cl
00415c1f  b901000000             mov      ecx, 1
00415c24  31c0                   xor      eax, eax
00415c26  0fbffe                 movsx    edi, si
00415c29  8a042b                 mov      al, byte ptr [ebx + ebp]
00415c2c  8b7424fe               mov      esi, dword ptr [esp - 2]
00415c30  29d0                   sub      eax, edx
00415c32  89fa                   mov      edx, edi
00415c34  8b5c2404               mov      ebx, dword ptr [esp + 4]
00415c38  29c2                   sub      edx, eax
00415c3a  c1fe10                 sar      esi, 0x10
00415c3d  0fbfd2                 movsx    edx, dx
00415c40  89f0                   mov      eax, esi
00415c42  e84f5b0400             call     0x45b796 ; PasteOmbreCmp
00415c47  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00415c4c  31d2                   xor      edx, edx
00415c4e  8a1428                 mov      dl, byte ptr [eax + ebp]
00415c51  83c203                 add      edx, 3
00415c54  bb10000000             mov      ebx, 0x10
00415c59  89d0                   mov      eax, edx
00415c5b  c1fa1f                 sar      edx, 0x1f
00415c5e  f7fb                   idiv     ebx
00415c60  b901000000             mov      ecx, 1
00415c65  81c2c5230000           add      edx, 0x23c5
00415c6b  31db                   xor      ebx, ebx
00415c6d  89f0                   mov      eax, esi
00415c6f  6689d3                 mov      bx, dx
00415c72  89fa                   mov      edx, edi
00415c74  e92e080000             jmp      0x4164a7 ;
00415c79  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415c7f  8a142a                 mov      dl, byte ptr [edx + ebp]
00415c82  81e2ff000000           and      edx, 0xff
00415c88  bb20000000             mov      ebx, 0x20
00415c8d  89d0                   mov      eax, edx
00415c8f  c1fa1f                 sar      edx, 0x1f
00415c92  f7fb                   idiv     ebx
00415c94  b901000000             mov      ecx, 1
00415c99  83c604                 add      esi, 4
00415c9c  81c2f51f0000           add      edx, 0x1ff5
00415ca2  31db                   xor      ebx, ebx
00415ca4  8b0424                 mov      eax, dword ptr [esp]
00415ca7  6689d3                 mov      bx, dx
00415caa  050b000000             add      eax, 0xb
00415caf  e903010000             jmp      0x415db7 ;
00415cb4  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415cba  8a142a                 mov      dl, byte ptr [edx + ebp]
00415cbd  81e2ff000000           and      edx, 0xff
00415cc3  bb20000000             mov      ebx, 0x20
00415cc8  89d0                   mov      eax, edx
00415cca  c1fa1f                 sar      edx, 0x1f
00415ccd  f7fb                   idiv     ebx
00415ccf  b901000000             mov      ecx, 1
00415cd4  83ee0b                 sub      esi, 0xb
00415cd7  81c215200000           add      edx, 0x2015
00415cdd  ebc3                   jmp      0x415ca2 ;
00415cdf  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415ce5  8a142a                 mov      dl, byte ptr [edx + ebp]
00415ce8  81e2ff000000           and      edx, 0xff
00415cee  bb20000000             mov      ebx, 0x20
00415cf3  89d0                   mov      eax, edx
00415cf5  c1fa1f                 sar      edx, 0x1f
00415cf8  f7fb                   idiv     ebx
00415cfa  b901000000             mov      ecx, 1
00415cff  83ee12                 sub      esi, 0x12
00415d02  81c235200000           add      edx, 0x2035
00415d08  eb98                   jmp      0x415ca2 ;
00415d0a  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415d10  8a142a                 mov      dl, byte ptr [edx + ebp]
00415d13  81e2ff000000           and      edx, 0xff
00415d19  bb20000000             mov      ebx, 0x20
00415d1e  89d0                   mov      eax, edx
00415d20  c1fa1f                 sar      edx, 0x1f
00415d23  f7fb                   idiv     ebx
00415d25  8d82f51f0000           lea      eax, [edx + 0x1ff5]
00415d2b  31db                   xor      ebx, ebx
00415d2d  b901000000             mov      ecx, 1
00415d32  6689c3                 mov      bx, ax
00415d35  8b0424                 mov      eax, dword ptr [esp]
00415d38  83c604                 add      esi, 4
00415d3b  e96affffff             jmp      0x415caa ;
00415d40  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415d46  8a142a                 mov      dl, byte ptr [edx + ebp]
00415d49  81e2ff000000           and      edx, 0xff
00415d4f  bb20000000             mov      ebx, 0x20
00415d54  89d0                   mov      eax, edx
00415d56  c1fa1f                 sar      edx, 0x1f
00415d59  f7fb                   idiv     ebx
00415d5b  81c215200000           add      edx, 0x2015
00415d61  89f0                   mov      eax, esi
00415d63  31db                   xor      ebx, ebx
00415d65  83e80b                 sub      eax, 0xb
00415d68  6689d3                 mov      bx, dx
00415d6b  0fbfd0                 movsx    edx, ax
00415d6e  8b0424                 mov      eax, dword ptr [esp]
00415d71  050b000000             add      eax, 0xb
00415d76  b901000000             mov      ecx, 1
00415d7b  98                     cwde
00415d7c  e8c6540400             call     0x45b247 ; PasteBobCmp
00415d81  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415d87  8a142a                 mov      dl, byte ptr [edx + ebp]
00415d8a  81e2ff000000           and      edx, 0xff
00415d90  bb20000000             mov      ebx, 0x20
00415d95  89d0                   mov      eax, edx
00415d97  c1fa1f                 sar      edx, 0x1f
00415d9a  f7fb                   idiv     ebx
00415d9c  b901000000             mov      ecx, 1
00415da1  83c60f                 add      esi, 0xf
00415da4  81c2f51f0000           add      edx, 0x1ff5
00415daa  31db                   xor      ebx, ebx
00415dac  8b0424                 mov      eax, dword ptr [esp]
00415daf  6689d3                 mov      bx, dx
00415db2  051c000000             add      eax, 0x1c
00415db7  0fbfd6                 movsx    edx, si
00415dba  98                     cwde
00415dbb  e887540400             call     0x45b247 ; PasteBobCmp
00415dc0  e973adffff             jmp      0x410b38 ;
00415dc5  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415dcb  8a142a                 mov      dl, byte ptr [edx + ebp]
00415dce  81e2ff000000           and      edx, 0xff
00415dd4  bb20000000             mov      ebx, 0x20
00415dd9  89d0                   mov      eax, edx
00415ddb  c1fa1f                 sar      edx, 0x1f
00415dde  f7fb                   idiv     ebx
00415de0  b901000000             mov      ecx, 1
00415de5  81c2f51f0000           add      edx, 0x1ff5
00415deb  31db                   xor      ebx, ebx
00415ded  8b4424fe               mov      eax, dword ptr [esp - 2]
00415df1  6689d3                 mov      bx, dx
00415df4  c1f810                 sar      eax, 0x10
00415df7  0fbfd6                 movsx    edx, si
00415dfa  e848540400             call     0x45b247 ; PasteBobCmp
00415dff  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415e05  8a142a                 mov      dl, byte ptr [edx + ebp]
00415e08  81e2ff000000           and      edx, 0xff
00415e0e  bb20000000             mov      ebx, 0x20
00415e13  89d0                   mov      eax, edx
00415e15  c1fa1f                 sar      edx, 0x1f
00415e18  f7fb                   idiv     ebx
00415e1a  81c235200000           add      edx, 0x2035
00415e20  89f0                   mov      eax, esi
00415e22  31db                   xor      ebx, ebx
00415e24  83e812                 sub      eax, 0x12
00415e27  6689d3                 mov      bx, dx
00415e2a  0fbfd0                 movsx    edx, ax
00415e2d  8b0424                 mov      eax, dword ptr [esp]
00415e30  050b000000             add      eax, 0xb
00415e35  b901000000             mov      ecx, 1
00415e3a  98                     cwde
00415e3b  e807540400             call     0x45b247 ; PasteBobCmp
00415e40  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415e46  8a142a                 mov      dl, byte ptr [edx + ebp]
00415e49  81e2ff000000           and      edx, 0xff
00415e4f  bb20000000             mov      ebx, 0x20
00415e54  89d0                   mov      eax, edx
00415e56  c1fa1f                 sar      edx, 0x1f
00415e59  f7fb                   idiv     ebx
00415e5b  8d8215200000           lea      eax, [edx + 0x2015]
00415e61  31db                   xor      ebx, ebx
00415e63  b901000000             mov      ecx, 1
00415e68  6689c3                 mov      bx, ax
00415e6b  8b0424                 mov      eax, dword ptr [esp]
00415e6e  83c608                 add      esi, 8
00415e71  e93cffffff             jmp      0x415db2 ;
00415e76  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415e7c  8a142a                 mov      dl, byte ptr [edx + ebp]
00415e7f  81e2ff000000           and      edx, 0xff
00415e85  bb20000000             mov      ebx, 0x20
00415e8a  89d0                   mov      eax, edx
00415e8c  c1fa1f                 sar      edx, 0x1f
00415e8f  f7fb                   idiv     ebx
00415e91  b901000000             mov      ecx, 1
00415e96  81c275200000           add      edx, 0x2075
00415e9c  31db                   xor      ebx, ebx
00415e9e  8b4424fe               mov      eax, dword ptr [esp - 2]
00415ea2  6689d3                 mov      bx, dx
00415ea5  c1f810                 sar      eax, 0x10
00415ea8  0fbfd6                 movsx    edx, si
00415eab  e90bffffff             jmp      0x415dbb ;
00415eb0  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415eb6  8a142a                 mov      dl, byte ptr [edx + ebp]
00415eb9  81e2ff000000           and      edx, 0xff
00415ebf  bb20000000             mov      ebx, 0x20
00415ec4  89d0                   mov      eax, edx
00415ec6  c1fa1f                 sar      edx, 0x1f
00415ec9  f7fb                   idiv     ebx
00415ecb  b901000000             mov      ecx, 1
00415ed0  81c275200000           add      edx, 0x2075
00415ed6  31db                   xor      ebx, ebx
00415ed8  8b0424                 mov      eax, dword ptr [esp]
00415edb  6689d3                 mov      bx, dx
00415ede  83e80a                 sub      eax, 0xa
00415ee1  e9d1feffff             jmp      0x415db7 ;
00415ee6  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415eec  8a142a                 mov      dl, byte ptr [edx + ebp]
00415eef  81e2ff000000           and      edx, 0xff
00415ef5  bb20000000             mov      ebx, 0x20
00415efa  89d0                   mov      eax, edx
00415efc  c1fa1f                 sar      edx, 0x1f
00415eff  f7fb                   idiv     ebx
00415f01  b901000000             mov      ecx, 1
00415f06  81c295200000           add      edx, 0x2095
00415f0c  31db                   xor      ebx, ebx
00415f0e  8b0424                 mov      eax, dword ptr [esp]
00415f11  6689d3                 mov      bx, dx
00415f14  83e814                 sub      eax, 0x14
00415f17  e99bfeffff             jmp      0x415db7 ;
00415f1c  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415f22  8a142a                 mov      dl, byte ptr [edx + ebp]
00415f25  81e2ff000000           and      edx, 0xff
00415f2b  bb20000000             mov      ebx, 0x20
00415f30  89d0                   mov      eax, edx
00415f32  c1fa1f                 sar      edx, 0x1f
00415f35  f7fb                   idiv     ebx
00415f37  b901000000             mov      ecx, 1
00415f3c  83ee10                 sub      esi, 0x10
00415f3f  81c2b5200000           add      edx, 0x20b5
00415f45  31db                   xor      ebx, ebx
00415f47  8b0424                 mov      eax, dword ptr [esp]
00415f4a  6689d3                 mov      bx, dx
00415f4d  83e818                 sub      eax, 0x18
00415f50  e962feffff             jmp      0x415db7 ;
00415f55  8a6c240c               mov      ch, byte ptr [esp + 0xc]
00415f59  bb1d290000             mov      ebx, 0x291d
00415f5e  84ed                   test     ch, ch
00415f60  741c                   je       0x415f7e
00415f62  31d2                   xor      edx, edx
00415f64  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00415f69  668b542408             mov      dx, word ptr [esp + 8]
00415f6e  b901000000             mov      ecx, 1
00415f73  8a0402                 mov      al, byte ptr [edx + eax]
00415f76  30e4                   xor      ah, ah
00415f78  01d8                   add      eax, ebx
00415f7a  31db                   xor      ebx, ebx
00415f7c  eb1d                   jmp      0x415f9b ;
00415f7e  31d2                   xor      edx, edx
00415f80  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00415f85  668b542408             mov      dx, word ptr [esp + 8]
00415f8a  b901000000             mov      ecx, 1
00415f8f  8a0402                 mov      al, byte ptr [edx + eax]
00415f92  30e4                   xor      ah, ah
00415f94  31db                   xor      ebx, ebx
00415f96  0579290000             add      eax, 0x2979
00415f9b  6689c3                 mov      bx, ax
00415f9e  89f0                   mov      eax, esi
00415fa0  83e81b                 sub      eax, 0x1b
00415fa3  0fbfd0                 movsx    edx, ax
00415fa6  8b0424                 mov      eax, dword ptr [esp]
00415fa9  0502000000             add      eax, 2
00415fae  98                     cwde
00415faf  e893520400             call     0x45b247 ; PasteBobCmp
00415fb4  31d2                   xor      edx, edx
00415fb6  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00415fbb  668b542408             mov      dx, word ptr [esp + 8]
00415fc0  8a0402                 mov      al, byte ptr [edx + eax]
00415fc3  30e4                   xor      ah, ah
00415fc5  31db                   xor      ebx, ebx
00415fc7  0539290000             add      eax, 0x2939
00415fcc  b901000000             mov      ecx, 1
00415fd1  6689c3                 mov      bx, ax
00415fd4  8b0424                 mov      eax, dword ptr [esp]
00415fd7  83c60d                 add      esi, 0xd
00415fda  0509000000             add      eax, 9
00415fdf  e9bf040000             jmp      0x4164a3 ;
00415fe4  8a4c240c               mov      cl, byte ptr [esp + 0xc]
00415fe8  bb19290000             mov      ebx, 0x2919
00415fed  84c9                   test     cl, cl
00415fef  741d                   je       0x41600e
00415ff1  31c0                   xor      eax, eax
00415ff3  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00415ff9  668b442408             mov      ax, word ptr [esp + 8]
00415ffe  b901000000             mov      ecx, 1
00416003  8a0402                 mov      al, byte ptr [edx + eax]
00416006  30e4                   xor      ah, ah
00416008  01d8                   add      eax, ebx
0041600a  31db                   xor      ebx, ebx
0041600c  eb1d                   jmp      0x41602b ;
0041600e  31d2                   xor      edx, edx
00416010  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00416015  668b542408             mov      dx, word ptr [esp + 8]
0041601a  b901000000             mov      ecx, 1
0041601f  8a0402                 mov      al, byte ptr [edx + eax]
00416022  30e4                   xor      ah, ah
00416024  31db                   xor      ebx, ebx
00416026  0575290000             add      eax, 0x2975
0041602b  6689c3                 mov      bx, ax
0041602e  89f0                   mov      eax, esi
00416030  83e824                 sub      eax, 0x24
00416033  0fbfd0                 movsx    edx, ax
00416036  8b0424                 mov      eax, dword ptr [esp]
00416039  83e804                 sub      eax, 4
0041603c  98                     cwde
0041603d  e805520400             call     0x45b247 ; PasteBobCmp
00416042  31c0                   xor      eax, eax
00416044  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
0041604a  668b442408             mov      ax, word ptr [esp + 8]
0041604f  8a0402                 mov      al, byte ptr [edx + eax]
00416052  30e4                   xor      ah, ah
00416054  31db                   xor      ebx, ebx
00416056  0535290000             add      eax, 0x2935
0041605b  b901000000             mov      ecx, 1
00416060  6689c3                 mov      bx, ax
00416063  8b0424                 mov      eax, dword ptr [esp]
00416066  83c615                 add      esi, 0x15
00416069  0506000000             add      eax, 6
0041606e  e930040000             jmp      0x4164a3 ;
00416073  8a74240c               mov      dh, byte ptr [esp + 0xc]
00416077  bb15290000             mov      ebx, 0x2915
0041607c  84f6                   test     dh, dh
0041607e  741c                   je       0x41609c
00416080  31d2                   xor      edx, edx
00416082  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00416087  668b542408             mov      dx, word ptr [esp + 8]
0041608c  b901000000             mov      ecx, 1
00416091  8a0402                 mov      al, byte ptr [edx + eax]
00416094  30e4                   xor      ah, ah
00416096  01d8                   add      eax, ebx
00416098  31db                   xor      ebx, ebx
0041609a  eb1e                   jmp      0x4160ba ;
0041609c  31c0                   xor      eax, eax
0041609e  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004160a4  668b442408             mov      ax, word ptr [esp + 8]
004160a9  b901000000             mov      ecx, 1
004160ae  8a0402                 mov      al, byte ptr [edx + eax]
004160b1  30e4                   xor      ah, ah
004160b3  31db                   xor      ebx, ebx
004160b5  0571290000             add      eax, 0x2971
004160ba  6689c3                 mov      bx, ax
004160bd  89f0                   mov      eax, esi
004160bf  83e853                 sub      eax, 0x53
004160c2  0fbfd0                 movsx    edx, ax
004160c5  8b0424                 mov      eax, dword ptr [esp]
004160c8  83e803                 sub      eax, 3
004160cb  98                     cwde
004160cc  e876510400             call     0x45b247 ; PasteBobCmp
004160d1  31d2                   xor      edx, edx
004160d3  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004160d8  668b542408             mov      dx, word ptr [esp + 8]
004160dd  8a0402                 mov      al, byte ptr [edx + eax]
004160e0  30e4                   xor      ah, ah
004160e2  31db                   xor      ebx, ebx
004160e4  0531290000             add      eax, 0x2931
004160e9  b901000000             mov      ecx, 1
004160ee  6689c3                 mov      bx, ax
004160f1  8b0424                 mov      eax, dword ptr [esp]
004160f4  83c606                 add      esi, 6
004160f7  0510000000             add      eax, 0x10
004160fc  e9a2030000             jmp      0x4164a3 ;
00416101  807c240c00             cmp      byte ptr [esp + 0xc], 0
00416106  7420                   je       0x416128
00416108  31c0                   xor      eax, eax
0041610a  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416110  668b442408             mov      ax, word ptr [esp + 8]
00416115  b901000000             mov      ecx, 1
0041611a  8a0402                 mov      al, byte ptr [edx + eax]
0041611d  30e4                   xor      ah, ah
0041611f  31db                   xor      ebx, ebx
00416121  0515290000             add      eax, 0x2915
00416126  eb1d                   jmp      0x416145 ;
00416128  31d2                   xor      edx, edx
0041612a  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0041612f  668b542408             mov      dx, word ptr [esp + 8]
00416134  b901000000             mov      ecx, 1
00416139  8a0402                 mov      al, byte ptr [edx + eax]
0041613c  30e4                   xor      ah, ah
0041613e  31db                   xor      ebx, ebx
00416140  0571290000             add      eax, 0x2971
00416145  6689c3                 mov      bx, ax
00416148  89f0                   mov      eax, esi
0041614a  83e859                 sub      eax, 0x59
0041614d  0fbfd0                 movsx    edx, ax
00416150  8b0424                 mov      eax, dword ptr [esp]
00416153  0503000000             add      eax, 3
00416158  98                     cwde
00416159  e8e9500400             call     0x45b247 ; PasteBobCmp
0041615e  31ff                   xor      edi, edi
00416160  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00416165  668b7c2408             mov      di, word ptr [esp + 8]
0041616a  8a0407                 mov      al, byte ptr [edi + eax]
0041616d  30e4                   xor      ah, ah
0041616f  31db                   xor      ebx, ebx
00416171  0531290000             add      eax, 0x2931
00416176  6689c3                 mov      bx, ax
00416179  8b0424                 mov      eax, dword ptr [esp]
0041617c  b901000000             mov      ecx, 1
00416181  0516000000             add      eax, 0x16
00416186  0fbfd6                 movsx    edx, si
00416189  98                     cwde
0041618a  e807560400             call     0x45b796 ; PasteOmbreCmp
0041618f  8b0c24                 mov      ecx, dword ptr [esp]
00416192  8a54240c               mov      dl, byte ptr [esp + 0xc]
00416196  89f0                   mov      eax, esi
00416198  83e903                 sub      ecx, 3
0041619b  83e813                 sub      eax, 0x13
0041619e  84d2                   test     dl, dl
004161a0  7416                   je       0x4161b8
004161a2  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004161a8  01d7                   add      edi, edx
004161aa  30f6                   xor      dh, dh
004161ac  8a17                   mov      dl, byte ptr [edi]
004161ae  31db                   xor      ebx, ebx
004161b0  81c21d290000           add      edx, 0x291d
004161b6  eb14                   jmp      0x4161cc ;
004161b8  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004161be  01d7                   add      edi, edx
004161c0  30f6                   xor      dh, dh
004161c2  8a17                   mov      dl, byte ptr [edi]
004161c4  31db                   xor      ebx, ebx
004161c6  81c279290000           add      edx, 0x2979
004161cc  6689d3                 mov      bx, dx
004161cf  0fbfd0                 movsx    edx, ax
004161d2  0fbfc1                 movsx    eax, cx
004161d5  b901000000             mov      ecx, 1
004161da  e868500400             call     0x45b247 ; PasteBobCmp
004161df  31c0                   xor      eax, eax
004161e1  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004161e7  668b442408             mov      ax, word ptr [esp + 8]
004161ec  8a0402                 mov      al, byte ptr [edx + eax]
004161ef  30e4                   xor      ah, ah
004161f1  31db                   xor      ebx, ebx
004161f3  0539290000             add      eax, 0x2939
004161f8  b901000000             mov      ecx, 1
004161fd  6689c3                 mov      bx, ax
00416200  8b0424                 mov      eax, dword ptr [esp]
00416203  83c615                 add      esi, 0x15
00416206  0504000000             add      eax, 4
0041620b  e993020000             jmp      0x4164a3 ;
00416210  8a74240c               mov      dh, byte ptr [esp + 0xc]
00416214  bb15290000             mov      ebx, 0x2915
00416219  84f6                   test     dh, dh
0041621b  741c                   je       0x416239
0041621d  31d2                   xor      edx, edx
0041621f  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00416224  668b542408             mov      dx, word ptr [esp + 8]
00416229  b901000000             mov      ecx, 1
0041622e  8a0402                 mov      al, byte ptr [edx + eax]
00416231  30e4                   xor      ah, ah
00416233  01d8                   add      eax, ebx
00416235  31db                   xor      ebx, ebx
00416237  eb1e                   jmp      0x416257 ;
00416239  31c0                   xor      eax, eax
0041623b  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416241  668b442408             mov      ax, word ptr [esp + 8]
00416246  b901000000             mov      ecx, 1
0041624b  8a0402                 mov      al, byte ptr [edx + eax]
0041624e  30e4                   xor      ah, ah
00416250  31db                   xor      ebx, ebx
00416252  0571290000             add      eax, 0x2971
00416257  6689c3                 mov      bx, ax
0041625a  89f0                   mov      eax, esi
0041625c  83e85b                 sub      eax, 0x5b
0041625f  0fbfd0                 movsx    edx, ax
00416262  8b0424                 mov      eax, dword ptr [esp]
00416265  83e804                 sub      eax, 4
00416268  98                     cwde
00416269  e8d94f0400             call     0x45b247 ; PasteBobCmp
0041626e  31ff                   xor      edi, edi
00416270  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00416275  668b7c2408             mov      di, word ptr [esp + 8]
0041627a  8a0407                 mov      al, byte ptr [edi + eax]
0041627d  30e4                   xor      ah, ah
0041627f  31db                   xor      ebx, ebx
00416281  0531290000             add      eax, 0x2931
00416286  6689c3                 mov      bx, ax
00416289  89f0                   mov      eax, esi
0041628b  83e802                 sub      eax, 2
0041628e  0fbfd0                 movsx    edx, ax
00416291  8b0424                 mov      eax, dword ptr [esp]
00416294  050f000000             add      eax, 0xf
00416299  b901000000             mov      ecx, 1
0041629e  98                     cwde
0041629f  e8f2540400             call     0x45b796 ; PasteOmbreCmp
004162a4  8b0424                 mov      eax, dword ptr [esp]
004162a7  8a5c240c               mov      bl, byte ptr [esp + 0xc]
004162ab  89f2                   mov      edx, esi
004162ad  83e807                 sub      eax, 7
004162b0  83ea18                 sub      edx, 0x18
004162b3  84db                   test     bl, bl
004162b5  7414                   je       0x4162cb
004162b7  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
004162bd  01df                   add      edi, ebx
004162bf  30ff                   xor      bh, bh
004162c1  8a1f                   mov      bl, byte ptr [edi]
004162c3  81c31d290000           add      ebx, 0x291d
004162c9  eb12                   jmp      0x4162dd ;
004162cb  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
004162d1  01df                   add      edi, ebx
004162d3  30ff                   xor      bh, bh
004162d5  8a1f                   mov      bl, byte ptr [edi]
004162d7  81c379290000           add      ebx, 0x2979
004162dd  b901000000             mov      ecx, 1
004162e2  81e3ffff0000           and      ebx, 0xffff
004162e8  0fbfd2                 movsx    edx, dx
004162eb  98                     cwde
004162ec  e8564f0400             call     0x45b247 ; PasteBobCmp
004162f1  31ff                   xor      edi, edi
004162f3  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004162f8  668b7c2408             mov      di, word ptr [esp + 8]
004162fd  8a0407                 mov      al, byte ptr [edi + eax]
00416300  30e4                   xor      ah, ah
00416302  31db                   xor      ebx, ebx
00416304  0539290000             add      eax, 0x2939
00416309  6689c3                 mov      bx, ax
0041630c  89f0                   mov      eax, esi
0041630e  0510000000             add      eax, 0x10
00416313  0fbfd0                 movsx    edx, ax
00416316  8b4424fe               mov      eax, dword ptr [esp - 2]
0041631a  b901000000             mov      ecx, 1
0041631f  c1f810                 sar      eax, 0x10
00416322  e86f540400             call     0x45b796 ; PasteOmbreCmp
00416327  8b0c24                 mov      ecx, dword ptr [esp]
0041632a  8a7c240c               mov      bh, byte ptr [esp + 0xc]
0041632e  89f0                   mov      eax, esi
00416330  83c10f                 add      ecx, 0xf
00416333  83e822                 sub      eax, 0x22
00416336  84ff                   test     bh, bh
00416338  7416                   je       0x416350
0041633a  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416340  01d7                   add      edi, edx
00416342  30f6                   xor      dh, dh
00416344  8a17                   mov      dl, byte ptr [edi]
00416346  31db                   xor      ebx, ebx
00416348  81c219290000           add      edx, 0x2919
0041634e  eb14                   jmp      0x416364 ;
00416350  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416356  01d7                   add      edi, edx
00416358  30f6                   xor      dh, dh
0041635a  8a17                   mov      dl, byte ptr [edi]
0041635c  31db                   xor      ebx, ebx
0041635e  81c275290000           add      edx, 0x2975
00416364  6689d3                 mov      bx, dx
00416367  0fbfd0                 movsx    edx, ax
0041636a  0fbfc1                 movsx    eax, cx
0041636d  b901000000             mov      ecx, 1
00416372  e8d04e0400             call     0x45b247 ; PasteBobCmp
00416377  31d2                   xor      edx, edx
00416379  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0041637e  668b542408             mov      dx, word ptr [esp + 8]
00416383  8a0402                 mov      al, byte ptr [edx + eax]
00416386  30e4                   xor      ah, ah
00416388  31db                   xor      ebx, ebx
0041638a  0535290000             add      eax, 0x2935
0041638f  b901000000             mov      ecx, 1
00416394  6689c3                 mov      bx, ax
00416397  8b0424                 mov      eax, dword ptr [esp]
0041639a  83c617                 add      esi, 0x17
0041639d  0519000000             add      eax, 0x19
004163a2  e9fc000000             jmp      0x4164a3 ;
004163a7  8b0c24                 mov      ecx, dword ptr [esp]
004163aa  8a54240c               mov      dl, byte ptr [esp + 0xc]
004163ae  89f0                   mov      eax, esi
004163b0  83e904                 sub      ecx, 4
004163b3  83e819                 sub      eax, 0x19
004163b6  84d2                   test     dl, dl
004163b8  7417                   je       0x4163d1
004163ba  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004163c0  01d5                   add      ebp, edx
004163c2  30f6                   xor      dh, dh
004163c4  8a5500                 mov      dl, byte ptr [ebp]
004163c7  31db                   xor      ebx, ebx
004163c9  81c229290000           add      edx, 0x2929
004163cf  eb15                   jmp      0x4163e6 ;
004163d1  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004163d7  01d5                   add      ebp, edx
004163d9  30f6                   xor      dh, dh
004163db  8a5500                 mov      dl, byte ptr [ebp]
004163de  31db                   xor      ebx, ebx
004163e0  81c285290000           add      edx, 0x2985
004163e6  6689d3                 mov      bx, dx
004163e9  0fbfd0                 movsx    edx, ax
004163ec  0fbfc1                 movsx    eax, cx
004163ef  b901000000             mov      ecx, 1
004163f4  e84e4e0400             call     0x45b247 ; PasteBobCmp
004163f9  31c0                   xor      eax, eax
004163fb  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416401  668b442408             mov      ax, word ptr [esp + 8]
00416406  8a0402                 mov      al, byte ptr [edx + eax]
00416409  30e4                   xor      ah, ah
0041640b  31db                   xor      ebx, ebx
0041640d  0545290000             add      eax, 0x2945
00416412  b901000000             mov      ecx, 1
00416417  6689c3                 mov      bx, ax
0041641a  8b0424                 mov      eax, dword ptr [esp]
0041641d  83c610                 add      esi, 0x10
00416420  e9b5fbffff             jmp      0x415fda ;
00416425  8b1424                 mov      edx, dword ptr [esp]
00416428  8a4c240c               mov      cl, byte ptr [esp + 0xc]
0041642c  89f0                   mov      eax, esi
0041642e  83ea07                 sub      edx, 7
00416431  83e82b                 sub      eax, 0x2b
00416434  84c9                   test     cl, cl
00416436  7415                   je       0x41644d
00416438  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
0041643e  01dd                   add      ebp, ebx
00416440  30ff                   xor      bh, bh
00416442  8a5d00                 mov      bl, byte ptr [ebp]
00416445  81c325290000           add      ebx, 0x2925
0041644b  eb13                   jmp      0x416460 ;
0041644d  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
00416453  01dd                   add      ebp, ebx
00416455  30ff                   xor      bh, bh
00416457  8a5d00                 mov      bl, byte ptr [ebp]
0041645a  81c381290000           add      ebx, 0x2981
00416460  b901000000             mov      ecx, 1
00416465  81e3ffff0000           and      ebx, 0xffff
0041646b  98                     cwde
0041646c  0fbffa                 movsx    edi, dx
0041646f  89c2                   mov      edx, eax
00416471  89f8                   mov      eax, edi
00416473  e8cf4d0400             call     0x45b247 ; PasteBobCmp
00416478  31d2                   xor      edx, edx
0041647a  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0041647f  668b542408             mov      dx, word ptr [esp + 8]
00416484  8a0402                 mov      al, byte ptr [edx + eax]
00416487  30e4                   xor      ah, ah
00416489  31db                   xor      ebx, ebx
0041648b  0541290000             add      eax, 0x2941
00416490  b901000000             mov      ecx, 1
00416495  6689c3                 mov      bx, ax
00416498  8b0424                 mov      eax, dword ptr [esp]
0041649b  83c60e                 add      esi, 0xe
0041649e  050e000000             add      eax, 0xe
004164a3  0fbfd6                 movsx    edx, si
004164a6  98                     cwde
004164a7  e8ea520400             call     0x45b796 ; PasteOmbreCmp
004164ac  e987a6ffff             jmp      0x410b38 ;
004164b1  8b1424                 mov      edx, dword ptr [esp]
004164b4  8a7c240c               mov      bh, byte ptr [esp + 0xc]
004164b8  89f0                   mov      eax, esi
004164ba  83ea0b                 sub      edx, 0xb
004164bd  83e841                 sub      eax, 0x41
004164c0  84ff                   test     bh, bh
004164c2  7428                   je       0x4164ec
004164c4  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
004164ca  01dd                   add      ebp, ebx
004164cc  30ff                   xor      bh, bh
004164ce  8a5d00                 mov      bl, byte ptr [ebp]
004164d1  81c321290000           add      ebx, 0x2921
004164d7  b901000000             mov      ecx, 1
004164dc  81e3ffff0000           and      ebx, 0xffff
004164e2  98                     cwde
004164e3  0fbffa                 movsx    edi, dx
004164e6  89c2                   mov      edx, eax
004164e8  89f8                   mov      eax, edi
004164ea  eb26                   jmp      0x416512 ;
004164ec  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
004164f2  01dd                   add      ebp, ebx
004164f4  30ff                   xor      bh, bh
004164f6  8a5d00                 mov      bl, byte ptr [ebp]
004164f9  81c37d290000           add      ebx, 0x297d
004164ff  b901000000             mov      ecx, 1
00416504  81e3ffff0000           and      ebx, 0xffff
0041650a  0fbff8                 movsx    edi, ax
0041650d  0fbfc2                 movsx    eax, dx
00416510  89fa                   mov      edx, edi
00416512  e8304d0400             call     0x45b247 ; PasteBobCmp
00416517  31d2                   xor      edx, edx
00416519  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0041651e  668b542408             mov      dx, word ptr [esp + 8]
00416523  8a0402                 mov      al, byte ptr [edx + eax]
00416526  30e4                   xor      ah, ah
00416528  31db                   xor      ebx, ebx
0041652a  053d290000             add      eax, 0x293d
0041652f  b901000000             mov      ecx, 1
00416534  6689c3                 mov      bx, ax
00416537  8b0424                 mov      eax, dword ptr [esp]
0041653a  83c60d                 add      esi, 0xd
0041653d  050c000000             add      eax, 0xc
00416542  e95cffffff             jmp      0x4164a3 ;
00416547  8b0c24                 mov      ecx, dword ptr [esp]
0041654a  8a54240c               mov      dl, byte ptr [esp + 0xc]
0041654e  89f0                   mov      eax, esi
00416550  83e90f                 sub      ecx, 0xf
00416553  83e84b                 sub      eax, 0x4b
00416556  84d2                   test     dl, dl
00416558  7417                   je       0x416571
0041655a  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416560  01d5                   add      ebp, edx
00416562  30f6                   xor      dh, dh
00416564  8a5500                 mov      dl, byte ptr [ebp]
00416567  31db                   xor      ebx, ebx
00416569  81c221290000           add      edx, 0x2921
0041656f  eb15                   jmp      0x416586 ;
00416571  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416577  01d5                   add      ebp, edx
00416579  30f6                   xor      dh, dh
0041657b  8a5500                 mov      dl, byte ptr [ebp]
0041657e  31db                   xor      ebx, ebx
00416580  81c27d290000           add      edx, 0x297d
00416586  6689d3                 mov      bx, dx
00416589  0fbfd0                 movsx    edx, ax
0041658c  0fbfc1                 movsx    eax, cx
0041658f  b901000000             mov      ecx, 1
00416594  e8ae4c0400             call     0x45b247 ; PasteBobCmp
00416599  31ff                   xor      edi, edi
0041659b  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004165a0  668b7c2408             mov      di, word ptr [esp + 8]
004165a5  8a0407                 mov      al, byte ptr [edi + eax]
004165a8  30e4                   xor      ah, ah
004165aa  31db                   xor      ebx, ebx
004165ac  053d290000             add      eax, 0x293d
004165b1  6689c3                 mov      bx, ax
004165b4  89f0                   mov      eax, esi
004165b6  0503000000             add      eax, 3
004165bb  0fbfd0                 movsx    edx, ax
004165be  8b0424                 mov      eax, dword ptr [esp]
004165c1  0508000000             add      eax, 8
004165c6  b901000000             mov      ecx, 1
004165cb  98                     cwde
004165cc  e8c5510400             call     0x45b796 ; PasteOmbreCmp
004165d1  8b1424                 mov      edx, dword ptr [esp]
004165d4  8a5c240c               mov      bl, byte ptr [esp + 0xc]
004165d8  89f0                   mov      eax, esi
004165da  83c207                 add      edx, 7
004165dd  83e811                 sub      eax, 0x11
004165e0  84db                   test     bl, bl
004165e2  7427                   je       0x41660b
004165e4  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
004165ea  01df                   add      edi, ebx
004165ec  30ff                   xor      bh, bh
004165ee  8a1f                   mov      bl, byte ptr [edi]
004165f0  81c329290000           add      ebx, 0x2929
004165f6  b901000000             mov      ecx, 1
004165fb  81e3ffff0000           and      ebx, 0xffff
00416601  0fbff8                 movsx    edi, ax
00416604  0fbfc2                 movsx    eax, dx
00416607  89fa                   mov      edx, edi
00416609  eb25                   jmp      0x416630 ;
0041660b  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
00416611  01df                   add      edi, ebx
00416613  30ff                   xor      bh, bh
00416615  8a1f                   mov      bl, byte ptr [edi]
00416617  81c385290000           add      ebx, 0x2985
0041661d  b901000000             mov      ecx, 1
00416622  81e3ffff0000           and      ebx, 0xffff
00416628  98                     cwde
00416629  0fbffa                 movsx    edi, dx
0041662c  89c2                   mov      edx, eax
0041662e  89f8                   mov      eax, edi
00416630  e8124c0400             call     0x45b247 ; PasteBobCmp
00416635  31c0                   xor      eax, eax
00416637  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
0041663d  668b442408             mov      ax, word ptr [esp + 8]
00416642  8a0402                 mov      al, byte ptr [edx + eax]
00416645  30e4                   xor      ah, ah
00416647  31db                   xor      ebx, ebx
00416649  0545290000             add      eax, 0x2945
0041664e  b901000000             mov      ecx, 1
00416653  6689c3                 mov      bx, ax
00416656  8b0424                 mov      eax, dword ptr [esp]
00416659  83c618                 add      esi, 0x18
0041665c  0514000000             add      eax, 0x14
00416661  e93dfeffff             jmp      0x4164a3 ;
00416666  8b0424                 mov      eax, dword ptr [esp]
00416669  8a5c240c               mov      bl, byte ptr [esp + 0xc]
0041666d  89f2                   mov      edx, esi
0041666f  83e807                 sub      eax, 7
00416672  83ea4a                 sub      edx, 0x4a
00416675  84db                   test     bl, bl
00416677  7415                   je       0x41668e
00416679  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
0041667f  01dd                   add      ebp, ebx
00416681  30ff                   xor      bh, bh
00416683  8a5d00                 mov      bl, byte ptr [ebp]
00416686  81c321290000           add      ebx, 0x2921
0041668c  eb13                   jmp      0x4166a1 ;
0041668e  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
00416694  01dd                   add      ebp, ebx
00416696  30ff                   xor      bh, bh
00416698  8a5d00                 mov      bl, byte ptr [ebp]
0041669b  81c37d290000           add      ebx, 0x297d
004166a1  b901000000             mov      ecx, 1
004166a6  81e3ffff0000           and      ebx, 0xffff
004166ac  0fbfd2                 movsx    edx, dx
004166af  98                     cwde
004166b0  e8924b0400             call     0x45b247 ; PasteBobCmp
004166b5  31ff                   xor      edi, edi
004166b7  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004166bc  668b7c2408             mov      di, word ptr [esp + 8]
004166c1  8a0407                 mov      al, byte ptr [edi + eax]
004166c4  30e4                   xor      ah, ah
004166c6  31db                   xor      ebx, ebx
004166c8  053d290000             add      eax, 0x293d
004166cd  6689c3                 mov      bx, ax
004166d0  89f0                   mov      eax, esi
004166d2  0504000000             add      eax, 4
004166d7  0fbfd0                 movsx    edx, ax
004166da  8b0424                 mov      eax, dword ptr [esp]
004166dd  0510000000             add      eax, 0x10
004166e2  b901000000             mov      ecx, 1
004166e7  98                     cwde
004166e8  e8a9500400             call     0x45b796 ; PasteOmbreCmp
004166ed  8b0c24                 mov      ecx, dword ptr [esp]
004166f0  8a7c240c               mov      bh, byte ptr [esp + 0xc]
004166f4  89f0                   mov      eax, esi
004166f6  83e912                 sub      ecx, 0x12
004166f9  83e828                 sub      eax, 0x28
004166fc  84ff                   test     bh, bh
004166fe  7416                   je       0x416716
00416700  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416706  01d7                   add      edi, edx
00416708  30f6                   xor      dh, dh
0041670a  8a17                   mov      dl, byte ptr [edi]
0041670c  31db                   xor      ebx, ebx
0041670e  81c225290000           add      edx, 0x2925
00416714  eb14                   jmp      0x41672a ;
00416716  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
0041671c  01d7                   add      edi, edx
0041671e  30f6                   xor      dh, dh
00416720  8a17                   mov      dl, byte ptr [edi]
00416722  31db                   xor      ebx, ebx
00416724  81c281290000           add      edx, 0x2981
0041672a  6689d3                 mov      bx, dx
0041672d  0fbfd0                 movsx    edx, ax
00416730  0fbfc1                 movsx    eax, cx
00416733  b901000000             mov      ecx, 1
00416738  e80a4b0400             call     0x45b247 ; PasteBobCmp
0041673d  31ff                   xor      edi, edi
0041673f  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00416744  668b7c2408             mov      di, word ptr [esp + 8]
00416749  8a0407                 mov      al, byte ptr [edi + eax]
0041674c  30e4                   xor      ah, ah
0041674e  31db                   xor      ebx, ebx
00416750  0541290000             add      eax, 0x2941
00416755  6689c3                 mov      bx, ax
00416758  89f0                   mov      eax, esi
0041675a  0511000000             add      eax, 0x11
0041675f  0fbfd0                 movsx    edx, ax
00416762  8b0424                 mov      eax, dword ptr [esp]
00416765  0503000000             add      eax, 3
0041676a  b901000000             mov      ecx, 1
0041676f  98                     cwde
00416770  e821500400             call     0x45b796 ; PasteOmbreCmp
00416775  8b0424                 mov      eax, dword ptr [esp]
00416778  8a4c240c               mov      cl, byte ptr [esp + 0xc]
0041677c  89f2                   mov      edx, esi
0041677e  050b000000             add      eax, 0xb
00416783  83ea11                 sub      edx, 0x11
00416786  84c9                   test     cl, cl
00416788  7414                   je       0x41679e
0041678a  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
00416790  01df                   add      edi, ebx
00416792  30ff                   xor      bh, bh
00416794  8a1f                   mov      bl, byte ptr [edi]
00416796  81c329290000           add      ebx, 0x2929
0041679c  eb12                   jmp      0x4167b0 ;
0041679e  8b1dac7d5000           mov      ebx, dword ptr [0x507dac]
004167a4  01df                   add      edi, ebx
004167a6  30ff                   xor      bh, bh
004167a8  8a1f                   mov      bl, byte ptr [edi]
004167aa  81c385290000           add      ebx, 0x2985
004167b0  b901000000             mov      ecx, 1
004167b5  81e3ffff0000           and      ebx, 0xffff
004167bb  0fbfd2                 movsx    edx, dx
004167be  98                     cwde
004167bf  e8834a0400             call     0x45b247 ; PasteBobCmp
004167c4  31d2                   xor      edx, edx
004167c6  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004167cb  668b542408             mov      dx, word ptr [esp + 8]
004167d0  8a0402                 mov      al, byte ptr [edx + eax]
004167d3  30e4                   xor      ah, ah
004167d5  31db                   xor      ebx, ebx
004167d7  0545290000             add      eax, 0x2945
004167dc  b901000000             mov      ecx, 1
004167e1  6689c3                 mov      bx, ax
004167e4  8b0424                 mov      eax, dword ptr [esp]
004167e7  83c618                 add      esi, 0x18
004167ea  0518000000             add      eax, 0x18
004167ef  e9affcffff             jmp      0x4164a3 ;
004167f4  8b0c24                 mov      ecx, dword ptr [esp]
004167f7  8a74240c               mov      dh, byte ptr [esp + 0xc]
004167fb  89f0                   mov      eax, esi
004167fd  83e905                 sub      ecx, 5
00416800  83e824                 sub      eax, 0x24
00416803  84f6                   test     dh, dh
00416805  7417                   je       0x41681e
00416807  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
0041680d  01d5                   add      ebp, edx
0041680f  30f6                   xor      dh, dh
00416811  8a5500                 mov      dl, byte ptr [ebp]
00416814  31db                   xor      ebx, ebx
00416816  81c22d290000           add      edx, 0x292d
0041681c  eb15                   jmp      0x416833 ;
0041681e  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00416824  01d5                   add      ebp, edx
00416826  30f6                   xor      dh, dh
00416828  8a5500                 mov      dl, byte ptr [ebp]
0041682b  31db                   xor      ebx, ebx
0041682d  81c289290000           add      edx, 0x2989
00416833  6689d3                 mov      bx, dx
00416836  0fbfd0                 movsx    edx, ax
00416839  0fbfc1                 movsx    eax, cx
0041683c  b901000000             mov      ecx, 1
00416841  e8014a0400             call     0x45b247 ; PasteBobCmp
00416846  31c0                   xor      eax, eax
00416848  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
0041684e  668b442408             mov      ax, word ptr [esp + 8]
00416853  8a0402                 mov      al, byte ptr [edx + eax]
00416856  30e4                   xor      ah, ah
00416858  31db                   xor      ebx, ebx
0041685a  0549290000             add      eax, 0x2949
0041685f  e92cfcffff             jmp      0x416490 ;
