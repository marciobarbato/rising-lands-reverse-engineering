; MissionLoad [0x46c2cf, 0x46c5e3)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0046c2cf  53                     push     ebx
0046c2d0  51                     push     ecx
0046c2d1  52                     push     edx
0046c2d2  56                     push     esi
0046c2d3  57                     push     edi
0046c2d4  81ec2c010000           sub      esp, 0x12c
0046c2da  a0e46f4900             mov      al, byte ptr [0x496fe4]
0046c2df  8d942400010000         lea      edx, [esp + 0x100]
0046c2e6  88842428010000         mov      byte ptr [esp + 0x128], al
0046c2ed  31c0                   xor      eax, eax
0046c2ef  be94955000             mov      esi, 0x509594
0046c2f4  8a842428010000         mov      al, byte ptr [esp + 0x128]
0046c2fb  89e7                   mov      edi, esp
0046c2fd  e8b6feffff             call     0x46c1b8 ; MakeMissionName
0046c302  57                     push     edi
0046c303  8a06                   mov      al, byte ptr [esi]
0046c305  8807                   mov      byte ptr [edi], al
0046c307  3c00                   cmp      al, 0
0046c309  7410                   je       0x46c31b
0046c30b  8a4601                 mov      al, byte ptr [esi + 1]
0046c30e  83c602                 add      esi, 2
0046c311  884701                 mov      byte ptr [edi + 1], al
0046c314  83c702                 add      edi, 2
0046c317  3c00                   cmp      al, 0
0046c319  75e8                   jne      0x46c303
0046c31b  5f                     pop      edi
0046c31c  8db42400010000         lea      esi, [esp + 0x100]
0046c323  89e7                   mov      edi, esp
0046c325  baffff0000             mov      edx, 0xffff
0046c32a  57                     push     edi
0046c32b  2bc9                   sub      ecx, ecx
0046c32d  49                     dec      ecx
0046c32e  b000                   mov      al, 0
0046c330  f2ae                   repne scasb al, byte ptr es:[edi]
0046c332  4f                     dec      edi
0046c333  8a06                   mov      al, byte ptr [esi]
0046c335  8807                   mov      byte ptr [edi], al
0046c337  3c00                   cmp      al, 0
0046c339  7410                   je       0x46c34b
0046c33b  8a4601                 mov      al, byte ptr [esi + 1]
0046c33e  83c602                 add      esi, 2
0046c341  884701                 mov      byte ptr [edi + 1], al
0046c344  83c702                 add      edi, 2
0046c347  3c00                   cmp      al, 0
0046c349  75e8                   jne      0x46c333
0046c34b  5f                     pop      edi
0046c34c  668915381a4e00         mov      word ptr [0x4e1a38], dx
0046c353  6689153a1a4e00         mov      word ptr [0x4e1a3a], dx
0046c35a  e83025ffff             call     0x45e88f ; IconeReset
0046c35f  e8b1efffff             call     0x46b315 ; TerrainReset
0046c364  e897dbffff             call     0x469f00 ; MiniMapReset
0046c369  e8eee3faff             call     0x41a75c ; BatimentResetAll
0046c36e  e8e652fdff             call     0x441659 ; EnginResetAll
0046c373  e8921c0000             call     0x46e00a ; ProjectileReset
0046c378  e88bd5ffff             call     0x469908 ; MessageBoxInit
0046c37d  e8ea57fdff             call     0x441b6c ; BallonInit
0046c382  ba3b4b4900             mov      edx, 0x494b3b
0046c387  89e0                   mov      eax, esp
0046c389  e892c0feff             call     0x458420 ; FileOpen
0046c38e  84c0                   test     al, al
0046c390  0f8442020000           je       0x46c5d8
0046c396  b804000000             mov      eax, 4
0046c39b  31d2                   xor      edx, edx
0046c39d  e8e9c0feff             call     0x45848b ; FileSeek
0046c3a2  ba00000100             mov      edx, 0x10000
0046c3a7  a1a87d5000             mov      eax, dword ptr [0x507da8]
0046c3ac  e8b0c0feff             call     0x458461 ; FileRead
0046c3b1  ba00000200             mov      edx, 0x20000
0046c3b6  a1707d5000             mov      eax, dword ptr [0x507d70]
0046c3bb  e8a1c0feff             call     0x458461 ; FileRead
0046c3c0  ba00000100             mov      edx, 0x10000
0046c3c5  a1747d5000             mov      eax, dword ptr [0x507d74]
0046c3ca  e892c0feff             call     0x458461 ; FileRead
0046c3cf  ba00000100             mov      edx, 0x10000
0046c3d4  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0046c3d9  e883c0feff             call     0x458461 ; FileRead
0046c3de  31c0                   xor      eax, eax
0046c3e0  eb08                   jmp      0x46c3ea ;
0046c3e2  40                     inc      eax
0046c3e3  3d00000100             cmp      eax, 0x10000
0046c3e8  7320                   jae      0x46c40a
0046c3ea  8b15747d5000           mov      edx, dword ptr [0x507d74]
0046c3f0  01c2                   add      edx, eax
0046c3f2  31db                   xor      ebx, ebx
0046c3f4  8a1a                   mov      bl, byte ptr [edx]
0046c3f6  83fb36                 cmp      ebx, 0x36
0046c3f9  75e7                   jne      0x46c3e2
0046c3fb  c60242                 mov      byte ptr [edx], 0x42
0046c3fe  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
0046c404  c6040201               mov      byte ptr [edx + eax], 1
0046c408  ebd8                   jmp      0x46c3e2 ;
0046c40a  30c9                   xor      cl, cl
0046c40c  eb27                   jmp      0x46c435 ;
0046c40e  ba02000000             mov      edx, 2
0046c413  8d842418010000         lea      eax, [esp + 0x118]
0046c41a  e842c0feff             call     0x458461 ; FileRead
0046c41f  31d2                   xor      edx, edx
0046c421  b801000000             mov      eax, 1
0046c426  668b942418010000       mov      dx, word ptr [esp + 0x118]
0046c42e  fec1                   inc      cl
0046c430  e867b5ffff             call     0x46799c ; SetMatiere
0046c435  31db                   xor      ebx, ebx
0046c437  88cb                   mov      bl, cl
0046c439  83fb04                 cmp      ebx, 4
0046c43c  7cd0                   jl       0x46c40e
0046c43e  30c9                   xor      cl, cl
0046c440  eb27                   jmp      0x46c469 ;
0046c442  ba02000000             mov      edx, 2
0046c447  8d842418010000         lea      eax, [esp + 0x118]
0046c44e  e80ec0feff             call     0x458461 ; FileRead
0046c453  31d2                   xor      edx, edx
0046c455  b802000000             mov      eax, 2
0046c45a  668b942418010000       mov      dx, word ptr [esp + 0x118]
0046c462  fec1                   inc      cl
0046c464  e833b5ffff             call     0x46799c ; SetMatiere
0046c469  31db                   xor      ebx, ebx
0046c46b  88cb                   mov      bl, cl
0046c46d  83fb04                 cmp      ebx, 4
0046c470  7cd0                   jl       0x46c442
0046c472  30c9                   xor      cl, cl
0046c474  eb24                   jmp      0x46c49a ;
0046c476  ba02000000             mov      edx, 2
0046c47b  8d842418010000         lea      eax, [esp + 0x118]
0046c482  e8dabffeff             call     0x458461 ; FileRead
0046c487  31d2                   xor      edx, edx
0046c489  31c0                   xor      eax, eax
0046c48b  668b942418010000       mov      dx, word ptr [esp + 0x118]
0046c493  fec1                   inc      cl
0046c495  e802b5ffff             call     0x46799c ; SetMatiere
0046c49a  31db                   xor      ebx, ebx
0046c49c  88cb                   mov      bl, cl
0046c49e  83fb04                 cmp      ebx, 4
0046c4a1  7cd3                   jl       0x46c476
0046c4a3  ba02000000             mov      edx, 2
0046c4a8  b868714900             mov      eax, 0x497168
0046c4ad  e8afbffeff             call     0x458461 ; FileRead
0046c4b2  ba02000000             mov      edx, 2
0046c4b7  b86a714900             mov      eax, 0x49716a
0046c4bc  31db                   xor      ebx, ebx
0046c4be  e89ebffeff             call     0x458461 ; FileRead
0046c4c3  be02000000             mov      esi, 2
0046c4c8  eb01                   jmp      0x46c4cb ;
0046c4ca  43                     inc      ebx
0046c4cb  31c0                   xor      eax, eax
0046c4cd  6689d8                 mov      ax, bx
0046c4d0  83f804                 cmp      eax, 4
0046c4d3  7d3d                   jge      0x46c512
0046c4d5  31d2                   xor      edx, edx
0046c4d7  8a1541805000           mov      dl, byte ptr [0x508041]
0046c4dd  39d0                   cmp      eax, edx
0046c4df  751a                   jne      0x46c4fb
0046c4e1  b820875000             mov      eax, 0x508720
0046c4e6  89f2                   mov      edx, esi
0046c4e8  e874bffeff             call     0x458461 ; FileRead
0046c4ed  b822875000             mov      eax, 0x508722
0046c4f2  89f2                   mov      edx, esi
0046c4f4  e868bffeff             call     0x458461 ; FileRead
0046c4f9  ebcf                   jmp      0x46c4ca ;
0046c4fb  8d842424010000         lea      eax, [esp + 0x124]
0046c502  89f2                   mov      edx, esi
0046c504  e858bffeff             call     0x458461 ; FileRead
0046c509  8d842424010000         lea      eax, [esp + 0x124]
0046c510  ebe0                   jmp      0x46c4f2 ;
0046c512  e80529fcff             call     0x42ee1c ; Chemin_Remap
0046c517  ba02000000             mov      edx, 2
0046c51c  8d84241c010000         lea      eax, [esp + 0x11c]
0046c523  e839bffeff             call     0x458461 ; FileRead
0046c528  ba02000000             mov      edx, 2
0046c52d  8d842414010000         lea      eax, [esp + 0x114]
0046c534  31db                   xor      ebx, ebx
0046c536  eb31                   jmp      0x46c569 ;
0046c538  ba02000000             mov      edx, 2
0046c53d  8d842420010000         lea      eax, [esp + 0x120]
0046c544  e818bffeff             call     0x458461 ; FileRead
0046c549  31c0                   xor      eax, eax
0046c54b  668b842420010000       mov      ax, word ptr [esp + 0x120]
0046c553  69c014010000           imul     eax, eax, 0x114
0046c559  31d2                   xor      edx, edx
0046c55b  668b942414010000       mov      dx, word ptr [esp + 0x114]
0046c563  05c8a04900             add      eax, 0x49a0c8
0046c568  43                     inc      ebx
0046c569  e8f3befeff             call     0x458461 ; FileRead
0046c56e  663b9c241c010000       cmp      bx, word ptr [esp + 0x11c]
0046c576  72c0                   jb       0x46c538
0046c578  e842e7ffff             call     0x46acbf ; LoadEngin
0046c57d  e8c88d0000             call     0x47534a ; LoadMine
0046c582  e8c6fc0000             call     0x47c24d ; IALoadAttaqueIni
0046c587  e83bf70000             call     0x47bcc7 ; LoadBatimentGhost
0046c58c  e8b9fa0000             call     0x47c04a ; LoadCadreInfluence
0046c591  e86fc5feff             call     0x458b05 ; LoadFinMission
0046c596  e874fd0000             call     0x47c30f ; LoadCalculMissionDivers
0046c59b  e864fe0000             call     0x47c404 ; LoadObjectif
0046c5a0  e88be60000             call     0x47ac30 ; LoadEntrerMonstre
0046c5a5  e8a2befeff             call     0x45844c ; FileClose
0046c5aa  e873fbffff             call     0x46c122 ; MissionPlaceTerrain
0046c5af  e8a54efdff             call     0x441459 ; EnginInitTechnologie
0046c5b4  e859cbfaff             call     0x419112 ; BatimentInitCave
0046c5b9  e86550fdff             call     0x441623 ; Engin_RetrieveExperimente
0046c5be  e87e190000             call     0x46df41 ; PlayerRetrieve
0046c5c3  31c0                   xor      eax, eax
0046c5c5  8a842428010000         mov      al, byte ptr [esp + 0x128]
0046c5cc  e89d2d0100             call     0x47f36e ; iaReset
0046c5d1  e8a63cffff             call     0x46027c ; MarcheResetAll
0046c5d6  b001                   mov      al, 1
0046c5d8  81c42c010000           add      esp, 0x12c
0046c5de  e94df6ffff             jmp      0x46bc30 ;
