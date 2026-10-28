; PasteBobCmp [0x45b247, 0x45b4fd)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045b247  56                     push     esi
0045b248  57                     push     edi
0045b249  55                     push     ebp
0045b24a  83ec1c                 sub      esp, 0x1c
0045b24d  50                     push     eax
0045b24e  52                     push     edx
0045b24f  31d2                   xor      edx, edx
0045b251  a16c8f5000             mov      eax, dword ptr [0x508f6c]
0045b256  6689da                 mov      dx, bx
0045b259  8b4490fc               mov      eax, dword ptr [eax + edx*4 - 4]
0045b25d  89442408               mov      dword ptr [esp + 8], eax
0045b261  84c9                   test     cl, cl
0045b263  7427                   je       0x45b28c
0045b265  66a122a04900           mov      ax, word ptr [0x49a022]
0045b26b  8944240c               mov      dword ptr [esp + 0xc], eax
0045b26f  66a120a04900           mov      ax, word ptr [0x49a020]
0045b275  8944241c               mov      dword ptr [esp + 0x1c], eax
0045b279  66a11ea04900           mov      ax, word ptr [0x49a01e]
0045b27f  668b3d1ca04900         mov      di, word ptr [0x49a01c]
0045b286  89442410               mov      dword ptr [esp + 0x10], eax
0045b28a  eb1a                   jmp      0x45b2a6 ;
0045b28c  ba1f030000             mov      edx, 0x31f
0045b291  b957020000             mov      ecx, 0x257
0045b296  31db                   xor      ebx, ebx
0045b298  31ff                   xor      edi, edi
0045b29a  8954240c               mov      dword ptr [esp + 0xc], edx
0045b29e  895c241c               mov      dword ptr [esp + 0x1c], ebx
0045b2a2  894c2410               mov      dword ptr [esp + 0x10], ecx
0045b2a6  31d2                   xor      edx, edx
0045b2a8  8b442402               mov      eax, dword ptr [esp + 2]
0045b2ac  668b54240c             mov      dx, word ptr [esp + 0xc]
0045b2b1  c1f810                 sar      eax, 0x10
0045b2b4  39d0                   cmp      eax, edx
0045b2b6  0f8f3a020000           jg       0x45b4f6
0045b2bc  31d2                   xor      edx, edx
0045b2be  8b5c24fe               mov      ebx, dword ptr [esp - 2]
0045b2c2  668b542410             mov      dx, word ptr [esp + 0x10]
0045b2c7  c1fb10                 sar      ebx, 0x10
0045b2ca  39d3                   cmp      ebx, edx
0045b2cc  0f8f24020000           jg       0x45b4f6
0045b2d2  31d2                   xor      edx, edx
0045b2d4  668b54241c             mov      dx, word ptr [esp + 0x1c]
0045b2d9  39d0                   cmp      eax, edx
0045b2db  7d13                   jge      0x45b2f0
0045b2dd  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045b2e1  31db                   xor      ebx, ebx
0045b2e3  668b19                 mov      bx, word ptr [ecx]
0045b2e6  01d8                   add      eax, ebx
0045b2e8  39d0                   cmp      eax, edx
0045b2ea  0f8c06020000           jl       0x45b4f6
0045b2f0  8b5424fe               mov      edx, dword ptr [esp - 2]
0045b2f4  31c0                   xor      eax, eax
0045b2f6  c1fa10                 sar      edx, 0x10
0045b2f9  6689f8                 mov      ax, di
0045b2fc  39c2                   cmp      edx, eax
0045b2fe  7d14                   jge      0x45b314
0045b300  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045b304  31db                   xor      ebx, ebx
0045b306  668b5902               mov      bx, word ptr [ecx + 2]
0045b30a  01da                   add      edx, ebx
0045b30c  39c2                   cmp      edx, eax
0045b30e  0f8ce2010000           jl       0x45b4f6
0045b314  8b4424fe               mov      eax, dword ptr [esp - 2]
0045b318  8b0da0174e00           mov      ecx, dword ptr [0x4e17a0]
0045b31e  c1f810                 sar      eax, 0x10
0045b321  0fafc8                 imul     ecx, eax
0045b324  8b542408               mov      edx, dword ptr [esp + 8]
0045b328  8b1d708f5000           mov      ebx, dword ptr [0x508f70]
0045b32e  8b442402               mov      eax, dword ptr [esp + 2]
0045b332  31f6                   xor      esi, esi
0045b334  c1f810                 sar      eax, 0x10
0045b337  89742418               mov      dword ptr [esp + 0x18], esi
0045b33b  01c8                   add      eax, ecx
0045b33d  8b5208                 mov      edx, dword ptr [edx + 8]
0045b340  01c3                   add      ebx, eax
0045b342  31c0                   xor      eax, eax
0045b344  8b4c24fe               mov      ecx, dword ptr [esp - 2]
0045b348  668b442418             mov      ax, word ptr [esp + 0x18]
0045b34d  c1f910                 sar      ecx, 0x10
0045b350  01c8                   add      eax, ecx
0045b352  31c9                   xor      ecx, ecx
0045b354  6689f9                 mov      cx, di
0045b357  39c8                   cmp      eax, ecx
0045b359  0f8d73000000           jge      0x45b3d2
0045b35f  31c9                   xor      ecx, ecx
0045b361  668b4c2410             mov      cx, word ptr [esp + 0x10]
0045b366  39c8                   cmp      eax, ecx
0045b368  7f68                   jg       0x45b3d2
0045b36a  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045b36e  8b442418               mov      eax, dword ptr [esp + 0x18]
0045b372  663b4102               cmp      ax, word ptr [ecx + 2]
0045b376  735a                   jae      0x45b3d2
0045b378  31c9                   xor      ecx, ecx
0045b37a  8b442408               mov      eax, dword ptr [esp + 8]
0045b37e  663b08                 cmp      cx, word ptr [eax]
0045b381  731e                   jae      0x45b3a1
0045b383  8a02                   mov      al, byte ptr [edx]
0045b385  0fbee8                 movsx    ebp, al
0045b388  42                     inc      edx
0045b389  85ed                   test     ebp, ebp
0045b38b  7d07                   jge      0x45b394
0045b38d  f6d8                   neg      al
0045b38f  0fbee8                 movsx    ebp, al
0045b392  01ea                   add      edx, ebp
0045b394  660fbef0               movsx    si, al
0045b398  0fbec0                 movsx    eax, al
0045b39b  01f1                   add      ecx, esi
0045b39d  01c3                   add      ebx, eax
0045b39f  ebd9                   jmp      0x45b37a ;
0045b3a1  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045b3a5  31c0                   xor      eax, eax
0045b3a7  668b01                 mov      ax, word ptr [ecx]
0045b3aa  ff442418               inc      dword ptr [esp + 0x18]
0045b3ae  8b0da0174e00           mov      ecx, dword ptr [0x4e17a0]
0045b3b4  29c1                   sub      ecx, eax
0045b3b6  01cb                   add      ebx, ecx
0045b3b8  eb88                   jmp      0x45b342 ;
0045b3ba  8b7c2418               mov      edi, dword ptr [esp + 0x18]
0045b3be  31c0                   xor      eax, eax
0045b3c0  8b0da0174e00           mov      ecx, dword ptr [0x4e17a0]
0045b3c6  6689f0                 mov      ax, si
0045b3c9  47                     inc      edi
0045b3ca  29c1                   sub      ecx, eax
0045b3cc  897c2418               mov      dword ptr [esp + 0x18], edi
0045b3d0  01cb                   add      ebx, ecx
0045b3d2  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045b3d6  8b442418               mov      eax, dword ptr [esp + 0x18]
0045b3da  663b4102               cmp      ax, word ptr [ecx + 2]
0045b3de  0f8312010000           jae      0x45b4f6
0045b3e4  31c9                   xor      ecx, ecx
0045b3e6  6689c1                 mov      cx, ax
0045b3e9  8b4424fe               mov      eax, dword ptr [esp - 2]
0045b3ed  c1f810                 sar      eax, 0x10
0045b3f0  01c1                   add      ecx, eax
0045b3f2  31c0                   xor      eax, eax
0045b3f4  668b442410             mov      ax, word ptr [esp + 0x10]
0045b3f9  39c1                   cmp      ecx, eax
0045b3fb  0f8ff5000000           jg       0x45b4f6
0045b401  31ff                   xor      edi, edi
0045b403  897c2414               mov      dword ptr [esp + 0x14], edi
0045b407  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045b40b  8b442414               mov      eax, dword ptr [esp + 0x14]
0045b40f  668b31                 mov      si, word ptr [ecx]
0045b412  6639f0                 cmp      ax, si
0045b415  73a3                   jae      0x45b3ba
0045b417  8a02                   mov      al, byte ptr [edx]
0045b419  88442420               mov      byte ptr [esp + 0x20], al
0045b41d  8b44241d               mov      eax, dword ptr [esp + 0x1d]
0045b421  c1f818                 sar      eax, 0x18
0045b424  42                     inc      edx
0045b425  85c0                   test     eax, eax
0045b427  0f8db2000000           jge      0x45b4df
0045b42d  8a642420               mov      ah, byte ptr [esp + 0x20]
0045b431  f6dc                   neg      ah
0045b433  31c9                   xor      ecx, ecx
0045b435  88642420               mov      byte ptr [esp + 0x20], ah
0045b439  8b442402               mov      eax, dword ptr [esp + 2]
0045b43d  668b4c2414             mov      cx, word ptr [esp + 0x14]
0045b442  c1f810                 sar      eax, 0x10
0045b445  01c8                   add      eax, ecx
0045b447  31c9                   xor      ecx, ecx
0045b449  668b4c241c             mov      cx, word ptr [esp + 0x1c]
0045b44e  39c8                   cmp      eax, ecx
0045b450  7c44                   jl       0x45b496
0045b452  8b6c241d               mov      ebp, dword ptr [esp + 0x1d]
0045b456  31c9                   xor      ecx, ecx
0045b458  c1fd18                 sar      ebp, 0x18
0045b45b  668b4c240c             mov      cx, word ptr [esp + 0xc]
0045b460  01e8                   add      eax, ebp
0045b462  39c8                   cmp      eax, ecx
0045b464  7f30                   jg       0x45b496
0045b466  8b4c241d               mov      ecx, dword ptr [esp + 0x1d]
0045b46a  89d6                   mov      esi, edx
0045b46c  89df                   mov      edi, ebx
0045b46e  c1f918                 sar      ecx, 0x18
0045b471  57                     push     edi
0045b472  89c8                   mov      eax, ecx
0045b474  c1e902                 shr      ecx, 2
0045b477  f2a5                   movsd    dword ptr es:[edi], dword ptr [esi]
0045b479  8ac8                   mov      cl, al
0045b47b  80e103                 and      cl, 3
0045b47e  f2a4                   repne movsb byte ptr es:[edi], byte ptr [esi]
0045b480  5f                     pop      edi
0045b481  660fbe442420           movsx    ax, byte ptr [esp + 0x20]
0045b487  8b7c2414               mov      edi, dword ptr [esp + 0x14]
0045b48b  01ea                   add      edx, ebp
0045b48d  01c7                   add      edi, eax
0045b48f  01eb                   add      ebx, ebp
0045b491  e96dffffff             jmp      0x45b403 ;
0045b496  30c0                   xor      al, al
0045b498  eb0d                   jmp      0x45b4a7 ;
0045b49a  8b4c2414               mov      ecx, dword ptr [esp + 0x14]
0045b49e  43                     inc      ebx
0045b49f  42                     inc      edx
0045b4a0  41                     inc      ecx
0045b4a1  fec0                   inc      al
0045b4a3  894c2414               mov      dword ptr [esp + 0x14], ecx
0045b4a7  8b4c241d               mov      ecx, dword ptr [esp + 0x1d]
0045b4ab  0fb6e8                 movzx    ebp, al
0045b4ae  c1f918                 sar      ecx, 0x18
0045b4b1  39cd                   cmp      ebp, ecx
0045b4b3  0f8d4effffff           jge      0x45b407
0045b4b9  8b4c2402               mov      ecx, dword ptr [esp + 2]
0045b4bd  0fb76c2414             movzx    ebp, word ptr [esp + 0x14]
0045b4c2  c1f910                 sar      ecx, 0x10
0045b4c5  01e9                   add      ecx, ebp
0045b4c7  0fb76c241c             movzx    ebp, word ptr [esp + 0x1c]
0045b4cc  39e9                   cmp      ecx, ebp
0045b4ce  7cca                   jl       0x45b49a
0045b4d0  0fb76c240c             movzx    ebp, word ptr [esp + 0xc]
0045b4d5  39e9                   cmp      ecx, ebp
0045b4d7  7fc1                   jg       0x45b49a
0045b4d9  8a22                   mov      ah, byte ptr [edx]
0045b4db  8823                   mov      byte ptr [ebx], ah
0045b4dd  ebbb                   jmp      0x45b49a ;
0045b4df  660fbe4c2420           movsx    cx, byte ptr [esp + 0x20]
0045b4e5  8b742414               mov      esi, dword ptr [esp + 0x14]
0045b4e9  01ce                   add      esi, ecx
0045b4eb  01c3                   add      ebx, eax
0045b4ed  89742414               mov      dword ptr [esp + 0x14], esi
0045b4f1  e911ffffff             jmp      0x45b407 ;
0045b4f6  83c424                 add      esp, 0x24
0045b4f9  5d                     pop      ebp
0045b4fa  5f                     pop      edi
0045b4fb  5e                     pop      esi
0045b4fc  c3                     ret
