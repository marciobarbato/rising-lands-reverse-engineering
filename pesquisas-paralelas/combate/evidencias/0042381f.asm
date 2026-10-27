; BatimentAdjacent; intervalo [0x0042381f, 0x004239a0)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042381f  53                       push     ebx
00423820  51                       push     ecx
00423821  56                       push     esi
00423822  57                       push     edi
00423823  55                       push     ebp
00423824  83ec24                   sub      esp, 0x24
00423827  50                       push     eax
00423828  52                       push     edx
00423829  31f6                     xor      esi, esi
0042382b  6689d6                   mov      si, dx
0042382e  bb00010000               mov      ebx, 0x100
00423833  89f2                     mov      edx, esi
00423835  89f0                     mov      eax, esi
00423837  c1fa1f                   sar      edx, 0x1f
0042383a  f7fb                     idiv     ebx
0042383c  89542408                 mov      dword ptr [esp + 8], edx
00423840  89f2                     mov      edx, esi
00423842  89f0                     mov      eax, esi
00423844  c1fa1f                   sar      edx, 0x1f
00423847  f7fb                     idiv     ebx
00423849  baffffffff               mov      edx, 0xffffffff
0042384e  bb00ff0000               mov      ebx, 0xff00
00423853  89442414                 mov      dword ptr [esp + 0x14], eax
00423857  6689542428               mov      word ptr [esp + 0x28], dx
0042385c  66895c2418               mov      word ptr [esp + 0x18], bx
00423861  31ed                     xor      ebp, ebp
00423863  eb14                     jmp      0x423879
00423865  8a642419                 mov      ah, byte ptr [esp + 0x19]
00423869  8b742428                 mov      esi, dword ptr [esp + 0x28]
0042386d  fec4                     inc      ah
0042386f  46                       inc      esi
00423870  88642419                 mov      byte ptr [esp + 0x19], ah
00423874  6689742428               mov      word ptr [esp + 0x28], si
00423879  8b442426                 mov      eax, dword ptr [esp + 0x26]
0042387d  c1f810                   sar      eax, 0x10
00423880  83f801                   cmp      eax, 1
00423883  0f8f0c010000             jg       0x423995
00423889  31d2                     xor      edx, edx
0042388b  668b542414               mov      dx, word ptr [esp + 0x14]
00423890  01d0                     add      eax, edx
00423892  85c0                     test     eax, eax
00423894  7ccf                     jl       0x423865
00423896  3d00010000               cmp      eax, 0x100
0042389b  7dc8                     jge      0x423865
0042389d  8b0424                   mov      eax, dword ptr [esp]
004238a0  8b742418                 mov      esi, dword ptr [esp + 0x18]
004238a4  05ffff0000               add      eax, 0xffff
004238a9  b9ffffffff               mov      ecx, 0xffffffff
004238ae  01f0                     add      eax, esi
004238b0  66894c2410               mov      word ptr [esp + 0x10], cx
004238b5  89442420                 mov      dword ptr [esp + 0x20], eax
004238b9  eb13                     jmp      0x4238ce
004238bb  8b5c2420                 mov      ebx, dword ptr [esp + 0x20]
004238bf  8b4c2410                 mov      ecx, dword ptr [esp + 0x10]
004238c3  43                       inc      ebx
004238c4  41                       inc      ecx
004238c5  895c2420                 mov      dword ptr [esp + 0x20], ebx
004238c9  66894c2410               mov      word ptr [esp + 0x10], cx
004238ce  8b44240e                 mov      eax, dword ptr [esp + 0xe]
004238d2  c1f810                   sar      eax, 0x10
004238d5  83f801                   cmp      eax, 1
004238d8  7f8b                     jg       0x423865
004238da  31d2                     xor      edx, edx
004238dc  668b542408               mov      dx, word ptr [esp + 8]
004238e1  01d0                     add      eax, edx
004238e3  85c0                     test     eax, eax
004238e5  7cd4                     jl       0x4238bb
004238e7  3d00010000               cmp      eax, 0x100
004238ec  7dcd                     jge      0x4238bb
004238ee  31c0                     xor      eax, eax
004238f0  668b442404               mov      ax, word ptr [esp + 4]
004238f5  69c014010000             imul     eax, eax, 0x114
004238fb  bec8a04900               mov      esi, 0x49a0c8
00423900  01c6                     add      esi, eax
00423902  668b4602                 mov      ax, word ptr [esi + 2]
00423906  31d2                     xor      edx, edx
00423908  89442424                 mov      dword ptr [esp + 0x24], eax
0042390c  8a4608                   mov      al, byte ptr [esi + 8]
0042390f  88c2                     mov      dl, al
00423911  6bd234                   imul     edx, edx, 0x34
00423914  668b828c5d4900           mov      ax, word ptr [edx + 0x495d8c]
0042391b  8b7c2420                 mov      edi, dword ptr [esp + 0x20]
0042391f  8944241c                 mov      dword ptr [esp + 0x1c], eax
00423923  668b828e5d4900           mov      ax, word ptr [edx + 0x495d8e]
0042392a  31c9                     xor      ecx, ecx
0042392c  8944240c                 mov      dword ptr [esp + 0xc], eax
00423930  eb01                     jmp      0x423933
00423932  41                       inc      ecx
00423933  663b4c240c               cmp      cx, word ptr [esp + 0xc]
00423938  734d                     jae      0x423987
0042393a  31db                     xor      ebx, ebx
0042393c  eb01                     jmp      0x42393f
0042393e  43                       inc      ebx
0042393f  663b5c241c               cmp      bx, word ptr [esp + 0x1c]
00423944  73ec                     jae      0x423932
00423946  31c0                     xor      eax, eax
00423948  31d2                     xor      edx, edx
0042394a  6689c8                   mov      ax, cx
0042394d  668b542424               mov      dx, word ptr [esp + 0x24]
00423952  c1e008                   shl      eax, 8
00423955  01c2                     add      edx, eax
00423957  31c0                     xor      eax, eax
00423959  6689d8                   mov      ax, bx
0042395c  01d0                     add      eax, edx
0042395e  31d2                     xor      edx, edx
00423960  6689fa                   mov      dx, di
00423963  39d0                     cmp      eax, edx
00423965  75d7                     jne      0x42393e
00423967  8b44241c                 mov      eax, dword ptr [esp + 0x1c]
0042396b  0fafc1                   imul     eax, ecx
0042396e  31d2                     xor      edx, edx
00423970  01d8                     add      eax, ebx
00423972  6689c2                   mov      dx, ax
00423975  31c0                     xor      eax, eax
00423977  8a4608                   mov      al, byte ptr [esi + 8]
0042397a  e8dd71ffff               call     0x41ab5c
0042397f  84c0                     test     al, al
00423981  74bb                     je       0x42393e
00423983  b001                     mov      al, 1
00423985  eb02                     jmp      0x423989
00423987  30c0                     xor      al, al
00423989  84c0                     test     al, al
0042398b  0f842affffff             je       0x4238bb
00423991  b001                     mov      al, 1
00423993  eb02                     jmp      0x423997
00423995  30c0                     xor      al, al
00423997  83c42c                   add      esp, 0x2c
0042399a  5d                       pop      ebp
0042399b  5f                       pop      edi
0042399c  5e                       pop      esi
0042399d  59                       pop      ecx
0042399e  5b                       pop      ebx
0042399f  c3                       ret
