; EnginGetBag; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004474a6  52                       push edx
004474a7  31d2                     xor edx, edx
004474a9  6689c2                   mov dx, ax
004474ac  89d0                     mov eax, edx
004474ae  c1e004                   shl eax, 4
004474b1  01d0                     add eax, edx
004474b3  c1e002                   shl eax, 2
004474b6  01c2                     add edx, eax
004474b8  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004474bd  c1e202                   shl edx, 2
004474c0  01d0                     add eax, edx
004474c2  83c00a                   add eax, 0xa
004474c5  5a                       pop edx
004474c6  c3                       ret
