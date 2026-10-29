; EnginVisible; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004465bf  52                       push edx
004465c0  31d2                     xor edx, edx
004465c2  6689c2                   mov dx, ax
004465c5  89d0                     mov eax, edx
004465c7  c1e004                   shl eax, 4
004465ca  01d0                     add eax, edx
004465cc  c1e002                   shl eax, 2
004465cf  01c2                     add edx, eax
004465d1  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004465d6  c1e202                   shl edx, 2
004465d9  8a440272                 mov al, byte ptr [edx + eax + 0x72]
004465dd  5a                       pop edx
004465de  c3                       ret
