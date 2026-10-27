; SacCherchePlace: limite por próximo símbolo SBL, fim exclusivo 0x00475bfe.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004757af  53                       push     ebx
004757b0  51                       push     ecx
004757b1  56                       push     esi
004757b2  57                       push     edi
004757b3  55                       push     ebp
004757b4  83ec64                   sub      esp, 0x64
004757b7  50                       push     eax
004757b8  88d3                     mov      bl, dl
004757ba  89c1                     mov      ecx, eax
004757bc  88d7                     mov      bh, dl
004757be  31c0                     xor      eax, eax
004757c0  8b15747d5000             mov      edx, dword ptr [0x507d74]
004757c6  6689c8                   mov      ax, cx
004757c9  01d0                     add      eax, edx
004757cb  8a10                     mov      dl, byte ptr [eax]
004757cd  38d3                     cmp      bl, dl
004757cf  7409                     je       0x4757da
004757d1  88d0                     mov      al, dl
004757d3  25ff000000               and      eax, 0xff
004757d8  7523                     jne      0x4757fd
004757da  31d2                     xor      edx, edx
004757dc  a1747d5000               mov      eax, dword ptr [0x507d74]
004757e1  6689ca                   mov      dx, cx
004757e4  3a3c02                   cmp      bh, byte ptr [edx + eax]
004757e7  7510                     jne      0x4757f9
004757e9  a1ac7d5000               mov      eax, dword ptr [0x507dac]
004757ee  01c2                     add      edx, eax
004757f0  31c0                     xor      eax, eax
004757f2  8a02                     mov      al, byte ptr [edx]
004757f4  83f81f                   cmp      eax, 0x1f
004757f7  7404                     je       0x4757fd
004757f9  b001                     mov      al, 1
004757fb  eb02                     jmp      0x4757ff
004757fd  30c0                     xor      al, al
004757ff  84c0                     test     al, al
00475801  7408                     je       0x47580b
00475803  8b0424                   mov      eax, dword ptr [esp]
00475806  e9ea030000               jmp      0x475bf5
0047580b  31f6                     xor      esi, esi
0047580d  668b3424                 mov      si, word ptr [esp]
00475811  bd00010000               mov      ebp, 0x100
00475816  89f2                     mov      edx, esi
00475818  89f0                     mov      eax, esi
0047581a  c1fa1f                   sar      edx, 0x1f
0047581d  f7fd                     idiv     ebp
0047581f  6689542420               mov      word ptr [esp + 0x20], dx
00475824  89f2                     mov      edx, esi
00475826  89f0                     mov      eax, esi
00475828  c1fa1f                   sar      edx, 0x1f
0047582b  f7fd                     idiv     ebp
0047582d  668944241c               mov      word ptr [esp + 0x1c], ax
00475832  89f0                     mov      eax, esi
00475834  80c4ff                   add      ah, 0xff
00475837  8944243c                 mov      dword ptr [esp + 0x3c], eax
0047583b  89f0                     mov      eax, esi
0047583d  fec4                     inc      ah
0047583f  b901000000               mov      ecx, 1
00475844  6689442418               mov      word ptr [esp + 0x18], ax
00475849  eb19                     jmp      0x475864
0047584b  8b7c243c                 mov      edi, dword ptr [esp + 0x3c]
0047584f  8a442419                 mov      al, byte ptr [esp + 0x19]
00475853  41                       inc      ecx
00475854  81ef00010000             sub      edi, 0x100
0047585a  fec0                     inc      al
0047585c  897c243c                 mov      dword ptr [esp + 0x3c], edi
00475860  88442419                 mov      byte ptr [esp + 0x19], al
00475864  0fbfc1                   movsx    eax, cx
00475867  83f806                   cmp      eax, 6
0047586a  0f8d80030000             jge      0x475bf0
00475870  89c6                     mov      esi, eax
00475872  31d2                     xor      edx, edx
00475874  b831000000               mov      eax, 0x31
00475879  c1e603                   shl      esi, 3
0047587c  e85bacffff               call     0x4704dc
00475881  f7f6                     div      esi
00475883  89542428                 mov      dword ptr [esp + 0x28], edx
00475887  89ca                     mov      edx, ecx
00475889  f7da                     neg      edx
0047588b  89d6                     mov      esi, edx
0047588d  c1e608                   shl      esi, 8
00475890  8974242c                 mov      dword ptr [esp + 0x2c], esi
00475894  89f7                     mov      edi, esi
00475896  8b3424                   mov      esi, dword ptr [esp]
00475899  01d7                     add      edi, edx
0047589b  01f7                     add      edi, esi
0047589d  8b74242c                 mov      esi, dword ptr [esp + 0x2c]
004758a1  01ce                     add      esi, ecx
004758a3  8974242c                 mov      dword ptr [esp + 0x2c], esi
004758a7  8b3424                   mov      esi, dword ptr [esp]
004758aa  0174242c                 add      dword ptr [esp + 0x2c], esi
004758ae  8b74242c                 mov      esi, dword ptr [esp + 0x2c]
004758b2  6689742444               mov      word ptr [esp + 0x44], si
004758b7  8b74243c                 mov      esi, dword ptr [esp + 0x3c]
004758bb  01d6                     add      esi, edx
004758bd  89742440                 mov      dword ptr [esp + 0x40], esi
004758c1  8b742418                 mov      esi, dword ptr [esp + 0x18]
004758c5  01d6                     add      esi, edx
004758c7  31c0                     xor      eax, eax
004758c9  eb1f                     jmp      0x4758ea
004758cb  8a7c2445                 mov      bh, byte ptr [esp + 0x45]
004758cf  8b742440                 mov      esi, dword ptr [esp + 0x40]
004758d3  81c700010000             add      edi, 0x100
004758d9  46                       inc      esi
004758da  42                       inc      edx
004758db  89742440                 mov      dword ptr [esp + 0x40], esi
004758df  8b742424                 mov      esi, dword ptr [esp + 0x24]
004758e3  fec7                     inc      bh
004758e5  46                       inc      esi
004758e6  887c2445                 mov      byte ptr [esp + 0x45], bh
004758ea  89742424                 mov      dword ptr [esp + 0x24], esi
004758ee  6639ca                   cmp      dx, cx
004758f1  0f8f54ffffff             jg       0x47584b
004758f7  8b74241e                 mov      esi, dword ptr [esp + 0x1e]
004758fb  0fbfe9                   movsx    ebp, cx
004758fe  c1fe10                   sar      esi, 0x10
00475901  29ee                     sub      esi, ebp
00475903  85f6                     test     esi, esi
00475905  0f8c92000000             jl       0x47599d
0047590b  8b74241a                 mov      esi, dword ptr [esp + 0x1a]
0047590f  0fbfea                   movsx    ebp, dx
00475912  c1fe10                   sar      esi, 0x10
00475915  01ee                     add      esi, ebp
00475917  85f6                     test     esi, esi
00475919  0f8c7e000000             jl       0x47599d
0047591f  81fe00010000             cmp      esi, 0x100
00475925  0f8d72000000             jge      0x47599d
0047592b  31f6                     xor      esi, esi
0047592d  8b2d747d5000             mov      ebp, dword ptr [0x507d74]
00475933  6689fe                   mov      si, di
00475936  01ee                     add      esi, ebp
00475938  897c2430                 mov      dword ptr [esp + 0x30], edi
0047593c  885c2450                 mov      byte ptr [esp + 0x50], bl
00475940  8a3e                     mov      bh, byte ptr [esi]
00475942  38fb                     cmp      bl, bh
00475944  7407                     je       0x47594d
00475946  0fb6f7                   movzx    esi, bh
00475949  85f6                     test     esi, esi
0047594b  752a                     jne      0x475977
0047594d  0fb76c2430               movzx    ebp, word ptr [esp + 0x30]
00475952  8b35747d5000             mov      esi, dword ptr [0x507d74]
00475958  8a3c2e                   mov      bh, byte ptr [esi + ebp]
0047595b  3a7c2450                 cmp      bh, byte ptr [esp + 0x50]
0047595f  750f                     jne      0x475970
00475961  8b35ac7d5000             mov      esi, dword ptr [0x507dac]
00475967  0fb6342e                 movzx    esi, byte ptr [esi + ebp]
0047596b  83fe1f                   cmp      esi, 0x1f
0047596e  7407                     je       0x475977
00475970  c644245401               mov      byte ptr [esp + 0x54], 1
00475975  eb06                     jmp      0x47597d
00475977  30ff                     xor      bh, bh
00475979  887c2454                 mov      byte ptr [esp + 0x54], bh
0047597d  807c245400               cmp      byte ptr [esp + 0x54], 0
00475982  7419                     je       0x47599d
00475984  8b742428                 mov      esi, dword ptr [esp + 0x28]
00475988  40                       inc      eax
00475989  6639f0                   cmp      ax, si
0047598c  750f                     jne      0x47599d
0047598e  8b0424                   mov      eax, dword ptr [esp]
00475991  c1e208                   shl      edx, 8
00475994  01d0                     add      eax, edx
00475996  29c8                     sub      eax, ecx
00475998  e958020000               jmp      0x475bf5
0047599d  8b74241e                 mov      esi, dword ptr [esp + 0x1e]
004759a1  0fbfe9                   movsx    ebp, cx
004759a4  c1fe10                   sar      esi, 0x10
004759a7  01ee                     add      esi, ebp
004759a9  81fe00010000             cmp      esi, 0x100
004759af  0f8da7000000             jge      0x475a5c
004759b5  8b74241a                 mov      esi, dword ptr [esp + 0x1a]
004759b9  c1fe10                   sar      esi, 0x10
004759bc  89742404                 mov      dword ptr [esp + 4], esi
004759c0  8b6c2404                 mov      ebp, dword ptr [esp + 4]
004759c4  0fbff2                   movsx    esi, dx
004759c7  01ee                     add      esi, ebp
004759c9  85f6                     test     esi, esi
004759cb  0f8c8b000000             jl       0x475a5c
004759d1  81fe00010000             cmp      esi, 0x100
004759d7  0f8d7f000000             jge      0x475a5c
004759dd  8b742444                 mov      esi, dword ptr [esp + 0x44]
004759e1  89742414                 mov      dword ptr [esp + 0x14], esi
004759e5  31f6                     xor      esi, esi
004759e7  8b2d747d5000             mov      ebp, dword ptr [0x507d74]
004759ed  668b742444               mov      si, word ptr [esp + 0x44]
004759f2  01ee                     add      esi, ebp
004759f4  885c245c                 mov      byte ptr [esp + 0x5c], bl
004759f8  8a3e                     mov      bh, byte ptr [esi]
004759fa  38fb                     cmp      bl, bh
004759fc  7407                     je       0x475a05
004759fe  0fb6f7                   movzx    esi, bh
00475a01  85f6                     test     esi, esi
00475a03  752f                     jne      0x475a34
00475a05  31f6                     xor      esi, esi
00475a07  8b2d747d5000             mov      ebp, dword ptr [0x507d74]
00475a0d  668b742414               mov      si, word ptr [esp + 0x14]
00475a12  01f5                     add      ebp, esi
00475a14  8a7d00                   mov      bh, byte ptr [ebp]
00475a17  3a7c245c                 cmp      bh, byte ptr [esp + 0x5c]
00475a1b  7510                     jne      0x475a2d
00475a1d  8b2dac7d5000             mov      ebp, dword ptr [0x507dac]
00475a23  01ee                     add      esi, ebp
00475a25  0fb636                   movzx    esi, byte ptr [esi]
00475a28  83fe1f                   cmp      esi, 0x1f
00475a2b  7407                     je       0x475a34
00475a2d  c644244c01               mov      byte ptr [esp + 0x4c], 1
00475a32  eb06                     jmp      0x475a3a
00475a34  30ff                     xor      bh, bh
00475a36  887c244c                 mov      byte ptr [esp + 0x4c], bh
00475a3a  807c244c00               cmp      byte ptr [esp + 0x4c], 0
00475a3f  741b                     je       0x475a5c
00475a41  8b742428                 mov      esi, dword ptr [esp + 0x28]
00475a45  40                       inc      eax
00475a46  6639f0                   cmp      ax, si
00475a49  7511                     jne      0x475a5c
00475a4b  89d0                     mov      eax, edx
00475a4d  8b1424                   mov      edx, dword ptr [esp]
00475a50  c1e008                   shl      eax, 8
00475a53  01d0                     add      eax, edx
00475a55  01c8                     add      eax, ecx
00475a57  e999010000               jmp      0x475bf5
00475a5c  0fbff1                   movsx    esi, cx
00475a5f  89f5                     mov      ebp, esi
00475a61  8974240c                 mov      dword ptr [esp + 0xc], esi
00475a65  f7dd                     neg      ebp
00475a67  0fbff2                   movsx    esi, dx
00475a6a  39ee                     cmp      esi, ebp
00475a6c  0f8459feffff             je       0x4758cb
00475a72  6639ca                   cmp      dx, cx
00475a75  0f8450feffff             je       0x4758cb
00475a7b  8b6c241a                 mov      ebp, dword ptr [esp + 0x1a]
00475a7f  c1fd10                   sar      ebp, 0x10
00475a82  2b6c240c                 sub      ebp, dword ptr [esp + 0xc]
00475a86  85ed                     test     ebp, ebp
00475a88  0f8c9a000000             jl       0x475b28
00475a8e  8b6c241e                 mov      ebp, dword ptr [esp + 0x1e]
00475a92  c1fd10                   sar      ebp, 0x10
00475a95  01ee                     add      esi, ebp
00475a97  85f6                     test     esi, esi
00475a99  0f8c89000000             jl       0x475b28
00475a9f  81fe00010000             cmp      esi, 0x100
00475aa5  0f8d7d000000             jge      0x475b28
00475aab  8b742440                 mov      esi, dword ptr [esp + 0x40]
00475aaf  89742434                 mov      dword ptr [esp + 0x34], esi
00475ab3  31f6                     xor      esi, esi
00475ab5  8b2d747d5000             mov      ebp, dword ptr [0x507d74]
00475abb  668b742440               mov      si, word ptr [esp + 0x40]
00475ac0  01ee                     add      esi, ebp
00475ac2  885c2458                 mov      byte ptr [esp + 0x58], bl
00475ac6  8a3e                     mov      bh, byte ptr [esi]
00475ac8  38fb                     cmp      bl, bh
00475aca  7407                     je       0x475ad3
00475acc  0fb6f7                   movzx    esi, bh
00475acf  85f6                     test     esi, esi
00475ad1  752f                     jne      0x475b02
00475ad3  31f6                     xor      esi, esi
00475ad5  8b2d747d5000             mov      ebp, dword ptr [0x507d74]
00475adb  668b742434               mov      si, word ptr [esp + 0x34]
00475ae0  01f5                     add      ebp, esi
00475ae2  8a7d00                   mov      bh, byte ptr [ebp]
00475ae5  3a7c2458                 cmp      bh, byte ptr [esp + 0x58]
00475ae9  7510                     jne      0x475afb
00475aeb  8b2dac7d5000             mov      ebp, dword ptr [0x507dac]
00475af1  01ee                     add      esi, ebp
00475af3  0fb636                   movzx    esi, byte ptr [esi]
00475af6  83fe1f                   cmp      esi, 0x1f
00475af9  7407                     je       0x475b02
00475afb  c644244801               mov      byte ptr [esp + 0x48], 1
00475b00  eb06                     jmp      0x475b08
00475b02  30ff                     xor      bh, bh
00475b04  887c2448                 mov      byte ptr [esp + 0x48], bh
00475b08  807c244800               cmp      byte ptr [esp + 0x48], 0
00475b0d  7419                     je       0x475b28
00475b0f  8b742428                 mov      esi, dword ptr [esp + 0x28]
00475b13  40                       inc      eax
00475b14  6639f0                   cmp      ax, si
00475b17  750f                     jne      0x475b28
00475b19  8b0424                   mov      eax, dword ptr [esp]
00475b1c  c1e108                   shl      ecx, 8
00475b1f  29c8                     sub      eax, ecx
00475b21  01d0                     add      eax, edx
00475b23  e9cd000000               jmp      0x475bf5
00475b28  8b74241a                 mov      esi, dword ptr [esp + 0x1a]
00475b2c  c1fe10                   sar      esi, 0x10
00475b2f  89742408                 mov      dword ptr [esp + 8], esi
00475b33  8b6c2408                 mov      ebp, dword ptr [esp + 8]
00475b37  0fbff1                   movsx    esi, cx
00475b3a  01ee                     add      esi, ebp
00475b3c  81fe00010000             cmp      esi, 0x100
00475b42  0f8d83fdffff             jge      0x4758cb
00475b48  8b74241e                 mov      esi, dword ptr [esp + 0x1e]
00475b4c  c1fe10                   sar      esi, 0x10
00475b4f  89742410                 mov      dword ptr [esp + 0x10], esi
00475b53  8b6c2410                 mov      ebp, dword ptr [esp + 0x10]
00475b57  0fbff2                   movsx    esi, dx
00475b5a  01ee                     add      esi, ebp
00475b5c  85f6                     test     esi, esi
00475b5e  0f8c67fdffff             jl       0x4758cb
00475b64  81fe00010000             cmp      esi, 0x100
00475b6a  0f8d5bfdffff             jge      0x4758cb
00475b70  8b742424                 mov      esi, dword ptr [esp + 0x24]
00475b74  89742438                 mov      dword ptr [esp + 0x38], esi
00475b78  31f6                     xor      esi, esi
00475b7a  8b2d747d5000             mov      ebp, dword ptr [0x507d74]
00475b80  668b742424               mov      si, word ptr [esp + 0x24]
00475b85  01ee                     add      esi, ebp
00475b87  885c2460                 mov      byte ptr [esp + 0x60], bl
00475b8b  8a3e                     mov      bh, byte ptr [esi]
00475b8d  38fb                     cmp      bl, bh
00475b8f  7407                     je       0x475b98
00475b91  0fb6f7                   movzx    esi, bh
00475b94  85f6                     test     esi, esi
00475b96  752a                     jne      0x475bc2
00475b98  0fb76c2438               movzx    ebp, word ptr [esp + 0x38]
00475b9d  8b35747d5000             mov      esi, dword ptr [0x507d74]
00475ba3  8a3c2e                   mov      bh, byte ptr [esi + ebp]
00475ba6  3a7c2460                 cmp      bh, byte ptr [esp + 0x60]
00475baa  750f                     jne      0x475bbb
00475bac  8b35ac7d5000             mov      esi, dword ptr [0x507dac]
00475bb2  0fb6342e                 movzx    esi, byte ptr [esi + ebp]
00475bb6  83fe1f                   cmp      esi, 0x1f
00475bb9  7407                     je       0x475bc2
00475bbb  c644246401               mov      byte ptr [esp + 0x64], 1
00475bc0  eb06                     jmp      0x475bc8
00475bc2  30ff                     xor      bh, bh
00475bc4  887c2464                 mov      byte ptr [esp + 0x64], bh
00475bc8  807c246400               cmp      byte ptr [esp + 0x64], 0
00475bcd  0f84f8fcffff             je       0x4758cb
00475bd3  8b742428                 mov      esi, dword ptr [esp + 0x28]
00475bd7  40                       inc      eax
00475bd8  6639f0                   cmp      ax, si
00475bdb  0f85eafcffff             jne      0x4758cb
00475be1  89c8                     mov      eax, ecx
00475be3  8b3c24                   mov      edi, dword ptr [esp]
00475be6  c1e008                   shl      eax, 8
00475be9  01f8                     add      eax, edi
00475beb  e931ffffff               jmp      0x475b21
00475bf0  b8ffff0000               mov      eax, 0xffff
00475bf5  83c468                   add      esp, 0x68
00475bf8  5d                       pop      ebp
00475bf9  5f                       pop      edi
00475bfa  5e                       pop      esi
00475bfb  59                       pop      ecx
00475bfc  5b                       pop      ebx
00475bfd  c3                       ret
