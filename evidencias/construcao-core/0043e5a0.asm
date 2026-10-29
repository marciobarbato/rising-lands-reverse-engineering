; AlloueCouleur; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0043e5a0  53                       push ebx
0043e5a1  52                       push edx
0043e5a2  31c0                     xor eax, eax
0043e5a4  a070154e00               mov al, byte ptr [0x4e1570]
0043e5a9  85c0                     test eax, eax
0043e5ab  7423                     je 0x43e5d0
0043e5ad  8a1d70154e00             mov bl, byte ptr [0x4e1570]
0043e5b3  8a9070154e00             mov dl, byte ptr [eax + 0x4e1570]
0043e5b9  31c0                     xor eax, eax
0043e5bb  fecb                     dec bl
0043e5bd  88d0                     mov al, dl
0043e5bf  30f6                     xor dh, dh
0043e5c1  881d70154e00             mov byte ptr [0x4e1570], bl
0043e5c7  88b070164e00             mov byte ptr [eax + 0x4e1670], dh
0043e5cd  5a                       pop edx
0043e5ce  5b                       pop ebx
0043e5cf  c3                       ret
0043e5d0  30c0                     xor al, al
0043e5d2  5a                       pop edx
0043e5d3  5b                       pop ebx
0043e5d4  c3                       ret
