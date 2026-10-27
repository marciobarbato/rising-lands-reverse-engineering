; AnimBallonStatic [0x447b2f, 0x447d95)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00447b2f  53                     push     ebx
00447b30  51                     push     ecx
00447b31  52                     push     edx
00447b32  56                     push     esi
00447b33  89c1                   mov      ecx, eax
00447b35  31c0                   xor      eax, eax
00447b37  6689c8                 mov      ax, cx
00447b3a  89c3                   mov      ebx, eax
00447b3c  c1e304                 shl      ebx, 4
00447b3f  01c3                   add      ebx, eax
00447b41  c1e302                 shl      ebx, 2
00447b44  01c3                   add      ebx, eax
00447b46  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
00447b4b  c1e302                 shl      ebx, 2
00447b4e  01c3                   add      ebx, eax
00447b50  31c0                   xor      eax, eax
00447b52  8a83ae000000           mov      al, byte ptr [ebx + 0xae]
00447b58  85c0                   test     eax, eax
00447b5a  0f8576000000           jne      0x447bd6
00447b60  b811000000             mov      eax, 0x11
00447b65  be28000000             mov      esi, 0x28
00447b6a  31d2                   xor      edx, edx
00447b6c  e86b890200             call     0x4704dc ; Random
00447b71  f7f6                   div      esi
00447b73  85d2                   test     edx, edx
00447b75  755f                   jne      0x447bd6
00447b77  31c0                   xor      eax, eax
00447b79  8a83ab000000           mov      al, byte ptr [ebx + 0xab]
00447b7f  39f0                   cmp      eax, esi
00447b81  7e3d                   jle      0x447bc0
00447b83  31c0                   xor      eax, eax
00447b85  8a8394000000           mov      al, byte ptr [ebx + 0x94]
00447b8b  85c0                   test     eax, eax
00447b8d  7508                   jne      0x447b97
00447b8f  fe8394000000           inc      byte ptr [ebx + 0x94]
00447b95  eb3f                   jmp      0x447bd6 ; 
00447b97  83f802                 cmp      eax, 2
00447b9a  750a                   jne      0x447ba6
00447b9c  fec8                   dec      al
00447b9e  888394000000           mov      byte ptr [ebx + 0x94], al
00447ba4  eb30                   jmp      0x447bd6 ; 
00447ba6  b812000000             mov      eax, 0x12
00447bab  be03000000             mov      esi, 3
00447bb0  e827890200             call     0x4704dc ; Random
00447bb5  f7f6                   div      esi
00447bb7  4a                     dec      edx
00447bb8  009394000000           add      byte ptr [ebx + 0x94], dl
00447bbe  eb16                   jmp      0x447bd6 ; 
00447bc0  31c0                   xor      eax, eax
00447bc2  8a8394000000           mov      al, byte ptr [ebx + 0x94]
00447bc8  85c0                   test     eax, eax
00447bca  740a                   je       0x447bd6
00447bcc  88c4                   mov      ah, al
00447bce  fecc                   dec      ah
00447bd0  88a394000000           mov      byte ptr [ebx + 0x94], ah
00447bd6  31c0                   xor      eax, eax
00447bd8  8a83ae000000           mov      al, byte ptr [ebx + 0xae]
00447bde  85c0                   test     eax, eax
00447be0  0f858f000000           jne      0x447c75
00447be6  b813000000             mov      eax, 0x13
00447beb  be0a000000             mov      esi, 0xa
00447bf0  31d2                   xor      edx, edx
00447bf2  e8e5880200             call     0x4704dc ; Random
00447bf7  f7f6                   div      esi
00447bf9  85d2                   test     edx, edx
00447bfb  0f8574000000           jne      0x447c75
00447c01  31c0                   xor      eax, eax
00447c03  8a83ab000000           mov      al, byte ptr [ebx + 0xab]
00447c09  83f828                 cmp      eax, 0x28
00447c0c  7f07                   jg       0x447c15
00447c0e  c6839500000000         mov      byte ptr [ebx + 0x95], 0
00447c15  31c0                   xor      eax, eax
00447c17  8a8395000000           mov      al, byte ptr [ebx + 0x95]
00447c1d  85c0                   test     eax, eax
00447c1f  7516                   jne      0x447c37
00447c21  8a8396000000           mov      al, byte ptr [ebx + 0x96]
00447c27  85c0                   test     eax, eax
00447c29  740c                   je       0x447c37
00447c2b  88c6                   mov      dh, al
00447c2d  fece                   dec      dh
00447c2f  88b396000000           mov      byte ptr [ebx + 0x96], dh
00447c35  eb17                   jmp      0x447c4e ; 
00447c37  31c0                   xor      eax, eax
00447c39  8a8396000000           mov      al, byte ptr [ebx + 0x96]
00447c3f  83f810                 cmp      eax, 0x10
00447c42  7d0a                   jge      0x447c4e
00447c44  88c2                   mov      dl, al
00447c46  fec2                   inc      dl
00447c48  889396000000           mov      byte ptr [ebx + 0x96], dl
00447c4e  31c0                   xor      eax, eax
00447c50  8a8396000000           mov      al, byte ptr [ebx + 0x96]
00447c56  85c0                   test     eax, eax
00447c58  7507                   jne      0x447c61
00447c5a  c6839500000001         mov      byte ptr [ebx + 0x95], 1
00447c61  31c0                   xor      eax, eax
00447c63  8a8396000000           mov      al, byte ptr [ebx + 0x96]
00447c69  83f80f                 cmp      eax, 0xf
00447c6c  7507                   jne      0x447c75
00447c6e  c6839500000000         mov      byte ptr [ebx + 0x95], 0
00447c75  80bbae00000000         cmp      byte ptr [ebx + 0xae], 0
00447c7c  7425                   je       0x447ca3
00447c7e  b814000000             mov      eax, 0x14
00447c83  be05000000             mov      esi, 5
00447c88  31d2                   xor      edx, edx
00447c8a  e84d880200             call     0x4704dc ; Random
00447c8f  f7f6                   div      esi
00447c91  85d2                   test     edx, edx
00447c93  7506                   jne      0x447c9b
00447c95  fe83ab000000           inc      byte ptr [ebx + 0xab]
00447c9b  fe83a4000000           inc      byte ptr [ebx + 0xa4]
00447ca1  eb1d                   jmp      0x447cc0 ; 
00447ca3  b815000000             mov      eax, 0x15
00447ca8  be0a000000             mov      esi, 0xa
00447cad  31d2                   xor      edx, edx
00447caf  e828880200             call     0x4704dc ; Random
00447cb4  f7f6                   div      esi
00447cb6  85d2                   test     edx, edx
00447cb8  7506                   jne      0x447cc0
00447cba  fe8bab000000           dec      byte ptr [ebx + 0xab]
00447cc0  31c0                   xor      eax, eax
00447cc2  8a83ae000000           mov      al, byte ptr [ebx + 0xae]
00447cc8  85c0                   test     eax, eax
00447cca  0f85ac000000           jne      0x447d7c
00447cd0  8a83ab000000           mov      al, byte ptr [ebx + 0xab]
00447cd6  83f828                 cmp      eax, 0x28
00447cd9  0f8d9d000000           jge      0x447d7c
00447cdf  31c0                   xor      eax, eax
00447ce1  8a8396000000           mov      al, byte ptr [ebx + 0x96]
00447ce7  85c0                   test     eax, eax
00447ce9  0f858d000000           jne      0x447d7c
00447cef  8a8394000000           mov      al, byte ptr [ebx + 0x94]
00447cf5  85c0                   test     eax, eax
00447cf7  0f857f000000           jne      0x447d7c
00447cfd  c683ae00000001         mov      byte ptr [ebx + 0xae], 1
00447d04  c683a400000000         mov      byte ptr [ebx + 0xa4], 0
00447d0b  81e1ffff0000           and      ecx, 0xffff
00447d11  89cb                   mov      ebx, ecx
00447d13  c1e304                 shl      ebx, 4
00447d16  01cb                   add      ebx, ecx
00447d18  c1e302                 shl      ebx, 2
00447d1b  01cb                   add      ebx, ecx
00447d1d  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
00447d22  c1e302                 shl      ebx, 2
00447d25  31d2                   xor      edx, edx
00447d27  01c3                   add      ebx, eax
00447d29  31c0                   xor      eax, eax
00447d2b  8a1541805000           mov      dl, byte ptr [0x508041]
00447d31  668b4308               mov      ax, word ptr [ebx + 8]
00447d35  e8b6e90200             call     0x4766f0 ; TerrainEstDecouvert
00447d3a  84c0                   test     al, al
00447d3c  7452                   je       0x447d90
00447d3e  89c8                   mov      eax, ecx
00447d40  e8188fffff             call     0x440c5d ; EnginGetVolume
00447d45  8b9304010000           mov      edx, dword ptr [ebx + 0x104]
00447d4b  c683f900000000         mov      byte ptr [ebx + 0xf9], 0
00447d52  83faff                 cmp      edx, -1
00447d55  7539                   jne      0x447d90
00447d57  50                     push     eax
00447d58  31d2                   xor      edx, edx
00447d5a  31c9                   xor      ecx, ecx
00447d5c  8a5301                 mov      dl, byte ptr [ebx + 1]
00447d5f  8d8304010000           lea      eax, [ebx + 0x104]
00447d65  c1e210                 shl      edx, 0x10
00447d68  89c3                   mov      ebx, eax
00447d6a  b850000000             mov      eax, 0x50
00447d6f  80ce08                 or       dh, 8
00447d72  e8022d0400             call     0x48aa79 ; PlaySnd_PostSound
00447d77  5e                     pop      esi
00447d78  5a                     pop      edx
00447d79  59                     pop      ecx
00447d7a  5b                     pop      ebx
00447d7b  c3                     ret      
00447d7c  31c0                   xor      eax, eax
00447d7e  8a83ab000000           mov      al, byte ptr [ebx + 0xab]
00447d84  83f832                 cmp      eax, 0x32
00447d87  7507                   jne      0x447d90
00447d89  c683ae00000000         mov      byte ptr [ebx + 0xae], 0
00447d90  5e                     pop      esi
00447d91  5a                     pop      edx
00447d92  59                     pop      ecx
00447d93  5b                     pop      ebx
00447d94  c3                     ret      
