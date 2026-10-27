; ProgInit [0x474beb, 0x474f8c)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00474beb  53                     push     ebx
00474bec  51                     push     ecx
00474bed  52                     push     edx
00474bee  56                     push     esi
00474bef  57                     push     edi
00474bf0  81ec00020000           sub      esp, 0x200
00474bf6  89c3                   mov      ebx, eax
00474bf8  e83732ffff             call     0x467e34 ; MemInit
00474bfd  b801000000             mov      eax, 1
00474c02  e819b9ffff             call     0x470520 ; Randomize
00474c07  e8b037feff             call     0x4583bc ; InitRand
00474c0c  6a00                   push     0
00474c0e  be94945000             mov      esi, 0x509494
00474c13  2eff15d0325200         call     dword ptr cs:[0x5232d0]
00474c1a  baff000000             mov      edx, 0xff
00474c1f  b894945000             mov      eax, 0x509494
00474c24  bf948f5000             mov      edi, 0x508f94
00474c29  e853780100             call     0x48c481 ; getcwd
00474c2e  57                     push     edi
00474c2f  8a06                   mov      al, byte ptr [esi]
00474c31  8807                   mov      byte ptr [edi], al
00474c33  3c00                   cmp      al, 0
00474c35  7410                   je       0x474c47
00474c37  8a4601                 mov      al, byte ptr [esi + 1]
00474c3a  83c602                 add      esi, 2
00474c3d  884701                 mov      byte ptr [edi + 1], al
00474c40  83c702                 add      edi, 2
00474c43  3c00                   cmp      al, 0
00474c45  75e8                   jne      0x474c2f
00474c47  5f                     pop      edi
00474c48  be524d4900             mov      esi, 0x494d52
00474c4d  57                     push     edi
00474c4e  2bc9                   sub      ecx, ecx
00474c50  49                     dec      ecx
00474c51  b000                   mov      al, 0
00474c53  f2ae                   repne scasb al, byte ptr es:[edi]
00474c55  4f                     dec      edi
00474c56  8a06                   mov      al, byte ptr [esi]
00474c58  8807                   mov      byte ptr [edi], al
00474c5a  3c00                   cmp      al, 0
00474c5c  7410                   je       0x474c6e
00474c5e  8a4601                 mov      al, byte ptr [esi + 1]
00474c61  83c602                 add      esi, 2
00474c64  884701                 mov      byte ptr [edi + 1], al
00474c67  83c702                 add      edi, 2
00474c6a  3c00                   cmp      al, 0
00474c6c  75e8                   jne      0x474c56
00474c6e  5f                     pop      edi
00474c6f  b85e4d4900             mov      eax, 0x494d5e
00474c74  e87738feff             call     0x4584f0 ; FindCD
00474c79  89c2                   mov      edx, eax
00474c7b  83f8ff                 cmp      eax, -1
00474c7e  743d                   je       0x474cbd
00474c80  be654d4900             mov      esi, 0x494d65
00474c85  bf94955000             mov      edi, 0x509594
00474c8a  80c241                 add      dl, 0x41
00474c8d  30e4                   xor      ah, ah
00474c8f  881594955000           mov      byte ptr [0x509594], dl
00474c95  882595955000           mov      byte ptr [0x509595], ah
00474c9b  57                     push     edi
00474c9c  2bc9                   sub      ecx, ecx
00474c9e  49                     dec      ecx
00474c9f  b000                   mov      al, 0
00474ca1  f2ae                   repne scasb al, byte ptr es:[edi]
00474ca3  4f                     dec      edi
00474ca4  8a06                   mov      al, byte ptr [esi]
00474ca6  8807                   mov      byte ptr [edi], al
00474ca8  3c00                   cmp      al, 0
00474caa  7410                   je       0x474cbc
00474cac  8a4601                 mov      al, byte ptr [esi + 1]
00474caf  83c602                 add      esi, 2
00474cb2  884701                 mov      byte ptr [edi + 1], al
00474cb5  83c702                 add      edi, 2
00474cb8  3c00                   cmp      al, 0
00474cba  75e8                   jne      0x474ca4
00474cbc  5f                     pop      edi
00474cbd  be94945000             mov      esi, 0x509494
00474cc2  bf94915000             mov      edi, 0x509194
00474cc7  57                     push     edi
00474cc8  8a06                   mov      al, byte ptr [esi]
00474cca  8807                   mov      byte ptr [edi], al
00474ccc  3c00                   cmp      al, 0
00474cce  7410                   je       0x474ce0
00474cd0  8a4601                 mov      al, byte ptr [esi + 1]
00474cd3  83c602                 add      esi, 2
00474cd6  884701                 mov      byte ptr [edi + 1], al
00474cd9  83c702                 add      edi, 2
00474cdc  3c00                   cmp      al, 0
00474cde  75e8                   jne      0x474cc8
00474ce0  5f                     pop      edi
00474ce1  be674d4900             mov      esi, 0x494d67
00474ce6  57                     push     edi
00474ce7  2bc9                   sub      ecx, ecx
00474ce9  49                     dec      ecx
00474cea  b000                   mov      al, 0
00474cec  f2ae                   repne scasb al, byte ptr es:[edi]
00474cee  4f                     dec      edi
00474cef  8a06                   mov      al, byte ptr [esi]
00474cf1  8807                   mov      byte ptr [edi], al
00474cf3  3c00                   cmp      al, 0
00474cf5  7410                   je       0x474d07
00474cf7  8a4601                 mov      al, byte ptr [esi + 1]
00474cfa  83c602                 add      esi, 2
00474cfd  884701                 mov      byte ptr [edi + 1], al
00474d00  83c702                 add      edi, 2
00474d03  3c00                   cmp      al, 0
00474d05  75e8                   jne      0x474cef
00474d07  5f                     pop      edi
00474d08  be94945000             mov      esi, 0x509494
00474d0d  bf94935000             mov      edi, 0x509394
00474d12  57                     push     edi
00474d13  8a06                   mov      al, byte ptr [esi]
00474d15  8807                   mov      byte ptr [edi], al
00474d17  3c00                   cmp      al, 0
00474d19  7410                   je       0x474d2b
00474d1b  8a4601                 mov      al, byte ptr [esi + 1]
00474d1e  83c602                 add      esi, 2
00474d21  884701                 mov      byte ptr [edi + 1], al
00474d24  83c702                 add      edi, 2
00474d27  3c00                   cmp      al, 0
00474d29  75e8                   jne      0x474d13
00474d2b  5f                     pop      edi
00474d2c  be6f4d4900             mov      esi, 0x494d6f
00474d31  57                     push     edi
00474d32  2bc9                   sub      ecx, ecx
00474d34  49                     dec      ecx
00474d35  b000                   mov      al, 0
00474d37  f2ae                   repne scasb al, byte ptr es:[edi]
00474d39  4f                     dec      edi
00474d3a  8a06                   mov      al, byte ptr [esi]
00474d3c  8807                   mov      byte ptr [edi], al
00474d3e  3c00                   cmp      al, 0
00474d40  7410                   je       0x474d52
00474d42  8a4601                 mov      al, byte ptr [esi + 1]
00474d45  83c602                 add      esi, 2
00474d48  884701                 mov      byte ptr [edi + 1], al
00474d4b  83c702                 add      edi, 2
00474d4e  3c00                   cmp      al, 0
00474d50  75e8                   jne      0x474d3a
00474d52  5f                     pop      edi
00474d53  be94945000             mov      esi, 0x509494
00474d58  bf94905000             mov      edi, 0x509094
00474d5d  57                     push     edi
00474d5e  8a06                   mov      al, byte ptr [esi]
00474d60  8807                   mov      byte ptr [edi], al
00474d62  3c00                   cmp      al, 0
00474d64  7410                   je       0x474d76
00474d66  8a4601                 mov      al, byte ptr [esi + 1]
00474d69  83c602                 add      esi, 2
00474d6c  884701                 mov      byte ptr [edi + 1], al
00474d6f  83c702                 add      edi, 2
00474d72  3c00                   cmp      al, 0
00474d74  75e8                   jne      0x474d5e
00474d76  5f                     pop      edi
00474d77  be7c4d4900             mov      esi, 0x494d7c
00474d7c  57                     push     edi
00474d7d  2bc9                   sub      ecx, ecx
00474d7f  49                     dec      ecx
00474d80  b000                   mov      al, 0
00474d82  f2ae                   repne scasb al, byte ptr es:[edi]
00474d84  4f                     dec      edi
00474d85  8a06                   mov      al, byte ptr [esi]
00474d87  8807                   mov      byte ptr [edi], al
00474d89  3c00                   cmp      al, 0
00474d8b  7410                   je       0x474d9d
00474d8d  8a4601                 mov      al, byte ptr [esi + 1]
00474d90  83c602                 add      esi, 2
00474d93  884701                 mov      byte ptr [edi + 1], al
00474d96  83c702                 add      edi, 2
00474d99  3c00                   cmp      al, 0
00474d9b  75e8                   jne      0x474d85
00474d9d  5f                     pop      edi
00474d9e  e8e2f9ffff             call     0x474785 ; SortLoadCaract
00474da3  be94945000             mov      esi, 0x509494
00474da8  89e7                   mov      edi, esp
00474daa  e832a9feff             call     0x45f6e1 ; PaletteAlloc
00474daf  57                     push     edi
00474db0  8a06                   mov      al, byte ptr [esi]
00474db2  8807                   mov      byte ptr [edi], al
00474db4  3c00                   cmp      al, 0
00474db6  7410                   je       0x474dc8
00474db8  8a4601                 mov      al, byte ptr [esi + 1]
00474dbb  83c602                 add      esi, 2
00474dbe  884701                 mov      byte ptr [edi + 1], al
00474dc1  83c702                 add      edi, 2
00474dc4  3c00                   cmp      al, 0
00474dc6  75e8                   jne      0x474db0
00474dc8  5f                     pop      edi
00474dc9  be884d4900             mov      esi, 0x494d88
00474dce  89e7                   mov      edi, esp
00474dd0  57                     push     edi
00474dd1  2bc9                   sub      ecx, ecx
00474dd3  49                     dec      ecx
00474dd4  b000                   mov      al, 0
00474dd6  f2ae                   repne scasb al, byte ptr es:[edi]
00474dd8  4f                     dec      edi
00474dd9  8a06                   mov      al, byte ptr [esi]
00474ddb  8807                   mov      byte ptr [edi], al
00474ddd  3c00                   cmp      al, 0
00474ddf  7410                   je       0x474df1
00474de1  8a4601                 mov      al, byte ptr [esi + 1]
00474de4  83c602                 add      esi, 2
00474de7  884701                 mov      byte ptr [edi + 1], al
00474dea  83c702                 add      edi, 2
00474ded  3c00                   cmp      al, 0
00474def  75e8                   jne      0x474dd9
00474df1  5f                     pop      edi
00474df2  89e0                   mov      eax, esp
00474df4  8b15b0244e00           mov      edx, dword ptr [0x4e24b0]
00474dfa  e8ea4a0000             call     0x4798e9 ; LoadPalette
00474dff  89d8                   mov      eax, ebx
00474e01  e852a7f9ff             call     0x40f558 ; AffInit
00474e06  31c0                   xor      eax, eax
00474e08  be94945000             mov      esi, 0x509494
00474e0d  e871450000             call     0x479383 ; InitTextLangue
00474e12  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
00474e17  8dbc2400010000         lea      edi, [esp + 0x100]
00474e1e  e80ea0fcff             call     0x43ee31 ; DDSetPalette
00474e23  e88ca5fcff             call     0x43f3b4 ; DDLockSurface
00474e28  a3708f5000             mov      dword ptr [0x508f70], eax
00474e2d  57                     push     edi
00474e2e  8a06                   mov      al, byte ptr [esi]
00474e30  8807                   mov      byte ptr [edi], al
00474e32  3c00                   cmp      al, 0
00474e34  7410                   je       0x474e46
00474e36  8a4601                 mov      al, byte ptr [esi + 1]
00474e39  83c602                 add      esi, 2
00474e3c  884701                 mov      byte ptr [edi + 1], al
00474e3f  83c702                 add      edi, 2
00474e42  3c00                   cmp      al, 0
00474e44  75e8                   jne      0x474e2e
00474e46  5f                     pop      edi
00474e47  be964d4900             mov      esi, 0x494d96
00474e4c  8dbc2400010000         lea      edi, [esp + 0x100]
00474e53  57                     push     edi
00474e54  2bc9                   sub      ecx, ecx
00474e56  49                     dec      ecx
00474e57  b000                   mov      al, 0
00474e59  f2ae                   repne scasb al, byte ptr es:[edi]
00474e5b  4f                     dec      edi
00474e5c  8a06                   mov      al, byte ptr [esi]
00474e5e  8807                   mov      byte ptr [edi], al
00474e60  3c00                   cmp      al, 0
00474e62  7410                   je       0x474e74
00474e64  8a4601                 mov      al, byte ptr [esi + 1]
00474e67  83c602                 add      esi, 2
00474e6a  884701                 mov      byte ptr [edi + 1], al
00474e6d  83c702                 add      edi, 2
00474e70  3c00                   cmp      al, 0
00474e72  75e8                   jne      0x474e5c
00474e74  5f                     pop      edi
00474e75  8d842400010000         lea      eax, [esp + 0x100]
00474e7c  8b15708f5000           mov      edx, dword ptr [0x508f70]
00474e82  e83d4b0000             call     0x4799c4 ; LoadPie
00474e87  a1708f5000             mov      eax, dword ptr [0x508f70]
00474e8c  e8b4a5fcff             call     0x43f445 ; DDUnlockSurface
00474e91  b801000000             mov      eax, 1
00474e96  e8b4a2fcff             call     0x43f14f ; DDFlipPage
00474e9b  e8da38faff             call     0x41877a ; LoadSTRATBank
00474ea0  ba3c000000             mov      edx, 0x3c
00474ea5  a35c8f5000             mov      dword ptr [0x508f5c], eax
00474eaa  e8e136faff             call     0x418590 ; SetBank
00474eaf  e864abf9ff             call     0x40fa18 ; CacheAlloc
00474eb4  e862cbfcff             call     0x441a1b ; EnginAlloc
00474eb9  e8d73ffaff             call     0x418e95 ; BatimentAlloc
00474ebe  e8cc64ffff             call     0x46b38f ; MissionAlloc
00474ec3  e8db87ffff             call     0x46d6a3 ; PlayerAlloc
00474ec8  e89b50ffff             call     0x469f68 ; MiniMapAlloc
00474ecd  e80fa3fbff             call     0x42f1e1 ; Chemin_Open
00474ed2  e83eac0000             call     0x47fb15 ; IaAlloc
00474ed7  e8c490ffff             call     0x46dfa0 ; ProjectileAlloc
00474edc  e8bbbcffff             call     0x470b9c ; RechercheInit
00474ee1  e8facffeff             call     0x461ee0 ; MarcheInit
00474ee6  e8c98dffff             call     0x46dcb4 ; InitPlayer
00474eeb  e83ba4feff             call     0x45f32b ; InitInputPlayer
00474ef0  e80d040000             call     0x475302 ; TerrainLoadObstacle
00474ef5  e826070000             call     0x475620 ; TerrainLoadColor
00474efa  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
00474eff  e83caafeff             call     0x45f940 ; CalculOmbrage
00474f04  ba3c000000             mov      edx, 0x3c
00474f09  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
00474f0e  e8e9abfeff             call     0x45fafc ; CalculEclairage
00474f13  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
00474f18  e888adfeff             call     0x45fca5 ; CalculNoirBlanc
00474f1d  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
00474f22  e80aaffeff             call     0x45fe31 ; CalculNegatif
00474f27  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
00474f2c  31db                   xor      ebx, ebx
00474f2e  e8acaefeff             call     0x45fddf ; CalculGris
00474f33  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
00474f38  ba04000000             mov      edx, 4
00474f3d  e81fb0feff             call     0x45ff61 ; CalculTabPlayer
00474f42  b803000000             mov      eax, 3
00474f47  e860a6feff             call     0x45f5ac ; SetCyclage
00474f4c  ba07000000             mov      edx, 7
00474f51  b805000000             mov      eax, 5
00474f56  31db                   xor      ebx, ebx
00474f58  e84fa6feff             call     0x45f5ac ; SetCyclage
00474f5d  ba0f000000             mov      edx, 0xf
00474f62  b808000000             mov      eax, 8
00474f67  31db                   xor      ebx, ebx
00474f69  e83ea6feff             call     0x45f5ac ; SetCyclage
00474f6e  30d2                   xor      dl, dl
00474f70  8815908f5000           mov      byte ptr [0x508f90], dl
00474f76  b601                   mov      dh, 1
00474f78  8835782f4e00           mov      byte ptr [0x4e2f78], dh
00474f7e  88f0                   mov      al, dh
00474f80  81c400020000           add      esp, 0x200
00474f86  5f                     pop      edi
00474f87  5e                     pop      esi
00474f88  5a                     pop      edx
00474f89  59                     pop      ecx
00474f8a  5b                     pop      ebx
00474f8b  c3                     ret      
