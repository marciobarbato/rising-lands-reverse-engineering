; TestRessource; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004676e5  56                       push esi
004676e6  89c6                     mov esi, eax
004676e8  31c0                     xor eax, eax
004676ea  8a442408                 mov al, byte ptr [esp + 8]
004676ee  c1e005                   shl eax, 5
004676f1  663bb0b22e4e00           cmp si, word ptr [eax + 0x4e2eb2]
004676f8  7606                     jbe 0x467700
004676fa  30c0                     xor al, al
004676fc  5e                       pop esi
004676fd  c20400                   ret 4
00467700  663b90ba2e4e00           cmp dx, word ptr [eax + 0x4e2eba]
00467707  77f1                     ja 0x4676fa
00467709  663b98aa2e4e00           cmp bx, word ptr [eax + 0x4e2eaa]
00467710  77e8                     ja 0x4676fa
00467712  b001                     mov al, 1
00467714  5e                       pop esi
00467715  c20400                   ret 4
