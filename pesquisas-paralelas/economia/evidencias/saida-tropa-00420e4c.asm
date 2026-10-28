; SortieTroupe economic prefix, through call to CalculPosition; exclusive end 0x00420f5f.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Capstone instruction listing, not inferred pseudocode.
00420e4c  53                       push     ebx
00420e4d  51                       push     ecx
00420e4e  56                       push     esi
00420e4f  57                       push     edi
00420e50  55                       push     ebp
00420e51  83ec0c                   sub      esp, 0xc
00420e54  50                       push     eax
00420e55  8854240c                 mov      byte ptr [esp + 0xc], dl
00420e59  31c0                     xor      eax, eax
00420e5b  668b0424                 mov      ax, word ptr [esp]
00420e5f  89c2                     mov      edx, eax
00420e61  c1e204                   shl      edx, 4
00420e64  01c2                     add      edx, eax
00420e66  c1e202                   shl      edx, 2
00420e69  01c2                     add      edx, eax
00420e6b  bfc8a04900               mov      edi, 0x49a0c8
00420e70  c1e202                   shl      edx, 2
00420e73  01d7                     add      edi, edx
00420e75  31c0                     xor      eax, eax
00420e77  8a477b                   mov      al, byte ptr [edi + 0x7b]
00420e7a  e838020200               call     0x4410b7
00420e7f  25ffff0000               and      eax, 0xffff
00420e84  89c2                     mov      edx, eax
00420e86  c1e202                   shl      edx, 2
00420e89  29c2                     sub      edx, eax
00420e8b  c1e203                   shl      edx, 3
00420e8e  01c2                     add      edx, eax
00420e90  8b9f8c000000             mov      ebx, dword ptr [edi + 0x8c]
00420e96  c1e202                   shl      edx, 2
00420e99  39da                     cmp      edx, ebx
00420e9b  0f8749030000             ja       0x4211ea
00420ea1  bb09000000               mov      ebx, 9
00420ea6  ba01000000               mov      edx, 1
00420eab  8d470c                   lea      eax, [edi + 0xc]
00420eae  e837640200               call     0x4472ea
00420eb3  89442404                 mov      dword ptr [esp + 4], eax
00420eb7  25ffff0000               and      eax, 0xffff
00420ebc  e8e5650200               call     0x4474a6
00420ec1  89c6                     mov      esi, eax
00420ec3  bb02000000               mov      ebx, 2
00420ec8  89f0                     mov      eax, esi
00420eca  89da                     mov      edx, ebx
00420ecc  e8e7620200               call     0x4471b8
00420ed1  6685c0                   test     ax, ax
00420ed4  742b                     je       0x420f01
00420ed6  bb02000000               mov      ebx, 2
00420edb  89f0                     mov      eax, esi
00420edd  0fb66f04                 movzx    ebp, byte ptr [edi + 4]
00420ee1  31c9                     xor      ecx, ecx
00420ee3  89da                     mov      edx, ebx
00420ee5  668b0c24                 mov      cx, word ptr [esp]
00420ee9  e8fc630200               call     0x4472ea
00420eee  31d2                     xor      edx, edx
00420ef0  89eb                     mov      ebx, ebp
00420ef2  6689c2                   mov      dx, ax
00420ef5  b802000000               mov      eax, 2
00420efa  e810250000               call     0x42340f
00420eff  ebc2                     jmp      0x420ec3
00420f01  bb01000000               mov      ebx, 1
00420f06  ba02000000               mov      edx, 2
00420f0b  89f0                     mov      eax, esi
00420f0d  e8a6620200               call     0x4471b8
00420f12  6685c0                   test     ax, ax
00420f15  742e                     je       0x420f45
00420f17  bb01000000               mov      ebx, 1
00420f1c  ba02000000               mov      edx, 2
00420f21  89f0                     mov      eax, esi
00420f23  0fb66f04                 movzx    ebp, byte ptr [edi + 4]
00420f27  31c9                     xor      ecx, ecx
00420f29  e8bc630200               call     0x4472ea
00420f2e  668b0c24                 mov      cx, word ptr [esp]
00420f32  31d2                     xor      edx, edx
00420f34  89eb                     mov      ebx, ebp
00420f36  6689c2                   mov      dx, ax
00420f39  b801000000               mov      eax, 1
00420f3e  e8cc240000               call     0x42340f
00420f43  ebbc                     jmp      0x420f01
00420f45  31c0                     xor      eax, eax
00420f47  31c9                     xor      ecx, ecx
00420f49  31db                     xor      ebx, ebx
00420f4b  31f6                     xor      esi, esi
00420f4d  668b0424                 mov      ax, word ptr [esp]
00420f51  8a5c240c                 mov      bl, byte ptr [esp + 0xc]
00420f55  668b742404               mov      si, word ptr [esp + 4]
00420f5a  e839f7ffff               call     0x420698
