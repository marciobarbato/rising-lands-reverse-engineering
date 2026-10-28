; BatimentNextEtape_prologo; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004268d4  53                       push ebx
004268d5  51                       push ecx
004268d6  52                       push edx
004268d7  56                       push esi
004268d8  57                       push edi
004268d9  55                       push ebp
004268da  89e5                     mov ebp, esp
004268dc  83ec34                   sub esp, 0x34
004268df  89c7                     mov edi, eax
004268e1  31d2                     xor edx, edx
004268e3  6689c2                   mov dx, ax
004268e6  89d0                     mov eax, edx
004268e8  c1e004                   shl eax, 4
004268eb  01d0                     add eax, edx
004268ed  c1e002                   shl eax, 2
004268f0  01d0                     add eax, edx
004268f2  bec8a04900               mov esi, 0x49a0c8
004268f7  c1e002                   shl eax, 2
004268fa  01c6                     add esi, eax
004268fc  8a4608                   mov al, byte ptr [esi + 8]
004268ff  88c4                     mov ah, al
00426901  fecc                     dec ah
00426903  80fc14                   cmp ah, 0x14
00426906  0f87b4180000             ja 0x4281c0
0042690c  31db                     xor ebx, ebx
0042690e  88e3                     mov bl, ah
00426910  2eff249d80684200         jmp dword ptr cs:[ebx*4 + 0x426880]
