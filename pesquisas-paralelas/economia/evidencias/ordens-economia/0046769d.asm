; GetRessourceStock; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046769d  56                       push esi
0046769e  57                       push edi
0046769f  89c6                     mov esi, eax
004676a1  89d7                     mov edi, edx
004676a3  31c0                     xor eax, eax
004676a5  8a44240c                 mov al, byte ptr [esp + 0xc]
004676a9  c1e005                   shl eax, 5
004676ac  668b90b22e4e00           mov dx, word ptr [eax + 0x4e2eb2]
004676b3  662b90b02e4e00           sub dx, word ptr [eax + 0x4e2eb0]
004676ba  668916                   mov word ptr [esi], dx
004676bd  668b90ba2e4e00           mov dx, word ptr [eax + 0x4e2eba]
004676c4  668bb0b82e4e00           mov si, word ptr [eax + 0x4e2eb8]
004676cb  29f2                     sub edx, esi
004676cd  668917                   mov word ptr [edi], dx
004676d0  668b90aa2e4e00           mov dx, word ptr [eax + 0x4e2eaa]
004676d7  668bb8a82e4e00           mov di, word ptr [eax + 0x4e2ea8]
004676de  29fa                     sub edx, edi
004676e0  668913                   mov word ptr [ebx], dx
004676e3  eb81                     jmp 0x467666
