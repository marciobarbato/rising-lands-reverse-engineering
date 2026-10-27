; EnginTrouveCibleScan; intervalo [0x00453da2, 0x00453f74)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00453da2  53                       push     ebx
00453da3  51                       push     ecx
00453da4  52                       push     edx
00453da5  56                       push     esi
00453da6  57                       push     edi
00453da7  55                       push     ebp
00453da8  83ec14                   sub      esp, 0x14
00453dab  31d2                     xor      edx, edx
00453dad  6689c2                   mov      dx, ax
00453db0  89d0                     mov      eax, edx
00453db2  c1e004                   shl      eax, 4
00453db5  01d0                     add      eax, edx
00453db7  c1e002                   shl      eax, 2
00453dba  01d0                     add      eax, edx
00453dbc  8b3da0194e00             mov      edi, dword ptr [0x4e19a0]
00453dc2  c1e002                   shl      eax, 2
00453dc5  01c7                     add      edi, eax
00453dc7  b900010000               mov      ecx, 0x100
00453dcc  31db                     xor      ebx, ebx
00453dce  8a07                     mov      al, byte ptr [edi]
00453dd0  668b5f08                 mov      bx, word ptr [edi + 8]
00453dd4  88442410                 mov      byte ptr [esp + 0x10], al
00453dd8  89da                     mov      edx, ebx
00453dda  8a4701                   mov      al, byte ptr [edi + 1]
00453ddd  c1fa1f                   sar      edx, 0x1f
00453de0  8844240c                 mov      byte ptr [esp + 0xc], al
00453de4  89d8                     mov      eax, ebx
00453de6  f7f9                     idiv     ecx
00453de8  891424                   mov      dword ptr [esp], edx
00453deb  89da                     mov      edx, ebx
00453ded  89d8                     mov      eax, ebx
00453def  c1fa1f                   sar      edx, 0x1f
00453df2  f7f9                     idiv     ecx
00453df4  31f6                     xor      esi, esi
00453df6  89442408                 mov      dword ptr [esp + 8], eax
00453dfa  eb01                     jmp      0x453dfd
00453dfc  46                       inc      esi
00453dfd  0fbfc6                   movsx    eax, si
00453e00  3d20030000               cmp      eax, 0x320
00453e05  0f8d5f010000             jge      0x453f6a
00453e0b  31c0                     xor      eax, eax
00453e0d  6689f0                   mov      ax, si
00453e10  69c014010000             imul     eax, eax, 0x114
00453e16  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00453e1c  8a440202                 mov      al, byte ptr [edx + eax + 2]
00453e20  25ff000000               and      eax, 0xff
00453e25  7409                     je       0x453e30
00453e27  83f804                   cmp      eax, 4
00453e2a  7404                     je       0x453e30
00453e2c  b001                     mov      al, 1
00453e2e  eb02                     jmp      0x453e32
00453e30  30c0                     xor      al, al
00453e32  84c0                     test     al, al
00453e34  74c6                     je       0x453dfc
00453e36  31db                     xor      ebx, ebx
00453e38  6689f3                   mov      bx, si
00453e3b  69db14010000             imul     ebx, ebx, 0x114
00453e41  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00453e46  01c3                     add      ebx, eax
00453e48  8a4372                   mov      al, byte ptr [ebx + 0x72]
00453e4b  84c0                     test     al, al
00453e4d  74ad                     je       0x453dfc
00453e4f  8a13                     mov      dl, byte ptr [ebx]
00453e51  8a4c2410                 mov      cl, byte ptr [esp + 0x10]
00453e55  88d3                     mov      bl, dl
00453e57  38ca                     cmp      dl, cl
00453e59  7412                     je       0x453e6d
00453e5b  31c0                     xor      eax, eax
00453e5d  88c8                     mov      al, cl
00453e5f  83f804                   cmp      eax, 4
00453e62  7431                     je       0x453e95
00453e64  31c0                     xor      eax, eax
00453e66  88d0                     mov      al, dl
00453e68  83f804                   cmp      eax, 4
00453e6b  7428                     je       0x453e95
00453e6d  31c0                     xor      eax, eax
00453e6f  88c8                     mov      al, cl
00453e71  3dc8000000               cmp      eax, 0xc8
00453e76  740c                     je       0x453e84
00453e78  31d2                     xor      edx, edx
00453e7a  88da                     mov      dl, bl
00453e7c  81fac8000000             cmp      edx, 0xc8
00453e82  7504                     jne      0x453e88
00453e84  30db                     xor      bl, bl
00453e86  eb0f                     jmp      0x453e97
00453e88  38cb                     cmp      bl, cl
00453e8a  74f8                     je       0x453e84
00453e8c  e8a7990100               call     0x46d838
00453e91  84c0                     test     al, al
00453e93  75ef                     jne      0x453e84
00453e95  b301                     mov      bl, 1
00453e97  84db                     test     bl, bl
00453e99  0f845dffffff             je       0x453dfc
00453e9f  31c0                     xor      eax, eax
00453ea1  6689f0                   mov      ax, si
00453ea4  69c014010000             imul     eax, eax, 0x114
00453eaa  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00453eb0  01c3                     add      ebx, eax
00453eb2  8a03                     mov      al, byte ptr [ebx]
00453eb4  25ff000000               and      eax, 0xff
00453eb9  3dc8000000               cmp      eax, 0xc8
00453ebe  0f8438ffffff             je       0x453dfc
00453ec4  8a4301                   mov      al, byte ptr [ebx + 1]
00453ec7  31d2                     xor      edx, edx
00453ec9  88c2                     mov      dl, al
00453ecb  83fa11                   cmp      edx, 0x11
00453ece  7405                     je       0x453ed5
00453ed0  83fa0a                   cmp      edx, 0xa
00453ed3  7504                     jne      0x453ed9
00453ed5  30db                     xor      bl, bl
00453ed7  eb17                     jmp      0x453ef0
00453ed9  83fa10                   cmp      edx, 0x10
00453edc  7510                     jne      0x453eee
00453ede  8a54240c                 mov      dl, byte ptr [esp + 0xc]
00453ee2  80fa02                   cmp      dl, 2
00453ee5  72ee                     jb       0x453ed5
00453ee7  7605                     jbe      0x453eee
00453ee9  80fa08                   cmp      dl, 8
00453eec  75e7                     jne      0x453ed5
00453eee  b301                     mov      bl, 1
00453ef0  84db                     test     bl, bl
00453ef2  0f8404ffffff             je       0x453dfc
00453ef8  0fbfc6                   movsx    eax, si
00453efb  69c014010000             imul     eax, eax, 0x114
00453f01  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00453f07  668b5c0308               mov      bx, word ptr [ebx + eax + 8]
00453f0c  81e3ffff0000             and      ebx, 0xffff
00453f12  b900010000               mov      ecx, 0x100
00453f17  89da                     mov      edx, ebx
00453f19  89d8                     mov      eax, ebx
00453f1b  c1fa1f                   sar      edx, 0x1f
00453f1e  f7f9                     idiv     ecx
00453f20  89542404                 mov      dword ptr [esp + 4], edx
00453f24  89da                     mov      edx, ebx
00453f26  89d8                     mov      eax, ebx
00453f28  c1fa1f                   sar      edx, 0x1f
00453f2b  f7f9                     idiv     ecx
00453f2d  89c2                     mov      edx, eax
00453f2f  30e4                     xor      ah, ah
00453f31  8a87bb000000             mov      al, byte ptr [edi + 0xbb]
00453f37  0fafc0                   imul     eax, eax
00453f3a  31db                     xor      ebx, ebx
00453f3c  31c9                     xor      ecx, ecx
00453f3e  668b5c2404               mov      bx, word ptr [esp + 4]
00453f43  6689d1                   mov      cx, dx
00453f46  31d2                     xor      edx, edx
00453f48  0fb7e8                   movzx    ebp, ax
00453f4b  31c0                     xor      eax, eax
00453f4d  668b542408               mov      dx, word ptr [esp + 8]
00453f52  668b0424                 mov      ax, word ptr [esp]
00453f56  e8fa550200               call     0x479555
00453f5b  39e8                     cmp      eax, ebp
00453f5d  0f8799feffff             ja       0x453dfc
00453f63  89f0                     mov      eax, esi
00453f65  e930b3ffff               jmp      0x44f29a
00453f6a  b8ffff0000               mov      eax, 0xffff
00453f6f  e926b3ffff               jmp      0x44f29a
