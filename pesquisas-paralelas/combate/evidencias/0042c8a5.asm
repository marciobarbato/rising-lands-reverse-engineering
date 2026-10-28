; CalculGameDespachoEstado; intervalo [0x0042c8a5, 0x0042c8bf)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042c8a5  a0782f4e00               mov      al, byte ptr [0x4e2f78]
0042c8aa  3c18                     cmp      al, 0x18
0042c8ac  0f87300c0000             ja       0x42d4e2
0042c8b2  25ff000000               and      eax, 0xff
0042c8b7  2eff248504c84200         jmp      dword ptr cs:[eax*4 + 0x42c804]
