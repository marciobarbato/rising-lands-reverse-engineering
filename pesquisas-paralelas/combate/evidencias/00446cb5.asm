; EnginAPortee; intervalo [0x00446cb5, 0x00446eed)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00446cb5  51                       push     ecx
00446cb6  56                       push     esi
00446cb7  57                       push     edi
00446cb8  55                       push     ebp
00446cb9  83ec10                   sub      esp, 0x10
00446cbc  50                       push     eax
00446cbd  88542410                 mov      byte ptr [esp + 0x10], dl
00446cc1  89de                     mov      esi, ebx
00446cc3  31c9                     xor      ecx, ecx
00446cc5  6689c1                   mov      cx, ax
00446cc8  89c8                     mov      eax, ecx
00446cca  c1e004                   shl      eax, 4
00446ccd  01c8                     add      eax, ecx
00446ccf  c1e002                   shl      eax, 2
00446cd2  01c8                     add      eax, ecx
00446cd4  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
00446cda  c1e002                   shl      eax, 2
00446cdd  01c1                     add      ecx, eax
00446cdf  30e4                     xor      ah, ah
00446ce1  ba04000000               mov      edx, 4
00446ce6  8a81b0000000             mov      al, byte ptr [ecx + 0xb0]
00446cec  31db                     xor      ebx, ebx
00446cee  89442404                 mov      dword ptr [esp + 4], eax
00446cf2  31c0                     xor      eax, eax
00446cf4  8a5901                   mov      bl, byte ptr [ecx + 1]
00446cf7  8a01                     mov      al, byte ptr [ecx]
00446cf9  668b7908                 mov      di, word ptr [ecx + 8]
00446cfd  e8be1ffeff               call     0x428cc0
00446d02  8b542404                 mov      edx, dword ptr [esp + 4]
00446d06  01c2                     add      edx, eax
00446d08  31c0                     xor      eax, eax
00446d0a  8a442410                 mov      al, byte ptr [esp + 0x10]
00446d0e  8954240c                 mov      dword ptr [esp + 0xc], edx
00446d12  83f801                   cmp      eax, 1
00446d15  0f8575000000             jne      0x446d90
00446d1b  31d2                     xor      edx, edx
00446d1d  6689f2                   mov      dx, si
00446d20  89d0                     mov      eax, edx
00446d22  c1e004                   shl      eax, 4
00446d25  01d0                     add      eax, edx
00446d27  c1e002                   shl      eax, 2
00446d2a  01d0                     add      eax, edx
00446d2c  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00446d32  668b54827c               mov      dx, word ptr [edx + eax*4 + 0x7c]
00446d37  31c0                     xor      eax, eax
00446d39  8a4102                   mov      al, byte ptr [ecx + 2]
00446d3c  89542408                 mov      dword ptr [esp + 8], edx
00446d40  83f818                   cmp      eax, 0x18
00446d43  0f8401010000             je       0x446e4a
00446d49  31c0                     xor      eax, eax
00446d4b  8a4101                   mov      al, byte ptr [ecx + 1]
00446d4e  83f810                   cmp      eax, 0x10
00446d51  7505                     jne      0x446d58
00446d53  6639d7                   cmp      di, dx
00446d56  eb68                     jmp      0x446dc0
00446d58  80797800                 cmp      byte ptr [ecx + 0x78], 0
00446d5c  7413                     je       0x446d71
00446d5e  83f815                   cmp      eax, 0x15
00446d61  740e                     je       0x446d71
00446d63  83f801                   cmp      eax, 1
00446d66  7409                     je       0x446d71
00446d68  83f804                   cmp      eax, 4
00446d6b  0f8501010000             jne      0x446e72
00446d71  31c0                     xor      eax, eax
00446d73  31d2                     xor      edx, edx
00446d75  668b0424                 mov      ax, word ptr [esp]
00446d79  6689f2                   mov      dx, si
00446d7c  e863fbffff               call     0x4468e4
00446d81  84c0                     test     al, al
00446d83  0f84e9000000             je       0x446e72
00446d89  b001                     mov      al, 1
00446d8b  e904a2ffff               jmp      0x440f94
00446d90  83f803                   cmp      eax, 3
00446d93  755c                     jne      0x446df1
00446d95  31c0                     xor      eax, eax
00446d97  6689f0                   mov      ax, si
00446d9a  e84341fdff               call     0x41aee2
00446d9f  89c2                     mov      edx, eax
00446da1  89442408                 mov      dword ptr [esp + 8], eax
00446da5  31c0                     xor      eax, eax
00446da7  8a4102                   mov      al, byte ptr [ecx + 2]
00446daa  83f818                   cmp      eax, 0x18
00446dad  0f8497000000             je       0x446e4a
00446db3  31c0                     xor      eax, eax
00446db5  8a4101                   mov      al, byte ptr [ecx + 1]
00446db8  83f810                   cmp      eax, 0x10
00446dbb  750a                     jne      0x446dc7
00446dbd  6639d7                   cmp      di, dx
00446dc0  74c7                     je       0x446d89
00446dc2  e91f010000               jmp      0x446ee6
00446dc7  80797800                 cmp      byte ptr [ecx + 0x78], 0
00446dcb  7413                     je       0x446de0
00446dcd  83f815                   cmp      eax, 0x15
00446dd0  740e                     je       0x446de0
00446dd2  83f801                   cmp      eax, 1
00446dd5  7409                     je       0x446de0
00446dd7  83f804                   cmp      eax, 4
00446dda  0f8592000000             jne      0x446e72
00446de0  31d2                     xor      edx, edx
00446de2  31c0                     xor      eax, eax
00446de4  6689fa                   mov      dx, di
00446de7  6689f0                   mov      ax, si
00446dea  e830cafdff               call     0x42381f
00446def  eb90                     jmp      0x446d81
00446df1  83f805                   cmp      eax, 5
00446df4  0f8578000000             jne      0x446e72
00446dfa  668b81b8000000           mov      ax, word ptr [ecx + 0xb8]
00446e01  89442408                 mov      dword ptr [esp + 8], eax
00446e05  31c0                     xor      eax, eax
00446e07  8a4102                   mov      al, byte ptr [ecx + 2]
00446e0a  83f818                   cmp      eax, 0x18
00446e0d  743b                     je       0x446e4a
00446e0f  31c0                     xor      eax, eax
00446e11  8a4101                   mov      al, byte ptr [ecx + 1]
00446e14  83f810                   cmp      eax, 0x10
00446e17  7507                     jne      0x446e20
00446e19  663b7c2408               cmp      di, word ptr [esp + 8]
00446e1e  eba0                     jmp      0x446dc0
00446e20  80797800                 cmp      byte ptr [ecx + 0x78], 0
00446e24  740f                     je       0x446e35
00446e26  83f815                   cmp      eax, 0x15
00446e29  740a                     je       0x446e35
00446e2b  83f801                   cmp      eax, 1
00446e2e  7405                     je       0x446e35
00446e30  83f804                   cmp      eax, 4
00446e33  753d                     jne      0x446e72
00446e35  31c0                     xor      eax, eax
00446e37  31d2                     xor      edx, edx
00446e39  668b0424                 mov      ax, word ptr [esp]
00446e3d  6689f2                   mov      dx, si
00446e40  e8c7fcffff               call     0x446b0c
00446e45  e937ffffff               jmp      0x446d81
00446e4a  31c0                     xor      eax, eax
00446e4c  ba04000000               mov      edx, 4
00446e51  8a81f4000000             mov      al, byte ptr [ecx + 0xf4]
00446e57  31db                     xor      ebx, ebx
00446e59  e86bd80200               call     0x4746c9
00446e5e  89c6                     mov      esi, eax
00446e60  31c0                     xor      eax, eax
00446e62  8a5901                   mov      bl, byte ptr [ecx + 1]
00446e65  8a01                     mov      al, byte ptr [ecx]
00446e67  e8541efeff               call     0x428cc0
00446e6c  01c6                     add      esi, eax
00446e6e  8974240c                 mov      dword ptr [esp + 0xc], esi
00446e72  31c9                     xor      ecx, ecx
00446e74  668b4c2408               mov      cx, word ptr [esp + 8]
00446e79  89ca                     mov      edx, ecx
00446e7b  89c8                     mov      eax, ecx
00446e7d  c1fa1f                   sar      edx, 0x1f
00446e80  c1e208                   shl      edx, 8
00446e83  1bc2                     sbb      eax, edx
00446e85  c1f808                   sar      eax, 8
00446e88  31db                     xor      ebx, ebx
00446e8a  be00010000               mov      esi, 0x100
00446e8f  6689c3                   mov      bx, ax
00446e92  89ca                     mov      edx, ecx
00446e94  89c8                     mov      eax, ecx
00446e96  c1fa1f                   sar      edx, 0x1f
00446e99  f7fe                     idiv     esi
00446e9b  31c9                     xor      ecx, ecx
00446e9d  31f6                     xor      esi, esi
00446e9f  6689f9                   mov      cx, di
00446ea2  6689d6                   mov      si, dx
00446ea5  89ca                     mov      edx, ecx
00446ea7  89c8                     mov      eax, ecx
00446ea9  c1fa1f                   sar      edx, 0x1f
00446eac  c1e208                   shl      edx, 8
00446eaf  1bc2                     sbb      eax, edx
00446eb1  c1f808                   sar      eax, 8
00446eb4  31ff                     xor      edi, edi
00446eb6  bd00010000               mov      ebp, 0x100
00446ebb  6689c7                   mov      di, ax
00446ebe  89ca                     mov      edx, ecx
00446ec0  89c8                     mov      eax, ecx
00446ec2  c1fa1f                   sar      edx, 0x1f
00446ec5  f7fd                     idiv     ebp
00446ec7  89d9                     mov      ecx, ebx
00446ec9  31c0                     xor      eax, eax
00446ecb  89f3                     mov      ebx, esi
00446ecd  6689d0                   mov      ax, dx
00446ed0  89fa                     mov      edx, edi
00446ed2  e87e260300               call     0x479555
00446ed7  31d2                     xor      edx, edx
00446ed9  668b54240c               mov      dx, word ptr [esp + 0xc]
00446ede  39d0                     cmp      eax, edx
00446ee0  0f86a3feffff             jbe      0x446d89
00446ee6  30c0                     xor      al, al
00446ee8  e9a7a0ffff               jmp      0x440f94
