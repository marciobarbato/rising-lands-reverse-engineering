; TroupeRessourceNecessaire: limite por próximo símbolo SBL, fim exclusivo 0x0045d80d.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0045d7cf  53                       push     ebx
0045d7d0  51                       push     ecx
0045d7d1  83ec20                   sub      esp, 0x20
0045d7d4  8854241c                 mov      byte ptr [esp + 0x1c], dl
0045d7d8  31d2                     xor      edx, edx
0045d7da  89542404                 mov      dword ptr [esp + 4], edx
0045d7de  89542408                 mov      dword ptr [esp + 8], edx
0045d7e2  8954240c                 mov      dword ptr [esp + 0xc], edx
0045d7e6  89542410                 mov      dword ptr [esp + 0x10], edx
0045d7ea  89542414                 mov      dword ptr [esp + 0x14], edx
0045d7ee  89542418                 mov      dword ptr [esp + 0x18], edx
0045d7f2  891424                   mov      dword ptr [esp], edx
0045d7f5  8d4c2408                 lea      ecx, [esp + 8]
0045d7f9  8d5c240c                 lea      ebx, [esp + 0xc]
0045d7fd  8d542404                 lea      edx, [esp + 4]
0045d801  25ff000000               and      eax, 0xff
0045d806  e8c738feff               call     0x4410d2
0045d80b  eb82                     jmp      0x45d78f
