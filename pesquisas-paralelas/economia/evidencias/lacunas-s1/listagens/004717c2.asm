; RechercheGetNiveau; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x4717e0
004717c2  53                       push     ebx
004717c3  25ff000000               and      eax, 0xff
004717c8  bbf4805000               mov      ebx, 0x5080f4
004717cd  c1e004                   shl      eax, 4
004717d0  01c3                     add      ebx, eax
004717d2  31c0                     xor      eax, eax
004717d4  6689d0                   mov      ax, dx
004717d7  8a0403                   mov      al, byte ptr [ebx + eax]
004717da  30e4                     xor      ah, ah
004717dc  5b                       pop      ebx
004717dd  c3                       ret      
004717de  0000                     add      byte ptr [eax], al
