; LibereCouleur; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0043e5d5  53                       push ebx
0043e5d6  52                       push edx
0043e5d7  88c2                     mov dl, al
0043e5d9  31c0                     xor eax, eax
0043e5db  a070154e00               mov al, byte ptr [0x4e1570]
0043e5e0  3dff000000               cmp eax, 0xff
0043e5e5  7d2c                     jge 0x43e613
0043e5e7  31c0                     xor eax, eax
0043e5e9  88d0                     mov al, dl
0043e5eb  80b870164e0000           cmp byte ptr [eax + 0x4e1670], 0
0043e5f2  751f                     jne 0x43e613
0043e5f4  84d2                     test dl, dl
0043e5f6  741b                     je 0x43e613
0043e5f8  fe0570154e00             inc byte ptr [0x4e1570]
0043e5fe  31db                     xor ebx, ebx
0043e600  8a1d70154e00             mov bl, byte ptr [0x4e1570]
0043e606  889370154e00             mov byte ptr [ebx + 0x4e1570], dl
0043e60c  c68070164e0001           mov byte ptr [eax + 0x4e1670], 1
0043e613  5a                       pop edx
0043e614  5b                       pop ebx
0043e615  c3                       ret
