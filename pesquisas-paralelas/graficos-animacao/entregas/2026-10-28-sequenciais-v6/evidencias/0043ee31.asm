; DDSetPalette [0x43ee31, 0x43ef40)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0043ee31  53                     push     ebx
0043ee32  51                     push     ecx
0043ee33  52                     push     edx
0043ee34  56                     push     esi
0043ee35  57                     push     edi
0043ee36  81ec00040000           sub      esp, 0x400
0043ee3c  89c6                   mov      esi, eax
0043ee3e  30e4                   xor      ah, ah
0043ee40  b3ff                   mov      bl, 0xff
0043ee42  882424                 mov      byte ptr [esp], ah
0043ee45  88642401               mov      byte ptr [esp + 1], ah
0043ee49  88642402               mov      byte ptr [esp + 2], ah
0043ee4d  889c24fc030000         mov      byte ptr [esp + 0x3fc], bl
0043ee54  889c24fd030000         mov      byte ptr [esp + 0x3fd], bl
0043ee5b  889c24fe030000         mov      byte ptr [esp + 0x3fe], bl
0043ee62  31db                   xor      ebx, ebx
0043ee64  eb1a                   jmp      0x43ee80 ;
0043ee66  8d0452                 lea      eax, [edx + edx*2]
0043ee69  8a0c06                 mov      cl, byte ptr [esi + eax]
0043ee6c  880c94                 mov      byte ptr [esp + edx*4], cl
0043ee6f  8a4c0601               mov      cl, byte ptr [esi + eax + 1]
0043ee73  884c9401               mov      byte ptr [esp + edx*4 + 1], cl
0043ee77  8a440602               mov      al, byte ptr [esi + eax + 2]
0043ee7b  43                     inc      ebx
0043ee7c  88449402               mov      byte ptr [esp + edx*4 + 2], al
0043ee80  31d2                   xor      edx, edx
0043ee82  6689da                 mov      dx, bx
0043ee85  81fa00010000           cmp      edx, 0x100
0043ee8b  7cd9                   jl       0x43ee66
0043ee8d  8b159c174e00           mov      edx, dword ptr [0x4e179c]
0043ee93  85d2                   test     edx, edx
0043ee95  7419                   je       0x43eeb0
0043ee97  89e6                   mov      esi, esp
0043ee99  56                     push     esi
0043ee9a  6800010000             push     0x100
0043ee9f  6a00                   push     0
0043eea1  6a00                   push     0
0043eea3  89d0                   mov      eax, edx
0043eea5  8b12                   mov      edx, dword ptr [edx]
0043eea7  50                     push     eax
0043eea8  ff5218                 call     dword ptr [edx + 0x18]
0043eeab  e985000000             jmp      0x43ef35 ;
0043eeb0  6a00                   push     0
0043eeb2  689c174e00             push     0x4e179c
0043eeb7  8d742408               lea      esi, [esp + 8]
0043eebb  56                     push     esi
0043eebc  a188174e00             mov      eax, dword ptr [0x4e1788]
0043eec1  6a44                   push     0x44
0043eec3  8b10                   mov      edx, dword ptr [eax]
0043eec5  50                     push     eax
0043eec6  ff5214                 call     dword ptr [edx + 0x14]
0043eec9  8b1d9c174e00           mov      ebx, dword ptr [0x4e179c]
0043eecf  a18c174e00             mov      eax, dword ptr [0x4e178c]
0043eed4  53                     push     ebx
0043eed5  8b10                   mov      edx, dword ptr [eax]
0043eed7  50                     push     eax
0043eed8  ff527c                 call     dword ptr [edx + 0x7c]
0043eedb  3dc2017688             cmp      eax, 0x887601c2
0043eee0  751d                   jne      0x43eeff
0043eee2  a18c174e00             mov      eax, dword ptr [0x4e178c]
0043eee7  50                     push     eax
0043eee8  8b10                   mov      edx, dword ptr [eax]
0043eeea  ff526c                 call     dword ptr [edx + 0x6c]
0043eeed  8b0d9c174e00           mov      ecx, dword ptr [0x4e179c]
0043eef3  a18c174e00             mov      eax, dword ptr [0x4e178c]
0043eef8  51                     push     ecx
0043eef9  8b10                   mov      edx, dword ptr [eax]
0043eefb  50                     push     eax
0043eefc  ff527c                 call     dword ptr [edx + 0x7c]
0043eeff  8b359c174e00           mov      esi, dword ptr [0x4e179c]
0043ef05  a190174e00             mov      eax, dword ptr [0x4e1790]
0043ef0a  56                     push     esi
0043ef0b  8b10                   mov      edx, dword ptr [eax]
0043ef0d  50                     push     eax
0043ef0e  ff527c                 call     dword ptr [edx + 0x7c]
0043ef11  3dc2017688             cmp      eax, 0x887601c2
0043ef16  751d                   jne      0x43ef35
0043ef18  a190174e00             mov      eax, dword ptr [0x4e1790]
0043ef1d  50                     push     eax
0043ef1e  8b10                   mov      edx, dword ptr [eax]
0043ef20  ff526c                 call     dword ptr [edx + 0x6c]
0043ef23  8b3d9c174e00           mov      edi, dword ptr [0x4e179c]
0043ef29  a190174e00             mov      eax, dword ptr [0x4e1790]
0043ef2e  57                     push     edi
0043ef2f  8b10                   mov      edx, dword ptr [eax]
0043ef31  50                     push     eax
0043ef32  ff527c                 call     dword ptr [edx + 0x7c]
0043ef35  81c400040000           add      esp, 0x400
0043ef3b  e9d6030000             jmp      0x43f316 ;
