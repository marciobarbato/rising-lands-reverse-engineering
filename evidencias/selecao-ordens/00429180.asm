; Deselection; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00429180  52                       push edx
00429181  31d2                     xor edx, edx
00429183  88c2                     mov dl, al
00429185  89d0                     mov eax, edx
00429187  e8ff940400               call 0x47268b
0042918c  89d0                     mov eax, edx
0042918e  e8d024ffff               call 0x41b663
00429193  b2ff                     mov dl, 0xff
00429195  30e4                     xor ah, ah
00429197  881507624900             mov byte ptr [0x496207], dl
0042919d  31d2                     xor edx, edx
0042919f  8825b0194e00             mov byte ptr [0x4e19b0], ah
004291a5  668915ae054e00           mov word ptr [0x4e05ae], dx
004291ac  b601                     mov dh, 1
004291ae  8825ab054e00             mov byte ptr [0x4e05ab], ah
004291b4  8835486d4900             mov byte ptr [0x496d48], dh
004291ba  5a                       pop edx
004291bb  c3                       ret
