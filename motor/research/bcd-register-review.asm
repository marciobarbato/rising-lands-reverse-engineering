; Static original-byte review only; no instructions executed.
; intact executable sha256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb

; IntToBCD sha256 8a21d5981c52647419ce7dab510c048a52230db9fbacb5a573daade33cb78de4
00467cd1: push     ebx
00467cd2: push     ecx
00467cd3: push     esi
00467cd4: push     edi
00467cd5: push     ebp
00467cd6: sub      esp, 4
00467cd9: push     eax
00467cda: push     edx
00467cdb: mov      ebx, 0x3e8
00467ce0: xor      esi, esi
00467ce2: xor      ecx, ecx
00467ce4: jmp      0x467d27
00467ce6: xor      eax, eax
00467ce8: xor      edx, edx
00467cea: mov      ax, word ptr [esp]
00467cee: mov      dx, si
00467cf1: sub      eax, edx
00467cf3: mov      edx, eax
00467cf5: movzx    ebp, bx
00467cf8: sar      edx, 0x1f
00467cfb: idiv     ebp
00467cfd: mov      word ptr [esp + 8], ax
00467d02: imul     eax, ebx
00467d05: mov      edx, 3
00467d0a: sub      edx, edi
00467d0c: add      edx, dword ptr [esp + 4]
00467d10: add      esi, eax
00467d12: mov      al, byte ptr [esp + 8]
00467d16: mov      byte ptr [edx], al
00467d18: mov      eax, ebx
00467d1a: xor      edx, edx
00467d1c: mov      ebx, 0xa
00467d21: div      bx
00467d24: inc      ecx
00467d25: mov      ebx, eax
00467d27: xor      edi, edi
00467d29: mov      di, cx
00467d2c: cmp      edi, 4
00467d2f: jl       0x467ce6
00467d31: add      esp, 0xc
00467d34: pop      ebp
00467d35: pop      edi
00467d36: pop      esi
00467d37: pop      ecx
00467d38: pop      ebx
00467d39: ret

; BCDToInt sha256 70017bfced23d7152b038f9ff2cc56de712aa3fe7b1bfa6dcf30a05ef28101bf
00467d3a: push     ebx
00467d3b: push     ecx
00467d3c: push     esi
00467d3d: push     edi
00467d3e: mov      esi, edx
00467d40: mov      edx, 1
00467d45: mov      word ptr [eax], 0
00467d4a: xor      ebx, ebx
00467d4c: jmp      0x467d62
00467d4e: mov      cl, byte ptr [ecx + esi]
00467d51: xor      ch, ch
00467d53: imul     ecx, edx
00467d56: mov      di, word ptr [eax]
00467d59: add      edi, ecx
00467d5b: inc      ebx
00467d5c: mov      word ptr [eax], di
00467d5f: imul     edx, edx, 0xa
00467d62: xor      ecx, ecx
00467d64: mov      cx, bx
00467d67: cmp      ecx, 4
00467d6a: jl       0x467d4e
00467d6c: pop      edi
00467d6d: pop      esi
00467d6e: pop      ecx
00467d6f: pop      ebx
00467d70: ret
