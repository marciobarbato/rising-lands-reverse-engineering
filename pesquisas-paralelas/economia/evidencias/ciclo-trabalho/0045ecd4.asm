; SetPlayerOrdre; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045ecd4  56                       push esi
0045ecd5  89d6                     mov esi, edx
0045ecd7  25ff000000               and eax, 0xff
0045ecdc  8b148558244e00           mov edx, dword ptr [eax*4 + 0x4e2458]
0045ece3  668932                   mov word ptr [edx], si
0045ece6  8b148558244e00           mov edx, dword ptr [eax*4 + 0x4e2458]
0045eced  66895a02                 mov word ptr [edx + 2], bx
0045ecf1  8b148558244e00           mov edx, dword ptr [eax*4 + 0x4e2458]
0045ecf8  66894a04                 mov word ptr [edx + 4], cx
0045ecfc  8b148558244e00           mov edx, dword ptr [eax*4 + 0x4e2458]
0045ed03  8b5c2408                 mov ebx, dword ptr [esp + 8]
0045ed07  66895a06                 mov word ptr [edx + 6], bx
0045ed0b  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045ed12  8b54240c                 mov edx, dword ptr [esp + 0xc]
0045ed16  66895008                 mov word ptr [eax + 8], dx
0045ed1a  5e                       pop esi
0045ed1b  c20800                   ret 8
