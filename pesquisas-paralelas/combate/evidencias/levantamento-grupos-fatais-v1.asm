
; iagUnitRemoveFromGroup 0x4832b1..0x483358
004832b1: push      ebx
004832b2: push      ecx
004832b3: push      esi
004832b4: mov       esi, 0x51a9e0
004832b9: shl       eax, 5
004832bc: mov       ecx, edx
004832be: add       esi, eax
004832c0: jne       0x4832cb
004832c2: mov       eax, 0x1a1a0010
004832c7: pop       esi
004832c8: pop       ecx
004832c9: pop       ebx
004832ca: ret       
004832cb: mov       ebx, 0xffff
004832d0: mov       ax, word ptr [esi + 0x10]
004832d4: xor       edx, edx
004832d6: mov       dx, ax
004832d9: cmp       edx, 0xffff
004832df: je        0x48334f
004832e1: imul      edx, edx, 0x114
004832e7: cmp       ax, cx
004832ea: jne       0x48333e
004832ec: xor       eax, eax
004832ee: mov       ax, bx
004832f1: cmp       eax, 0xffff
004832f6: je        0x48331e
004832f8: mov       ecx, dword ptr [0x4e19a0]
004832fe: lea       ebx, [ecx + edx]
00483301: mov       edx, eax
00483303: shl       eax, 4
00483306: add       eax, edx
00483308: shl       eax, 2
0048330b: add       eax, edx
0048330d: mov       dx, word ptr [ebx + 0x108]
00483314: mov       word ptr [ecx + eax*4 + 0x108], dx
0048331c: jmp       0x48332f
0048331e: mov       eax, dword ptr [0x4e19a0]
00483323: mov       ax, word ptr [edx + eax + 0x108]
0048332b: mov       word ptr [esi + 0x10], ax
0048332f: mov       dx, word ptr [esi + 0x12]
00483333: dec       edx
00483334: xor       eax, eax
00483336: mov       word ptr [esi + 0x12], dx
0048333a: pop       esi
0048333b: pop       ecx
0048333c: pop       ebx
0048333d: ret       
0048333e: mov       ebx, eax
00483340: mov       eax, dword ptr [0x4e19a0]
00483345: mov       ax, word ptr [edx + eax + 0x108]
0048334d: jmp       0x4832d4
0048334f: mov       eax, 0x1a1a0012
00483354: pop       esi
00483355: pop       ecx
00483356: pop       ebx
00483357: ret       

; iagWarAddEnnemyToBattle 0x487b78..0x487e2a
00487b78: push      ecx
00487b79: push      esi
00487b7a: push      edi
00487b7b: push      ebp
00487b7c: sub       esp, 0x18
00487b7f: mov       ecx, eax
00487b81: mov       esi, edx
00487b83: mov       dword ptr [esp + 0xc], ebx
00487b87: test      byte ptr [esp + 0xd], 0x80
00487b8c: je        0x487ba1
00487b8e: mov       eax, dword ptr [esp + 0xc]
00487b92: and       ah, 0x7f
00487b95: and       eax, 0xffff
00487b9a: call      0x41a08c
00487b9f: jmp       0x487bad
00487ba1: xor       eax, eax
00487ba3: mov       ax, word ptr [esp + 0xc]
00487ba8: call      0x442045
00487bad: and       eax, 0xff
00487bb2: cmp       eax, ecx
00487bb4: jne       0x487bbd
00487bb6: xor       al, cl
00487bb8: jmp       0x487e22
00487bbd: mov       eax, ecx
00487bbf: shl       eax, 4
00487bc2: add       eax, ecx
00487bc4: shl       eax, 2
00487bc7: mov       edx, eax
00487bc9: shl       eax, 6
00487bcc: mov       ecx, 0x51bcfc
00487bd1: add       eax, edx
00487bd3: add       ecx, eax
00487bd5: mov       eax, esi
00487bd7: shl       eax, 4
00487bda: add       eax, esi
00487bdc: add       ecx, 0x28
00487bdf: shl       eax, 4
00487be2: add       ecx, eax
00487be4: xor       eax, eax
00487be6: mov       ax, word ptr [ecx + 0xe]
00487bea: cmp       eax, 0x20
00487bed: jl        0x487bf6
00487bef: xor       al, al
00487bf1: jmp       0x487e22
00487bf6: mov       dl, byte ptr [esp + 0xd]
00487bfa: lea       eax, [ecx + 0x10]
00487bfd: test      dl, 0x80
00487c00: je        0x487c30
00487c02: mov       edx, dword ptr [esp + 0xc]
00487c06: xor       ebx, ebx
00487c08: and       dh, 0x7f
00487c0b: mov       bx, dx
00487c0e: mov       edx, ebx
00487c10: shl       edx, 4
00487c13: add       edx, ebx
00487c15: shl       edx, 2
00487c18: add       edx, ebx
00487c1a: mov       dl, byte ptr [edx*4 + 0x49a0d0]
00487c21: and       edx, 0xff
00487c27: mov       edx, dword ptr [edx*4 + 0x498d5c]
00487c2e: jmp       0x487c5a
00487c30: xor       ebx, ebx
00487c32: mov       bx, word ptr [esp + 0xc]
00487c37: mov       edx, ebx
00487c39: shl       edx, 4
00487c3c: add       edx, ebx
00487c3e: shl       edx, 2
00487c41: add       edx, ebx
00487c43: mov       ebx, dword ptr [0x4e19a0]
00487c49: mov       dl, byte ptr [ebx + edx*4 + 1]
00487c4d: and       edx, 0xff
00487c53: mov       edx, dword ptr [edx*4 + 0x498cf4]
00487c5a: mov       ebp, 0xffffffff
00487c5f: mov       ebx, dword ptr [esp + 0xc]
00487c63: mov       byte ptr [esp + 0x14], dl
00487c67: mov       esi, ebp
00487c69: and       bh, 0x7f
00487c6c: xor       edx, edx
00487c6e: mov       dword ptr [esp + 0x10], ebx
00487c72: jmp       0x487d5e
00487c77: xor       ebx, ebx
00487c79: movzx     edi, byte ptr [esp + 0x14]
00487c7e: mov       bx, word ptr [eax + 4]
00487c82: cmp       ebx, edi
00487c84: jne       0x487d4e
00487c8a: test      byte ptr [esp + 0xd], 0x80
00487c8f: je        0x487cba
00487c91: xor       ebx, ebx
00487c93: mov       bx, word ptr [esp + 0x10]
00487c98: imul      ebx, ebx, 0x114
00487c9e: add       ebx, 0x49a0c8
00487ca4: xor       edi, edi
00487ca6: mov       di, word ptr [ebx + 0xa]
00487caa: mov       bx, word ptr [ebx + 6]
00487cae: and       ebx, 0xffff
00487cb4: sub       edi, ebx
00487cb6: mov       ebx, edi
00487cb8: jmp       0x487cdc
00487cba: xor       ebx, ebx
00487cbc: mov       bx, word ptr [esp + 0xc]
00487cc1: imul      ebx, ebx, 0x114
00487cc7: mov       edi, dword ptr [0x4e19a0]
00487ccd: add       ebx, edi
00487ccf: mov       bx, word ptr [ebx + 0x9a]
00487cd6: and       ebx, 0xffff
00487cdc: mov       dword ptr [esp + 8], ebx
00487ce0: mov       bx, word ptr [eax]
00487ce3: test      bh, 0x80
00487ce6: je        0x487d15
00487ce8: and       bh, 0x7f
00487ceb: and       ebx, 0xffff
00487cf1: imul      ebx, ebx, 0x114
00487cf7: add       ebx, 0x49a0c8
00487cfd: xor       edi, edi
00487cff: mov       di, word ptr [ebx + 0xa]
00487d03: mov       bx, word ptr [ebx + 6]
00487d07: and       ebx, 0xffff
00487d0d: sub       edi, ebx
00487d0f: mov       dword ptr [esp + 4], edi
00487d13: jmp       0x487d40
00487d15: and       ebx, 0xffff
00487d1b: imul      ebx, ebx, 0x114
00487d21: mov       dword ptr [esp], ebx
00487d24: mov       edi, dword ptr [esp]
00487d27: mov       ebx, dword ptr [0x4e19a0]
00487d2d: add       ebx, edi
00487d2f: mov       bx, word ptr [ebx + 0x9a]
00487d36: and       ebx, 0xffff
00487d3c: mov       dword ptr [esp + 4], ebx
00487d40: mov       ebx, dword ptr [esp + 8]
00487d44: cmp       ebx, dword ptr [esp + 4]
00487d48: jge       0x487d5a
00487d4a: mov       esi, edx
00487d4c: jmp       0x487d5a
00487d4e: jge       0x487d5a
00487d50: cmp       esi, ebp
00487d52: je        0x487d58
00487d54: mov       ebp, esi
00487d56: jmp       0x487d5a
00487d58: mov       ebp, edx
00487d5a: add       eax, 8
00487d5d: inc       edx
00487d5e: xor       ebx, ebx
00487d60: mov       bx, word ptr [ecx + 0xe]
00487d64: cmp       edx, ebx
00487d66: jge       0x487d99
00487d68: cmp       ebp, -1
00487d6b: jne       0x487d99
00487d6d: xor       ebx, ebx
00487d6f: mov       edi, dword ptr [esp + 0xc]
00487d73: mov       bx, word ptr [eax]
00487d76: cmp       ebx, edi
00487d78: jne       0x487c77
00487d7e: mov       ax, word ptr [eax + 2]
00487d82: and       eax, 0xffff
00487d87: jne       0x487bef
00487d8d: mov       eax, ecx
00487d8f: call      0x487eef
00487d94: jmp       0x487bef
00487d99: cmp       ebp, -1
00487d9c: jne       0x487dd1
00487d9e: xor       eax, eax
00487da0: xor       dh, dh
00487da2: mov       ax, word ptr [ecx + 0xe]
00487da6: mov       dl, byte ptr [esp + 0x14]
00487daa: mov       word ptr [ecx + eax*8 + 0x14], dx
00487daf: xor       eax, eax
00487db1: mov       ax, word ptr [ecx + 0xe]
00487db5: mov       edx, dword ptr [esp + 0xc]
00487db9: mov       word ptr [ecx + eax*8 + 0x10], dx
00487dbe: xor       eax, eax
00487dc0: mov       ax, word ptr [ecx + 0xe]
00487dc4: mov       word ptr [ecx + eax*8 + 0x12], 0
00487dcb: movzx     ebp, word ptr [ecx + 0xe]
00487dcf: jmp       0x487e0e
00487dd1: xor       edx, edx
00487dd3: mov       dx, word ptr [ecx + 0xe]
00487dd7: dec       edx
00487dd8: mov       eax, edx
00487dda: shl       eax, 3
00487ddd: add       eax, ecx
00487ddf: jmp       0x487ded
00487de1: lea       edi, [eax + 0x18]
00487de4: lea       esi, [eax + 0x10]
00487de7: sub       eax, 8
00487dea: dec       edx
00487deb: movsd     dword ptr es:[edi], dword ptr [esi]
00487dec: movsd     dword ptr es:[edi], dword ptr [esi]
00487ded: cmp       edx, ebp
00487def: jge       0x487de1
00487df1: xor       dh, dh
00487df3: mov       eax, ebp
00487df5: mov       dl, byte ptr [esp + 0x14]
00487df9: mov       word ptr [ecx + eax*8 + 0x12], 0
00487e00: mov       word ptr [ecx + eax*8 + 0x14], dx
00487e05: mov       edx, dword ptr [esp + 0xc]
00487e09: mov       word ptr [ecx + eax*8 + 0x10], dx
00487e0e: mov       dx, word ptr [ecx + 0xe]
00487e12: inc       edx
00487e13: mov       eax, ecx
00487e15: mov       word ptr [ecx + 0xe], dx
00487e19: mov       edx, ebp
00487e1b: call      0x487eef
00487e20: mov       al, 1
00487e22: add       esp, 0x18
00487e25: pop       ebp
00487e26: pop       edi
00487e27: pop       esi
00487e28: pop       ecx
00487e29: ret       

; iabPlusCible_ChangeDeCibleOuObjectifRealise 0x489ca2..0x489d6c
00489ca2: push      ebx
00489ca3: push      ecx
00489ca4: push      esi
00489ca5: mov       esi, eax
00489ca7: shl       eax, 4
00489caa: add       eax, esi
00489cac: shl       eax, 2
00489caf: add       eax, esi
00489cb1: mov       edx, dword ptr [0x4e19a0]
00489cb7: shl       eax, 2
00489cba: add       eax, edx
00489cbc: mov       ecx, dword ptr [eax + 0x10c]
00489cc2: shl       ecx, 5
00489cc5: add       ecx, 0x51a9e0
00489ccb: je        0x489d68
00489cd1: cmp       dword ptr [ecx + 0xc], -1
00489cd5: je        0x489d23
00489cd7: xor       edx, edx
00489cd9: mov       dl, byte ptr [eax + 0xb7]
00489cdf: cmp       edx, 3
00489ce2: jne       0x489cfa
00489ce4: mov       dx, word ptr [eax + 0xb8]
00489ceb: xor       ebx, ebx
00489ced: or        dh, 0x80
00489cf0: mov       al, byte ptr [eax]
00489cf2: mov       bx, dx
00489cf5: mov       edx, dword ptr [ecx + 0xc]
00489cf8: jmp       0x489d0d
00489cfa: cmp       edx, 1
00489cfd: jne       0x489d17
00489cff: xor       ebx, ebx
00489d01: mov       edx, dword ptr [ecx + 0xc]
00489d04: mov       bx, word ptr [eax + 0xb8]
00489d0b: mov       al, byte ptr [eax]
00489d0d: and       eax, 0xff
00489d12: call      0x487e2a
00489d17: mov       eax, esi
00489d19: mov       edx, dword ptr [ecx + 0xc]
00489d1c: call      0x48829d
00489d21: jmp       0x489d28
00489d23: mov       eax, 0xffff
00489d28: and       eax, 0xffff
00489d2d: cmp       eax, 0xffff
00489d32: jne       0x489d68
00489d34: mov       ebx, esi
00489d36: shl       ebx, 4
00489d39: add       ebx, esi
00489d3b: shl       ebx, 2
00489d3e: add       ebx, esi
00489d40: mov       eax, dword ptr [0x4e19a0]
00489d45: shl       ebx, 2
00489d48: xor       edx, edx
00489d4a: mov       dx, word ptr [ebx + eax + 0x7c]
00489d4f: xor       eax, eax
00489d51: mov       ax, si
00489d54: call      0x4457d3
00489d59: mov       eax, dword ptr [0x4e19a0]
00489d5e: mov       word ptr [ebx + eax + 0xb8], 0xffff
00489d68: pop       esi
00489d69: pop       ecx
00489d6a: pop       ebx
00489d6b: ret       

; EnginSetFatigue 0x453b84..0x453d56
00453b84: push      ebx
00453b85: push      ecx
00453b86: push      edx
00453b87: push      esi
00453b88: push      edi
00453b89: push      ebp
00453b8a: push      eax
00453b8b: movzx     ebp, ax
00453b8e: mov       esi, ebp
00453b90: shl       esi, 4
00453b93: add       esi, ebp
00453b95: shl       esi, 2
00453b98: lea       edi, [esi + ebp]
00453b9b: mov       esi, dword ptr [0x4e19a0]
00453ba1: shl       edi, 2
00453ba4: add       esi, edi
00453ba6: xor       eax, eax
00453ba8: mov       ax, word ptr [esi + 4]
00453bac: cmp       eax, 4
00453baf: je        0x44b342
00453bb5: xor       eax, eax
00453bb7: mov       al, byte ptr [esi + 2]
00453bba: cmp       eax, 0x13
00453bbd: je        0x44b342
00453bc3: xor       ah, ah
00453bc5: mov       ecx, 0x43
00453bca: mov       word ptr [esi + 0xa0], ax
00453bd1: mov       edx, 0x14
00453bd6: mov       ax, word ptr [esi + 0x7e]
00453bda: push      ebp
00453bdb: mov       word ptr [esi + 0xa2], ax
00453be2: xor       eax, eax
00453be4: mov       ebx, ecx
00453be6: mov       ax, word ptr [esi + 8]
00453bea: call      0x477b74
00453bef: xor       edx, edx
00453bf1: mov       dx, ax
00453bf4: cmp       edx, 0xffff
00453bfa: je        0x453c4f
00453bfc: mov       word ptr [esi + 0xc2], 0xffff
00453c05: mov       byte ptr [esi + 2], 0x13
00453c09: mov       edx, dword ptr [0x4e19a0]
00453c0f: add       edi, edx
00453c11: mov       word ptr [edi + 0x7e], ax
00453c15: mov       eax, dword ptr [esp]
00453c18: cmp       ax, word ptr [0x496304]
00453c1f: jne       0x453c43
00453c21: mov       esi, 0xffff
00453c26: xor       bl, bl
00453c28: xor       ecx, ecx
00453c2a: mov       byte ptr [0x4e0f36], bl
00453c30: mov       byte ptr [0x4e0f37], bl
00453c36: mov       dword ptr [0x4e0f3c], ecx
00453c3c: mov       word ptr [0x496304], si
00453c43: mov       byte ptr [edi + 0x88], 0
00453c4a: jmp       0x44b342
00453c4f: xor       eax, eax
00453c51: xor       ecx, ecx
00453c53: mov       al, byte ptr [esi]
00453c55: xor       ebx, ebx
00453c57: push      eax
00453c58: xor       edx, edx
00453c5a: mov       eax, 3
00453c5f: call      0x4676e5
00453c64: test      al, al
00453c66: je        0x44b342
00453c6c: mov       ebx, 3
00453c71: mov       edx, 0x28
00453c76: xor       ecx, ecx
00453c78: xor       eax, eax
00453c7a: mov       cl, byte ptr [esi]
00453c7c: mov       ax, word ptr [esi + 8]
00453c80: call      0x4538fa
00453c85: mov       edx, eax
00453c87: xor       eax, eax
00453c89: mov       ax, dx
00453c8c: cmp       eax, 0xffff
00453c91: je        0x453ce2
00453c93: call      0x41aee2
00453c98: mov       byte ptr [esi + 2], 0x13
00453c9c: mov       word ptr [esi + 0xc2], dx
00453ca3: mov       edx, dword ptr [0x4e19a0]
00453ca9: add       edi, edx
00453cab: mov       word ptr [edi + 0x7e], ax
00453caf: mov       eax, dword ptr [esp]
00453cb2: cmp       ax, word ptr [0x496304]
00453cb9: jne       0x453c43
00453cbb: xor       dl, dl
00453cbd: xor       ebx, ebx
00453cbf: mov       byte ptr [0x4e0f36], dl
00453cc5: mov       dword ptr [0x4e0f3c], ebx
00453ccb: mov       ebx, 0xffff
00453cd0: mov       byte ptr [0x4e0f37], dl
00453cd6: mov       word ptr [0x496304], bx
00453cdd: jmp       0x453c43
00453ce2: mov       al, byte ptr [esi]
00453ce4: cmp       al, byte ptr [0x508041]
00453cea: jne       0x44b342
00453cf0: xor       eax, eax
00453cf2: mov       ax, word ptr [esi + 0x74]
00453cf6: cmp       eax, 1
00453cf9: jne       0x44b342
00453cff: mov       esi, dword ptr [0x4e19a0]
00453d05: xor       edx, edx
00453d07: add       esi, edi
00453d09: xor       eax, eax
00453d0b: mov       dl, byte ptr [0x508041]
00453d11: mov       ax, word ptr [esi + 8]
00453d15: call      0x4766f0
00453d1a: test      al, al
00453d1c: je        0x44b342
00453d22: mov       eax, ebp
00453d24: call      0x440c5d
00453d29: mov       edx, dword ptr [esi + 0x104]
00453d2f: mov       byte ptr [esi + 0xf9], 0
00453d36: cmp       edx, -1
00453d39: jne       0x44b342
00453d3f: push      eax
00453d40: xor       eax, eax
00453d42: mov       al, byte ptr [esi + 1]
00453d45: shl       eax, 0x10
00453d48: lea       ebx, [esi + 0x104]
00453d4e: or        ah, 0xc
00453d51: jmp       0x44b334

; EnginGetDegat 0x44f98a..0x44f9a6
0044f98a: push      ebx
0044f98b: and       eax, 0xff
0044f990: mov       ebx, dword ptr [0x4e199c]
0044f996: shl       eax, 2
0044f999: add       eax, ebx
0044f99b: xor       ebx, ebx
0044f99d: mov       eax, dword ptr [eax]
0044f99f: mov       bl, dl
0044f9a1: mov       al, byte ptr [ebx + eax]
0044f9a4: pop       ebx
0044f9a5: ret       
