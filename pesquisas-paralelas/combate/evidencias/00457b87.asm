; EnginSetType; intervalo [0x00457b87, 0x00457e0c)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00457b87  56                       push     esi
00457b88  57                       push     edi
00457b89  83ec0c                   sub      esp, 0xc
00457b8c  89d6                     mov      esi, edx
00457b8e  884c2404                 mov      byte ptr [esp + 4], cl
00457b92  31c9                     xor      ecx, ecx
00457b94  6689c1                   mov      cx, ax
00457b97  89ca                     mov      edx, ecx
00457b99  c1e204                   shl      edx, 4
00457b9c  01ca                     add      edx, ecx
00457b9e  c1e202                   shl      edx, 2
00457ba1  01d1                     add      ecx, edx
00457ba3  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00457ba9  c1e102                   shl      ecx, 2
00457bac  01ca                     add      edx, ecx
00457bae  66897208                 mov      word ptr [edx + 8], si
00457bb2  6689727c                 mov      word ptr [edx + 0x7c], si
00457bb6  8b3da0194e00             mov      edi, dword ptr [0x4e19a0]
00457bbc  01f9                     add      ecx, edi
00457bbe  6689717e                 mov      word ptr [ecx + 0x7e], si
00457bc2  663b0504634900           cmp      ax, word ptr [0x496304]
00457bc9  7522                     jne      0x457bed
00457bcb  bfffff0000               mov      edi, 0xffff
00457bd0  30ff                     xor      bh, bh
00457bd2  31f6                     xor      esi, esi
00457bd4  883d360f4e00             mov      byte ptr [0x4e0f36], bh
00457bda  883d370f4e00             mov      byte ptr [0x4e0f37], bh
00457be0  89353c0f4e00             mov      dword ptr [0x4e0f3c], esi
00457be6  66893d04634900           mov      word ptr [0x496304], di
00457bed  c6818800000000           mov      byte ptr [ecx + 0x88], 0
00457bf4  66c782b2000000ffff       mov      word ptr [edx + 0xb2], 0xffff
00457bfd  c682ab00000000           mov      byte ptr [edx + 0xab], 0
00457c04  c6829700000000           mov      byte ptr [edx + 0x97], 0
00457c0b  c6829500000000           mov      byte ptr [edx + 0x95], 0
00457c12  c6829600000000           mov      byte ptr [edx + 0x96], 0
00457c19  c6829200000000           mov      byte ptr [edx + 0x92], 0
00457c20  c6828600000000           mov      byte ptr [edx + 0x86], 0
00457c27  c6828700000000           mov      byte ptr [edx + 0x87], 0
00457c2e  c682b600000000           mov      byte ptr [edx + 0xb6], 0
00457c35  c682aa00000000           mov      byte ptr [edx + 0xaa], 0
00457c3c  c6829c00000063           mov      byte ptr [edx + 0x9c], 0x63
00457c43  c682a400000000           mov      byte ptr [edx + 0xa4], 0
00457c4a  c682a900000000           mov      byte ptr [edx + 0xa9], 0
00457c51  c6829e00000000           mov      byte ptr [edx + 0x9e], 0
00457c58  66c782b8000000ffff       mov      word ptr [edx + 0xb8], 0xffff
00457c61  66c7828c0000000000       mov      word ptr [edx + 0x8c], 0
00457c6a  c6828e00000000           mov      byte ptr [edx + 0x8e], 0
00457c71  889a90000000             mov      byte ptr [edx + 0x90], bl
00457c77  889a91000000             mov      byte ptr [edx + 0x91], bl
00457c7d  b107                     mov      cl, 7
00457c7f  889a94000000             mov      byte ptr [edx + 0x94], bl
00457c85  884c2408                 mov      byte ptr [esp + 8], cl
00457c89  31c9                     xor      ecx, ecx
00457c8b  8a5c2404                 mov      bl, byte ptr [esp + 4]
00457c8f  6689c1                   mov      cx, ax
00457c92  885a01                   mov      byte ptr [edx + 1], bl
00457c95  89cb                     mov      ebx, ecx
00457c97  c6828800000000           mov      byte ptr [edx + 0x88], 0
00457c9e  c1e304                   shl      ebx, 4
00457ca1  c6828b00000000           mov      byte ptr [edx + 0x8b], 0
00457ca8  01cb                     add      ebx, ecx
00457caa  c682bc00000000           mov      byte ptr [edx + 0xbc], 0
00457cb1  c1e302                   shl      ebx, 2
00457cb4  c682bd00000000           mov      byte ptr [edx + 0xbd], 0
00457cbb  01d9                     add      ecx, ebx
00457cbd  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00457cc3  c1e102                   shl      ecx, 2
00457cc6  89c6                     mov      esi, eax
00457cc8  8a5c1902                 mov      bl, byte ptr [ecx + ebx + 2]
00457ccc  81e3ff000000             and      ebx, 0xff
00457cd2  7409                     je       0x457cdd
00457cd4  83fb04                   cmp      ebx, 4
00457cd7  7404                     je       0x457cdd
00457cd9  b301                     mov      bl, 1
00457cdb  eb02                     jmp      0x457cdf
00457cdd  30db                     xor      bl, bl
00457cdf  84db                     test     bl, bl
00457ce1  744e                     je       0x457d31
00457ce3  31c9                     xor      ecx, ecx
00457ce5  6689f1                   mov      cx, si
00457ce8  89cb                     mov      ebx, ecx
00457cea  c1e304                   shl      ebx, 4
00457ced  01cb                     add      ebx, ecx
00457cef  c1e302                   shl      ebx, 2
00457cf2  01cb                     add      ebx, ecx
00457cf4  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
00457cfa  c1e302                   shl      ebx, 2
00457cfd  01cb                     add      ebx, ecx
00457cff  8a4c2408                 mov      cl, byte ptr [esp + 8]
00457d03  884b02                   mov      byte ptr [ebx + 2], cl
00457d06  663b3504634900           cmp      si, word ptr [0x496304]
00457d0d  7522                     jne      0x457d31
00457d0f  30ed                     xor      ch, ch
00457d11  31ff                     xor      edi, edi
00457d13  882d360f4e00             mov      byte ptr [0x4e0f36], ch
00457d19  882d370f4e00             mov      byte ptr [0x4e0f37], ch
00457d1f  b9ffff0000               mov      ecx, 0xffff
00457d24  893d3c0f4e00             mov      dword ptr [0x4e0f3c], edi
00457d2a  66890d04634900           mov      word ptr [0x496304], cx
00457d31  0fb6742404               movzx    esi, byte ptr [esp + 4]
00457d36  89f3                     mov      ebx, esi
00457d38  c1e302                   shl      ebx, 2
00457d3b  29f3                     sub      ebx, esi
00457d3d  c1e303                   shl      ebx, 3
00457d40  66c742040400             mov      word ptr [edx + 4], 4
00457d46  01f3                     add      ebx, esi
00457d48  66c742740000             mov      word ptr [edx + 0x74], 0
00457d4e  8a0c5dd8654900           mov      cl, byte ptr [ebx*2 + 0x4965d8]
00457d55  888abb000000             mov      byte ptr [edx + 0xbb], cl
00457d5b  8a1c5dda654900           mov      bl, byte ptr [ebx*2 + 0x4965da]
00457d62  66c742760400             mov      word ptr [edx + 0x76], 4
00457d68  c6420604                 mov      byte ptr [edx + 6], 4
00457d6c  31c9                     xor      ecx, ecx
00457d6e  66c782c20000000000       mov      word ptr [edx + 0xc2], 0
00457d77  6689c1                   mov      cx, ax
00457d7a  c6427800                 mov      byte ptr [edx + 0x78], 0
00457d7e  89c8                     mov      eax, ecx
00457d80  889ab0000000             mov      byte ptr [edx + 0xb0], bl
00457d86  e8c5f5ffff               call     0x457350
00457d8b  89f0                     mov      eax, esi
00457d8d  31db                     xor      ebx, ebx
00457d8f  e818f8feff               call     0x4475ac
00457d94  89c6                     mov      esi, eax
00457d96  31c0                     xor      eax, eax
00457d98  8a5a01                   mov      bl, byte ptr [edx + 1]
00457d9b  8a02                     mov      al, byte ptr [edx]
00457d9d  ba01000000               mov      edx, 1
00457da2  e8190ffdff               call     0x428cc0
00457da7  89ca                     mov      edx, ecx
00457da9  c1e204                   shl      edx, 4
00457dac  01ca                     add      edx, ecx
00457dae  89f3                     mov      ebx, esi
00457db0  c1e202                   shl      edx, 2
00457db3  01c3                     add      ebx, eax
00457db5  01ca                     add      edx, ecx
00457db7  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00457dbc  c1e202                   shl      edx, 2
00457dbf  01c2                     add      edx, eax
00457dc1  83c20a                   add      edx, 0xa
00457dc4  66c742660000             mov      word ptr [edx + 0x66], 0
00457dca  66c742040000             mov      word ptr [edx + 4], 0
00457dd0  891c24                   mov      dword ptr [esp], ebx
00457dd3  66c742020000             mov      word ptr [edx + 2], 0
00457dd9  31c0                     xor      eax, eax
00457ddb  89d6                     mov      esi, edx
00457ddd  89d1                     mov      ecx, edx
00457ddf  66c7020000               mov      word ptr [edx], 0
00457de4  eb0f                     jmp      0x457df5
00457de6  89d3                     mov      ebx, edx
00457de8  66c74459060000           mov      word ptr [ecx + ebx*2 + 6], 0
00457def  40                       inc      eax
00457df0  c644114200               mov      byte ptr [ecx + edx + 0x42], 0
00457df5  31d2                     xor      edx, edx
00457df7  6689c2                   mov      dx, ax
00457dfa  83fa1e                   cmp      edx, 0x1e
00457dfd  7ce7                     jl       0x457de6
00457dff  8b0424                   mov      eax, dword ptr [esp]
00457e02  66894602                 mov      word ptr [esi + 2], ax
00457e06  83c40c                   add      esp, 0xc
00457e09  5f                       pop      edi
00457e0a  5e                       pop      esi
00457e0b  c3                       ret
