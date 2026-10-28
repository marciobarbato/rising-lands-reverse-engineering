; type4_bonus12_then_frame; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045782b  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00457830  01d8                     add eax, ebx
00457832  8a5001                   mov dl, byte ptr [eax + 1]
00457835  31db                     xor ebx, ebx
00457837  88d3                     mov bl, dl
00457839  8a00                     mov al, byte ptr [eax]
0045783b  ba0c000000               mov edx, 0xc
00457840  25ff000000               and eax, 0xff
00457845  e87614fdff               call 0x428cc0
0045784a  040a                     add al, 0xa
0045784c  c6417a05                 mov byte ptr [ecx + 0x7a], 5
00457850  8881da000000             mov byte ptr [ecx + 0xda], al
00457856  5a                       pop edx
00457857  59                       pop ecx
00457858  5b                       pop ebx
00457859  c3                       ret
