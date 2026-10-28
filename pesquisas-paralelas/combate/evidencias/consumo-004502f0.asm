; EnginInfligeDegat; [0x004502f0, 0x00450856)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004502f0  56                       push     esi
004502f1  57                       push     edi
004502f2  55                       push     ebp
004502f3  83ec2c                   sub      esp, 0x2c
004502f6  89c7                     mov      edi, eax
004502f8  8854241c                 mov      byte ptr [esp + 0x1c], dl
004502fc  895c2414                 mov      dword ptr [esp + 0x14], ebx
00450300  88cb                     mov      bl, cl
00450302  31c0                     xor      eax, eax
00450304  6689f8                   mov      ax, di
00450307  89442408                 mov      dword ptr [esp + 8], eax
0045030b  89c2                     mov      edx, eax
0045030d  c1e004                   shl      eax, 4
00450310  01d0                     add      eax, edx
00450312  c1e002                   shl      eax, 2
00450315  8b2da0194e00             mov      ebp, dword ptr [0x4e19a0]
0045031b  01d0                     add      eax, edx
0045031d  31c9                     xor      ecx, ecx
0045031f  c1e002                   shl      eax, 2
00450322  668b4c2414               mov      cx, word ptr [esp + 0x14]
00450327  8d3428                   lea      esi, [eax + ebp]
0045032a  89c8                     mov      eax, ecx
0045032c  c1e004                   shl      eax, 4
0045032f  01c8                     add      eax, ecx
00450331  c1e002                   shl      eax, 2
00450334  01c8                     add      eax, ecx
00450336  c1e002                   shl      eax, 2
00450339  89442404                 mov      dword ptr [esp + 4], eax
0045033d  01c5                     add      ebp, eax
0045033f  668b467c                 mov      ax, word ptr [esi + 0x7c]
00450343  89442410                 mov      dword ptr [esp + 0x10], eax
00450347  8a64241c                 mov      ah, byte ptr [esp + 0x1c]
0045034b  80fc04                   cmp      ah, 4
0045034e  0f8234020000             jb       0x450588
00450354  0f866c010000             jbe      0x4504c6
0045035a  80fc08                   cmp      ah, 8
0045035d  0f8239020000             jb       0x45059c
00450363  0f860c010000             jbe      0x450475
00450369  80fc09                   cmp      ah, 9
0045036c  0f8422010000             je       0x450494
00450372  e925020000               jmp      0x45059c
00450377  8a4601                   mov      al, byte ptr [esi + 1]
0045037a  31db                     xor      ebx, ebx
0045037c  88c3                     mov      bl, al
0045037e  89c8                     mov      eax, ecx
00450380  e86fa1fcff               call     0x41a4f4
00450385  ba01000000               mov      edx, 1
0045038a  25ff000000               and      eax, 0xff
0045038f  e8f687fcff               call     0x418b8a
00450394  ba4c000000               mov      edx, 0x4c
00450399  88442420                 mov      byte ptr [esp + 0x20], al
0045039d  89c8                     mov      eax, ecx
0045039f  89cb                     mov      ebx, ecx
004503a1  e8e69cfcff               call     0x41a08c
004503a6  88442428                 mov      byte ptr [esp + 0x28], al
004503aa  8b442408                 mov      eax, dword ptr [esp + 8]
004503ae  e815260300               call     0x4829c8
004503b3  e9e4010000               jmp      0x45059c
004503b8  8a4601                   mov      al, byte ptr [esi + 1]
004503bb  31db                     xor      ebx, ebx
004503bd  88442424                 mov      byte ptr [esp + 0x24], al
004503c1  8a4501                   mov      al, byte ptr [ebp + 1]
004503c4  88c3                     mov      bl, al
004503c6  89d8                     mov      eax, ebx
004503c8  8b159c194e00             mov      edx, dword ptr [0x4e199c]
004503ce  c1e002                   shl      eax, 2
004503d1  01d0                     add      eax, edx
004503d3  31d2                     xor      edx, edx
004503d5  8b00                     mov      eax, dword ptr [eax]
004503d7  8a542424                 mov      dl, byte ptr [esp + 0x24]
004503db  8a0402                   mov      al, byte ptr [edx + eax]
004503de  8aa5f7000000             mov      ah, byte ptr [ebp + 0xf7]
004503e4  00c4                     add      ah, al
004503e6  88642420                 mov      byte ptr [esp + 0x20], ah
004503ea  31c0                     xor      eax, eax
004503ec  ba05000000               mov      edx, 5
004503f1  8a4500                   mov      al, byte ptr [ebp]
004503f4  e8c788fdff               call     0x428cc0
004503f9  8a742420                 mov      dh, byte ptr [esp + 0x20]
004503fd  8b4c2404                 mov      ecx, dword ptr [esp + 4]
00450401  00c6                     add      dh, al
00450403  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450408  01c8                     add      eax, ecx
0045040a  31db                     xor      ebx, ebx
0045040c  88742420                 mov      byte ptr [esp + 0x20], dh
00450410  668b507c                 mov      dx, word ptr [eax + 0x7c]
00450414  6689d3                   mov      bx, dx
00450417  8a00                     mov      al, byte ptr [eax]
00450419  31d2                     xor      edx, edx
0045041b  b90a000000               mov      ecx, 0xa
00450420  88c2                     mov      dl, al
00450422  b802000000               mov      eax, 2
00450427  e8b8fcffff               call     0x4500e4
0045042c  84c0                     test     al, al
0045042e  740f                     je       0x45043f
00450430  8a5c2420                 mov      bl, byte ptr [esp + 0x20]
00450434  a0ac654900               mov      al, byte ptr [0x4965ac]
00450439  00c3                     add      bl, al
0045043b  885c2420                 mov      byte ptr [esp + 0x20], bl
0045043f  ba48000000               mov      edx, 0x48
00450444  31c9                     xor      ecx, ecx
00450446  31c0                     xor      eax, eax
00450448  668b4c2414               mov      cx, word ptr [esp + 0x14]
0045044d  6689f8                   mov      ax, di
00450450  89cb                     mov      ebx, ecx
00450452  e871250300               call     0x4829c8
00450457  89c8                     mov      eax, ecx
00450459  c1e004                   shl      eax, 4
0045045c  01c8                     add      eax, ecx
0045045e  c1e002                   shl      eax, 2
00450461  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00450467  01c8                     add      eax, ecx
00450469  8a0482                   mov      al, byte ptr [edx + eax*4]
0045046c  88442428                 mov      byte ptr [esp + 0x28], al
00450470  e927010000               jmp      0x45059c
00450475  a19c194e00               mov      eax, dword ptr [0x4e199c]
0045047a  8a5601                   mov      dl, byte ptr [esi + 1]
0045047d  83c068                   add      eax, 0x68
00450480  81e2ff000000             and      edx, 0xff
00450486  8b00                     mov      eax, dword ptr [eax]
00450488  8a0402                   mov      al, byte ptr [edx + eax]
0045048b  88442420                 mov      byte ptr [esp + 0x20], al
0045048f  e908010000               jmp      0x45059c
00450494  668b869a000000           mov      ax, word ptr [esi + 0x9a]
0045049b  31d2                     xor      edx, edx
0045049d  6689c2                   mov      dx, ax
004504a0  89d0                     mov      eax, edx
004504a2  c1fa1f                   sar      edx, 0x1f
004504a5  2bc2                     sub      eax, edx
004504a7  d1f8                     sar      eax, 1
004504a9  88442420                 mov      byte ptr [esp + 0x20], al
004504ad  8b44241d                 mov      eax, dword ptr [esp + 0x1d]
004504b1  c1f818                   sar      eax, 0x18
004504b4  85c0                     test     eax, eax
004504b6  0f85e0000000             jne      0x45059c
004504bc  c644242001               mov      byte ptr [esp + 0x20], 1
004504c1  e9d6000000               jmp      0x45059c
004504c6  31c0                     xor      eax, eax
004504c8  88d8                     mov      al, bl
004504ca  83f81d                   cmp      eax, 0x1d
004504cd  750b                     jne      0x4504da
004504cf  a06c714900               mov      al, byte ptr [0x49716c]
004504d4  88442420                 mov      byte ptr [esp + 0x20], al
004504d8  eb24                     jmp      0x4504fe
004504da  83f81e                   cmp      eax, 0x1e
004504dd  751f                     jne      0x4504fe
004504df  a06e714900               mov      al, byte ptr [0x49716e]
004504e4  ebee                     jmp      0x4504d4
004504e6  66c7010100               mov      word ptr [ecx], 1
004504eb  66c7020100               mov      word ptr [edx], 1
004504f0  eb48                     jmp      0x45053a
004504f2  66c7010200               mov      word ptr [ecx], 2
004504f7  66c7020200               mov      word ptr [edx], 2
004504fc  eb3c                     jmp      0x45053a
004504fe  31c0                     xor      eax, eax
00450500  6689f8                   mov      ax, di
00450503  890424                   mov      dword ptr [esp], eax
00450506  8b1c24                   mov      ebx, dword ptr [esp]
00450509  c1e004                   shl      eax, 4
0045050c  01d8                     add      eax, ebx
0045050e  c1e002                   shl      eax, 2
00450511  01d8                     add      eax, ebx
00450513  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00450519  c1e002                   shl      eax, 2
0045051c  01d8                     add      eax, ebx
0045051e  8d4c2418                 lea      ecx, [esp + 0x18]
00450522  8d54240c                 lea      edx, [esp + 0xc]
00450526  8a4001                   mov      al, byte ptr [eax + 1]
00450529  3c19                     cmp      al, 0x19
0045052b  770d                     ja       0x45053a
0045052d  25ff000000               and      eax, 0xff
00450532  2eff248588024500         jmp      dword ptr cs:[eax*4 + 0x450288]
0045053a  31c0                     xor      eax, eax
0045053c  668b442418               mov      ax, word ptr [esp + 0x18]
00450541  83f802                   cmp      eax, 2
00450544  7524                     jne      0x45056a
00450546  31c0                     xor      eax, eax
00450548  668b44240c               mov      ax, word ptr [esp + 0xc]
0045054d  83f802                   cmp      eax, 2
00450550  7518                     jne      0x45056a
00450552  8b54241d                 mov      edx, dword ptr [esp + 0x1d]
00450556  c1fa18                   sar      edx, 0x18
00450559  89d0                     mov      eax, edx
0045055b  c1fa1f                   sar      edx, 0x1f
0045055e  c1e202                   shl      edx, 2
00450561  1bc2                     sbb      eax, edx
00450563  c1f802                   sar      eax, 2
00450566  88442420                 mov      byte ptr [esp + 0x20], al
0045056a  31d2                     xor      edx, edx
0045056c  668b542414               mov      dx, word ptr [esp + 0x14]
00450571  89d0                     mov      eax, edx
00450573  c1e004                   shl      eax, 4
00450576  01d0                     add      eax, edx
00450578  c1e002                   shl      eax, 2
0045057b  01d0                     add      eax, edx
0045057d  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00450583  e9e1feffff               jmp      0x450469
00450588  80fc01                   cmp      ah, 1
0045058b  720f                     jb       0x45059c
0045058d  0f8625feffff             jbe      0x4503b8
00450593  80fc03                   cmp      ah, 3
00450596  0f84dbfdffff             je       0x450377
0045059c  8a7c2420                 mov      bh, byte ptr [esp + 0x20]
004505a0  2abef6000000             sub      bh, byte ptr [esi + 0xf6]
004505a6  ba06000000               mov      edx, 6
004505ab  887c2420                 mov      byte ptr [esp + 0x20], bh
004505af  31c0                     xor      eax, eax
004505b1  31db                     xor      ebx, ebx
004505b3  8a4500                   mov      al, byte ptr [ebp]
004505b6  8a5d01                   mov      bl, byte ptr [ebp + 1]
004505b9  8a4c2420                 mov      cl, byte ptr [esp + 0x20]
004505bd  e8fe86fdff               call     0x428cc0
004505c2  28c1                     sub      cl, al
004505c4  884c2420                 mov      byte ptr [esp + 0x20], cl
004505c8  8b44241d                 mov      eax, dword ptr [esp + 0x1d]
004505cc  c1f818                   sar      eax, 0x18
004505cf  85c0                     test     eax, eax
004505d1  7d05                     jge      0x4505d8
004505d3  c644242001               mov      byte ptr [esp + 0x20], 1
004505d8  31db                     xor      ebx, ebx
004505da  6689fb                   mov      bx, di
004505dd  89d8                     mov      eax, ebx
004505df  c1e004                   shl      eax, 4
004505e2  01d8                     add      eax, ebx
004505e4  c1e002                   shl      eax, 2
004505e7  8b2da0194e00             mov      ebp, dword ptr [0x4e19a0]
004505ed  01d8                     add      eax, ebx
004505ef  89da                     mov      edx, ebx
004505f1  c1e002                   shl      eax, 2
004505f4  31da                     xor      edx, ebx
004505f6  01c5                     add      ebp, eax
004505f8  31c0                     xor      eax, eax
004505fa  8a1541805000             mov      dl, byte ptr [0x508041]
00450600  668b4508                 mov      ax, word ptr [ebp + 8]
00450604  e8e7600200               call     0x4766f0
00450609  84c0                     test     al, al
0045060b  7437                     je       0x450644
0045060d  89d8                     mov      eax, ebx
0045060f  e84906ffff               call     0x440c5d
00450614  8b9504010000             mov      edx, dword ptr [ebp + 0x104]
0045061a  c685f900000000           mov      byte ptr [ebp + 0xf9], 0
00450621  83faff                   cmp      edx, -1
00450624  751e                     jne      0x450644
00450626  50                       push     eax
00450627  31d2                     xor      edx, edx
00450629  8d9d04010000             lea      ebx, [ebp + 0x104]
0045062f  8a5501                   mov      dl, byte ptr [ebp + 1]
00450632  31c9                     xor      ecx, ecx
00450634  c1e210                   shl      edx, 0x10
00450637  b850000000               mov      eax, 0x50
0045063c  80ce01                   or       dh, 1
0045063f  e835a40300               call     0x48aa79
00450644  31d2                     xor      edx, edx
00450646  6689fa                   mov      dx, di
00450649  89d0                     mov      eax, edx
0045064b  c1e004                   shl      eax, 4
0045064e  01d0                     add      eax, edx
00450650  c1e002                   shl      eax, 2
00450653  01d0                     add      eax, edx
00450655  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
0045065b  8a8482dc000000           mov      al, byte ptr [edx + eax*4 + 0xdc]
00450662  ba03000000               mov      edx, 3
00450667  25ff000000               and      eax, 0xff
0045066c  e826770100               call     0x467d97
00450671  84c0                     test     al, al
00450673  7404                     je       0x450679
00450675  fe4c2420                 dec      byte ptr [esp + 0x20]
00450679  8b44241d                 mov      eax, dword ptr [esp + 0x1d]
0045067d  31d2                     xor      edx, edx
0045067f  c1f818                   sar      eax, 0x18
00450682  668b969a000000           mov      dx, word ptr [esi + 0x9a]
00450689  39c2                     cmp      edx, eax
0045068b  7e14                     jle      0x4506a1
0045068d  660fbe442420             movsx    ax, byte ptr [esp + 0x20]
00450693  29c2                     sub      edx, eax
00450695  6689969a000000           mov      word ptr [esi + 0x9a], dx
0045069c  e9ae010000               jmp      0x45084f
004506a1  31c0                     xor      eax, eax
004506a3  8a44241c                 mov      al, byte ptr [esp + 0x1c]
004506a7  83f801                   cmp      eax, 1
004506aa  7405                     je       0x4506b1
004506ac  e9a3000000               jmp      0x450754
004506b1  31d2                     xor      edx, edx
004506b3  668b542414               mov      dx, word ptr [esp + 0x14]
004506b8  89d0                     mov      eax, edx
004506ba  c1e004                   shl      eax, 4
004506bd  01d0                     add      eax, edx
004506bf  c1e002                   shl      eax, 2
004506c2  01d0                     add      eax, edx
004506c4  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004506ca  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
004506ce  3c06                     cmp      al, 6
004506d0  7212                     jb       0x4506e4
004506d2  3c07                     cmp      al, 7
004506d4  7610                     jbe      0x4506e6
004506d6  3c09                     cmp      al, 9
004506d8  720c                     jb       0x4506e6
004506da  3c0a                     cmp      al, 0xa
004506dc  7608                     jbe      0x4506e6
004506de  3c19                     cmp      al, 0x19
004506e0  7404                     je       0x4506e6
004506e2  eb06                     jmp      0x4506ea
004506e4  3c03                     cmp      al, 3
004506e6  b001                     mov      al, 1
004506e8  eb02                     jmp      0x4506ec
004506ea  30c0                     xor      al, al
004506ec  84c0                     test     al, al
004506ee  7464                     je       0x450754
004506f0  31db                     xor      ebx, ebx
004506f2  668b5c2414               mov      bx, word ptr [esp + 0x14]
004506f7  89d8                     mov      eax, ebx
004506f9  c1e004                   shl      eax, 4
004506fc  01d8                     add      eax, ebx
004506fe  c1e002                   shl      eax, 2
00450701  01d8                     add      eax, ebx
00450703  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00450709  c1e002                   shl      eax, 2
0045070c  01d0                     add      eax, edx
0045070e  8a90af000000             mov      dl, byte ptr [eax + 0xaf]
00450714  80e21f                   and      dl, 0x1f
00450717  80c20a                   add      dl, 0xa
0045071a  8ab0af000000             mov      dh, byte ptr [eax + 0xaf]
00450720  31c9                     xor      ecx, ecx
00450722  c0ee05                   shr      dh, 5
00450725  88d1                     mov      cl, dl
00450727  83f90a                   cmp      ecx, 0xa
0045072a  7c18                     jl       0x450744
0045072c  80a0af000000e0           and      byte ptr [eax + 0xaf], 0xe0
00450733  88f0                     mov      al, dh
00450735  fec0                     inc      al
00450737  31d2                     xor      edx, edx
00450739  88c2                     mov      dl, al
0045073b  89d8                     mov      eax, ebx
0045073d  e8def3ffff               call     0x44fb20
00450742  eb10                     jmp      0x450754
00450744  80c20a                   add      dl, 0xa
00450747  c0e605                   shl      dh, 5
0045074a  00d6                     add      dh, dl
0045074c  00f2                     add      dl, dh
0045074e  8890af000000             mov      byte ptr [eax + 0xaf], dl
00450754  31d2                     xor      edx, edx
00450756  6689fa                   mov      dx, di
00450759  89d0                     mov      eax, edx
0045075b  c1e004                   shl      eax, 4
0045075e  01d0                     add      eax, edx
00450760  c1e002                   shl      eax, 2
00450763  66c7869a0000000000       mov      word ptr [esi + 0x9a], 0
0045076c  01c2                     add      edx, eax
0045076e  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450773  c1e202                   shl      edx, 2
00450776  8a440201                 mov      al, byte ptr [edx + eax + 1]
0045077a  25ff000000               and      eax, 0xff
0045077f  83f801                   cmp      eax, 1
00450782  751f                     jne      0x4507a3
00450784  6a00                     push     0
00450786  6a00                     push     0
00450788  6a00                     push     0
0045078a  31d2                     xor      edx, edx
0045078c  6a00                     push     0
0045078e  b806000000               mov      eax, 6
00450793  668b542420               mov      dx, word ptr [esp + 0x20]
00450798  6a00                     push     0
0045079a  31c9                     xor      ecx, ecx
0045079c  89d3                     mov      ebx, edx
0045079e  e8a9dc0100               call     0x46e44c
004507a3  31d2                     xor      edx, edx
004507a5  6689fa                   mov      dx, di
004507a8  89d0                     mov      eax, edx
004507aa  e88941ffff               call     0x444938
004507af  89d0                     mov      eax, edx
004507b1  c1e004                   shl      eax, 4
004507b4  01d0                     add      eax, edx
004507b6  c1e002                   shl      eax, 2
004507b9  01c2                     add      edx, eax
004507bb  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
004507c0  c1e202                   shl      edx, 2
004507c3  8a440201                 mov      al, byte ptr [edx + eax + 1]
004507c7  3c0c                     cmp      al, 0xc
004507c9  7216                     jb       0x4507e1
004507cb  3c0d                     cmp      al, 0xd
004507cd  760a                     jbe      0x4507d9
004507cf  3c0f                     cmp      al, 0xf
004507d1  7206                     jb       0x4507d9
004507d3  7604                     jbe      0x4507d9
004507d5  3c11                     cmp      al, 0x11
004507d7  7704                     ja       0x4507dd
004507d9  30c0                     xor      al, al
004507db  eb10                     jmp      0x4507ed
004507dd  b001                     mov      al, 1
004507df  eb0c                     jmp      0x4507ed
004507e1  3c03                     cmp      al, 3
004507e3  72f8                     jb       0x4507dd
004507e5  76f2                     jbe      0x4507d9
004507e7  3c0b                     cmp      al, 0xb
004507e9  74ee                     je       0x4507d9
004507eb  ebf0                     jmp      0x4507dd
004507ed  84c0                     test     al, al
004507ef  742b                     je       0x45081c
004507f1  31d2                     xor      edx, edx
004507f3  6689fa                   mov      dx, di
004507f6  89d0                     mov      eax, edx
004507f8  c1e004                   shl      eax, 4
004507fb  01d0                     add      eax, edx
004507fd  c1e002                   shl      eax, 2
00450800  31c9                     xor      ecx, ecx
00450802  01d0                     add      eax, edx
00450804  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
0045080a  8a4c2428                 mov      cl, byte ptr [esp + 0x28]
0045080e  8a0482                   mov      al, byte ptr [edx + eax*4]
00450811  25ff000000               and      eax, 0xff
00450816  89ca                     mov      edx, ecx
00450818  31db                     xor      ebx, ebx
0045081a  eb2e                     jmp      0x45084a
0045081c  31d2                     xor      edx, edx
0045081e  6689fa                   mov      dx, di
00450821  89d0                     mov      eax, edx
00450823  c1e004                   shl      eax, 4
00450826  01d0                     add      eax, edx
00450828  c1e002                   shl      eax, 2
0045082b  31c9                     xor      ecx, ecx
0045082d  01c2                     add      edx, eax
0045082f  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450834  c1e202                   shl      edx, 2
00450837  8a4c2428                 mov      cl, byte ptr [esp + 0x28]
0045083b  8a0402                   mov      al, byte ptr [edx + eax]
0045083e  bb01000000               mov      ebx, 1
00450843  25ff000000               and      eax, 0xff
00450848  89ca                     mov      edx, ecx
0045084a  e8c9480200               call     0x475118
0045084f  83c42c                   add      esp, 0x2c
00450852  5d                       pop      ebp
00450853  5f                       pop      edi
00450854  5e                       pop      esi
00450855  c3                       ret
