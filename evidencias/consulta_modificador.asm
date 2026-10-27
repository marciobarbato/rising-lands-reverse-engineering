; consulta_modificador: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00428cc0  51                    push     ecx
00428cc1  25ff000000            and      eax, 0xff
00428cc6  3dc8000000            cmp      eax, 0xc8
00428ccb  7409                  je       0x428cd6
00428ccd  83f804                cmp      eax, 4
00428cd0  0f8584010000          jne      0x428e5a
00428cd6  31c0                  xor      eax, eax
00428cd8  59                    pop      ecx
00428cd9  c3                    ret
00428cda  69c8d4010000          imul     ecx, eax, 0x1d4
00428ce0  31d2                  xor      edx, edx
00428ce2  88da                  mov      dl, bl
00428ce4  89d0                  mov      eax, edx
00428ce6  c1e003                shl      eax, 3
00428ce9  01d0                  add      eax, edx
00428ceb  668b8c41a0fb4d00      mov      cx, word ptr [ecx + eax*2 + 0x4dfba0]
00428cf3  89c8                  mov      eax, ecx
00428cf5  59                    pop      ecx
00428cf6  c3                    ret
00428cf7  69c8d4010000          imul     ecx, eax, 0x1d4
00428cfd  31d2                  xor      edx, edx
00428cff  88da                  mov      dl, bl
00428d01  89d0                  mov      eax, edx
00428d03  c1e003                shl      eax, 3
00428d06  01d0                  add      eax, edx
00428d08  01c0                  add      eax, eax
00428d0a  01c8                  add      eax, ecx
00428d0c  30ed                  xor      ch, ch
00428d0e  8a88a2fb4d00          mov      cl, byte ptr [eax + 0x4dfba2]
00428d14  89c8                  mov      eax, ecx
00428d16  59                    pop      ecx
00428d17  c3                    ret
00428d18  69c8d4010000          imul     ecx, eax, 0x1d4
00428d1e  31d2                  xor      edx, edx
00428d20  88da                  mov      dl, bl
00428d22  89d0                  mov      eax, edx
00428d24  c1e003                shl      eax, 3
00428d27  01d0                  add      eax, edx
00428d29  668b8c41a4fb4d00      mov      cx, word ptr [ecx + eax*2 + 0x4dfba4]
00428d31  89c8                  mov      eax, ecx
00428d33  59                    pop      ecx
00428d34  c3                    ret
00428d35  69c8d4010000          imul     ecx, eax, 0x1d4
00428d3b  31d2                  xor      edx, edx
00428d3d  88da                  mov      dl, bl
00428d3f  89d0                  mov      eax, edx
00428d41  c1e003                shl      eax, 3
00428d44  01d0                  add      eax, edx
00428d46  01c0                  add      eax, eax
00428d48  01c8                  add      eax, ecx
00428d4a  30ed                  xor      ch, ch
00428d4c  8a88aafb4d00          mov      cl, byte ptr [eax + 0x4dfbaa]
00428d52  89c8                  mov      eax, ecx
00428d54  59                    pop      ecx
00428d55  c3                    ret
00428d56  69c8d4010000          imul     ecx, eax, 0x1d4
00428d5c  31d2                  xor      edx, edx
00428d5e  88da                  mov      dl, bl
00428d60  89d0                  mov      eax, edx
00428d62  c1e003                shl      eax, 3
00428d65  01d0                  add      eax, edx
00428d67  668b8c41a8fb4d00      mov      cx, word ptr [ecx + eax*2 + 0x4dfba8]
00428d6f  89c8                  mov      eax, ecx
00428d71  59                    pop      ecx
00428d72  c3                    ret
00428d73  69c8d4010000          imul     ecx, eax, 0x1d4
00428d79  31d2                  xor      edx, edx
00428d7b  88da                  mov      dl, bl
00428d7d  89d0                  mov      eax, edx
00428d7f  c1e003                shl      eax, 3
00428d82  01d0                  add      eax, edx
00428d84  01c0                  add      eax, eax
00428d86  01c8                  add      eax, ecx
00428d88  30ed                  xor      ch, ch
00428d8a  8a88abfb4d00          mov      cl, byte ptr [eax + 0x4dfbab]
00428d90  89c8                  mov      eax, ecx
00428d92  59                    pop      ecx
00428d93  c3                    ret
00428d94  69c8d4010000          imul     ecx, eax, 0x1d4
00428d9a  31d2                  xor      edx, edx
00428d9c  88da                  mov      dl, bl
00428d9e  89d0                  mov      eax, edx
00428da0  c1e003                shl      eax, 3
00428da3  01d0                  add      eax, edx
00428da5  01c0                  add      eax, eax
00428da7  01c8                  add      eax, ecx
00428da9  30ed                  xor      ch, ch
00428dab  8a88a6fb4d00          mov      cl, byte ptr [eax + 0x4dfba6]
00428db1  89c8                  mov      eax, ecx
00428db3  59                    pop      ecx
00428db4  c3                    ret
00428db5  69c8d4010000          imul     ecx, eax, 0x1d4
00428dbb  31d2                  xor      edx, edx
00428dbd  88da                  mov      dl, bl
00428dbf  89d0                  mov      eax, edx
00428dc1  c1e003                shl      eax, 3
00428dc4  01d0                  add      eax, edx
00428dc6  01c0                  add      eax, eax
00428dc8  01c8                  add      eax, ecx
00428dca  30ed                  xor      ch, ch
00428dcc  8a88acfb4d00          mov      cl, byte ptr [eax + 0x4dfbac]
00428dd2  89c8                  mov      eax, ecx
00428dd4  59                    pop      ecx
00428dd5  c3                    ret
00428dd6  69c8d4010000          imul     ecx, eax, 0x1d4
00428ddc  31d2                  xor      edx, edx
00428dde  88da                  mov      dl, bl
00428de0  89d0                  mov      eax, edx
00428de2  c1e003                shl      eax, 3
00428de5  01d0                  add      eax, edx
00428de7  01c0                  add      eax, eax
00428de9  01c8                  add      eax, ecx
00428deb  30ed                  xor      ch, ch
00428ded  8a88b1fb4d00          mov      cl, byte ptr [eax + 0x4dfbb1]
00428df3  89c8                  mov      eax, ecx
00428df5  59                    pop      ecx
00428df6  c3                    ret
00428df7  69c8d4010000          imul     ecx, eax, 0x1d4
00428dfd  31d2                  xor      edx, edx
00428dff  88da                  mov      dl, bl
00428e01  89d0                  mov      eax, edx
00428e03  c1e003                shl      eax, 3
00428e06  01d0                  add      eax, edx
00428e08  01c0                  add      eax, eax
00428e0a  01c8                  add      eax, ecx
00428e0c  30ed                  xor      ch, ch
00428e0e  8a88b0fb4d00          mov      cl, byte ptr [eax + 0x4dfbb0]
00428e14  89c8                  mov      eax, ecx
00428e16  59                    pop      ecx
00428e17  c3                    ret
00428e18  69c8d4010000          imul     ecx, eax, 0x1d4
00428e1e  31d2                  xor      edx, edx
00428e20  88da                  mov      dl, bl
00428e22  89d0                  mov      eax, edx
00428e24  c1e003                shl      eax, 3
00428e27  01d0                  add      eax, edx
00428e29  01c0                  add      eax, eax
00428e2b  01c8                  add      eax, ecx
00428e2d  30ed                  xor      ch, ch
00428e2f  8a88affb4d00          mov      cl, byte ptr [eax + 0x4dfbaf]
00428e35  89c8                  mov      eax, ecx
00428e37  59                    pop      ecx
00428e38  c3                    ret
00428e39  69c8d4010000          imul     ecx, eax, 0x1d4
00428e3f  31d2                  xor      edx, edx
00428e41  88da                  mov      dl, bl
00428e43  89d0                  mov      eax, edx
00428e45  c1e003                shl      eax, 3
00428e48  01d0                  add      eax, edx
00428e4a  01c0                  add      eax, eax
00428e4c  01c8                  add      eax, ecx
00428e4e  30ed                  xor      ch, ch
00428e50  8a88aefb4d00          mov      cl, byte ptr [eax + 0x4dfbae]
00428e56  89c8                  mov      eax, ecx
00428e58  59                    pop      ecx
00428e59  c3                    ret
00428e5a  80fa0c                cmp      dl, 0xc
00428e5d  0f8790feffff          ja       0x428cf3
00428e63  81e2ff000000          and      edx, 0xff
00428e69  2eff24958c8c4200      jmp      dword ptr cs:[edx*4 + 0x428c8c]
