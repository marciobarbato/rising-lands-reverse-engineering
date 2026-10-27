; TypeEnginGetBagOrdre: limite por próximo símbolo SBL, fim exclusivo 0x004474f3.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004474c7  53                       push     ebx
004474c8  25ff000000               and      eax, 0xff
004474cd  8b1db8194e00             mov      ebx, dword ptr [0x4e19b8]
004474d3  c1e002                   shl      eax, 2
004474d6  01c3                     add      ebx, eax
004474d8  81e2ff000000             and      edx, 0xff
004474de  89d0                     mov      eax, edx
004474e0  c1e002                   shl      eax, 2
004474e3  29d0                     sub      eax, edx
004474e5  c1e002                   shl      eax, 2
004474e8  01c2                     add      edx, eax
004474ea  c1e203                   shl      edx, 3
004474ed  8b03                     mov      eax, dword ptr [ebx]
004474ef  01d0                     add      eax, edx
004474f1  5b                       pop      ebx
004474f2  c3                       ret
