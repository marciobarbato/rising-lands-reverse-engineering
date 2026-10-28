; RechercheCalculNew: Inventory only (MissionLoadName tail); not reconstructed in Stage 16; exclusive end 0x004716fe.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047150f  53                       push     ebx
00471510  51                       push     ecx
00471511  52                       push     edx
00471512  56                       push     esi
00471513  57                       push     edi
00471514  55                       push     ebp
00471515  83ec08                   sub      esp, 8
00471518  e8fa9fffff               call     0x46b517
0047151d  31d2                     xor      edx, edx
0047151f  e84d79fbff               call     0x428e71
00471524  6689542404               mov      word ptr [esp + 4], dx
00471529  eb1d                     jmp      0x471548
0047152b  8b4c2404                 mov      ecx, dword ptr [esp + 4]
0047152f  c1e604                   shl      esi, 4
00471532  41                       inc      ecx
00471533  8dbef4805000             lea      edi, [esi + 0x5080f4]
00471539  8db634815000             lea      esi, [esi + 0x508134]
0047153f  66894c2404               mov      word ptr [esp + 4], cx
00471544  a5                       movsd    dword ptr es:[edi], dword ptr [esi]
00471545  a5                       movsd    dword ptr es:[edi], dword ptr [esi]
00471546  a5                       movsd    dword ptr es:[edi], dword ptr [esi]
00471547  a5                       movsd    dword ptr es:[edi], dword ptr [esi]
00471548  31f6                     xor      esi, esi
0047154a  668b742404               mov      si, word ptr [esp + 4]
0047154f  83fe04                   cmp      esi, 4
00471552  7cd7                     jl       0x47152b
00471554  31db                     xor      ebx, ebx
00471556  66895c2404               mov      word ptr [esp + 4], bx
0047155b  eb05                     jmp      0x471562
0047155d  66ff442404               inc      word ptr [esp + 4]
00471562  31c0                     xor      eax, eax
00471564  668b442404               mov      ax, word ptr [esp + 4]
00471569  83f804                   cmp      eax, 4
0047156c  0f8d74000000             jge      0x4715e6
00471572  31ff                     xor      edi, edi
00471574  31ed                     xor      ebp, ebp
00471576  eb01                     jmp      0x471579
00471578  47                       inc      edi
00471579  31c0                     xor      eax, eax
0047157b  6689f8                   mov      ax, di
0047157e  83f804                   cmp      eax, 4
00471581  7dda                     jge      0x47155d
00471583  89ee                     mov      esi, ebp
00471585  eb01                     jmp      0x471588
00471587  46                       inc      esi
00471588  31c0                     xor      eax, eax
0047158a  31d2                     xor      edx, edx
0047158c  668b442404               mov      ax, word ptr [esp + 4]
00471591  6689fa                   mov      dx, di
00471594  c1e004                   shl      eax, 4
00471597  8a8402f4805000           mov      al, byte ptr [edx + eax + 0x5080f4]
0047159e  25ff000000               and      eax, 0xff
004715a3  39c6                     cmp      esi, eax
004715a5  7dd1                     jge      0x471578
004715a7  69d268010000             imul     edx, edx, 0x168
004715ad  31c0                     xor      eax, eax
004715af  6689f0                   mov      ax, si
004715b2  6bc00c                   imul     eax, eax, 0xc
004715b5  8a840282815000           mov      al, byte ptr [edx + eax + 0x508182]
004715bc  25ff000000               and      eax, 0xff
004715c1  3dff000000               cmp      eax, 0xff
004715c6  0f95c0                   setne    al
004715c9  84c0                     test     al, al
004715cb  74ba                     je       0x471587
004715cd  31db                     xor      ebx, ebx
004715cf  31d2                     xor      edx, edx
004715d1  31c0                     xor      eax, eax
004715d3  31c9                     xor      ecx, ecx
004715d5  8a442404                 mov      al, byte ptr [esp + 4]
004715d9  6689fb                   mov      bx, di
004715dc  6689f2                   mov      dx, si
004715df  e8b4f9ffff               call     0x470f98
004715e4  eba1                     jmp      0x471587
004715e6  31f6                     xor      esi, esi
004715e8  6689742404               mov      word ptr [esp + 4], si
004715ed  eb05                     jmp      0x4715f4
004715ef  66ff442404               inc      word ptr [esp + 4]
004715f4  31c0                     xor      eax, eax
004715f6  668b442404               mov      ax, word ptr [esp + 4]
004715fb  83f804                   cmp      eax, 4
004715fe  0f8df1000000             jge      0x4716f5
00471604  30d2                     xor      dl, dl
00471606  31ff                     xor      edi, edi
00471608  88901c875000             mov      byte ptr [eax + 0x50871c], dl
0047160e  eb01                     jmp      0x471611
00471610  47                       inc      edi
00471611  31c0                     xor      eax, eax
00471613  6689f8                   mov      ax, di
00471616  83f804                   cmp      eax, 4
00471619  7dd4                     jge      0x4715ef
0047161b  31c0                     xor      eax, eax
0047161d  bdf4805000               mov      ebp, 0x5080f4
00471622  668b442404               mov      ax, word ptr [esp + 4]
00471627  31d2                     xor      edx, edx
00471629  c1e004                   shl      eax, 4
0047162c  66891424                 mov      word ptr [esp], dx
00471630  01c5                     add      ebp, eax
00471632  31f6                     xor      esi, esi
00471634  6689fe                   mov      si, di
00471637  69f668010000             imul     esi, esi, 0x168
0047163d  31c0                     xor      eax, eax
0047163f  668b0424                 mov      ax, word ptr [esp]
00471643  6bc00c                   imul     eax, eax, 0xc
00471646  01c6                     add      esi, eax
00471648  31c0                     xor      eax, eax
0047164a  8a8682815000             mov      al, byte ptr [esi + 0x508182]
00471650  3dff000000               cmp      eax, 0xff
00471655  7419                     je       0x471670
00471657  31d2                     xor      edx, edx
00471659  8a9681815000             mov      dl, byte ptr [esi + 0x508181]
0047165f  e8b6aaffff               call     0x46c11a
00471664  25ffff0000               and      eax, 0xffff
00471669  39c2                     cmp      edx, eax
0047166b  0f9ec0                   setle    al
0047166e  eb02                     jmp      0x471672
00471670  30c0                     xor      al, al
00471672  84c0                     test     al, al
00471674  749a                     je       0x471610
00471676  31c0                     xor      eax, eax
00471678  6689f8                   mov      ax, di
0047167b  8a1428                   mov      dl, byte ptr [eax + ebp]
0047167e  31f6                     xor      esi, esi
00471680  81e2ff000000             and      edx, 0xff
00471686  668b3424                 mov      si, word ptr [esp]
0047168a  39f2                     cmp      edx, esi
0047168c  7f5e                     jg       0x4716ec
0047168e  69c068010000             imul     eax, eax, 0x168
00471694  6bf60c                   imul     esi, esi, 0xc
00471697  01c6                     add      esi, eax
00471699  31c0                     xor      eax, eax
0047169b  8a8682815000             mov      al, byte ptr [esi + 0x508182]
004716a1  3dff000000               cmp      eax, 0xff
004716a6  7419                     je       0x4716c1
004716a8  31d2                     xor      edx, edx
004716aa  8a9680815000             mov      dl, byte ptr [esi + 0x508180]
004716b0  e865aaffff               call     0x46c11a
004716b5  25ffff0000               and      eax, 0xffff
004716ba  39c2                     cmp      edx, eax
004716bc  0f9ec0                   setle    al
004716bf  eb02                     jmp      0x4716c3
004716c1  30c0                     xor      al, al
004716c3  84c0                     test     al, al
004716c5  7425                     je       0x4716ec
004716c7  b901000000               mov      ecx, 1
004716cc  31f6                     xor      esi, esi
004716ce  31d2                     xor      edx, edx
004716d0  31c0                     xor      eax, eax
004716d2  668b1424                 mov      dx, word ptr [esp]
004716d6  6689fe                   mov      si, di
004716d9  8a442404                 mov      al, byte ptr [esp + 4]
004716dd  89f3                     mov      ebx, esi
004716df  e8b4f8ffff               call     0x470f98
004716e4  8a0424                   mov      al, byte ptr [esp]
004716e7  fec0                     inc      al
004716e9  88042e                   mov      byte ptr [esi + ebp], al
004716ec  66ff0424                 inc      word ptr [esp]
004716f0  e93dffffff               jmp      0x471632
004716f5  83c408                   add      esp, 8
004716f8  5d                       pop      ebp
004716f9  e9f5f2ffff               jmp      0x4709f3
