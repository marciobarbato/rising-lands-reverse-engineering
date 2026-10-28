; ResetBatimentTerrainModify; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041b888  53                       push ebx
0041b889  51                       push ecx
0041b88a  56                       push esi
0041b88b  57                       push edi
0041b88c  55                       push ebp
0041b88d  83ec24                   sub esp, 0x24
0041b890  88542420                 mov byte ptr [esp + 0x20], dl
0041b894  31d2                     xor edx, edx
0041b896  6689c2                   mov dx, ax
0041b899  89d0                     mov eax, edx
0041b89b  c1e004                   shl eax, 4
0041b89e  01d0                     add eax, edx
0041b8a0  c1e002                   shl eax, 2
0041b8a3  01d0                     add eax, edx
0041b8a5  bdc8a04900               mov ebp, 0x49a0c8
0041b8aa  c1e002                   shl eax, 2
0041b8ad  01c5                     add ebp, eax
0041b8af  31d2                     xor edx, edx
0041b8b1  8a5508                   mov dl, byte ptr [ebp + 8]
0041b8b4  89d0                     mov eax, edx
0041b8b6  c1e002                   shl eax, 2
0041b8b9  29d0                     sub eax, edx
0041b8bb  31ff                     xor edi, edi
0041b8bd  c1e002                   shl eax, 2
0041b8c0  668b5d02                 mov bx, word ptr [ebp + 2]
0041b8c4  01d0                     add eax, edx
0041b8c6  b900010000               mov ecx, 0x100
0041b8cb  6689df                   mov di, bx
0041b8ce  668b14858c5d4900         mov dx, word ptr [eax*4 + 0x495d8c]
0041b8d6  668b04858e5d4900         mov ax, word ptr [eax*4 + 0x495d8e]
0041b8de  89542408                 mov dword ptr [esp + 8], edx
0041b8e2  89442418                 mov dword ptr [esp + 0x18], eax
0041b8e6  89fa                     mov edx, edi
0041b8e8  89f8                     mov eax, edi
0041b8ea  c1fa1f                   sar edx, 0x1f
0041b8ed  f7f9                     idiv ecx
0041b8ef  89d6                     mov esi, edx
0041b8f1  89fa                     mov edx, edi
0041b8f3  89f8                     mov eax, edi
0041b8f5  c1fa1f                   sar edx, 0x1f
0041b8f8  f7f9                     idiv ecx
0041b8fa  8b4c2408                 mov ecx, dword ptr [esp + 8]
0041b8fe  8944241c                 mov dword ptr [esp + 0x1c], eax
0041b902  31d2                     xor edx, edx
0041b904  b800010000               mov eax, 0x100
0041b909  8954240c                 mov dword ptr [esp + 0xc], edx
0041b90d  29c8                     sub eax, ecx
0041b90f  894c2414                 mov dword ptr [esp + 0x14], ecx
0041b913  89442404                 mov dword ptr [esp + 4], eax
0041b917  eb18                     jmp 0x41b931
0041b919  8b442404                 mov eax, dword ptr [esp + 4]
0041b91d  8b54241c                 mov edx, dword ptr [esp + 0x1c]
0041b921  8b4c240c                 mov ecx, dword ptr [esp + 0xc]
0041b925  42                       inc edx
0041b926  41                       inc ecx
0041b927  01c3                     add ebx, eax
0041b929  8954241c                 mov dword ptr [esp + 0x1c], edx
0041b92d  894c240c                 mov dword ptr [esp + 0xc], ecx
0041b931  8b44240c                 mov eax, dword ptr [esp + 0xc]
0041b935  663b442418               cmp ax, word ptr [esp + 0x18]
0041b93a  0f838e000000             jae 0x41b9ce
0041b940  0faf442408               imul eax, dword ptr [esp + 8]
0041b945  8b542414                 mov edx, dword ptr [esp + 0x14]
0041b949  01c2                     add edx, eax
0041b94b  89c1                     mov ecx, eax
0041b94d  89542410                 mov dword ptr [esp + 0x10], edx
0041b951  eb25                     jmp 0x41b978
0041b953  31d2                     xor edx, edx
0041b955  31c0                     xor eax, eax
0041b957  6689ca                   mov dx, cx
0041b95a  8a4508                   mov al, byte ptr [ebp + 8]
0041b95d  e8faf1ffff               call 0x41ab5c
0041b962  84c0                     test al, al
0041b964  740f                     je 0x41b975
0041b966  31c0                     xor eax, eax
0041b968  ba01000000               mov edx, 1
0041b96d  6689d8                   mov ax, bx
0041b970  e8c9a80500               call 0x47623e
0041b975  43                       inc ebx
0041b976  46                       inc esi
0041b977  41                       inc ecx
0041b978  663b4c2410               cmp cx, word ptr [esp + 0x10]
0041b97d  739a                     jae 0x41b919
0041b97f  807c242000               cmp byte ptr [esp + 0x20], 0
0041b984  75cd                     jne 0x41b953
0041b986  31d2                     xor edx, edx
0041b988  6689f2                   mov dx, si
0041b98b  bf08000000               mov edi, 8
0041b990  89d0                     mov eax, edx
0041b992  c1fa1f                   sar edx, 0x1f
0041b995  f7ff                     idiv edi
0041b997  89d7                     mov edi, edx
0041b999  31d2                     xor edx, edx
0041b99b  668b54241c               mov dx, word ptr [esp + 0x1c]
0041b9a0  c7042408000000           mov dword ptr [esp], 8
0041b9a7  89d0                     mov eax, edx
0041b9a9  c1fa1f                   sar edx, 0x1f
0041b9ac  f73c24                   idiv dword ptr [esp]
0041b9af  81c75d010000             add edi, 0x15d
0041b9b5  31c0                     xor eax, eax
0041b9b7  c1e203                   shl edx, 3
0041b9ba  6689d8                   mov ax, bx
0041b9bd  01d7                     add edi, edx
0041b9bf  8b15707d5000             mov edx, dword ptr [0x507d70]
0041b9c5  01c0                     add eax, eax
0041b9c7  01d0                     add eax, edx
0041b9c9  668938                   mov word ptr [eax], di
0041b9cc  eba7                     jmp 0x41b975
0041b9ce  83c424                   add esp, 0x24
0041b9d1  e9c47f0000               jmp 0x42399a
