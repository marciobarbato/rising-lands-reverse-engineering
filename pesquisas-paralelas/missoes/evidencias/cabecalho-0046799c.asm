; SetMatiere; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046799c  81e3ffff0000             and ebx, 0xffff
004679a2  c1e302                   shl ebx, 2
004679a5  25ff000000               and eax, 0xff
004679aa  01d8                     add eax, ebx
004679ac  668914c5a82e4e00         mov word ptr [eax*8 + 0x4e2ea8], dx
004679b4  668914c5aa2e4e00         mov word ptr [eax*8 + 0x4e2eaa], dx
004679bc  31d2                     xor edx, edx
004679be  668914c5ac2e4e00         mov word ptr [eax*8 + 0x4e2eac], dx
004679c6  30d2                     xor dl, dl
004679c8  8814c5ae2e4e00           mov byte ptr [eax*8 + 0x4e2eae], dl
004679cf  c3                       ret
