; MarcheQuitte; exclusive end 0x004663eb.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004663d6  52                       push     edx
004663d7  25ff000000               and      eax, 0xff
004663dc  31d2                     xor      edx, edx
004663de  8a908c6f4900             mov      dl, byte ptr [eax + 0x496f8c]
004663e4  e865ffffff               call     0x46634e
004663e9  5a                       pop      edx
004663ea  c3                       ret
