; MemAlloc; intervalo [0x00467ea6, 0x00467ecb)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00467ea6  51                       push     ecx
00467ea7  52                       push     edx
00467ea8  8b153c2f4e00             mov      edx, dword ptr [0x4e2f3c]
00467eae  50                       push     eax
00467eaf  01c2                     add      edx, eax
00467eb1  6a00                     push     0
00467eb3  89153c2f4e00             mov      dword ptr [0x4e2f3c], edx
00467eb9  2eff15c0315200           call     dword ptr cs:[0x5231c0]
00467ec0  50                       push     eax
00467ec1  2eff15d0315200           call     dword ptr cs:[0x5231d0]
00467ec8  5a                       pop      edx
00467ec9  59                       pop      ecx
00467eca  c3                       ret
