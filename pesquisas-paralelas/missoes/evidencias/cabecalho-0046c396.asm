; MissionLoad_successful_open_prelude; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c396  b804000000               mov eax, 4
0046c39b  31d2                     xor edx, edx
0046c39d  e8e9c0feff               call 0x45848b
0046c3a2  ba00000100               mov edx, 0x10000
0046c3a7  a1a87d5000               mov eax, dword ptr [0x507da8]
0046c3ac  e8b0c0feff               call 0x458461
0046c3b1  ba00000200               mov edx, 0x20000
0046c3b6  a1707d5000               mov eax, dword ptr [0x507d70]
0046c3bb  e8a1c0feff               call 0x458461
0046c3c0  ba00000100               mov edx, 0x10000
0046c3c5  a1747d5000               mov eax, dword ptr [0x507d74]
0046c3ca  e892c0feff               call 0x458461
0046c3cf  ba00000100               mov edx, 0x10000
0046c3d4  a1ac7d5000               mov eax, dword ptr [0x507dac]
0046c3d9  e883c0feff               call 0x458461
0046c3de  31c0                     xor eax, eax
0046c3e0  eb08                     jmp 0x46c3ea
0046c3e2  40                       inc eax
0046c3e3  3d00000100               cmp eax, 0x10000
0046c3e8  7320                     jae 0x46c40a
0046c3ea  8b15747d5000             mov edx, dword ptr [0x507d74]
0046c3f0  01c2                     add edx, eax
0046c3f2  31db                     xor ebx, ebx
0046c3f4  8a1a                     mov bl, byte ptr [edx]
0046c3f6  83fb36                   cmp ebx, 0x36
0046c3f9  75e7                     jne 0x46c3e2
0046c3fb  c60242                   mov byte ptr [edx], 0x42
0046c3fe  8b15ac7d5000             mov edx, dword ptr [0x507dac]
0046c404  c6040201                 mov byte ptr [edx + eax], 1
0046c408  ebd8                     jmp 0x46c3e2
0046c40a  30c9                     xor cl, cl
0046c40c  eb27                     jmp 0x46c435
0046c40e  ba02000000               mov edx, 2
0046c413  8d842418010000           lea eax, [esp + 0x118]
0046c41a  e842c0feff               call 0x458461
0046c41f  31d2                     xor edx, edx
0046c421  b801000000               mov eax, 1
0046c426  668b942418010000         mov dx, word ptr [esp + 0x118]
0046c42e  fec1                     inc cl
0046c430  e867b5ffff               call 0x46799c
0046c435  31db                     xor ebx, ebx
0046c437  88cb                     mov bl, cl
0046c439  83fb04                   cmp ebx, 4
0046c43c  7cd0                     jl 0x46c40e
0046c43e  30c9                     xor cl, cl
0046c440  eb27                     jmp 0x46c469
0046c442  ba02000000               mov edx, 2
0046c447  8d842418010000           lea eax, [esp + 0x118]
0046c44e  e80ec0feff               call 0x458461
0046c453  31d2                     xor edx, edx
0046c455  b802000000               mov eax, 2
0046c45a  668b942418010000         mov dx, word ptr [esp + 0x118]
0046c462  fec1                     inc cl
0046c464  e833b5ffff               call 0x46799c
0046c469  31db                     xor ebx, ebx
0046c46b  88cb                     mov bl, cl
0046c46d  83fb04                   cmp ebx, 4
0046c470  7cd0                     jl 0x46c442
0046c472  30c9                     xor cl, cl
0046c474  eb24                     jmp 0x46c49a
0046c476  ba02000000               mov edx, 2
0046c47b  8d842418010000           lea eax, [esp + 0x118]
0046c482  e8dabffeff               call 0x458461
0046c487  31d2                     xor edx, edx
0046c489  31c0                     xor eax, eax
0046c48b  668b942418010000         mov dx, word ptr [esp + 0x118]
0046c493  fec1                     inc cl
0046c495  e802b5ffff               call 0x46799c
0046c49a  31db                     xor ebx, ebx
0046c49c  88cb                     mov bl, cl
0046c49e  83fb04                   cmp ebx, 4
0046c4a1  7cd3                     jl 0x46c476
0046c4a3  ba02000000               mov edx, 2
0046c4a8  b868714900               mov eax, 0x497168
0046c4ad  e8afbffeff               call 0x458461
0046c4b2  ba02000000               mov edx, 2
0046c4b7  b86a714900               mov eax, 0x49716a
0046c4bc  31db                     xor ebx, ebx
0046c4be  e89ebffeff               call 0x458461
0046c4c3  be02000000               mov esi, 2
0046c4c8  eb01                     jmp 0x46c4cb
0046c4ca  43                       inc ebx
0046c4cb  31c0                     xor eax, eax
0046c4cd  6689d8                   mov ax, bx
0046c4d0  83f804                   cmp eax, 4
0046c4d3  7d3d                     jge 0x46c512
0046c4d5  31d2                     xor edx, edx
0046c4d7  8a1541805000             mov dl, byte ptr [0x508041]
0046c4dd  39d0                     cmp eax, edx
0046c4df  751a                     jne 0x46c4fb
0046c4e1  b820875000               mov eax, 0x508720
0046c4e6  89f2                     mov edx, esi
0046c4e8  e874bffeff               call 0x458461
0046c4ed  b822875000               mov eax, 0x508722
0046c4f2  89f2                     mov edx, esi
0046c4f4  e868bffeff               call 0x458461
0046c4f9  ebcf                     jmp 0x46c4ca
0046c4fb  8d842424010000           lea eax, [esp + 0x124]
0046c502  89f2                     mov edx, esi
0046c504  e858bffeff               call 0x458461
0046c509  8d842424010000           lea eax, [esp + 0x124]
0046c510  ebe0                     jmp 0x46c4f2
0046c512  e80529fcff               call 0x42ee1c
