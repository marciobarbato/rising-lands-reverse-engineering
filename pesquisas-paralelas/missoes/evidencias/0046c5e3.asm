; MissionLoadName; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c5e3  53                       push ebx
0046c5e4  51                       push ecx
0046c5e5  52                       push edx
0046c5e6  56                       push esi
0046c5e7  57                       push edi
0046c5e8  55                       push ebp
0046c5e9  81ec14010000             sub esp, 0x114
0046c5ef  50                       push eax
0046c5f0  bd00000100               mov ebp, 0x10000
0046c5f5  baffff0000               mov edx, 0xffff
0046c5fa  31c9                     xor ecx, ecx
0046c5fc  668915381a4e00           mov word ptr [0x4e1a38], dx
0046c603  6689153a1a4e00           mov word ptr [0x4e1a3a], dx
0046c60a  e88022ffff               call 0x45e88f
0046c60f  e801edffff               call 0x46b315
0046c614  e8e7d8ffff               call 0x469f00
0046c619  e83ee1faff               call 0x41a75c
0046c61e  e83650fdff               call 0x441659
0046c623  e8e2190000               call 0x46e00a
0046c628  e8dbd2ffff               call 0x469908
0046c62d  eb1c                     jmp 0x46c64b
0046c62f  31db                     xor ebx, ebx
0046c631  6689cb                   mov bx, cx
0046c634  6bdb1a                   imul ebx, ebx, 0x1a
0046c637  40                       inc eax
0046c638  c6841a34194e0000         mov byte ptr [edx + ebx + 0x4e1934], 0
0046c640  31d2                     xor edx, edx
0046c642  6689c2                   mov dx, ax
0046c645  83fa1a                   cmp edx, 0x1a
0046c648  7ce5                     jl 0x46c62f
0046c64a  41                       inc ecx
0046c64b  31c0                     xor eax, eax
0046c64d  6689c8                   mov ax, cx
0046c650  83f804                   cmp eax, 4
0046c653  7d04                     jge 0x46c659
0046c655  31c8                     xor eax, ecx
0046c657  ebe7                     jmp 0x46c640
0046c659  30c9                     xor cl, cl
0046c65b  eb1d                     jmp 0x46c67a
0046c65d  31db                     xor ebx, ebx
0046c65f  88cb                     mov bl, cl
0046c661  6bdb16                   imul ebx, ebx, 0x16
0046c664  30ed                     xor ch, ch
0046c666  40                       inc eax
0046c667  88ac1ad4fa4d00           mov byte ptr [edx + ebx + 0x4dfad4], ch
0046c66e  31d2                     xor edx, edx
0046c670  6689c2                   mov dx, ax
0046c673  83fa16                   cmp edx, 0x16
0046c676  7ce5                     jl 0x46c65d
0046c678  fec1                     inc cl
0046c67a  31c0                     xor eax, eax
0046c67c  88c8                     mov al, cl
0046c67e  83f804                   cmp eax, 4
0046c681  7d04                     jge 0x46c687
0046c683  31c0                     xor eax, eax
0046c685  ebe7                     jmp 0x46c66e
0046c687  e866830000               call 0x4749f2
0046c68c  e8b5440000               call 0x470b46
0046c691  e8da4dfdff               call 0x441470
0046c696  c605e46f490032           mov byte ptr [0x496fe4], 0x32
0046c69d  e80efdfbff               call 0x42c3b0
0046c6a2  84c0                     test al, al
0046c6a4  740a                     je 0x46c6b0
0046c6a6  e853500000               call 0x4716fe
0046c6ab  e8404e0000               call 0x4714f0
0046c6b0  e8b754fdff               call 0x441b6c
0046c6b5  8b3c24                   mov edi, dword ptr [esp]
0046c6b8  8b1424                   mov edx, dword ptr [esp]
0046c6bb  29c9                     sub ecx, ecx
0046c6bd  49                       dec ecx
0046c6be  31c0                     xor eax, eax
0046c6c0  f2ae                     repne scasb al, byte ptr es:[edi]
0046c6c2  f7d1                     not ecx
0046c6c4  49                       dec ecx
0046c6c5  8d41fc                   lea eax, [ecx - 4]
0046c6c8  01d0                     add eax, edx
0046c6ca  ba3e4b4900               mov edx, 0x494b3e
0046c6cf  e88d0e0200               call 0x48d561
0046c6d4  85c0                     test eax, eax
0046c6d6  7507                     jne 0x46c6df
0046c6d8  be94945000               mov esi, 0x509494
0046c6dd  eb05                     jmp 0x46c6e4
0046c6df  be94955000               mov esi, 0x509594
0046c6e4  8d7c2404                 lea edi, [esp + 4]
0046c6e8  57                       push edi
0046c6e9  8a06                     mov al, byte ptr [esi]
0046c6eb  8807                     mov byte ptr [edi], al
0046c6ed  3c00                     cmp al, 0
0046c6ef  7410                     je 0x46c701
0046c6f1  8a4601                   mov al, byte ptr [esi + 1]
0046c6f4  83c602                   add esi, 2
0046c6f7  884701                   mov byte ptr [edi + 1], al
0046c6fa  83c702                   add edi, 2
0046c6fd  3c00                     cmp al, 0
0046c6ff  75e8                     jne 0x46c6e9
0046c701  5f                       pop edi
0046c702  be434b4900               mov esi, 0x494b43
0046c707  8d7c2404                 lea edi, [esp + 4]
0046c70b  57                       push edi
0046c70c  2bc9                     sub ecx, ecx
0046c70e  49                       dec ecx
0046c70f  b000                     mov al, 0
0046c711  f2ae                     repne scasb al, byte ptr es:[edi]
0046c713  4f                       dec edi
0046c714  8a06                     mov al, byte ptr [esi]
0046c716  8807                     mov byte ptr [edi], al
0046c718  3c00                     cmp al, 0
0046c71a  7410                     je 0x46c72c
0046c71c  8a4601                   mov al, byte ptr [esi + 1]
0046c71f  83c602                   add esi, 2
0046c722  884701                   mov byte ptr [edi + 1], al
0046c725  83c702                   add edi, 2
0046c728  3c00                     cmp al, 0
0046c72a  75e8                     jne 0x46c714
0046c72c  5f                       pop edi
0046c72d  8b3424                   mov esi, dword ptr [esp]
0046c730  8d7c2404                 lea edi, [esp + 4]
0046c734  ba4b4b4900               mov edx, 0x494b4b
0046c739  57                       push edi
0046c73a  2bc9                     sub ecx, ecx
0046c73c  49                       dec ecx
0046c73d  b000                     mov al, 0
0046c73f  f2ae                     repne scasb al, byte ptr es:[edi]
0046c741  4f                       dec edi
0046c742  8a06                     mov al, byte ptr [esi]
0046c744  8807                     mov byte ptr [edi], al
0046c746  3c00                     cmp al, 0
0046c748  7410                     je 0x46c75a
0046c74a  8a4601                   mov al, byte ptr [esi + 1]
0046c74d  83c602                   add esi, 2
0046c750  884701                   mov byte ptr [edi + 1], al
0046c753  83c702                   add edi, 2
0046c756  3c00                     cmp al, 0
0046c758  75e8                     jne 0x46c742
0046c75a  5f                       pop edi
0046c75b  8d442404                 lea eax, [esp + 4]
0046c75f  e8bcbcfeff               call 0x458420
0046c764  84c0                     test al, al
0046c766  0f842e020000             je 0x46c99a
0046c76c  b804000000               mov eax, 4
0046c771  31d2                     xor edx, edx
0046c773  e813bdfeff               call 0x45848b
0046c778  a1a87d5000               mov eax, dword ptr [0x507da8]
0046c77d  89ea                     mov edx, ebp
0046c77f  e8ddbcfeff               call 0x458461
0046c784  a1707d5000               mov eax, dword ptr [0x507d70]
0046c789  8d542d00                 lea edx, [ebp + ebp]
0046c78d  e8cfbcfeff               call 0x458461
0046c792  a1747d5000               mov eax, dword ptr [0x507d74]
0046c797  89ea                     mov edx, ebp
0046c799  e8c3bcfeff               call 0x458461
0046c79e  a1ac7d5000               mov eax, dword ptr [0x507dac]
0046c7a3  89ea                     mov edx, ebp
0046c7a5  e8b7bcfeff               call 0x458461
0046c7aa  31c0                     xor eax, eax
0046c7ac  eb01                     jmp 0x46c7af
0046c7ae  40                       inc eax
0046c7af  39e8                     cmp eax, ebp
0046c7b1  7320                     jae 0x46c7d3
0046c7b3  8b15747d5000             mov edx, dword ptr [0x507d74]
0046c7b9  01c2                     add edx, eax
0046c7bb  31db                     xor ebx, ebx
0046c7bd  8a1a                     mov bl, byte ptr [edx]
0046c7bf  83fb36                   cmp ebx, 0x36
0046c7c2  75ea                     jne 0x46c7ae
0046c7c4  c60242                   mov byte ptr [edx], 0x42
0046c7c7  8b15ac7d5000             mov edx, dword ptr [0x507dac]
0046c7cd  c6040201                 mov byte ptr [edx + eax], 1
0046c7d1  ebdb                     jmp 0x46c7ae
0046c7d3  30c9                     xor cl, cl
0046c7d5  eb27                     jmp 0x46c7fe
0046c7d7  ba02000000               mov edx, 2
0046c7dc  8d84240c010000           lea eax, [esp + 0x10c]
0046c7e3  e879bcfeff               call 0x458461
0046c7e8  31d2                     xor edx, edx
0046c7ea  b801000000               mov eax, 1
0046c7ef  668b94240c010000         mov dx, word ptr [esp + 0x10c]
0046c7f7  fec1                     inc cl
0046c7f9  e89eb1ffff               call 0x46799c
0046c7fe  31db                     xor ebx, ebx
0046c800  88cb                     mov bl, cl
0046c802  83fb04                   cmp ebx, 4
0046c805  7cd0                     jl 0x46c7d7
0046c807  30c9                     xor cl, cl
0046c809  eb27                     jmp 0x46c832
0046c80b  ba02000000               mov edx, 2
0046c810  8d84240c010000           lea eax, [esp + 0x10c]
0046c817  e845bcfeff               call 0x458461
0046c81c  31d2                     xor edx, edx
0046c81e  b802000000               mov eax, 2
0046c823  668b94240c010000         mov dx, word ptr [esp + 0x10c]
0046c82b  fec1                     inc cl
0046c82d  e86ab1ffff               call 0x46799c
0046c832  31db                     xor ebx, ebx
0046c834  88cb                     mov bl, cl
0046c836  83fb04                   cmp ebx, 4
0046c839  7cd0                     jl 0x46c80b
0046c83b  30c9                     xor cl, cl
0046c83d  eb24                     jmp 0x46c863
0046c83f  ba02000000               mov edx, 2
0046c844  8d84240c010000           lea eax, [esp + 0x10c]
0046c84b  e811bcfeff               call 0x458461
0046c850  31d2                     xor edx, edx
0046c852  31c0                     xor eax, eax
0046c854  668b94240c010000         mov dx, word ptr [esp + 0x10c]
0046c85c  fec1                     inc cl
0046c85e  e839b1ffff               call 0x46799c
0046c863  31db                     xor ebx, ebx
0046c865  88cb                     mov bl, cl
0046c867  83fb04                   cmp ebx, 4
0046c86a  7cd3                     jl 0x46c83f
0046c86c  ba02000000               mov edx, 2
0046c871  b868714900               mov eax, 0x497168
0046c876  e8e6bbfeff               call 0x458461
0046c87b  ba02000000               mov edx, 2
0046c880  b86a714900               mov eax, 0x49716a
0046c885  31db                     xor ebx, ebx
0046c887  e8d5bbfeff               call 0x458461
0046c88c  b902000000               mov ecx, 2
0046c891  eb01                     jmp 0x46c894
0046c893  43                       inc ebx
0046c894  31c0                     xor eax, eax
0046c896  6689d8                   mov ax, bx
0046c899  83f804                   cmp eax, 4
0046c89c  7d3d                     jge 0x46c8db
0046c89e  31d2                     xor edx, edx
0046c8a0  8a1541805000             mov dl, byte ptr [0x508041]
0046c8a6  39d0                     cmp eax, edx
0046c8a8  751a                     jne 0x46c8c4
0046c8aa  b820875000               mov eax, 0x508720
0046c8af  89ca                     mov edx, ecx
0046c8b1  e8abbbfeff               call 0x458461
0046c8b6  b822875000               mov eax, 0x508722
0046c8bb  89ca                     mov edx, ecx
0046c8bd  e89fbbfeff               call 0x458461
0046c8c2  ebcf                     jmp 0x46c893
0046c8c4  8d842404010000           lea eax, [esp + 0x104]
0046c8cb  89ca                     mov edx, ecx
0046c8cd  e88fbbfeff               call 0x458461
0046c8d2  8d842404010000           lea eax, [esp + 0x104]
0046c8d9  ebe0                     jmp 0x46c8bb
0046c8db  e83c25fcff               call 0x42ee1c
0046c8e0  ba02000000               mov edx, 2
0046c8e5  8d842408010000           lea eax, [esp + 0x108]
0046c8ec  e870bbfeff               call 0x458461
0046c8f1  ba02000000               mov edx, 2
0046c8f6  8d842414010000           lea eax, [esp + 0x114]
0046c8fd  31db                     xor ebx, ebx
0046c8ff  eb31                     jmp 0x46c932
0046c901  ba02000000               mov edx, 2
0046c906  8d842410010000           lea eax, [esp + 0x110]
0046c90d  e84fbbfeff               call 0x458461
0046c912  31c0                     xor eax, eax
0046c914  668b842410010000         mov ax, word ptr [esp + 0x110]
0046c91c  69c014010000             imul eax, eax, 0x114
0046c922  31d2                     xor edx, edx
0046c924  668b942414010000         mov dx, word ptr [esp + 0x114]
0046c92c  05c8a04900               add eax, 0x49a0c8
0046c931  43                       inc ebx
0046c932  e82abbfeff               call 0x458461
0046c937  663b9c2408010000         cmp bx, word ptr [esp + 0x108]
0046c93f  72c0                     jb 0x46c901
0046c941  e879e3ffff               call 0x46acbf
0046c946  e8ff890000               call 0x47534a
0046c94b  e8fdf80000               call 0x47c24d
0046c950  e872f30000               call 0x47bcc7
0046c955  e8f0f60000               call 0x47c04a
0046c95a  e8a6c1feff               call 0x458b05
0046c95f  e8abf90000               call 0x47c30f
0046c964  e89bfa0000               call 0x47c404
0046c969  e8c2e20000               call 0x47ac30
0046c96e  e8d9bafeff               call 0x45844c
0046c973  e8aaf7ffff               call 0x46c122
0046c978  e8dc4afdff               call 0x441459
0046c97d  e890c7faff               call 0x419112
0046c982  e8884b0000               call 0x47150f
0046c987  31c0                     xor eax, eax
0046c989  a0e46f4900               mov al, byte ptr [0x496fe4]
0046c98e  e8db290100               call 0x47f36e
0046c993  e8e438ffff               call 0x46027c
0046c998  b001                     mov al, 1
0046c99a  81c418010000             add esp, 0x118
0046c9a0  e98af2ffff               jmp 0x46bc2f
