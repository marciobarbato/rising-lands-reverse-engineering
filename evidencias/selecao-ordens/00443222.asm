; tail 0x443222 (SetTransporteEngin); original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00443222  01d0                     add eax, edx
00443224  6689487e                 mov word ptr [eax + 0x7e], cx
00443228  663b1d04634900           cmp bx, word ptr [0x496304]
0044322f  7522                     jne 0x443253
00443231  30d2                     xor dl, dl
00443233  bbffff0000               mov ebx, 0xffff
00443238  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044323e  8815370f4e00             mov byte ptr [0x4e0f37], dl
00443244  31d2                     xor edx, edx
00443246  66891d04634900           mov word ptr [0x496304], bx
0044324d  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
00443253  c6808800000000           mov byte ptr [eax + 0x88], 0
0044325a  59                       pop ecx
0044325b  5b                       pop ebx
0044325c  c3                       ret
