; ChercheBatimentProximiteCaveOuSanctuaire 0x4539f3..0x453b84
004539f3: push      ebx
004539f4: push      ecx
004539f5: push      esi
004539f6: push      edi
004539f7: push      ebp
004539f8: sub       esp, 0x14
004539fb: push      eax
004539fc: mov       byte ptr [esp + 0x14], dl
00453a00: mov       edx, 0xffffffff
00453a05: mov       dword ptr [esp + 4], edx
00453a09: mov       dword ptr [esp + 8], edx
00453a0d: mov       edx, 0xffff
00453a12: xor       esi, esi
00453a14: mov       dword ptr [esp + 0x10], edx
00453a18: mov       dword ptr [esp + 0xc], edx
00453a1c: jmp       0x453a9c
00453a21: cmp       eax, 3
00453a24: jne       0x453a9b
00453a26: mov       eax, edx
00453a28: xor       ebx, ebx
00453a2a: call      0x41aee2
00453a2f: mov       bx, ax
00453a32: mov       edx, ebx
00453a34: mov       eax, ebx
00453a36: sar       edx, 0x1f
00453a39: shl       edx, 8
00453a3c: sbb       eax, edx
00453a3e: sar       eax, 8
00453a41: xor       ecx, ecx
00453a43: mov       cx, ax
00453a46: mov       edx, ebx
00453a48: mov       eax, ebx
00453a4a: sar       edx, 0x1f
00453a4d: mov       ebx, 0x100
00453a52: idiv      ebx
00453a54: xor       ebx, ebx
00453a56: mov       bx, word ptr [esp]
00453a5a: movzx     ebp, dx
00453a5d: mov       edx, ebx
00453a5f: mov       eax, ebx
00453a61: sar       edx, 0x1f
00453a64: shl       edx, 8
00453a67: sbb       eax, edx
00453a69: sar       eax, 8
00453a6c: xor       edi, edi
00453a6e: mov       di, ax
00453a71: mov       edx, ebx
00453a73: mov       eax, ebx
00453a75: sar       edx, 0x1f
00453a78: mov       ebx, 0x100
00453a7d: idiv      ebx
00453a7f: xor       eax, eax
00453a81: mov       ebx, ebp
00453a83: mov       ax, dx
00453a86: mov       edx, edi
00453a88: call      0x479555
00453a8d: cmp       eax, dword ptr [esp + 8]
00453a91: jae       0x453a9b
00453a93: mov       dword ptr [esp + 8], eax
00453a97: mov       dword ptr [esp + 0x10], esi
00453a9b: inc       esi
00453a9c: xor       edx, edx
00453a9e: mov       dx, si
00453aa1: cmp       edx, 0x3e8
00453aa7: jge       0x453b5b
00453aad: mov       eax, edx
00453aaf: call      0x41a4f4
00453ab4: mov       bl, al
00453ab6: mov       eax, edx
00453ab8: call      0x41a735
00453abd: test      al, al
00453abf: je        0x453a9b
00453ac1: mov       eax, edx
00453ac3: call      0x41a08c
00453ac8: cmp       al, byte ptr [esp + 0x14]
00453acc: jne       0x453a9b
00453ace: xor       eax, eax
00453ad0: mov       al, bl
00453ad2: cmp       eax, 2
00453ad5: jne       0x453a21
00453adb: mov       eax, edx
00453add: xor       ebx, ebx
00453adf: call      0x41aee2
00453ae4: mov       bx, ax
00453ae7: mov       edx, ebx
00453ae9: mov       eax, ebx
00453aeb: sar       edx, 0x1f
00453aee: shl       edx, 8
00453af1: sbb       eax, edx
00453af3: sar       eax, 8
00453af6: xor       ecx, ecx
00453af8: mov       cx, ax
00453afb: mov       edx, ebx
00453afd: mov       eax, ebx
00453aff: sar       edx, 0x1f
00453b02: mov       ebx, 0x100
00453b07: idiv      ebx
00453b09: xor       ebx, ebx
00453b0b: xor       edi, edi
00453b0d: mov       bx, word ptr [esp]
00453b11: mov       di, dx
00453b14: mov       edx, ebx
00453b16: mov       eax, ebx
00453b18: sar       edx, 0x1f
00453b1b: shl       edx, 8
00453b1e: sbb       eax, edx
00453b20: sar       eax, 8
00453b23: movzx     ebp, ax
00453b26: mov       edx, ebx
00453b28: mov       eax, ebx
00453b2a: sar       edx, 0x1f
00453b2d: mov       ebx, 0x100
00453b32: idiv      ebx
00453b34: xor       eax, eax
00453b36: mov       ebx, edi
00453b38: mov       ax, dx
00453b3b: mov       edx, ebp
00453b3d: mov       edi, dword ptr [esp + 4]
00453b41: call      0x479555
00453b46: cmp       eax, edi
00453b48: jae       0x453a9b
00453b4e: mov       dword ptr [esp + 4], eax
00453b52: mov       dword ptr [esp + 0xc], esi
00453b56: jmp       0x453a9b
00453b5b: xor       eax, eax
00453b5d: mov       ax, word ptr [esp + 0x10]
00453b62: cmp       eax, 0xffff
00453b67: jne       0x453b7c
00453b69: xor       eax, eax
00453b6b: mov       ax, word ptr [esp + 0xc]
00453b70: cmp       eax, 0xffff
00453b75: jne       0x453b7c
00453b77: mov       eax, 0xffff
00453b7c: add       esp, 0x18
00453b7f: jmp       0x445f27
