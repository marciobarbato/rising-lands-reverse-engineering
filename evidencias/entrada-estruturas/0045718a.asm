; EnginGetVie; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045718a  52                       push edx
0045718b  31d2                     xor edx, edx
0045718d  6689c2                   mov dx, ax
00457190  89d0                     mov eax, edx
00457192  c1e004                   shl eax, 4
00457195  01d0                     add eax, edx
00457197  c1e002                   shl eax, 2
0045719a  01c2                     add edx, eax
0045719c  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004571a1  c1e202                   shl edx, 2
004571a4  668b84029a000000         mov ax, word ptr [edx + eax + 0x9a]
004571ac  5a                       pop edx
004571ad  c3                       ret
