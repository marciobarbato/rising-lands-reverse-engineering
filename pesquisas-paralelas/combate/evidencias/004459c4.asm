; SetEnginLanceSortilege; intervalo [0x004459c4, 0x00445a36)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004459c4  56                       push     esi
004459c5  57                       push     edi
004459c6  83ec04                   sub      esp, 4
004459c9  89c6                     mov      esi, eax
004459cb  881424                   mov      byte ptr [esp], dl
004459ce  31ff                     xor      edi, edi
004459d0  6689c7                   mov      di, ax
004459d3  89fa                     mov      edx, edi
004459d5  c1e204                   shl      edx, 4
004459d8  01fa                     add      edx, edi
004459da  c1e202                   shl      edx, 2
004459dd  01fa                     add      edx, edi
004459df  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
004459e4  c1e202                   shl      edx, 2
004459e7  01c2                     add      edx, eax
004459e9  89f8                     mov      eax, edi
004459eb  e88cdbffff               call     0x44357c
004459f0  31c0                     xor      eax, eax
004459f2  8a4201                   mov      al, byte ptr [edx + 1]
004459f5  83f804                   cmp      eax, 4
004459f8  7421                     je       0x445a1b
004459fa  eb34                     jmp      0x445a30
004459fc  6639ce                   cmp      si, cx
004459ff  742f                     je       0x445a30
00445a01  c6420218                 mov      byte ptr [edx + 2], 0x18
00445a05  c6828a00000000           mov      byte ptr [edx + 0x8a], 0
00445a0c  889ab7000000             mov      byte ptr [edx + 0xb7], bl
00445a12  66898ab8000000           mov      word ptr [edx + 0xb8], cx
00445a19  eb15                     jmp      0x445a30
00445a1b  8a0424                   mov      al, byte ptr [esp]
00445a1e  8882f4000000             mov      byte ptr [edx + 0xf4], al
00445a24  80fb01                   cmp      bl, 1
00445a27  7207                     jb       0x445a30
00445a29  76d1                     jbe      0x4459fc
00445a2b  80fb05                   cmp      bl, 5
00445a2e  74d1                     je       0x445a01
00445a30  83c404                   add      esp, 4
00445a33  5f                       pop      edi
00445a34  5e                       pop      esi
00445a35  c3                       ret
