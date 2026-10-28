; BatimentLoadCaract: INI loader: TMPSCONSTRUCTION +4, COUTPATATE +0x0c, COUTROCHE +0x0e, NAME +0x13, DIVERS globals; exclusive end 0x00418e95.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00418c70  53                       push     ebx
00418c71  51                       push     ecx
00418c72  52                       push     edx
00418c73  56                       push     esi
00418c74  55                       push     ebp
00418c75  89e5                     mov      ebp, esp
00418c77  83ec04                   sub      esp, 4
00418c7a  b80b000000               mov      eax, 0xb
00418c7f  e813ffffff               call     0x418b97
00418c84  b80a000000               mov      eax, 0xa
00418c89  31d2                     xor      edx, edx
00418c8b  e807ffffff               call     0x418b97
00418c90  668955fc                 mov      word ptr [ebp - 4], dx
00418c94  e98f000000               jmp      0x418d28
00418c99  6bdb34                   imul     ebx, ebx, 0x34
00418c9c  31c0                     xor      eax, eax
00418c9e  8a45fc                   mov      al, byte ptr [ebp - 4]
00418ca1  6bc034                   imul     eax, eax, 0x34
00418ca4  68948f5000               push     0x508f94
00418ca9  682c010000               push     0x12c
00418cae  058c5d4900               add      eax, 0x495d8c
00418cb3  686a424900               push     0x49426a
00418cb8  8d7013                   lea      esi, [eax + 0x13]
00418cbb  56                       push     esi
00418cbc  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418cc3  68948f5000               push     0x508f94
00418cc8  6a05                     push     5
00418cca  687b424900               push     0x49427b
00418ccf  56                       push     esi
00418cd0  668983905d4900           mov      word ptr [ebx + 0x495d90], ax
00418cd7  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418cde  68948f5000               push     0x508f94
00418ce3  6a05                     push     5
00418ce5  6886424900               push     0x494286
00418cea  56                       push     esi
00418ceb  668983985d4900           mov      word ptr [ebx + 0x495d98], ax
00418cf2  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418cf9  6689839a5d4900           mov      word ptr [ebx + 0x495d9a], ax
00418d00  b88c5d4900               mov      eax, 0x495d8c
00418d05  68948f5000               push     0x508f94
00418d0a  01d8                     add      eax, ebx
00418d0c  6a1e                     push     0x1e
00418d0e  83c013                   add      eax, 0x13
00418d11  50                       push     eax
00418d12  56                       push     esi
00418d13  8b5dfc                   mov      ebx, dword ptr [ebp - 4]
00418d16  6890424900               push     0x494290
00418d1b  43                       inc      ebx
00418d1c  56                       push     esi
00418d1d  66895dfc                 mov      word ptr [ebp - 4], bx
00418d21  2eff15b0315200           call     dword ptr cs:[0x5231b0]
00418d28  31db                     xor      ebx, ebx
00418d2a  668b5dfc                 mov      bx, word ptr [ebp - 4]
00418d2e  83fb16                   cmp      ebx, 0x16
00418d31  0f8c62ffffff             jl       0x418c99
00418d37  68948f5000               push     0x508f94
00418d3c  6800020000               push     0x200
00418d41  6895424900               push     0x494295
00418d46  68a3424900               push     0x4942a3
00418d4b  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418d52  68948f5000               push     0x508f94
00418d57  6800020000               push     0x200
00418d5c  68aa424900               push     0x4942aa
00418d61  68b9424900               push     0x4942b9
00418d66  66a3ea734900             mov      word ptr [0x4973ea], ax
00418d6c  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418d73  68948f5000               push     0x508f94
00418d78  6800020000               push     0x200
00418d7d  68c0424900               push     0x4942c0
00418d82  68ce424900               push     0x4942ce
00418d87  66a3f45b4900             mov      word ptr [0x495bf4], ax
00418d8d  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418d94  68948f5000               push     0x508f94
00418d99  6800020000               push     0x200
00418d9e  68d5424900               push     0x4942d5
00418da3  68e4424900               push     0x4942e4
00418da8  66a3f65b4900             mov      word ptr [0x495bf6], ax
00418dae  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418db5  68948f5000               push     0x508f94
00418dba  6800020000               push     0x200
00418dbf  68eb424900               push     0x4942eb
00418dc4  68f5424900               push     0x4942f5
00418dc9  66a3f05b4900             mov      word ptr [0x495bf0], ax
00418dcf  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418dd6  68948f5000               push     0x508f94
00418ddb  6a64                     push     0x64
00418ddd  68fc424900               push     0x4942fc
00418de2  680d434900               push     0x49430d
00418de7  66a3f25b4900             mov      word ptr [0x495bf2], ax
00418ded  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418df4  68948f5000               push     0x508f94
00418df9  6a64                     push     0x64
00418dfb  6814434900               push     0x494314
00418e00  6825434900               push     0x494325
00418e05  66a3906f4900             mov      word ptr [0x496f90], ax
00418e0b  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418e12  68948f5000               push     0x508f94
00418e17  6a1e                     push     0x1e
00418e19  682c434900               push     0x49432c
00418e1e  683f434900               push     0x49433f
00418e23  66a3926f4900             mov      word ptr [0x496f92], ax
00418e29  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418e30  66a3fa5b4900             mov      word ptr [0x495bfa], ax
00418e36  68948f5000               push     0x508f94
00418e3b  6a1e                     push     0x1e
00418e3d  6846434900               push     0x494346
00418e42  685d434900               push     0x49435d
00418e47  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418e4e  68948f5000               push     0x508f94
00418e53  6a07                     push     7
00418e55  6864434900               push     0x494364
00418e5a  6877434900               push     0x494377
00418e5f  66a3fc5b4900             mov      word ptr [0x495bfc], ax
00418e65  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418e6c  68948f5000               push     0x508f94
00418e71  6a07                     push     7
00418e73  687e434900               push     0x49437e
00418e78  6894434900               push     0x494394
00418e7d  66a3005c4900             mov      word ptr [0x495c00], ax
00418e83  2eff15ac315200           call     dword ptr cs:[0x5231ac]
00418e8a  66a3fe5b4900             mov      word ptr [0x495bfe], ax
00418e90  e9d3fdffff               jmp      0x418c68
