; CalculAttaqueEngin; intervalo [0x00451914, 0x00452c94)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00451914  53                       push     ebx
00451915  51                       push     ecx
00451916  52                       push     edx
00451917  56                       push     esi
00451918  57                       push     edi
00451919  55                       push     ebp
0045191a  83ec50                   sub      esp, 0x50
0045191d  89c7                     mov      edi, eax
0045191f  31d2                     xor      edx, edx
00451921  6689c2                   mov      dx, ax
00451924  89d0                     mov      eax, edx
00451926  c1e004                   shl      eax, 4
00451929  01d0                     add      eax, edx
0045192b  c1e002                   shl      eax, 2
0045192e  8d1c02                   lea      ebx, [edx + eax]
00451931  8b35a0194e00             mov      esi, dword ptr [0x4e19a0]
00451937  c1e302                   shl      ebx, 2
0045193a  01de                     add      esi, ebx
0045193c  8a868a000000             mov      al, byte ptr [esi + 0x8a]
00451942  3c03                     cmp      al, 3
00451944  0f873f130000             ja       0x452c89
0045194a  25ff000000               and      eax, 0xff
0045194f  2eff248504194500         jmp      dword ptr cs:[eax*4 + 0x451904]
00451957  8b8683000000             mov      eax, dword ptr [esi + 0x83]
0045195d  c1f818                   sar      eax, 0x18
00451960  85c0                     test     eax, eax
00451962  0f8528050000             jne      0x451e90
00451968  8b8684000000             mov      eax, dword ptr [esi + 0x84]
0045196e  c1f818                   sar      eax, 0x18
00451971  85c0                     test     eax, eax
00451973  0f8517050000             jne      0x451e90
00451979  6689f8                   mov      ax, di
0045197c  31db                     xor      ebx, ebx
0045197e  31d2                     xor      edx, edx
00451980  668b9eb8000000           mov      bx, word ptr [esi + 0xb8]
00451987  8a96b7000000             mov      dl, byte ptr [esi + 0xb7]
0045198d  e82353ffff               call     0x446cb5
00451992  84c0                     test     al, al
00451994  0f84f6040000             je       0x451e90
0045199a  31db                     xor      ebx, ebx
0045199c  31c0                     xor      eax, eax
0045199e  31d2                     xor      edx, edx
004519a0  6689f8                   mov      ax, di
004519a3  668b9eb8000000           mov      bx, word ptr [esi + 0xb8]
004519aa  8a96b7000000             mov      dl, byte ptr [esi + 0xb7]
004519b0  e8edfdffff               call     0x4517a2
004519b5  84c0                     test     al, al
004519b7  0f84d3040000             je       0x451e90
004519bd  89fb                     mov      ebx, edi
004519bf  31d2                     xor      edx, edx
004519c1  6689da                   mov      dx, bx
004519c4  89d0                     mov      eax, edx
004519c6  c1e004                   shl      eax, 4
004519c9  01d0                     add      eax, edx
004519cb  c1e002                   shl      eax, 2
004519ce  01d0                     add      eax, edx
004519d0  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004519d6  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
004519db  31d2                     xor      edx, edx
004519dd  6689da                   mov      dx, bx
004519e0  89442440                 mov      dword ptr [esp + 0x40], eax
004519e4  89d0                     mov      eax, edx
004519e6  c1e004                   shl      eax, 4
004519e9  01d0                     add      eax, edx
004519eb  c1e002                   shl      eax, 2
004519ee  01d0                     add      eax, edx
004519f0  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004519f6  c1e002                   shl      eax, 2
004519f9  01d0                     add      eax, edx
004519fb  8b542440                 mov      edx, dword ptr [esp + 0x40]
004519ff  6689507e                 mov      word ptr [eax + 0x7e], dx
00451a03  663b1d04634900           cmp      bx, word ptr [0x496304]
00451a0a  0f8522000000             jne      0x451a32
00451a10  bbffff0000               mov      ebx, 0xffff
00451a15  30d2                     xor      dl, dl
00451a17  31ed                     xor      ebp, ebp
00451a19  8815360f4e00             mov      byte ptr [0x4e0f36], dl
00451a1f  8815370f4e00             mov      byte ptr [0x4e0f37], dl
00451a25  892d3c0f4e00             mov      dword ptr [0x4e0f3c], ebp
00451a2b  66891d04634900           mov      word ptr [0x496304], bx
00451a32  31d2                     xor      edx, edx
00451a34  6689fa                   mov      dx, di
00451a37  c6808800000000           mov      byte ptr [eax + 0x88], 0
00451a3e  89d0                     mov      eax, edx
00451a40  c1e004                   shl      eax, 4
00451a43  01d0                     add      eax, edx
00451a45  c1e002                   shl      eax, 2
00451a48  01d0                     add      eax, edx
00451a4a  8b2da0194e00             mov      ebp, dword ptr [0x4e19a0]
00451a50  c1e002                   shl      eax, 2
00451a53  8d1c28                   lea      ebx, [eax + ebp]
00451a56  897c2418                 mov      dword ptr [esp + 0x18], edi
00451a5a  8a93b7000000             mov      dl, byte ptr [ebx + 0xb7]
00451a60  b8ffff0000               mov      eax, 0xffff
00451a65  80fa03                   cmp      dl, 3
00451a68  0f82d3010000             jb       0x451c41
00451a6e  7630                     jbe      0x451aa0
00451a70  80fa05                   cmp      dl, 5
00451a73  0f84bc010000             je       0x451c35
00451a79  e97f000000               jmp      0x451afd
00451a7e  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00451a85  31d2                     xor      edx, edx
00451a87  6689c2                   mov      dx, ax
00451a8a  89d0                     mov      eax, edx
00451a8c  c1e004                   shl      eax, 4
00451a8f  01d0                     add      eax, edx
00451a91  c1e002                   shl      eax, 2
00451a94  01d0                     add      eax, edx
00451a96  668b44857c               mov      ax, word ptr [ebp + eax*4 + 0x7c]
00451a9b  e95d000000               jmp      0x451afd
00451aa0  31d2                     xor      edx, edx
00451aa2  8a93b0000000             mov      dl, byte ptr [ebx + 0xb0]
00451aa8  85d2                     test     edx, edx
00451aaa  7405                     je       0x451ab1
00451aac  83fa01                   cmp      edx, 1
00451aaf  7531                     jne      0x451ae2
00451ab1  31d2                     xor      edx, edx
00451ab3  668b542418               mov      dx, word ptr [esp + 0x18]
00451ab8  89d0                     mov      eax, edx
00451aba  c1e004                   shl      eax, 4
00451abd  01d0                     add      eax, edx
00451abf  c1e002                   shl      eax, 2
00451ac2  01d0                     add      eax, edx
00451ac4  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00451aca  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
00451acf  31d2                     xor      edx, edx
00451ad1  6689c2                   mov      dx, ax
00451ad4  31c0                     xor      eax, eax
00451ad6  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00451add  e8be1efdff               call     0x4239a0
00451ae2  31d2                     xor      edx, edx
00451ae4  6689c2                   mov      dx, ax
00451ae7  81faffff0000             cmp      edx, 0xffff
00451aed  750e                     jne      0x451afd
00451aef  31c0                     xor      eax, eax
00451af1  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00451af8  e8e593fcff               call     0x41aee2
00451afd  31d2                     xor      edx, edx
00451aff  6689fa                   mov      dx, di
00451b02  89c3                     mov      ebx, eax
00451b04  89d0                     mov      eax, edx
00451b06  c1e004                   shl      eax, 4
00451b09  01d0                     add      eax, edx
00451b0b  c1e002                   shl      eax, 2
00451b0e  01c2                     add      edx, eax
00451b10  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00451b15  c1e202                   shl      edx, 2
00451b18  8a440201                 mov      al, byte ptr [edx + eax + 1]
00451b1c  3c0c                     cmp      al, 0xc
00451b1e  720e                     jb       0x451b2e
00451b20  0f8629010000             jbe      0x451c4f
00451b26  3c0f                     cmp      al, 0xf
00451b28  0f8421010000             je       0x451c4f
00451b2e  30c0                     xor      al, al
00451b30  84c0                     test     al, al
00451b32  0f854e010000             jne      0x451c86
00451b38  6a08                     push     8
00451b3a  81e3ffff0000             and      ebx, 0xffff
00451b40  89da                     mov      edx, ebx
00451b42  89d8                     mov      eax, ebx
00451b44  c1fa1f                   sar      edx, 0x1f
00451b47  c1e208                   shl      edx, 8
00451b4a  1bc2                     sbb      eax, edx
00451b4c  c1f808                   sar      eax, 8
00451b4f  31c9                     xor      ecx, ecx
00451b51  bd00010000               mov      ebp, 0x100
00451b56  6689c1                   mov      cx, ax
00451b59  89da                     mov      edx, ebx
00451b5b  89d8                     mov      eax, ebx
00451b5d  c1fa1f                   sar      edx, 0x1f
00451b60  f7fd                     idiv     ebp
00451b62  31db                     xor      ebx, ebx
00451b64  668b5e08                 mov      bx, word ptr [esi + 8]
00451b68  0fb7ea                   movzx    ebp, dx
00451b6b  89da                     mov      edx, ebx
00451b6d  89d8                     mov      eax, ebx
00451b6f  c1fa1f                   sar      edx, 0x1f
00451b72  c1e208                   shl      edx, 8
00451b75  1bc2                     sbb      eax, edx
00451b77  c1f808                   sar      eax, 8
00451b7a  25ffff0000               and      eax, 0xffff
00451b7f  89da                     mov      edx, ebx
00451b81  89442408                 mov      dword ptr [esp + 8], eax
00451b85  b800010000               mov      eax, 0x100
00451b8a  c1fa1f                   sar      edx, 0x1f
00451b8d  8944240c                 mov      dword ptr [esp + 0xc], eax
00451b91  89d8                     mov      eax, ebx
00451b93  f77c240c                 idiv     dword ptr [esp + 0xc]
00451b97  31c0                     xor      eax, eax
00451b99  89eb                     mov      ebx, ebp
00451b9b  6689d0                   mov      ax, dx
00451b9e  8b542408                 mov      edx, dword ptr [esp + 8]
00451ba2  e8247b0200               call     0x4796cb
00451ba7  00c0                     add      al, al
00451ba9  fec8                     dec      al
00451bab  888690000000             mov      byte ptr [esi + 0x90], al
00451bb1  31c0                     xor      eax, eax
00451bb3  8a4601                   mov      al, byte ptr [esi + 1]
00451bb6  83f803                   cmp      eax, 3
00451bb9  0f851e000000             jne      0x451bdd
00451bbf  31d2                     xor      edx, edx
00451bc1  8a9690000000             mov      dl, byte ptr [esi + 0x90]
00451bc7  83c20b                   add      edx, 0xb
00451bca  bb10000000               mov      ebx, 0x10
00451bcf  89d0                     mov      eax, edx
00451bd1  c1fa1f                   sar      edx, 0x1f
00451bd4  f7fb                     idiv     ebx
00451bd6  42                       inc      edx
00451bd7  889690000000             mov      byte ptr [esi + 0x90], dl
00451bdd  31d2                     xor      edx, edx
00451bdf  6689fa                   mov      dx, di
00451be2  89d0                     mov      eax, edx
00451be4  c1e004                   shl      eax, 4
00451be7  01d0                     add      eax, edx
00451be9  c1e002                   shl      eax, 2
00451bec  01d0                     add      eax, edx
00451bee  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00451bf4  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
00451bf8  3c0c                     cmp      al, 0xc
00451bfa  720e                     jb       0x451c0a
00451bfc  0f8640010000             jbe      0x451d42
00451c02  3c0f                     cmp      al, 0xf
00451c04  0f8438010000             je       0x451d42
00451c0a  30c0                     xor      al, al
00451c0c  84c0                     test     al, al
00451c0e  0f8539010000             jne      0x451d4d
00451c14  8a8691000000             mov      al, byte ptr [esi + 0x91]
00451c1a  3a8690000000             cmp      al, byte ptr [esi + 0x90]
00451c20  0f8427010000             je       0x451d4d
00451c26  31c0                     xor      eax, eax
00451c28  6689f8                   mov      ax, di
00451c2b  e86969ffff               call     0x448599
00451c30  e954100000               jmp      0x452c89
00451c35  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00451c3c  e9bcfeffff               jmp      0x451afd
00451c41  80fa01                   cmp      dl, 1
00451c44  0f8434feffff             je       0x451a7e
00451c4a  e9aefeffff               jmp      0x451afd
00451c4f  b001                     mov      al, 1
00451c51  e9dafeffff               jmp      0x451b30
00451c56  31d2                     xor      edx, edx
00451c58  668b542438               mov      dx, word ptr [esp + 0x38]
00451c5d  89d0                     mov      eax, edx
00451c5f  c1e004                   shl      eax, 4
00451c62  01d0                     add      eax, edx
00451c64  c1e002                   shl      eax, 2
00451c67  01d0                     add      eax, edx
00451c69  668b4c837c               mov      cx, word ptr [ebx + eax*4 + 0x7c]
00451c6e  eb53                     jmp      0x451cc3
00451c70  31c0                     xor      eax, eax
00451c72  668b442438               mov      ax, word ptr [esp + 0x38]
00451c77  e86692fcff               call     0x41aee2
00451c7c  89c1                     mov      ecx, eax
00451c7e  eb43                     jmp      0x451cc3
00451c80  8b4c2438                 mov      ecx, dword ptr [esp + 0x38]
00451c84  eb3d                     jmp      0x451cc3
00451c86  668b96b8000000           mov      dx, word ptr [esi + 0xb8]
00451c8d  89542438                 mov      dword ptr [esp + 0x38], edx
00451c91  31d2                     xor      edx, edx
00451c93  6689fa                   mov      dx, di
00451c96  89d5                     mov      ebp, edx
00451c98  c1e504                   shl      ebp, 4
00451c9b  01d5                     add      ebp, edx
00451c9d  c1e502                   shl      ebp, 2
00451ca0  01d5                     add      ebp, edx
00451ca2  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00451ca8  c1e502                   shl      ebp, 2
00451cab  8a86b7000000             mov      al, byte ptr [esi + 0xb7]
00451cb1  01dd                     add      ebp, ebx
00451cb3  3c03                     cmp      al, 3
00451cb5  7208                     jb       0x451cbf
00451cb7  76b7                     jbe      0x451c70
00451cb9  3c05                     cmp      al, 5
00451cbb  74c3                     je       0x451c80
00451cbd  eb04                     jmp      0x451cc3
00451cbf  3c01                     cmp      al, 1
00451cc1  7493                     je       0x451c56
00451cc3  31db                     xor      ebx, ebx
00451cc5  6689cb                   mov      bx, cx
00451cc8  89da                     mov      edx, ebx
00451cca  89d8                     mov      eax, ebx
00451ccc  c1fa1f                   sar      edx, 0x1f
00451ccf  c1e208                   shl      edx, 8
00451cd2  1bc2                     sbb      eax, edx
00451cd4  c1f808                   sar      eax, 8
00451cd7  31c9                     xor      ecx, ecx
00451cd9  6689c1                   mov      cx, ax
00451cdc  89da                     mov      edx, ebx
00451cde  b800010000               mov      eax, 0x100
00451ce3  c1fa1f                   sar      edx, 0x1f
00451ce6  89442408                 mov      dword ptr [esp + 8], eax
00451cea  89d8                     mov      eax, ebx
00451cec  f77c2408                 idiv     dword ptr [esp + 8]
00451cf0  31c0                     xor      eax, eax
00451cf2  31db                     xor      ebx, ebx
00451cf4  6689d0                   mov      ax, dx
00451cf7  668b5d08                 mov      bx, word ptr [ebp + 8]
00451cfb  89442404                 mov      dword ptr [esp + 4], eax
00451cff  89da                     mov      edx, ebx
00451d01  89d8                     mov      eax, ebx
00451d03  c1fa1f                   sar      edx, 0x1f
00451d06  c1e208                   shl      edx, 8
00451d09  1bc2                     sbb      eax, edx
00451d0b  c1f808                   sar      eax, 8
00451d0e  0fb7e8                   movzx    ebp, ax
00451d11  89da                     mov      edx, ebx
00451d13  b800010000               mov      eax, 0x100
00451d18  c1fa1f                   sar      edx, 0x1f
00451d1b  89442408                 mov      dword ptr [esp + 8], eax
00451d1f  89d8                     mov      eax, ebx
00451d21  f77c2408                 idiv     dword ptr [esp + 8]
00451d25  6a20                     push     0x20
00451d27  31c0                     xor      eax, eax
00451d29  8b5c2408                 mov      ebx, dword ptr [esp + 8]
00451d2d  6689d0                   mov      ax, dx
00451d30  89ea                     mov      edx, ebp
00451d32  e894790200               call     0x4796cb
00451d37  8886da000000             mov      byte ptr [esi + 0xda], al
00451d3d  e99bfeffff               jmp      0x451bdd
00451d42  b001                     mov      al, 1
00451d44  e9c3feffff               jmp      0x451c0c
00451d49  b001                     mov      al, 1
00451d4b  eb29                     jmp      0x451d76
00451d4d  31d2                     xor      edx, edx
00451d4f  6689fa                   mov      dx, di
00451d52  89d0                     mov      eax, edx
00451d54  c1e004                   shl      eax, 4
00451d57  01d0                     add      eax, edx
00451d59  c1e002                   shl      eax, 2
00451d5c  01c2                     add      edx, eax
00451d5e  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00451d63  c1e202                   shl      edx, 2
00451d66  8a440201                 mov      al, byte ptr [edx + eax + 1]
00451d6a  3c0c                     cmp      al, 0xc
00451d6c  7206                     jb       0x451d74
00451d6e  76d9                     jbe      0x451d49
00451d70  3c0f                     cmp      al, 0xf
00451d72  74d5                     je       0x451d49
00451d74  30c0                     xor      al, al
00451d76  84c0                     test     al, al
00451d78  741d                     je       0x451d97
00451d7a  8a8694000000             mov      al, byte ptr [esi + 0x94]
00451d80  3a86da000000             cmp      al, byte ptr [esi + 0xda]
00451d86  740f                     je       0x451d97
00451d88  31c0                     xor      eax, eax
00451d8a  6689f8                   mov      ax, di
00451d8d  e81567ffff               call     0x4484a7
00451d92  e9f20e0000               jmp      0x452c89
00451d97  31d2                     xor      edx, edx
00451d99  6689fa                   mov      dx, di
00451d9c  89d0                     mov      eax, edx
00451d9e  c1e004                   shl      eax, 4
00451da1  01d0                     add      eax, edx
00451da3  c1e002                   shl      eax, 2
00451da6  01d0                     add      eax, edx
00451da8  8b2da0194e00             mov      ebp, dword ptr [0x4e19a0]
00451dae  c1e002                   shl      eax, 2
00451db1  01c5                     add      ebp, eax
00451db3  31db                     xor      ebx, ebx
00451db5  8a5d01                   mov      bl, byte ptr [ebp + 1]
00451db8  89d8                     mov      eax, ebx
00451dba  c1e002                   shl      eax, 2
00451dbd  29d8                     sub      eax, ebx
00451dbf  c1e003                   shl      eax, 3
00451dc2  01d8                     add      eax, ebx
00451dc4  31c9                     xor      ecx, ecx
00451dc6  668b0c45de654900         mov      cx, word ptr [eax*2 + 0x4965de]
00451dce  31c0                     xor      eax, eax
00451dd0  ba03000000               mov      edx, 3
00451dd5  8a4500                   mov      al, byte ptr [ebp]
00451dd8  e8e36efdff               call     0x428cc0
00451ddd  25ffff0000               and      eax, 0xffff
00451de2  29c1                     sub      ecx, eax
00451de4  31c0                     xor      eax, eax
00451de6  668b8502010000           mov      ax, word ptr [ebp + 0x102]
00451ded  39c8                     cmp      eax, ecx
00451def  0f9dc0                   setge    al
00451df2  84c0                     test     al, al
00451df4  0f848f0e0000             je       0x452c89
00451dfa  66c786020100000000       mov      word ptr [esi + 0x102], 0
00451e03  31c0                     xor      eax, eax
00451e05  8a4601                   mov      al, byte ptr [esi + 1]
00451e08  c6868a00000001           mov      byte ptr [esi + 0x8a], 1
00451e0f  83f810                   cmp      eax, 0x10
00451e12  740e                     je       0x451e22
00451e14  c686a400000000           mov      byte ptr [esi + 0xa4], 0
00451e1b  c686a900000000           mov      byte ptr [esi + 0xa9], 0
00451e22  31d2                     xor      edx, edx
00451e24  6689fa                   mov      dx, di
00451e27  89d0                     mov      eax, edx
00451e29  c1e004                   shl      eax, 4
00451e2c  01d0                     add      eax, edx
00451e2e  c1e002                   shl      eax, 2
00451e31  01d0                     add      eax, edx
00451e33  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00451e39  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
00451e3d  3c0e                     cmp      al, 0xe
00451e3f  7206                     jb       0x451e47
00451e41  7649                     jbe      0x451e8c
00451e43  3c10                     cmp      al, 0x10
00451e45  7445                     je       0x451e8c
00451e47  30c0                     xor      al, al
00451e49  84c0                     test     al, al
00451e4b  0f84380e0000             je       0x452c89
00451e51  31db                     xor      ebx, ebx
00451e53  6689fb                   mov      bx, di
00451e56  89d8                     mov      eax, ebx
00451e58  c1e004                   shl      eax, 4
00451e5b  01d8                     add      eax, ebx
00451e5d  c1e002                   shl      eax, 2
00451e60  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00451e66  01d8                     add      eax, ebx
00451e68  8a8482da000000           mov      al, byte ptr [edx + eax*4 + 0xda]
00451e6f  25ff000000               and      eax, 0xff
00451e74  0f850f0e0000             jne      0x452c89
00451e7a  31d2                     xor      edx, edx
00451e7c  89d8                     mov      eax, ebx
00451e7e  668b567c                 mov      dx, word ptr [esi + 0x7c]
00451e82  e84c39ffff               call     0x4457d3
00451e87  e9fd0d0000               jmp      0x452c89
00451e8c  b001                     mov      al, 1
00451e8e  ebb9                     jmp      0x451e49
00451e90  8b8683000000             mov      eax, dword ptr [esi + 0x83]
00451e96  c1f818                   sar      eax, 0x18
00451e99  85c0                     test     eax, eax
00451e9b  0f8560010000             jne      0x452001
00451ea1  8b8684000000             mov      eax, dword ptr [esi + 0x84]
00451ea7  c1f818                   sar      eax, 0x18
00451eaa  85c0                     test     eax, eax
00451eac  0f854f010000             jne      0x452001
00451eb2  0fb7ef                   movzx    ebp, di
00451eb5  31db                     xor      ebx, ebx
00451eb7  31d2                     xor      edx, edx
00451eb9  89e8                     mov      eax, ebp
00451ebb  668b9eb8000000           mov      bx, word ptr [esi + 0xb8]
00451ec2  8a96b7000000             mov      dl, byte ptr [esi + 0xb7]
00451ec8  e8e84dffff               call     0x446cb5
00451ecd  88c2                     mov      dl, al
00451ecf  89e8                     mov      eax, ebp
00451ed1  c1e004                   shl      eax, 4
00451ed4  01e8                     add      eax, ebp
00451ed6  c1e002                   shl      eax, 2
00451ed9  01e8                     add      eax, ebp
00451edb  c1e002                   shl      eax, 2
00451ede  84d2                     test     dl, dl
00451ee0  0f852a010000             jne      0x452010
00451ee6  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
00451eec  8d1c01                   lea      ebx, [ecx + eax]
00451eef  897c2430                 mov      dword ptr [esp + 0x30], edi
00451ef3  8a93b7000000             mov      dl, byte ptr [ebx + 0xb7]
00451ef9  b8ffff0000               mov      eax, 0xffff
00451efe  80fa03                   cmp      dl, 3
00451f01  0f829a000000             jb       0x451fa1
00451f07  7630                     jbe      0x451f39
00451f09  80fa05                   cmp      dl, 5
00451f0c  0f8486000000             je       0x451f98
00451f12  e993000000               jmp      0x451faa
00451f17  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00451f1e  31d2                     xor      edx, edx
00451f20  6689c2                   mov      dx, ax
00451f23  89d0                     mov      eax, edx
00451f25  c1e004                   shl      eax, 4
00451f28  01d0                     add      eax, edx
00451f2a  c1e002                   shl      eax, 2
00451f2d  01d0                     add      eax, edx
00451f2f  668b44817c               mov      ax, word ptr [ecx + eax*4 + 0x7c]
00451f34  e971000000               jmp      0x451faa
00451f39  31d2                     xor      edx, edx
00451f3b  8a93b0000000             mov      dl, byte ptr [ebx + 0xb0]
00451f41  85d2                     test     edx, edx
00451f43  7405                     je       0x451f4a
00451f45  83fa01                   cmp      edx, 1
00451f48  7531                     jne      0x451f7b
00451f4a  31d2                     xor      edx, edx
00451f4c  668b542430               mov      dx, word ptr [esp + 0x30]
00451f51  89d0                     mov      eax, edx
00451f53  c1e004                   shl      eax, 4
00451f56  01d0                     add      eax, edx
00451f58  c1e002                   shl      eax, 2
00451f5b  01d0                     add      eax, edx
00451f5d  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00451f63  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
00451f68  31d2                     xor      edx, edx
00451f6a  6689c2                   mov      dx, ax
00451f6d  31c0                     xor      eax, eax
00451f6f  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00451f76  e8251afdff               call     0x4239a0
00451f7b  31d2                     xor      edx, edx
00451f7d  6689c2                   mov      dx, ax
00451f80  81faffff0000             cmp      edx, 0xffff
00451f86  7522                     jne      0x451faa
00451f88  31c0                     xor      eax, eax
00451f8a  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00451f91  e84c8ffcff               call     0x41aee2
00451f96  eb12                     jmp      0x451faa
00451f98  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00451f9f  eb09                     jmp      0x451faa
00451fa1  80fa01                   cmp      dl, 1
00451fa4  0f846dffffff             je       0x451f17
00451faa  663b467e                 cmp      ax, word ptr [esi + 0x7e]
00451fae  7451                     je       0x452001
00451fb0  31d2                     xor      edx, edx
00451fb2  6689fa                   mov      dx, di
00451fb5  89d3                     mov      ebx, edx
00451fb7  c1e304                   shl      ebx, 4
00451fba  01d3                     add      ebx, edx
00451fbc  c1e302                   shl      ebx, 2
00451fbf  01d3                     add      ebx, edx
00451fc1  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00451fc7  c1e302                   shl      ebx, 2
00451fca  01da                     add      edx, ebx
00451fcc  6689427e                 mov      word ptr [edx + 0x7e], ax
00451fd0  663b3d04634900           cmp      di, word ptr [0x496304]
00451fd7  7521                     jne      0x451ffa
00451fd9  b8ffff0000               mov      eax, 0xffff
00451fde  30db                     xor      bl, bl
00451fe0  31c9                     xor      ecx, ecx
00451fe2  881d360f4e00             mov      byte ptr [0x4e0f36], bl
00451fe8  881d370f4e00             mov      byte ptr [0x4e0f37], bl
00451fee  890d3c0f4e00             mov      dword ptr [0x4e0f3c], ecx
00451ff4  66a304634900             mov      word ptr [0x496304], ax
00451ffa  c6828800000000           mov      byte ptr [edx + 0x88], 0
00452001  31c0                     xor      eax, eax
00452003  6689f8                   mov      ax, di
00452006  e80173ffff               call     0x44930c
0045200b  e9790c0000               jmp      0x452c89
00452010  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00452016  8a96b7000000             mov      dl, byte ptr [esi + 0xb7]
0045201c  668b440308               mov      ax, word ptr [ebx + eax + 8]
00452021  8854244c                 mov      byte ptr [esp + 0x4c], dl
00452025  89442414                 mov      dword ptr [esp + 0x14], eax
00452029  31c0                     xor      eax, eax
0045202b  8a44244c                 mov      al, byte ptr [esp + 0x4c]
0045202f  668b96b8000000           mov      dx, word ptr [esi + 0xb8]
00452036  83f801                   cmp      eax, 1
00452039  0f8599000000             jne      0x4520d8
0045203f  81e2ffff0000             and      edx, 0xffff
00452045  89d0                     mov      eax, edx
00452047  c1e004                   shl      eax, 4
0045204a  01d0                     add      eax, edx
0045204c  c1e002                   shl      eax, 2
0045204f  01d0                     add      eax, edx
00452051  c1e002                   shl      eax, 2
00452054  01d8                     add      eax, ebx
00452056  8a5001                   mov      dl, byte ptr [eax + 1]
00452059  81e2ff000000             and      edx, 0xff
0045205f  83fa10                   cmp      edx, 0x10
00452062  7574                     jne      0x4520d8
00452064  668b407c                 mov      ax, word ptr [eax + 0x7c]
00452068  31db                     xor      ebx, ebx
0045206a  6689c3                   mov      bx, ax
0045206d  89da                     mov      edx, ebx
0045206f  89d8                     mov      eax, ebx
00452071  c1fa1f                   sar      edx, 0x1f
00452074  c1e208                   shl      edx, 8
00452077  1bc2                     sbb      eax, edx
00452079  c1f808                   sar      eax, 8
0045207c  31c9                     xor      ecx, ecx
0045207e  bd00010000               mov      ebp, 0x100
00452083  6689c1                   mov      cx, ax
00452086  89da                     mov      edx, ebx
00452088  89d8                     mov      eax, ebx
0045208a  c1fa1f                   sar      edx, 0x1f
0045208d  f7fd                     idiv     ebp
0045208f  31c0                     xor      eax, eax
00452091  31db                     xor      ebx, ebx
00452093  6689d0                   mov      ax, dx
00452096  668b5c2414               mov      bx, word ptr [esp + 0x14]
0045209b  89442404                 mov      dword ptr [esp + 4], eax
0045209f  89da                     mov      edx, ebx
004520a1  89d8                     mov      eax, ebx
004520a3  c1fa1f                   sar      edx, 0x1f
004520a6  f7fd                     idiv     ebp
004520a8  0fb7e8                   movzx    ebp, ax
004520ab  89da                     mov      edx, ebx
004520ad  b800010000               mov      eax, 0x100
004520b2  c1fa1f                   sar      edx, 0x1f
004520b5  89442408                 mov      dword ptr [esp + 8], eax
004520b9  89d8                     mov      eax, ebx
004520bb  f77c2408                 idiv     dword ptr [esp + 8]
004520bf  31c0                     xor      eax, eax
004520c1  8b5c2404                 mov      ebx, dword ptr [esp + 4]
004520c5  6689d0                   mov      ax, dx
004520c8  89ea                     mov      edx, ebp
004520ca  e886740200               call     0x479555
004520cf  83f804                   cmp      eax, 4
004520d2  7704                     ja       0x4520d8
004520d4  30c0                     xor      al, al
004520d6  eb02                     jmp      0x4520da
004520d8  b001                     mov      al, 1
004520da  84c0                     test     al, al
004520dc  0f8587010000             jne      0x452269
004520e2  31c0                     xor      eax, eax
004520e4  6689f8                   mov      ax, di
004520e7  89c3                     mov      ebx, eax
004520e9  c1e304                   shl      ebx, 4
004520ec  01c3                     add      ebx, eax
004520ee  c1e302                   shl      ebx, 2
004520f1  01c3                     add      ebx, eax
004520f3  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
004520f9  c1e302                   shl      ebx, 2
004520fc  01cb                     add      ebx, ecx
004520fe  897c242c                 mov      dword ptr [esp + 0x2c], edi
00452102  8a93b7000000             mov      dl, byte ptr [ebx + 0xb7]
00452108  b8ffff0000               mov      eax, 0xffff
0045210d  80fa03                   cmp      dl, 3
00452110  0f829a000000             jb       0x4521b0
00452116  7630                     jbe      0x452148
00452118  80fa05                   cmp      dl, 5
0045211b  0f8486000000             je       0x4521a7
00452121  e993000000               jmp      0x4521b9
00452126  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
0045212d  31d2                     xor      edx, edx
0045212f  6689c2                   mov      dx, ax
00452132  89d0                     mov      eax, edx
00452134  c1e004                   shl      eax, 4
00452137  01d0                     add      eax, edx
00452139  c1e002                   shl      eax, 2
0045213c  01d0                     add      eax, edx
0045213e  668b44817c               mov      ax, word ptr [ecx + eax*4 + 0x7c]
00452143  e971000000               jmp      0x4521b9
00452148  31d2                     xor      edx, edx
0045214a  8a93b0000000             mov      dl, byte ptr [ebx + 0xb0]
00452150  85d2                     test     edx, edx
00452152  7405                     je       0x452159
00452154  83fa01                   cmp      edx, 1
00452157  7531                     jne      0x45218a
00452159  31d2                     xor      edx, edx
0045215b  668b54242c               mov      dx, word ptr [esp + 0x2c]
00452160  89d0                     mov      eax, edx
00452162  c1e004                   shl      eax, 4
00452165  01d0                     add      eax, edx
00452167  c1e002                   shl      eax, 2
0045216a  01d0                     add      eax, edx
0045216c  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00452172  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
00452177  31d2                     xor      edx, edx
00452179  6689c2                   mov      dx, ax
0045217c  31c0                     xor      eax, eax
0045217e  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00452185  e81618fdff               call     0x4239a0
0045218a  31d2                     xor      edx, edx
0045218c  6689c2                   mov      dx, ax
0045218f  81faffff0000             cmp      edx, 0xffff
00452195  7522                     jne      0x4521b9
00452197  31c0                     xor      eax, eax
00452199  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
004521a0  e83d8dfcff               call     0x41aee2
004521a5  eb12                     jmp      0x4521b9
004521a7  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
004521ae  eb09                     jmp      0x4521b9
004521b0  80fa01                   cmp      dl, 1
004521b3  0f846dffffff             je       0x452126
004521b9  668b5608                 mov      dx, word ptr [esi + 8]
004521bd  89c3                     mov      ebx, eax
004521bf  6639d0                   cmp      ax, dx
004521c2  7440                     je       0x452204
004521c4  31d2                     xor      edx, edx
004521c6  668b5608                 mov      dx, word ptr [esi + 8]
004521ca  25ffff0000               and      eax, 0xffff
004521cf  e86e4e0200               call     0x477042
004521d4  31d2                     xor      edx, edx
004521d6  88c2                     mov      dl, al
004521d8  31c0                     xor      eax, eax
004521da  668b4608                 mov      ax, word ptr [esi + 8]
004521de  e80b4f0200               call     0x4770ee
004521e3  31d2                     xor      edx, edx
004521e5  668b5608                 mov      dx, word ptr [esi + 8]
004521e9  25ffff0000               and      eax, 0xffff
004521ee  e84f4e0200               call     0x477042
004521f3  31d2                     xor      edx, edx
004521f5  88c2                     mov      dl, al
004521f7  31c0                     xor      eax, eax
004521f9  668b4608                 mov      ax, word ptr [esi + 8]
004521fd  e8ec4e0200               call     0x4770ee
00452202  89c3                     mov      ebx, eax
00452204  663b5e7e                 cmp      bx, word ptr [esi + 0x7e]
00452208  0f84f3fdffff             je       0x452001
0045220e  31d2                     xor      edx, edx
00452210  6689fa                   mov      dx, di
00452213  89d0                     mov      eax, edx
00452215  c1e004                   shl      eax, 4
00452218  01d0                     add      eax, edx
0045221a  c1e002                   shl      eax, 2
0045221d  01d0                     add      eax, edx
0045221f  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00452225  c1e002                   shl      eax, 2
00452228  01d0                     add      eax, edx
0045222a  6689587e                 mov      word ptr [eax + 0x7e], bx
0045222e  663b3d04634900           cmp      di, word ptr [0x496304]
00452235  7522                     jne      0x452259
00452237  30c9                     xor      cl, cl
00452239  baffff0000               mov      edx, 0xffff
0045223e  880d360f4e00             mov      byte ptr [0x4e0f36], cl
00452244  880d370f4e00             mov      byte ptr [0x4e0f37], cl
0045224a  31c9                     xor      ecx, ecx
0045224c  66891504634900           mov      word ptr [0x496304], dx
00452253  890d3c0f4e00             mov      dword ptr [0x4e0f3c], ecx
00452259  c6808800000000           mov      byte ptr [eax + 0x88], 0
00452260  e99cfdffff               jmp      0x452001
00452265  b001                     mov      al, 1
00452267  eb37                     jmp      0x4522a0
00452269  31d2                     xor      edx, edx
0045226b  6689fa                   mov      dx, di
0045226e  89d0                     mov      eax, edx
00452270  c1e004                   shl      eax, 4
00452273  01d0                     add      eax, edx
00452275  c1e002                   shl      eax, 2
00452278  01d0                     add      eax, edx
0045227a  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00452280  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
00452284  3c08                     cmp      al, 8
00452286  7212                     jb       0x45229a
00452288  76db                     jbe      0x452265
0045228a  3c0c                     cmp      al, 0xc
0045228c  7210                     jb       0x45229e
0045228e  76d5                     jbe      0x452265
00452290  3c16                     cmp      al, 0x16
00452292  720a                     jb       0x45229e
00452294  3c17                     cmp      al, 0x17
00452296  76cd                     jbe      0x452265
00452298  eb04                     jmp      0x45229e
0045229a  3c04                     cmp      al, 4
0045229c  74c7                     je       0x452265
0045229e  30c0                     xor      al, al
004522a0  84c0                     test     al, al
004522a2  0f85e1090000             jne      0x452c89
004522a8  31d2                     xor      edx, edx
004522aa  6689fa                   mov      dx, di
004522ad  89d0                     mov      eax, edx
004522af  c1e004                   shl      eax, 4
004522b2  01d0                     add      eax, edx
004522b4  c1e002                   shl      eax, 2
004522b7  01d0                     add      eax, edx
004522b9  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
004522bf  c1e002                   shl      eax, 2
004522c2  8d1c01                   lea      ebx, [ecx + eax]
004522c5  897c2410                 mov      dword ptr [esp + 0x10], edi
004522c9  8a93b7000000             mov      dl, byte ptr [ebx + 0xb7]
004522cf  b8ffff0000               mov      eax, 0xffff
004522d4  80fa03                   cmp      dl, 3
004522d7  0f829a000000             jb       0x452377
004522dd  7630                     jbe      0x45230f
004522df  80fa05                   cmp      dl, 5
004522e2  0f8486000000             je       0x45236e
004522e8  e993000000               jmp      0x452380
004522ed  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
004522f4  25ffff0000               and      eax, 0xffff
004522f9  89c3                     mov      ebx, eax
004522fb  c1e304                   shl      ebx, 4
004522fe  01c3                     add      ebx, eax
00452300  c1e302                   shl      ebx, 2
00452303  01c3                     add      ebx, eax
00452305  668b44997c               mov      ax, word ptr [ecx + ebx*4 + 0x7c]
0045230a  e971000000               jmp      0x452380
0045230f  31d2                     xor      edx, edx
00452311  8a93b0000000             mov      dl, byte ptr [ebx + 0xb0]
00452317  85d2                     test     edx, edx
00452319  7405                     je       0x452320
0045231b  83fa01                   cmp      edx, 1
0045231e  7531                     jne      0x452351
00452320  31d2                     xor      edx, edx
00452322  668b542410               mov      dx, word ptr [esp + 0x10]
00452327  89d0                     mov      eax, edx
00452329  c1e004                   shl      eax, 4
0045232c  01d0                     add      eax, edx
0045232e  c1e002                   shl      eax, 2
00452331  01d0                     add      eax, edx
00452333  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00452339  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
0045233e  31d2                     xor      edx, edx
00452340  6689c2                   mov      dx, ax
00452343  31c0                     xor      eax, eax
00452345  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
0045234c  e84f16fdff               call     0x4239a0
00452351  31d2                     xor      edx, edx
00452353  6689c2                   mov      dx, ax
00452356  81faffff0000             cmp      edx, 0xffff
0045235c  7522                     jne      0x452380
0045235e  31c0                     xor      eax, eax
00452360  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00452367  e8768bfcff               call     0x41aee2
0045236c  eb12                     jmp      0x452380
0045236e  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00452375  eb09                     jmp      0x452380
00452377  80fa01                   cmp      dl, 1
0045237a  0f846dffffff             je       0x4522ed
00452380  663b467e                 cmp      ax, word ptr [esi + 0x7e]
00452384  0f8477fcffff             je       0x452001
0045238a  31d2                     xor      edx, edx
0045238c  6689fa                   mov      dx, di
0045238f  89d3                     mov      ebx, edx
00452391  c1e304                   shl      ebx, 4
00452394  01d3                     add      ebx, edx
00452396  c1e302                   shl      ebx, 2
00452399  01d3                     add      ebx, edx
0045239b  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004523a1  c1e302                   shl      ebx, 2
004523a4  01da                     add      edx, ebx
004523a6  6689427e                 mov      word ptr [edx + 0x7e], ax
004523aa  663b3d04634900           cmp      di, word ptr [0x496304]
004523b1  0f8543fcffff             jne      0x451ffa
004523b7  30c0                     xor      al, al
004523b9  31f6                     xor      esi, esi
004523bb  a2360f4e00               mov      byte ptr [0x4e0f36], al
004523c0  89353c0f4e00             mov      dword ptr [0x4e0f3c], esi
004523c6  beffff0000               mov      esi, 0xffff
004523cb  a2370f4e00               mov      byte ptr [0x4e0f37], al
004523d0  66893504634900           mov      word ptr [0x496304], si
004523d7  e91efcffff               jmp      0x451ffa
004523dc  89d0                     mov      eax, edx
004523de  e8e155ffff               call     0x4479c4
004523e3  31c0                     xor      eax, eax
004523e5  8a86a9000000             mov      al, byte ptr [esi + 0xa9]
004523eb  85c0                     test     eax, eax
004523ed  0f8550000000             jne      0x452443
004523f3  8a86a4000000             mov      al, byte ptr [esi + 0xa4]
004523f9  3a467a                   cmp      al, byte ptr [esi + 0x7a]
004523fc  0f8401010000             je       0x452503
00452402  e93c000000               jmp      0x452443
00452407  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
0045240e  31d2                     xor      edx, edx
00452410  6689c2                   mov      dx, ax
00452413  89d0                     mov      eax, edx
00452415  c1e004                   shl      eax, 4
00452418  01d0                     add      eax, edx
0045241a  c1e002                   shl      eax, 2
0045241d  01d0                     add      eax, edx
0045241f  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00452425  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
0045242a  89442424                 mov      dword ptr [esp + 0x24], eax
0045242e  8a4602                   mov      al, byte ptr [esi + 2]
00452431  3c01                     cmp      al, 1
00452433  720e                     jb       0x452443
00452435  0f86ff000000             jbe      0x45253a
0045243b  3c18                     cmp      al, 0x18
0045243d  0f84bb050000             je       0x4529fe
00452443  31c0                     xor      eax, eax
00452445  8a86a9000000             mov      al, byte ptr [esi + 0xa9]
0045244b  85c0                     test     eax, eax
0045244d  0f8536080000             jne      0x452c89
00452453  8a86a4000000             mov      al, byte ptr [esi + 0xa4]
00452459  85c0                     test     eax, eax
0045245b  0f8528080000             jne      0x452c89
00452461  8aa68b000000             mov      ah, byte ptr [esi + 0x8b]
00452467  84e4                     test     ah, ah
00452469  0f84cb050000             je       0x452a3a
0045246f  88e2                     mov      dl, ah
00452471  31c0                     xor      eax, eax
00452473  feca                     dec      dl
00452475  8a4601                   mov      al, byte ptr [esi + 1]
00452478  88968b000000             mov      byte ptr [esi + 0x8b], dl
0045247e  83f803                   cmp      eax, 3
00452481  0f859e050000             jne      0x452a25
00452487  c686a400000005           mov      byte ptr [esi + 0xa4], 5
0045248e  e9f6070000               jmp      0x452c89
00452493  31d2                     xor      edx, edx
00452495  8a93b0000000             mov      dl, byte ptr [ebx + 0xb0]
0045249b  85d2                     test     edx, edx
0045249d  7405                     je       0x4524a4
0045249f  83fa01                   cmp      edx, 1
004524a2  752f                     jne      0x4524d3
004524a4  31d2                     xor      edx, edx
004524a6  6689ca                   mov      dx, cx
004524a9  89d0                     mov      eax, edx
004524ab  c1e004                   shl      eax, 4
004524ae  01d0                     add      eax, edx
004524b0  c1e002                   shl      eax, 2
004524b3  01d0                     add      eax, edx
004524b5  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004524bb  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
004524c0  31d2                     xor      edx, edx
004524c2  6689c2                   mov      dx, ax
004524c5  31c0                     xor      eax, eax
004524c7  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
004524ce  e8cd14fdff               call     0x4239a0
004524d3  31d2                     xor      edx, edx
004524d5  6689c2                   mov      dx, ax
004524d8  81faffff0000             cmp      edx, 0xffff
004524de  0f8546ffffff             jne      0x45242a
004524e4  31c0                     xor      eax, eax
004524e6  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
004524ed  e8f089fcff               call     0x41aee2
004524f2  e933ffffff               jmp      0x45242a
004524f7  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
004524fe  e927ffffff               jmp      0x45242a
00452503  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00452508  01c3                     add      ebx, eax
0045250a  89f9                     mov      ecx, edi
0045250c  8a93b7000000             mov      dl, byte ptr [ebx + 0xb7]
00452512  b8ffff0000               mov      eax, 0xffff
00452517  80fa03                   cmp      dl, 3
0045251a  7210                     jb       0x45252c
0045251c  0f8671ffffff             jbe      0x452493
00452522  80fa05                   cmp      dl, 5
00452525  74d0                     je       0x4524f7
00452527  e9fefeffff               jmp      0x45242a
0045252c  80fa01                   cmp      dl, 1
0045252f  0f84d2feffff             je       0x452407
00452535  e9f0feffff               jmp      0x45242a
0045253a  0fb7ef                   movzx    ebp, di
0045253d  89e8                     mov      eax, ebp
0045253f  c1e004                   shl      eax, 4
00452542  01e8                     add      eax, ebp
00452544  c1e002                   shl      eax, 2
00452547  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
0045254d  01e8                     add      eax, ebp
0045254f  89ea                     mov      edx, ebp
00452551  c1e002                   shl      eax, 2
00452554  31ea                     xor      edx, ebp
00452556  01c3                     add      ebx, eax
00452558  31c0                     xor      eax, eax
0045255a  8a1541805000             mov      dl, byte ptr [0x508041]
00452560  668b4308                 mov      ax, word ptr [ebx + 8]
00452564  e887410200               call     0x4766f0
00452569  84c0                     test     al, al
0045256b  7439                     je       0x4525a6
0045256d  89e8                     mov      eax, ebp
0045256f  e8e9e6feff               call     0x440c5d
00452574  8b8b04010000             mov      ecx, dword ptr [ebx + 0x104]
0045257a  c683f900000000           mov      byte ptr [ebx + 0xf9], 0
00452581  83f9ff                   cmp      ecx, -1
00452584  7520                     jne      0x4525a6
00452586  50                       push     eax
00452587  31d2                     xor      edx, edx
00452589  31c9                     xor      ecx, ecx
0045258b  8a5301                   mov      dl, byte ptr [ebx + 1]
0045258e  8d8304010000             lea      eax, [ebx + 0x104]
00452594  c1e210                   shl      edx, 0x10
00452597  89c3                     mov      ebx, eax
00452599  b850000000               mov      eax, 0x50
0045259e  80ce23                   or       dh, 0x23
004525a1  e8d3840300               call     0x48aa79
004525a6  31d2                     xor      edx, edx
004525a8  6689fa                   mov      dx, di
004525ab  89d0                     mov      eax, edx
004525ad  c1e004                   shl      eax, 4
004525b0  01d0                     add      eax, edx
004525b2  c1e002                   shl      eax, 2
004525b5  01d0                     add      eax, edx
004525b7  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004525bd  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
004525c1  3c0e                     cmp      al, 0xe
004525c3  720e                     jb       0x4525d3
004525c5  0f869b000000             jbe      0x452666
004525cb  3c10                     cmp      al, 0x10
004525cd  0f8493000000             je       0x452666
004525d3  30c0                     xor      al, al
004525d5  84c0                     test     al, al
004525d7  7431                     je       0x45260a
004525d9  31d2                     xor      edx, edx
004525db  6689fa                   mov      dx, di
004525de  89d0                     mov      eax, edx
004525e0  c1e004                   shl      eax, 4
004525e3  01d0                     add      eax, edx
004525e5  c1e002                   shl      eax, 2
004525e8  01c2                     add      edx, eax
004525ea  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
004525ef  c1e202                   shl      edx, 2
004525f2  01d0                     add      eax, edx
004525f4  31d2                     xor      edx, edx
004525f6  8a90da000000             mov      dl, byte ptr [eax + 0xda]
004525fc  85d2                     test     edx, edx
004525fe  740a                     je       0x45260a
00452600  88d5                     mov      ch, dl
00452602  fecd                     dec      ch
00452604  88a8da000000             mov      byte ptr [eax + 0xda], ch
0045260a  807e7800                 cmp      byte ptr [esi + 0x78], 0
0045260e  0f84d1020000             je       0x4528e5
00452614  31d2                     xor      edx, edx
00452616  8d442434                 lea      eax, [esp + 0x34]
0045261a  6689fa                   mov      dx, di
0045261d  890424                   mov      dword ptr [esp], eax
00452620  89d0                     mov      eax, edx
00452622  c1e004                   shl      eax, 4
00452625  01d0                     add      eax, edx
00452627  c1e002                   shl      eax, 2
0045262a  31c9                     xor      ecx, ecx
0045262c  01c2                     add      edx, eax
0045262e  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00452633  c1e202                   shl      edx, 2
00452636  66894c2420               mov      word ptr [esp + 0x20], cx
0045263b  01d0                     add      eax, edx
0045263d  66894c2434               mov      word ptr [esp + 0x34], cx
00452642  31db                     xor      ebx, ebx
00452644  8a5001                   mov      dl, byte ptr [eax + 1]
00452647  8d6c2420                 lea      ebp, [esp + 0x20]
0045264b  88d3                     mov      bl, dl
0045264d  88542444                 mov      byte ptr [esp + 0x44], dl
00452651  83fb01                   cmp      ebx, 1
00452654  0f845e000000             je       0x4526b8
0045265a  83fb15                   cmp      ebx, 0x15
0045265d  7459                     je       0x4526b8
0045265f  83fb0b                   cmp      ebx, 0xb
00452662  750d                     jne      0x452671
00452664  eb52                     jmp      0x4526b8
00452666  b001                     mov      al, 1
00452668  e968ffffff               jmp      0x4525d5
0045266d  b201                     mov      dl, 1
0045266f  eb0e                     jmp      0x45267f
00452671  80fa0c                   cmp      dl, 0xc
00452674  7207                     jb       0x45267d
00452676  76f5                     jbe      0x45266d
00452678  80fa0f                   cmp      dl, 0xf
0045267b  74f0                     je       0x45266d
0045267d  30d2                     xor      dl, dl
0045267f  84d2                     test     dl, dl
00452681  740d                     je       0x452690
00452683  31d2                     xor      edx, edx
00452685  8b0c24                   mov      ecx, dword ptr [esp]
00452688  8a9094000000             mov      dl, byte ptr [eax + 0x94]
0045268e  eb0b                     jmp      0x45269b
00452690  31d2                     xor      edx, edx
00452692  8b0c24                   mov      ecx, dword ptr [esp]
00452695  8a9091000000             mov      dl, byte ptr [eax + 0x91]
0045269b  31c0                     xor      eax, eax
0045269d  89eb                     mov      ebx, ebp
0045269f  8a442444                 mov      al, byte ptr [esp + 0x44]
004526a3  e8fdeaffff               call     0x4511a5
004526a8  8b1c24                   mov      ebx, dword ptr [esp]
004526ab  31c0                     xor      eax, eax
004526ad  89ea                     mov      edx, ebp
004526af  8a442444                 mov      al, byte ptr [esp + 0x44]
004526b3  e814e9fbff               call     0x410fcc
004526b8  8a8691000000             mov      al, byte ptr [esi + 0x91]
004526be  88442448                 mov      byte ptr [esp + 0x48], al
004526c2  31c0                     xor      eax, eax
004526c4  8a4601                   mov      al, byte ptr [esi + 1]
004526c7  83f80b                   cmp      eax, 0xb
004526ca  756e                     jne      0x45273a
004526cc  31db                     xor      ebx, ebx
004526ce  668b5c2424               mov      bx, word ptr [esp + 0x24]
004526d3  89da                     mov      edx, ebx
004526d5  89d8                     mov      eax, ebx
004526d7  c1fa1f                   sar      edx, 0x1f
004526da  c1e208                   shl      edx, 8
004526dd  1bc2                     sbb      eax, edx
004526df  c1f808                   sar      eax, 8
004526e2  31c9                     xor      ecx, ecx
004526e4  bd00010000               mov      ebp, 0x100
004526e9  6689c1                   mov      cx, ax
004526ec  89da                     mov      edx, ebx
004526ee  89d8                     mov      eax, ebx
004526f0  c1fa1f                   sar      edx, 0x1f
004526f3  f7fd                     idiv     ebp
004526f5  31c0                     xor      eax, eax
004526f7  31db                     xor      ebx, ebx
004526f9  6689d0                   mov      ax, dx
004526fc  668b5e08                 mov      bx, word ptr [esi + 8]
00452700  89442404                 mov      dword ptr [esp + 4], eax
00452704  89da                     mov      edx, ebx
00452706  89d8                     mov      eax, ebx
00452708  c1fa1f                   sar      edx, 0x1f
0045270b  f7fd                     idiv     ebp
0045270d  0fb7e8                   movzx    ebp, ax
00452710  89da                     mov      edx, ebx
00452712  b800010000               mov      eax, 0x100
00452717  c1fa1f                   sar      edx, 0x1f
0045271a  89442408                 mov      dword ptr [esp + 8], eax
0045271e  89d8                     mov      eax, ebx
00452720  f77c2408                 idiv     dword ptr [esp + 8]
00452724  6a20                     push     0x20
00452726  31c0                     xor      eax, eax
00452728  8b5c2408                 mov      ebx, dword ptr [esp + 8]
0045272c  6689d0                   mov      ax, dx
0045272f  89ea                     mov      edx, ebp
00452731  e8956f0200               call     0x4796cb
00452736  88442448                 mov      byte ptr [esp + 0x48], al
0045273a  31c0                     xor      eax, eax
0045273c  8a4601                   mov      al, byte ptr [esi + 1]
0045273f  83f803                   cmp      eax, 3
00452742  0f848e000000             je       0x4527d6
00452748  83f819                   cmp      eax, 0x19
0045274b  0f8485000000             je       0x4527d6
00452751  31c0                     xor      eax, eax
00452753  8a86b7000000             mov      al, byte ptr [esi + 0xb7]
00452759  30db                     xor      bl, bl
0045275b  83f801                   cmp      eax, 1
0045275e  7406                     je       0x452766
00452760  eb36                     jmp      0x452798
00452762  b001                     mov      al, 1
00452764  eb2c                     jmp      0x452792
00452766  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
0045276d  31d2                     xor      edx, edx
0045276f  6689c2                   mov      dx, ax
00452772  89d0                     mov      eax, edx
00452774  c1e004                   shl      eax, 4
00452777  01d0                     add      eax, edx
00452779  c1e002                   shl      eax, 2
0045277c  01d0                     add      eax, edx
0045277e  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00452784  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
00452788  3c10                     cmp      al, 0x10
0045278a  7204                     jb       0x452790
0045278c  3c11                     cmp      al, 0x11
0045278e  76d2                     jbe      0x452762
00452790  30c0                     xor      al, al
00452792  84c0                     test     al, al
00452794  7402                     je       0x452798
00452796  b301                     mov      bl, 1
00452798  31c0                     xor      eax, eax
0045279a  88d8                     mov      al, bl
0045279c  50                       push     eax
0045279d  8b442436                 mov      eax, dword ptr [esp + 0x36]
004527a1  c1f810                   sar      eax, 0x10
004527a4  50                       push     eax
004527a5  8b442426                 mov      eax, dword ptr [esp + 0x26]
004527a9  c1f810                   sar      eax, 0x10
004527ac  50                       push     eax
004527ad  31c0                     xor      eax, eax
004527af  b901000000               mov      ecx, 1
004527b4  8a442454                 mov      al, byte ptr [esp + 0x54]
004527b8  31d2                     xor      edx, edx
004527ba  50                       push     eax
004527bb  31c0                     xor      eax, eax
004527bd  668b5608                 mov      dx, word ptr [esi + 8]
004527c1  6689f8                   mov      ax, di
004527c4  31db                     xor      ebx, ebx
004527c6  50                       push     eax
004527c7  31c0                     xor      eax, eax
004527c9  668b5c2438               mov      bx, word ptr [esp + 0x38]
004527ce  8a4679                   mov      al, byte ptr [esi + 0x79]
004527d1  e876bc0100               call     0x46e44c
004527d6  31c0                     xor      eax, eax
004527d8  8a4601                   mov      al, byte ptr [esi + 1]
004527db  83f80b                   cmp      eax, 0xb
004527de  7405                     je       0x4527e5
004527e0  83f803                   cmp      eax, 3
004527e3  7530                     jne      0x452815
004527e5  6a00                     push     0
004527e7  6a00                     push     0
004527e9  31c0                     xor      eax, eax
004527eb  6a00                     push     0
004527ed  8a442454                 mov      al, byte ptr [esp + 0x54]
004527f1  b901000000               mov      ecx, 1
004527f6  50                       push     eax
004527f7  31c0                     xor      eax, eax
004527f9  31d2                     xor      edx, edx
004527fb  6689f8                   mov      ax, di
004527fe  668b542434               mov      dx, word ptr [esp + 0x34]
00452803  50                       push     eax
00452804  89d3                     mov      ebx, edx
00452806  b81a000000               mov      eax, 0x1a
0045280b  e83cbc0100               call     0x46e44c
00452810  e92efcffff               jmp      0x452443
00452815  83f819                   cmp      eax, 0x19
00452818  0f8525fcffff             jne      0x452443
0045281e  6a00                     push     0
00452820  6a00                     push     0
00452822  31c0                     xor      eax, eax
00452824  6a00                     push     0
00452826  8a442454                 mov      al, byte ptr [esp + 0x54]
0045282a  b901000000               mov      ecx, 1
0045282f  50                       push     eax
00452830  31c0                     xor      eax, eax
00452832  31d2                     xor      edx, edx
00452834  6689f8                   mov      ax, di
00452837  668b542434               mov      dx, word ptr [esp + 0x34]
0045283c  50                       push     eax
0045283d  89d3                     mov      ebx, edx
0045283f  b821000000               mov      eax, 0x21
00452844  ebc5                     jmp      0x45280b
00452846  66c7020100               mov      word ptr [edx], 1
0045284b  66c7030100               mov      word ptr [ebx], 1
00452850  31c0                     xor      eax, eax
00452852  668b44240c               mov      ax, word ptr [esp + 0xc]
00452857  83f802                   cmp      eax, 2
0045285a  0f8510000000             jne      0x452870
00452860  31c0                     xor      eax, eax
00452862  668b442428               mov      ax, word ptr [esp + 0x28]
00452867  83f802                   cmp      eax, 2
0045286a  0f843f010000             je       0x4529af
00452870  31d2                     xor      edx, edx
00452872  31c0                     xor      eax, eax
00452874  8a9691000000             mov      dl, byte ptr [esi + 0x91]
0045287a  668b4608                 mov      ax, word ptr [esi + 8]
0045287e  e86b480200               call     0x4770ee
00452883  8944243c                 mov      dword ptr [esp + 0x3c], eax
00452887  31c0                     xor      eax, eax
00452889  8a4601                   mov      al, byte ptr [esi + 1]
0045288c  83f810                   cmp      eax, 0x10
0045288f  7526                     jne      0x4528b7
00452891  6a00                     push     0
00452893  6a00                     push     0
00452895  b901000000               mov      ecx, 1
0045289a  6a00                     push     0
0045289c  31c0                     xor      eax, eax
0045289e  31d2                     xor      edx, edx
004528a0  6a00                     push     0
004528a2  6689f8                   mov      ax, di
004528a5  668b54244c               mov      dx, word ptr [esp + 0x4c]
004528aa  50                       push     eax
004528ab  89d3                     mov      ebx, edx
004528ad  b808000000               mov      eax, 8
004528b2  e895bb0100               call     0x46e44c
004528b7  6a00                     push     0
004528b9  ba01000000               mov      edx, 1
004528be  31db                     xor      ebx, ebx
004528c0  31c0                     xor      eax, eax
004528c2  31c9                     xor      ecx, ecx
004528c4  668b442440               mov      ax, word ptr [esp + 0x40]
004528c9  6689fb                   mov      bx, di
004528cc  e8a3dfffff               call     0x450874
004528d1  e96dfbffff               jmp      0x452443
004528d6  66c7020200               mov      word ptr [edx], 2
004528db  66c7030200               mov      word ptr [ebx], 2
004528e0  e96bffffff               jmp      0x452850
004528e5  0fb7ef                   movzx    ebp, di
004528e8  89e8                     mov      eax, ebp
004528ea  c1e004                   shl      eax, 4
004528ed  01e8                     add      eax, ebp
004528ef  c1e002                   shl      eax, 2
004528f2  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
004528f8  01e8                     add      eax, ebp
004528fa  8d54240c                 lea      edx, [esp + 0xc]
004528fe  8a448101                 mov      al, byte ptr [ecx + eax*4 + 1]
00452902  8d5c2428                 lea      ebx, [esp + 0x28]
00452906  3c19                     cmp      al, 0x19
00452908  0f8742ffffff             ja       0x452850
0045290e  25ff000000               and      eax, 0xff
00452913  2eff24859c184500         jmp      dword ptr cs:[eax*4 + 0x45189c]
0045291b  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00452922  31d2                     xor      edx, edx
00452924  6689c2                   mov      dx, ax
00452927  89d0                     mov      eax, edx
00452929  c1e004                   shl      eax, 4
0045292c  01d0                     add      eax, edx
0045292e  c1e002                   shl      eax, 2
00452931  01d0                     add      eax, edx
00452933  668b44817c               mov      ax, word ptr [ecx + eax*4 + 0x7c]
00452938  e946ffffff               jmp      0x452883
0045293d  31d2                     xor      edx, edx
0045293f  8a93b0000000             mov      dl, byte ptr [ebx + 0xb0]
00452945  85d2                     test     edx, edx
00452947  7405                     je       0x45294e
00452949  83fa01                   cmp      edx, 1
0045294c  7531                     jne      0x45297f
0045294e  31d2                     xor      edx, edx
00452950  668b54241c               mov      dx, word ptr [esp + 0x1c]
00452955  89d0                     mov      eax, edx
00452957  c1e004                   shl      eax, 4
0045295a  01d0                     add      eax, edx
0045295c  c1e002                   shl      eax, 2
0045295f  01d0                     add      eax, edx
00452961  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00452967  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
0045296c  31d2                     xor      edx, edx
0045296e  6689c2                   mov      dx, ax
00452971  31c0                     xor      eax, eax
00452973  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
0045297a  e82110fdff               call     0x4239a0
0045297f  31d2                     xor      edx, edx
00452981  6689c2                   mov      dx, ax
00452984  81faffff0000             cmp      edx, 0xffff
0045298a  0f85f3feffff             jne      0x452883
00452990  31c0                     xor      eax, eax
00452992  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
00452999  e84485fcff               call     0x41aee2
0045299e  e9e0feffff               jmp      0x452883
004529a3  668b83b8000000           mov      ax, word ptr [ebx + 0xb8]
004529aa  e9d4feffff               jmp      0x452883
004529af  31d2                     xor      edx, edx
004529b1  6689fa                   mov      dx, di
004529b4  89d0                     mov      eax, edx
004529b6  c1e004                   shl      eax, 4
004529b9  01d0                     add      eax, edx
004529bb  c1e002                   shl      eax, 2
004529be  01d0                     add      eax, edx
004529c0  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
004529c6  c1e002                   shl      eax, 2
004529c9  8d1c01                   lea      ebx, [ecx + eax]
004529cc  897c241c                 mov      dword ptr [esp + 0x1c], edi
004529d0  8a93b7000000             mov      dl, byte ptr [ebx + 0xb7]
004529d6  b8ffff0000               mov      eax, 0xffff
004529db  80fa03                   cmp      dl, 3
004529de  7210                     jb       0x4529f0
004529e0  0f8657ffffff             jbe      0x45293d
004529e6  80fa05                   cmp      dl, 5
004529e9  74b8                     je       0x4529a3
004529eb  e993feffff               jmp      0x452883
004529f0  80fa01                   cmp      dl, 1
004529f3  0f8422ffffff             je       0x45291b
004529f9  e985feffff               jmp      0x452883
004529fe  0fb7ef                   movzx    ebp, di
00452a01  31db                     xor      ebx, ebx
00452a03  31d2                     xor      edx, edx
00452a05  89e8                     mov      eax, ebp
00452a07  668b9eb8000000           mov      bx, word ptr [esi + 0xb8]
00452a0e  8a96f4000000             mov      dl, byte ptr [esi + 0xf4]
00452a14  e8f70a0200               call     0x473510
00452a19  89e8                     mov      eax, ebp
00452a1b  e85c0bffff               call     0x44357c
00452a20  e91efaffff               jmp      0x452443
00452a25  83f80b                   cmp      eax, 0xb
00452a28  0f855b020000             jne      0x452c89
00452a2e  c686a400000000           mov      byte ptr [esi + 0xa4], 0
00452a35  e94f020000               jmp      0x452c89
00452a3a  88a68a000000             mov      byte ptr [esi + 0x8a], ah
00452a40  31c0                     xor      eax, eax
00452a42  8a4601                   mov      al, byte ptr [esi + 1]
00452a45  83f810                   cmp      eax, 0x10
00452a48  7407                     je       0x452a51
00452a4a  c686a400000000           mov      byte ptr [esi + 0xa4], 0
00452a51  66c786020100000000       mov      word ptr [esi + 0x102], 0
00452a5a  e92a020000               jmp      0x452c89
00452a5f  89d0                     mov      eax, edx
00452a61  e8c950ffff               call     0x447b2f
00452a66  eb4c                     jmp      0x452ab4
00452a68  8ab6a9000000             mov      dh, byte ptr [esi + 0xa9]
00452a6e  fec6                     inc      dh
00452a70  8a9ea7000000             mov      bl, byte ptr [esi + 0xa7]
00452a76  88b6a9000000             mov      byte ptr [esi + 0xa9], dh
00452a7c  38de                     cmp      dh, bl
00452a7e  7534                     jne      0x452ab4
00452a80  31d2                     xor      edx, edx
00452a82  8a96a4000000             mov      dl, byte ptr [esi + 0xa4]
00452a88  31db                     xor      ebx, ebx
00452a8a  42                       inc      edx
00452a8b  8a9ea5000000             mov      bl, byte ptr [esi + 0xa5]
00452a91  89d0                     mov      eax, edx
00452a93  c1fa1f                   sar      edx, 0x1f
00452a96  f7fb                     idiv     ebx
00452a98  c686a900000000           mov      byte ptr [esi + 0xa9], 0
00452a9f  8896a4000000             mov      byte ptr [esi + 0xa4], dl
00452aa5  eb0d                     jmp      0x452ab4
00452aa7  8a4601                   mov      al, byte ptr [esi + 1]
00452aaa  3c10                     cmp      al, 0x10
00452aac  7206                     jb       0x452ab4
00452aae  76b8                     jbe      0x452a68
00452ab0  3c11                     cmp      al, 0x11
00452ab2  74ab                     je       0x452a5f
00452ab4  31c0                     xor      eax, eax
00452ab6  8a868b000000             mov      al, byte ptr [esi + 0x8b]
00452abc  83f801                   cmp      eax, 1
00452abf  7518                     jne      0x452ad9
00452ac1  31c0                     xor      eax, eax
00452ac3  8a4601                   mov      al, byte ptr [esi + 1]
00452ac6  83f810                   cmp      eax, 0x10
00452ac9  740e                     je       0x452ad9
00452acb  c686a400000000           mov      byte ptr [esi + 0xa4], 0
00452ad2  c686a900000000           mov      byte ptr [esi + 0xa9], 0
00452ad9  8abe8b000000             mov      bh, byte ptr [esi + 0x8b]
00452adf  31c0                     xor      eax, eax
00452ae1  fecf                     dec      bh
00452ae3  88f8                     mov      al, bh
00452ae5  88be8b000000             mov      byte ptr [esi + 0x8b], bh
00452aeb  85c0                     test     eax, eax
00452aed  0f8596010000             jne      0x452c89
00452af3  8a4601                   mov      al, byte ptr [esi + 1]
00452af6  c6868a00000001           mov      byte ptr [esi + 0x8a], 1
00452afd  83f810                   cmp      eax, 0x10
00452b00  740e                     je       0x452b10
00452b02  c686a400000000           mov      byte ptr [esi + 0xa4], 0
00452b09  c686a900000000           mov      byte ptr [esi + 0xa9], 0
00452b10  31c0                     xor      eax, eax
00452b12  6689f8                   mov      ax, di
00452b15  89c3                     mov      ebx, eax
00452b17  c1e304                   shl      ebx, 4
00452b1a  01c3                     add      ebx, eax
00452b1c  c1e302                   shl      ebx, 2
00452b1f  01c3                     add      ebx, eax
00452b21  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00452b26  8a449801                 mov      al, byte ptr [eax + ebx*4 + 1]
00452b2a  3c0e                     cmp      al, 0xe
00452b2c  7206                     jb       0x452b34
00452b2e  7648                     jbe      0x452b78
00452b30  3c10                     cmp      al, 0x10
00452b32  7444                     je       0x452b78
00452b34  30c0                     xor      al, al
00452b36  84c0                     test     al, al
00452b38  0f8513f3ffff             jne      0x451e51
00452b3e  0fb7ef                   movzx    ebp, di
00452b41  31db                     xor      ebx, ebx
00452b43  31d2                     xor      edx, edx
00452b45  89e8                     mov      eax, ebp
00452b47  668b9eb8000000           mov      bx, word ptr [esi + 0xb8]
00452b4e  8a96b7000000             mov      dl, byte ptr [esi + 0xb7]
00452b54  e85c41ffff               call     0x446cb5
00452b59  84c0                     test     al, al
00452b5b  740f                     je       0x452b6c
00452b5d  89e8                     mov      eax, ebp
00452b5f  e800e9ffff               call     0x451464
00452b64  84c0                     test     al, al
00452b66  0f851d010000             jne      0x452c89
00452b6c  c6868a00000000           mov      byte ptr [esi + 0x8a], 0
00452b73  e911010000               jmp      0x452c89
00452b78  b001                     mov      al, 1
00452b7a  ebba                     jmp      0x452b36
00452b7c  31c0                     xor      eax, eax
00452b7e  8a4601                   mov      al, byte ptr [esi + 1]
00452b81  83f810                   cmp      eax, 0x10
00452b84  7411                     je       0x452b97
00452b86  e96a000000               jmp      0x452bf5
00452b8b  89d0                     mov      eax, edx
00452b8d  e89d4fffff               call     0x447b2f
00452b92  e95e000000               jmp      0x452bf5
00452b97  89f3                     mov      ebx, esi
00452b99  3c08                     cmp      al, 8
00452b9b  7220                     jb       0x452bbd
00452b9d  7620                     jbe      0x452bbf
00452b9f  3c12                     cmp      al, 0x12
00452ba1  7210                     jb       0x452bb3
00452ba3  761a                     jbe      0x452bbf
00452ba5  3c17                     cmp      al, 0x17
00452ba7  7216                     jb       0x452bbf
00452ba9  3c18                     cmp      al, 0x18
00452bab  7612                     jbe      0x452bbf
00452bad  3c19                     cmp      al, 0x19
00452baf  740e                     je       0x452bbf
00452bb1  eb42                     jmp      0x452bf5
00452bb3  3c0a                     cmp      al, 0xa
00452bb5  7608                     jbe      0x452bbf
00452bb7  3c11                     cmp      al, 0x11
00452bb9  74d0                     je       0x452b8b
00452bbb  eb38                     jmp      0x452bf5
00452bbd  3c04                     cmp      al, 4
00452bbf  b824000000               mov      eax, 0x24
00452bc4  b9c8000000               mov      ecx, 0xc8
00452bc9  31d2                     xor      edx, edx
00452bcb  e80cd90100               call     0x4704dc
00452bd0  f7f1                     div      ecx
00452bd2  85d2                     test     edx, edx
00452bd4  751f                     jne      0x452bf5
00452bd6  8a9391000000             mov      dl, byte ptr [ebx + 0x91]
00452bdc  b910000000               mov      ecx, 0x10
00452be1  89d0                     mov      eax, edx
00452be3  c1fa1f                   sar      edx, 0x1f
00452be6  f7f9                     idiv     ecx
00452be8  42                       inc      edx
00452be9  889390000000             mov      byte ptr [ebx + 0x90], dl
00452bef  889391000000             mov      byte ptr [ebx + 0x91], dl
00452bf5  31d2                     xor      edx, edx
00452bf7  6689fa                   mov      dx, di
00452bfa  89d0                     mov      eax, edx
00452bfc  c1e004                   shl      eax, 4
00452bff  01d0                     add      eax, edx
00452c01  c1e002                   shl      eax, 2
00452c04  b107                     mov      cl, 7
00452c06  01c2                     add      edx, eax
00452c08  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00452c0d  c1e202                   shl      edx, 2
00452c10  89fb                     mov      ebx, edi
00452c12  8a440202                 mov      al, byte ptr [edx + eax + 2]
00452c16  25ff000000               and      eax, 0xff
00452c1b  7409                     je       0x452c26
00452c1d  83f804                   cmp      eax, 4
00452c20  7404                     je       0x452c26
00452c22  b001                     mov      al, 1
00452c24  eb02                     jmp      0x452c28
00452c26  30c0                     xor      al, al
00452c28  84c0                     test     al, al
00452c2a  7446                     je       0x452c72
00452c2c  31d2                     xor      edx, edx
00452c2e  6689da                   mov      dx, bx
00452c31  89d0                     mov      eax, edx
00452c33  c1e004                   shl      eax, 4
00452c36  01d0                     add      eax, edx
00452c38  c1e002                   shl      eax, 2
00452c3b  01d0                     add      eax, edx
00452c3d  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00452c43  884c8202                 mov      byte ptr [edx + eax*4 + 2], cl
00452c47  663b1d04634900           cmp      bx, word ptr [0x496304]
00452c4e  7522                     jne      0x452c72
00452c50  bbffff0000               mov      ebx, 0xffff
00452c55  30e4                     xor      ah, ah
00452c57  31d2                     xor      edx, edx
00452c59  8825360f4e00             mov      byte ptr [0x4e0f36], ah
00452c5f  8825370f4e00             mov      byte ptr [0x4e0f37], ah
00452c65  89153c0f4e00             mov      dword ptr [0x4e0f3c], edx
00452c6b  66891d04634900           mov      word ptr [0x496304], bx
00452c72  66c786b8000000ffff       mov      word ptr [esi + 0xb8], 0xffff
00452c7b  c686a400000000           mov      byte ptr [esi + 0xa4], 0
00452c82  c686a900000000           mov      byte ptr [esi + 0xa9], 0
00452c89  83c450                   add      esp, 0x50
00452c8c  e90cc6ffff               jmp      0x44f29d
00452c91  30c0                     xor      al, al
00452c93  c3                       ret
