; SetEnginDecharge; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004447fa  53                       push ebx
004447fb  51                       push ecx
004447fc  56                       push esi
004447fd  57                       push edi
004447fe  89c3                     mov ebx, eax
00444800  89d1                     mov ecx, edx
00444802  31f6                     xor esi, esi
00444804  6689c6                   mov si, ax
00444807  89f7                     mov edi, esi
00444809  c1e704                   shl edi, 4
0044480c  01f7                     add edi, esi
0044480e  c1e702                   shl edi, 2
00444811  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00444817  01f7                     add edi, esi
00444819  89f0                     mov eax, esi
0044481b  c1e702                   shl edi, 2
0044481e  e859edffff               call 0x44357c
00444823  c6843a8200000002         mov byte ptr [edx + edi + 0x82], 2
0044482b  c6443a0205               mov byte ptr [edx + edi + 2], 5
00444830  c6843a8900000002         mov byte ptr [edx + edi + 0x89], 2
00444838  31c0                     xor eax, eax
0044483a  66898c3a80000000         mov word ptr [edx + edi + 0x80], cx
00444842  8a443a01                 mov al, byte ptr [edx + edi + 1]
00444846  66898c3ac0000000         mov word ptr [edx + edi + 0xc0], cx
0044484e  83f80d                   cmp eax, 0xd
00444851  7557                     jne 0x4448aa
00444853  31d2                     xor edx, edx
00444855  6689ca                   mov dx, cx
00444858  89d0                     mov eax, edx
0044485a  e8c8f2fdff               call 0x423b27
0044485f  89c1                     mov ecx, eax
00444861  89d0                     mov eax, edx
00444863  e877effdff               call 0x4237df
00444868  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044486e  01fa                     add edx, edi
00444870  81e9fe000000             sub ecx, 0xfe
00444876  66894a7e                 mov word ptr [edx + 0x7e], cx
0044487a  663b1d04634900           cmp bx, word ptr [0x496304]
00444881  0f8589000000             jne 0x444910
00444887  b8ffff0000               mov eax, 0xffff
0044488c  30ff                     xor bh, bh
0044488e  31c9                     xor ecx, ecx
00444890  883d360f4e00             mov byte ptr [0x4e0f36], bh
00444896  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044489c  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
004448a2  66a304634900             mov word ptr [0x496304], ax
004448a8  eb66                     jmp 0x444910
004448aa  83f805                   cmp eax, 5
004448ad  7405                     je 0x4448b4
004448af  83f807                   cmp eax, 7
004448b2  7563                     jne 0x444917
004448b4  31c0                     xor eax, eax
004448b6  6689c8                   mov ax, cx
004448b9  e82466fdff               call 0x41aee2
004448be  89c1                     mov ecx, eax
004448c0  31c0                     xor eax, eax
004448c2  6689d8                   mov ax, bx
004448c5  89c2                     mov edx, eax
004448c7  c1e204                   shl edx, 4
004448ca  01c2                     add edx, eax
004448cc  c1e202                   shl edx, 2
004448cf  01d0                     add eax, edx
004448d1  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004448d7  c1e002                   shl eax, 2
004448da  01c2                     add edx, eax
004448dc  66894a7e                 mov word ptr [edx + 0x7e], cx
004448e0  668b0d04634900           mov cx, word ptr [0x496304]
004448e7  6639cb                   cmp bx, cx
004448ea  7524                     jne 0x444910
004448ec  beffff0000               mov esi, 0xffff
004448f1  30e4                     xor ah, ah
004448f3  30cb                     xor bl, cl
004448f5  8825360f4e00             mov byte ptr [0x4e0f36], ah
004448fb  881d370f4e00             mov byte ptr [0x4e0f37], bl
00444901  31db                     xor ebx, ebx
00444903  66893504634900           mov word ptr [0x496304], si
0044490a  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
00444910  c6828800000000           mov byte ptr [edx + 0x88], 0
00444917  5f                       pop edi
00444918  5e                       pop esi
00444919  59                       pop ecx
0044491a  5b                       pop ebx
0044491b  c3                       ret
