; BatimentGetCaseAdjacent; intervalo [0x004239a0, 0x00423b27)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004239a0  53                       push     ebx
004239a1  51                       push     ecx
004239a2  56                       push     esi
004239a3  57                       push     edi
004239a4  55                       push     ebp
004239a5  83ec24                   sub      esp, 0x24
004239a8  50                       push     eax
004239a9  52                       push     edx
004239aa  31f6                     xor      esi, esi
004239ac  6689d6                   mov      si, dx
004239af  bb00010000               mov      ebx, 0x100
004239b4  89f2                     mov      edx, esi
004239b6  89f0                     mov      eax, esi
004239b8  c1fa1f                   sar      edx, 0x1f
004239bb  f7fb                     idiv     ebx
004239bd  89542428                 mov      dword ptr [esp + 0x28], edx
004239c1  89f2                     mov      edx, esi
004239c3  89f0                     mov      eax, esi
004239c5  c1fa1f                   sar      edx, 0x1f
004239c8  f7fb                     idiv     ebx
004239ca  baffffffff               mov      edx, 0xffffffff
004239cf  bb00ff0000               mov      ebx, 0xff00
004239d4  89442410                 mov      dword ptr [esp + 0x10], eax
004239d8  6689542424               mov      word ptr [esp + 0x24], dx
004239dd  66895c2414               mov      word ptr [esp + 0x14], bx
004239e2  31ed                     xor      ebp, ebp
004239e4  eb09                     jmp      0x4239ef
004239e6  fe442415                 inc      byte ptr [esp + 0x15]
004239ea  66ff442424               inc      word ptr [esp + 0x24]
004239ef  8b442422                 mov      eax, dword ptr [esp + 0x22]
004239f3  c1f810                   sar      eax, 0x10
004239f6  83f801                   cmp      eax, 1
004239f9  0f8f1e010000             jg       0x423b1d
004239ff  31d2                     xor      edx, edx
00423a01  668b542410               mov      dx, word ptr [esp + 0x10]
00423a06  01d0                     add      eax, edx
00423a08  85c0                     test     eax, eax
00423a0a  7cda                     jl       0x4239e6
00423a0c  3d00010000               cmp      eax, 0x100
00423a11  7dd3                     jge      0x4239e6
00423a13  8b0424                   mov      eax, dword ptr [esp]
00423a16  8b742414                 mov      esi, dword ptr [esp + 0x14]
00423a1a  05ffff0000               add      eax, 0xffff
00423a1f  b9ffffffff               mov      ecx, 0xffffffff
00423a24  01f0                     add      eax, esi
00423a26  66894c241c               mov      word ptr [esp + 0x1c], cx
00423a2b  89442418                 mov      dword ptr [esp + 0x18], eax
00423a2f  eb13                     jmp      0x423a44
00423a31  8b742418                 mov      esi, dword ptr [esp + 0x18]
00423a35  8b7c241c                 mov      edi, dword ptr [esp + 0x1c]
00423a39  46                       inc      esi
00423a3a  47                       inc      edi
00423a3b  89742418                 mov      dword ptr [esp + 0x18], esi
00423a3f  66897c241c               mov      word ptr [esp + 0x1c], di
00423a44  8b44241a                 mov      eax, dword ptr [esp + 0x1a]
00423a48  c1f810                   sar      eax, 0x10
00423a4b  83f801                   cmp      eax, 1
00423a4e  7f96                     jg       0x4239e6
00423a50  31d2                     xor      edx, edx
00423a52  668b542428               mov      dx, word ptr [esp + 0x28]
00423a57  01d0                     add      eax, edx
00423a59  85c0                     test     eax, eax
00423a5b  7cd4                     jl       0x423a31
00423a5d  3d00010000               cmp      eax, 0x100
00423a62  7dcd                     jge      0x423a31
00423a64  31f6                     xor      esi, esi
00423a66  668b742404               mov      si, word ptr [esp + 4]
00423a6b  69f614010000             imul     esi, esi, 0x114
00423a71  8b442418                 mov      eax, dword ptr [esp + 0x18]
00423a75  81c6c8a04900             add      esi, 0x49a0c8
00423a7b  31d2                     xor      edx, edx
00423a7d  89442420                 mov      dword ptr [esp + 0x20], eax
00423a81  8a4608                   mov      al, byte ptr [esi + 8]
00423a84  88c2                     mov      dl, al
00423a86  6bd234                   imul     edx, edx, 0x34
00423a89  668b828c5d4900           mov      ax, word ptr [edx + 0x495d8c]
00423a90  668b7e02                 mov      di, word ptr [esi + 2]
00423a94  89442408                 mov      dword ptr [esp + 8], eax
00423a98  668b828e5d4900           mov      ax, word ptr [edx + 0x495d8e]
00423a9f  31c9                     xor      ecx, ecx
00423aa1  8944240c                 mov      dword ptr [esp + 0xc], eax
00423aa5  eb01                     jmp      0x423aa8
00423aa7  41                       inc      ecx
00423aa8  663b4c240c               cmp      cx, word ptr [esp + 0xc]
00423aad  734d                     jae      0x423afc
00423aaf  31db                     xor      ebx, ebx
00423ab1  eb01                     jmp      0x423ab4
00423ab3  43                       inc      ebx
00423ab4  663b5c2408               cmp      bx, word ptr [esp + 8]
00423ab9  73ec                     jae      0x423aa7
00423abb  31c0                     xor      eax, eax
00423abd  31d2                     xor      edx, edx
00423abf  6689c8                   mov      ax, cx
00423ac2  6689fa                   mov      dx, di
00423ac5  c1e008                   shl      eax, 8
00423ac8  01d0                     add      eax, edx
00423aca  31d2                     xor      edx, edx
00423acc  6689da                   mov      dx, bx
00423acf  01c2                     add      edx, eax
00423ad1  31c0                     xor      eax, eax
00423ad3  668b442420               mov      ax, word ptr [esp + 0x20]
00423ad8  39c2                     cmp      edx, eax
00423ada  75d7                     jne      0x423ab3
00423adc  8b442408                 mov      eax, dword ptr [esp + 8]
00423ae0  0fafc1                   imul     eax, ecx
00423ae3  31d2                     xor      edx, edx
00423ae5  01d8                     add      eax, ebx
00423ae7  6689c2                   mov      dx, ax
00423aea  31c0                     xor      eax, eax
00423aec  8a4608                   mov      al, byte ptr [esi + 8]
00423aef  e86870ffff               call     0x41ab5c
00423af4  84c0                     test     al, al
00423af6  74bb                     je       0x423ab3
00423af8  b001                     mov      al, 1
00423afa  eb02                     jmp      0x423afe
00423afc  30c0                     xor      al, al
00423afe  84c0                     test     al, al
00423b00  0f842bffffff             je       0x423a31
00423b06  8b442424                 mov      eax, dword ptr [esp + 0x24]
00423b0a  8b5c241c                 mov      ebx, dword ptr [esp + 0x1c]
00423b0e  c1e008                   shl      eax, 8
00423b11  8b0c24                   mov      ecx, dword ptr [esp]
00423b14  01d8                     add      eax, ebx
00423b16  01c8                     add      eax, ecx
00423b18  e97afeffff               jmp      0x423997
00423b1d  b8ffff0000               mov      eax, 0xffff
00423b22  e970feffff               jmp      0x423997
