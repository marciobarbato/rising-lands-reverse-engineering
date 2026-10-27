; composicao_cmp: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0045c779  53                    push     ebx
0045c77a  51                    push     ecx
0045c77b  56                    push     esi
0045c77c  57                    push     edi
0045c77d  83ec0c                sub      esp, 0xc
0045c780  89d1                  mov      ecx, edx
0045c782  31f6                  xor      esi, esi
0045c784  8b156c8f5000          mov      edx, dword ptr [0x508f6c]
0045c78a  6689c6                mov      si, ax
0045c78d  8b74b2fc              mov      esi, dword ptr [edx + esi*4 - 4]
0045c791  81e1ffff0000          and      ecx, 0xffff
0045c797  8b4c8afc              mov      ecx, dword ptr [edx + ecx*4 - 4]
0045c79b  8b7608                mov      esi, dword ptr [esi + 8]
0045c79e  668b01                mov      ax, word ptr [ecx]
0045c7a1  31d2                  xor      edx, edx
0045c7a3  89442404              mov      dword ptr [esp + 4], eax
0045c7a7  668b4102              mov      ax, word ptr [ecx + 2]
0045c7ab  89542408              mov      dword ptr [esp + 8], edx
0045c7af  890424                mov      dword ptr [esp], eax
0045c7b2  8b4908                mov      ecx, dword ptr [ecx + 8]
0045c7b5  eb04                  jmp      0x45c7bb
0045c7b7  ff442408              inc      dword ptr [esp + 8]
0045c7bb  8b442408              mov      eax, dword ptr [esp + 8]
0045c7bf  663b0424              cmp      ax, word ptr [esp]
0045c7c3  7332                  jae      0x45c7f7
0045c7c5  46                    inc      esi
0045c7c6  31ff                  xor      edi, edi
0045c7c8  663b7c2404            cmp      di, word ptr [esp + 4]
0045c7cd  73e8                  jae      0x45c7b7
0045c7cf  8a19                  mov      bl, byte ptr [ecx]
0045c7d1  0fbed3                movsx    edx, bl
0045c7d4  41                    inc      ecx
0045c7d5  85d2                  test     edx, edx
0045c7d7  7d11                  jge      0x45c7ea
0045c7d9  f6db                  neg      bl
0045c7db  89f0                  mov      eax, esi
0045c7dd  0fbed3                movsx    edx, bl
0045c7e0  e8d52f0000            call     0x45f7ba
0045c7e5  0fbed3                movsx    edx, bl
0045c7e8  01d1                  add      ecx, edx
0045c7ea  660fbed3              movsx    dx, bl
0045c7ee  01d7                  add      edi, edx
0045c7f0  0fbed3                movsx    edx, bl
0045c7f3  01d6                  add      esi, edx
0045c7f5  ebd1                  jmp      0x45c7c8
0045c7f7  83c40c                add      esp, 0xc
0045c7fa  5f                    pop      edi
0045c7fb  5e                    pop      esi
0045c7fc  59                    pop      ecx
0045c7fd  5b                    pop      ebx
