; BatimentRessourceNecessaire: limite por próximo símbolo SBL, fim exclusivo 0x0045d7cf.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0045d753  53                       push     ebx
0045d754  51                       push     ecx
0045d755  83ec20                   sub      esp, 0x20
0045d758  8854241c                 mov      byte ptr [esp + 0x1c], dl
0045d75c  31d2                     xor      edx, edx
0045d75e  89542404                 mov      dword ptr [esp + 4], edx
0045d762  89542408                 mov      dword ptr [esp + 8], edx
0045d766  8954240c                 mov      dword ptr [esp + 0xc], edx
0045d76a  89542410                 mov      dword ptr [esp + 0x10], edx
0045d76e  89542414                 mov      dword ptr [esp + 0x14], edx
0045d772  89542418                 mov      dword ptr [esp + 0x18], edx
0045d776  891424                   mov      dword ptr [esp], edx
0045d779  8d4c2408                 lea      ecx, [esp + 8]
0045d77d  8d5c240c                 lea      ebx, [esp + 0xc]
0045d781  8d542404                 lea      edx, [esp + 4]
0045d785  25ff000000               and      eax, 0xff
0045d78a  e83fd3fbff               call     0x41aace
0045d78f  31c0                     xor      eax, eax
0045d791  89e1                     mov      ecx, esp
0045d793  8a44241c                 mov      al, byte ptr [esp + 0x1c]
0045d797  8d5c2414                 lea      ebx, [esp + 0x14]
0045d79b  50                       push     eax
0045d79c  8d54241c                 lea      edx, [esp + 0x1c]
0045d7a0  8d442414                 lea      eax, [esp + 0x14]
0045d7a4  e8c79e0000               call     0x467670
0045d7a9  8b442404                 mov      eax, dword ptr [esp + 4]
0045d7ad  663b442410               cmp      ax, word ptr [esp + 0x10]
0045d7b2  7608                     jbe      0x45d7bc
0045d7b4  b001                     mov      al, 1
0045d7b6  83c420                   add      esp, 0x20
0045d7b9  59                       pop      ecx
0045d7ba  5b                       pop      ebx
0045d7bb  c3                       ret
0045d7bc  8b44240c                 mov      eax, dword ptr [esp + 0xc]
0045d7c0  663b442418               cmp      ax, word ptr [esp + 0x18]
0045d7c5  7604                     jbe      0x45d7cb
0045d7c7  b002                     mov      al, 2
0045d7c9  ebeb                     jmp      0x45d7b6
0045d7cb  30c0                     xor      al, al
0045d7cd  ebe7                     jmp      0x45d7b6
