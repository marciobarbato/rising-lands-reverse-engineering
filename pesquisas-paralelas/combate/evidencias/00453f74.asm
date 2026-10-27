; EnginTrouveCible; intervalo [0x00453f74, 0x00454235)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00453f74  53                       push     ebx
00453f75  51                       push     ecx
00453f76  52                       push     edx
00453f77  56                       push     esi
00453f78  57                       push     edi
00453f79  55                       push     ebp
00453f7a  83ec38                   sub      esp, 0x38
00453f7d  89c2                     mov      edx, eax
00453f7f  31db                     xor      ebx, ebx
00453f81  6689c3                   mov      bx, ax
00453f84  89d8                     mov      eax, ebx
00453f86  c1e004                   shl      eax, 4
00453f89  01d8                     add      eax, ebx
00453f8b  c1e002                   shl      eax, 2
00453f8e  01d8                     add      eax, ebx
00453f90  8b35a0194e00             mov      esi, dword ptr [0x4e19a0]
00453f96  c1e002                   shl      eax, 2
00453f99  01c6                     add      esi, eax
00453f9b  8a4601                   mov      al, byte ptr [esi + 1]
00453f9e  88442434                 mov      byte ptr [esp + 0x34], al
00453fa2  3c02                     cmp      al, 2
00453fa4  720a                     jb       0x453fb0
00453fa6  7604                     jbe      0x453fac
00453fa8  3c08                     cmp      al, 8
00453faa  7504                     jne      0x453fb0
00453fac  b001                     mov      al, 1
00453fae  eb02                     jmp      0x453fb2
00453fb0  30c0                     xor      al, al
00453fb2  84c0                     test     al, al
00453fb4  741f                     je       0x453fd5
00453fb6  31c0                     xor      eax, eax
00453fb8  6689d0                   mov      ax, dx
00453fbb  31d2                     xor      edx, edx
00453fbd  e8e0fdffff               call     0x453da2
00453fc2  6689c2                   mov      dx, ax
00453fc5  8944240c                 mov      dword ptr [esp + 0xc], eax
00453fc9  81faffff0000             cmp      edx, 0xffff
00453fcf  0f8558020000             jne      0x45422d
00453fd5  31db                     xor      ebx, ebx
00453fd7  668b5e08                 mov      bx, word ptr [esi + 8]
00453fdb  b900010000               mov      ecx, 0x100
00453fe0  89da                     mov      edx, ebx
00453fe2  89d8                     mov      eax, ebx
00453fe4  c1fa1f                   sar      edx, 0x1f
00453fe7  f7f9                     idiv     ecx
00453fe9  89542410                 mov      dword ptr [esp + 0x10], edx
00453fed  89da                     mov      edx, ebx
00453fef  89d8                     mov      eax, ebx
00453ff1  c1fa1f                   sar      edx, 0x1f
00453ff4  f7f9                     idiv     ecx
00453ff6  89442408                 mov      dword ptr [esp + 8], eax
00453ffa  8944242c                 mov      dword ptr [esp + 0x2c], eax
00453ffe  30e4                     xor      ah, ah
00454000  8a86bb000000             mov      al, byte ptr [esi + 0xbb]
00454006  89c2                     mov      edx, eax
00454008  01c2                     add      edx, eax
0045400a  42                       inc      edx
0045400b  31db                     xor      ebx, ebx
0045400d  891424                   mov      dword ptr [esp], edx
00454010  89542420                 mov      dword ptr [esp + 0x20], edx
00454014  31d2                     xor      edx, edx
00454016  668b5c2410               mov      bx, word ptr [esp + 0x10]
0045401b  88c2                     mov      dl, al
0045401d  39d3                     cmp      ebx, edx
0045401f  7e0a                     jle      0x45402b
00454021  89da                     mov      edx, ebx
00454023  29c2                     sub      edx, eax
00454025  89542414                 mov      dword ptr [esp + 0x14], edx
00454029  eb10                     jmp      0x45403b
0045402b  29d8                     sub      eax, ebx
0045402d  8b1c24                   mov      ebx, dword ptr [esp]
00454030  31c9                     xor      ecx, ecx
00454032  29c3                     sub      ebx, eax
00454034  894c2414                 mov      dword ptr [esp + 0x14], ecx
00454038  891c24                   mov      dword ptr [esp], ebx
0045403b  31d2                     xor      edx, edx
0045403d  31c0                     xor      eax, eax
0045403f  668b54242c               mov      dx, word ptr [esp + 0x2c]
00454044  8a86bb000000             mov      al, byte ptr [esi + 0xbb]
0045404a  39c2                     cmp      edx, eax
0045404c  7e0c                     jle      0x45405a
0045404e  89d1                     mov      ecx, edx
00454050  30e4                     xor      ah, ah
00454052  29c1                     sub      ecx, eax
00454054  894c242c                 mov      dword ptr [esp + 0x2c], ecx
00454058  eb14                     jmp      0x45406e
0045405a  30e4                     xor      ah, ah
0045405c  29d0                     sub      eax, edx
0045405e  8b542420                 mov      edx, dword ptr [esp + 0x20]
00454062  31db                     xor      ebx, ebx
00454064  29c2                     sub      edx, eax
00454066  895c242c                 mov      dword ptr [esp + 0x2c], ebx
0045406a  89542420                 mov      dword ptr [esp + 0x20], edx
0045406e  30e4                     xor      ah, ah
00454070  88642430                 mov      byte ptr [esp + 0x30], ah
00454074  8b44242c                 mov      eax, dword ptr [esp + 0x2c]
00454078  8b542414                 mov      edx, dword ptr [esp + 0x14]
0045407c  c1e008                   shl      eax, 8
0045407f  01c2                     add      edx, eax
00454081  8b44242c                 mov      eax, dword ptr [esp + 0x2c]
00454085  89542418                 mov      dword ptr [esp + 0x18], edx
00454089  8b1424                   mov      edx, dword ptr [esp]
0045408c  6689442404               mov      word ptr [esp + 4], ax
00454091  b800010000               mov      eax, 0x100
00454096  bfffff0000               mov      edi, 0xffff
0045409b  29d0                     sub      eax, edx
0045409d  897c2424                 mov      dword ptr [esp + 0x24], edi
004540a1  8944241c                 mov      dword ptr [esp + 0x1c], eax
004540a5  bdffff0000               mov      ebp, 0xffff
004540aa  eb18                     jmp      0x4540c4
004540ac  8b44241c                 mov      eax, dword ptr [esp + 0x1c]
004540b0  8b7c2418                 mov      edi, dword ptr [esp + 0x18]
004540b4  01c7                     add      edi, eax
004540b6  8b442404                 mov      eax, dword ptr [esp + 4]
004540ba  40                       inc      eax
004540bb  897c2418                 mov      dword ptr [esp + 0x18], edi
004540bf  6689442404               mov      word ptr [esp + 4], ax
004540c4  31c0                     xor      eax, eax
004540c6  31d2                     xor      edx, edx
004540c8  668b44242c               mov      ax, word ptr [esp + 0x2c]
004540cd  668b542420               mov      dx, word ptr [esp + 0x20]
004540d2  01c2                     add      edx, eax
004540d4  8b442402                 mov      eax, dword ptr [esp + 2]
004540d8  c1f810                   sar      eax, 0x10
004540db  39d0                     cmp      eax, edx
004540dd  0f8d38010000             jge      0x45421b
004540e3  3d00010000               cmp      eax, 0x100
004540e8  7dc2                     jge      0x4540ac
004540ea  8b7c2414                 mov      edi, dword ptr [esp + 0x14]
004540ee  e9ce000000               jmp      0x4541c1
004540f3  89ea                     mov      edx, ebp
004540f5  31c0                     xor      eax, eax
004540f7  6689d0                   mov      ax, dx
004540fa  89542428                 mov      dword ptr [esp + 0x28], edx
004540fe  3dffff0000               cmp      eax, 0xffff
00454103  0f84ae000000             je       0x4541b7
00454109  69d814010000             imul     ebx, eax, 0x114
0045410f  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00454114  8a0403                   mov      al, byte ptr [ebx + eax]
00454117  25ff000000               and      eax, 0xff
0045411c  3dc8000000               cmp      eax, 0xc8
00454121  0f8490000000             je       0x4541b7
00454127  31d2                     xor      edx, edx
00454129  8a16                     mov      dl, byte ptr [esi]
0045412b  e808970100               call     0x46d838
00454130  84c0                     test     al, al
00454132  0f857f000000             jne      0x4541b7
00454138  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
0045413d  8a440301                 mov      al, byte ptr [ebx + eax + 1]
00454141  25ff000000               and      eax, 0xff
00454146  83f811                   cmp      eax, 0x11
00454149  7405                     je       0x454150
0045414b  83f80a                   cmp      eax, 0xa
0045414e  7504                     jne      0x454154
00454150  30c0                     xor      al, al
00454152  eb17                     jmp      0x45416b
00454154  83f810                   cmp      eax, 0x10
00454157  7510                     jne      0x454169
00454159  8a742434                 mov      dh, byte ptr [esp + 0x34]
0045415d  80fe02                   cmp      dh, 2
00454160  72ee                     jb       0x454150
00454162  7605                     jbe      0x454169
00454164  80fe08                   cmp      dh, 8
00454167  75e7                     jne      0x454150
00454169  b001                     mov      al, 1
0045416b  84c0                     test     al, al
0045416d  7448                     je       0x4541b7
0045416f  31c9                     xor      ecx, ecx
00454171  31db                     xor      ebx, ebx
00454173  31d2                     xor      edx, edx
00454175  31c0                     xor      eax, eax
00454177  668b4c2404               mov      cx, word ptr [esp + 4]
0045417c  668b542408               mov      dx, word ptr [esp + 8]
00454181  668b442410               mov      ax, word ptr [esp + 0x10]
00454186  6689fb                   mov      bx, di
00454189  e8c7530200               call     0x479555
0045418e  30f6                     xor      dh, dh
00454190  8a96bb000000             mov      dl, byte ptr [esi + 0xbb]
00454196  0fafd2                   imul     edx, edx
00454199  6639d0                   cmp      ax, dx
0045419c  7719                     ja       0x4541b7
0045419e  663b442424               cmp      ax, word ptr [esp + 0x24]
004541a3  7312                     jae      0x4541b7
004541a5  b101                     mov      cl, 1
004541a7  89442424                 mov      dword ptr [esp + 0x24], eax
004541ab  8b442428                 mov      eax, dword ptr [esp + 0x28]
004541af  884c2430                 mov      byte ptr [esp + 0x30], cl
004541b3  8944240c                 mov      dword ptr [esp + 0xc], eax
004541b7  8b4c2418                 mov      ecx, dword ptr [esp + 0x18]
004541bb  41                       inc      ecx
004541bc  47                       inc      edi
004541bd  894c2418                 mov      dword ptr [esp + 0x18], ecx
004541c1  31d2                     xor      edx, edx
004541c3  31c0                     xor      eax, eax
004541c5  668b542414               mov      dx, word ptr [esp + 0x14]
004541ca  668b0424                 mov      ax, word ptr [esp]
004541ce  01c2                     add      edx, eax
004541d0  0fbfc7                   movsx    eax, di
004541d3  39d0                     cmp      eax, edx
004541d5  0f8dd1feffff             jge      0x4540ac
004541db  3d00010000               cmp      eax, 0x100
004541e0  7dd5                     jge      0x4541b7
004541e2  31c0                     xor      eax, eax
004541e4  668b442418               mov      ax, word ptr [esp + 0x18]
004541e9  8b15380f4e00             mov      edx, dword ptr [0x4e0f38]
004541ef  01c0                     add      eax, eax
004541f1  01d0                     add      eax, edx
004541f3  668b10                   mov      dx, word ptr [eax]
004541f6  30d2                     xor      dl, dl
004541f8  80e6c0                   and      dh, 0xc0
004541fb  6681fa0040               cmp      dx, 0x4000
00454200  0f85edfeffff             jne      0x4540f3
00454206  668b00                   mov      ax, word ptr [eax]
00454209  31d2                     xor      edx, edx
0045420b  25f83f0000               and      eax, 0x3ff8
00454210  6689c2                   mov      dx, ax
00454213  c1fa03                   sar      edx, 3
00454216  e9dafeffff               jmp      0x4540f5
0045421b  807c243000               cmp      byte ptr [esp + 0x30], 0
00454220  7406                     je       0x454228
00454222  8b44240c                 mov      eax, dword ptr [esp + 0xc]
00454226  eb05                     jmp      0x45422d
00454228  b8ffff0000               mov      eax, 0xffff
0045422d  83c438                   add      esp, 0x38
00454230  e968b0ffff               jmp      0x44f29d
