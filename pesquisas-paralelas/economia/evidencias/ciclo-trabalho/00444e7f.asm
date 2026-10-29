; SetTransporteEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00444e7f  53                       push ebx
00444e80  51                       push ecx
00444e81  89c3                     mov ebx, eax
00444e83  89d1                     mov ecx, edx
00444e85  31d2                     xor edx, edx
00444e87  6689c2                   mov dx, ax
00444e8a  89d0                     mov eax, edx
00444e8c  c1e004                   shl eax, 4
00444e8f  01d0                     add eax, edx
00444e91  c1e002                   shl eax, 2
00444e94  01c2                     add edx, eax
00444e96  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444e9b  c1e202                   shl edx, 2
00444e9e  c644020212               mov byte ptr [edx + eax + 2], 0x12
00444ea3  c684028900000000         mov byte ptr [edx + eax + 0x89], 0
00444eab  66898c02b2000000         mov word ptr [edx + eax + 0xb2], cx
00444eb3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444eb8  e965e3ffff               jmp 0x443222
