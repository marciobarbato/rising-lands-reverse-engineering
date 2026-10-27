; despacho_simulacao: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0042d2de  e845030400            call     0x46d628
0042d2e3  e8ceae0200            call     0x4581b6
0042d2e8  84c0                  test     al, al
0042d2ea  0f85fa010000          jne      0x42d4ea
0042d2f0  803d282f4e0000        cmp      byte ptr [0x4e2f28], 0
0042d2f7  7534                  jne      0x42d32d
0042d2f9  8a1d181d4e00          mov      bl, byte ptr [0x4e1d18]
0042d2ff  31d2                  xor      edx, edx
0042d301  88da                  mov      dl, bl
0042d303  8a92181c4e00          mov      dl, byte ptr [edx + 0x4e1c18]
0042d309  81e2ff000000          and      edx, 0xff
0042d30f  b902000000            mov      ecx, 2
0042d314  89d0                  mov      eax, edx
0042d316  c1fa1f                sar      edx, 0x1f
0042d319  f7f9                  idiv     ecx
0042d31b  8d040a                lea      eax, [edx + ecx]
0042d31e  fec3                  inc      bl
0042d320  31d2                  xor      edx, edx
0042d322  881d181d4e00          mov      byte ptr [0x4e1d18], bl
0042d328  e85fa70300            call     0x467a8c
0042d32d  30c9                  xor      cl, cl
0042d32f  eb59                  jmp      0x42d38a
0042d331  3a0d41805000          cmp      cl, byte ptr [0x508041]
0042d337  7510                  jne      0x42d349
0042d339  89d8                  mov      eax, ebx
0042d33b  e838bfffff            call     0x429278
0042d340  89d8                  mov      eax, ebx
0042d342  e858190300            call     0x45ec9f
0042d347  eb3f                  jmp      0x42d388
0042d349  89d8                  mov      eax, ebx
0042d34b  e82c170300            call     0x45ea7c
0042d350  eb36                  jmp      0x42d388
0042d352  31d2                  xor      edx, edx
0042d354  e8c1ed0300            call     0x46c11a
0042d359  88c2                  mov      dl, al
0042d35b  89d8                  mov      eax, ebx
0042d35d  e888280500            call     0x47fbea
0042d362  3a0d41805000          cmp      cl, byte ptr [0x508041]
0042d368  751e                  jne      0x42d388
0042d36a  89d8                  mov      eax, ebx
0042d36c  e807bfffff            call     0x429278
0042d371  eb15                  jmp      0x42d388
0042d373  31db                  xor      ebx, ebx
0042d375  88cb                  mov      bl, cl
0042d377  89d8                  mov      eax, ebx
0042d379  e899040400            call     0x46d817
0042d37e  3c01                  cmp      al, 1
0042d380  7206                  jb       0x42d388
0042d382  76ad                  jbe      0x42d331
0042d384  3c02                  cmp      al, 2
0042d386  74ca                  je       0x42d352
0042d388  fec1                  inc      cl
0042d38a  31c0                  xor      eax, eax
0042d38c  88c8                  mov      al, cl
0042d38e  83f804                cmp      eax, 4
0042d391  7f0f                  jg       0x42d3a2
0042d393  8a1530074e00          mov      dl, byte ptr [0x4e0730]
0042d399  84d2                  test     dl, dl
0042d39b  74d6                  je       0x42d373
0042d39d  83f804                cmp      eax, 4
0042d3a0  75d1                  jne      0x42d373
0042d3a2  a041805000            mov      al, byte ptr [0x508041]
0042d3a7  30db                  xor      bl, bl
0042d3a9  a280244e00            mov      byte ptr [0x4e2480], al
0042d3ae  eb07                  jmp      0x42d3b7
0042d3b0  e80b1a0300            call     0x45edc0
0042d3b5  fec3                  inc      bl
0042d3b7  31c0                  xor      eax, eax
0042d3b9  88d8                  mov      al, bl
0042d3bb  83f804                cmp      eax, 4
0042d3be  7cf0                  jl       0x42d3b0
0042d3c0  8a25782f4e00          mov      ah, byte ptr [0x4e2f78]
0042d3c6  80fc12                cmp      ah, 0x12
0042d3c9  7416                  je       0x42d3e1
0042d3cb  80fc10                cmp      ah, 0x10
0042d3ce  0f850e010000          jne      0x42d4e2
0042d3d4  a030074e00            mov      al, byte ptr [0x4e0730]
0042d3d9  84c0                  test     al, al
0042d3db  0f8401010000          je       0x42d4e2
0042d3e1  e8e8c90300            call     0x469dce
0042d3e6  e82afc0200            call     0x45d015
0042d3eb  e854150300            call     0x45e944
0042d3f0  e81a280400            call     0x46fc0f
0042d3f5  e8bb990200            call     0x456db5 ; iterar_unidades
0042d3fa  e8c8adffff            call     0x4281c7
0042d3ff  e8583e0400            call     0x47125c
0042d404  e832060400            call     0x46da3b
0042d409  e81a7f0400            call     0x475328
0042d40e  e8f3b30400            call     0x478806
0042d413  e800a30300            call     0x467718
0042d418  31c0                  xor      eax, eax
0042d41a  a041805000            mov      al, byte ptr [0x508041]
0042d41f  e8ad990300            call     0x466dd1
0042d424  31c0                  xor      eax, eax
0042d426  a041805000            mov      al, byte ptr [0x508041]
0042d42b  31d2                  xor      edx, edx
0042d42d  e8699a0300            call     0x466e9b
0042d432  31c0                  xor      eax, eax
0042d434  668b1522875000        mov      dx, word ptr [0x508722]
0042d43b  66a120875000          mov      ax, word ptr [0x508720]
0042d441  e8baa20400            call     0x477700
0042d446  a030074e00            mov      al, byte ptr [0x4e0730]
0042d44b  84c0                  test     al, al
0042d44d  7407                  je       0x42d456
0042d44f  e8a6a00400            call     0x4774fa
0042d454  eb16                  jmp      0x42d46c
0042d456  31d2                  xor      edx, edx
0042d458  31c0                  xor      eax, eax
0042d45a  668b1522875000        mov      dx, word ptr [0x508722]
0042d461  66a120875000          mov      ax, word ptr [0x508720]
0042d467  e8809e0400            call     0x4772ec
0042d46c  e8b8010400            call     0x46d629
0042d471  a030074e00            mov      al, byte ptr [0x4e0730]
0042d476  84c0                  test     al, al
0042d478  7568                  jne      0x42d4e2
0042d47a  31c0                  xor      eax, eax
0042d47c  a041805000            mov      al, byte ptr [0x508041]
0042d481  e880b10200            call     0x458606
0042d486  a2a0054e00            mov      byte ptr [0x4e05a0], al
0042d48b  84c0                  test     al, al
0042d48d  7453                  je       0x42d4e2
0042d48f  e886ec0300            call     0x46c11a
0042d494  25ffff0000            and      eax, 0xffff
0042d499  83f806                cmp      eax, 6
0042d49c  7518                  jne      0x42d4b6
0042d49e  833d1c064e0000        cmp      dword ptr [0x4e061c], 0
0042d4a5  750f                  jne      0x42d4b6
0042d4a7  baf4010000            mov      edx, 0x1f4
0042d4ac  b80a000000            mov      eax, 0xa
0042d4b1  e895c40300            call     0x46994b
0042d4b6  8b0d1c064e00          mov      ecx, dword ptr [0x4e061c]
0042d4bc  41                    inc      ecx
0042d4bd  890d1c064e00          mov      dword ptr [0x4e061c], ecx
0042d4c3  83f964                cmp      ecx, 0x64
0042d4c6  7c1a                  jl       0x42d4e2
0042d4c8  e8f8d50500            call     0x48aac5
0042d4cd  31c0                  xor      eax, eax
0042d4cf  ba13000000            mov      edx, 0x13
0042d4d4  e953f4ffff            jmp      0x42c92c
0042d4d9  6a00                  push     0
0042d4db  2eff15bc325200        call     dword ptr cs:[0x5232bc] ; USER32.dll!PostQuitMessage
0042d4e2  30f6                  xor      dh, dh
0042d4e4  8835b0995000          mov      byte ptr [0x5099b0], dh
0042d4ea  81c40c010000          add      esp, 0x10c
0042d4f0  e91feeffff            jmp      0x42c314
