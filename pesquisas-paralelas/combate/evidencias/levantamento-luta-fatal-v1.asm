
; iagUnitSendMessage 0x4829c8..0x482ebc
004829c8: push      ecx
004829c9: push      esi
004829ca: push      edi
004829cb: push      ebp
004829cc: mov       ebp, esp
004829ce: sub       esp, 0x1c
004829d1: mov       esi, eax
004829d3: mov       byte ptr [ebp - 4], dl
004829d6: mov       edx, ebx
004829d8: xor       ebx, ebx
004829da: mov       bx, ax
004829dd: mov       edi, ebx
004829df: shl       edi, 4
004829e2: add       edi, ebx
004829e4: shl       edi, 2
004829e7: add       edi, ebx
004829e9: mov       eax, dword ptr [0x4e19a0]
004829ee: shl       edi, 2
004829f1: mov       al, byte ptr [edi + eax]
004829f4: and       eax, 0xff
004829f9: mov       dword ptr [ebp - 0x1c], eax
004829fc: xor       eax, eax
004829fe: mov       al, byte ptr [ebp - 0x1c]
00482a01: call      0x46d817
00482a06: and       eax, 0xff
00482a0b: cmp       eax, 2
00482a0e: jne       0x482eb5
00482a14: mov       eax, dword ptr [0x4e19a0]
00482a19: mov       edi, dword ptr [edi + eax + 0x10c]
00482a20: cmp       edi, -1
00482a23: je        0x482a35
00482a25: mov       ecx, edi
00482a27: shl       ecx, 5
00482a2a: add       ecx, 0x51a9e0
00482a30: jmp       0x482a37
00482a35: xor       ecx, ecx
00482a37: mov       al, byte ptr [ebp - 4]
00482a3a: sub       al, 0x41
00482a3c: cmp       al, 0xb
00482a3e: ja        0x482eb5
00482a44: and       eax, 0xff
00482a49: jmp       dword ptr cs:[eax*4 + 0x482998]
00482a51: test      ecx, ecx
00482a53: je        0x482eb5
00482a59: xor       edx, edx
00482a5b: mov       eax, edi
00482a5d: mov       dx, si
00482a60: call      0x4832b1
00482a65: xor       edx, edx
00482a67: mov       dx, si
00482a6a: mov       eax, edx
00482a6c: shl       eax, 4
00482a6f: add       eax, edx
00482a71: shl       eax, 2
00482a74: add       edx, eax
00482a76: mov       eax, dword ptr [0x4e19a0]
00482a7b: shl       edx, 2
00482a7e: add       eax, edx
00482a80: xor       edx, edx
00482a82: mov       dl, byte ptr [eax]
00482a84: mov       eax, edx
00482a86: shl       eax, 2
00482a89: sub       eax, edx
00482a8b: xor       edx, edx
00482a8d: shl       eax, 5
00482a90: mov       dx, si
00482a93: mov       ebx, dword ptr [eax + 0x51b68c]
00482a99: mov       eax, edx
00482a9b: shl       eax, 4
00482a9e: add       eax, edx
00482aa0: shl       eax, 2
00482aa3: mov       ecx, ebx
00482aa5: add       eax, edx
00482aa7: mov       edx, dword ptr [0x4e19a0]
00482aad: shl       eax, 2
00482ab0: shl       ecx, 5
00482ab3: add       edx, eax
00482ab5: mov       eax, 0x51a9e0
00482aba: add       eax, ecx
00482abc: je        0x482eb5
00482ac2: mov       cx, word ptr [eax + 0x10]
00482ac6: mov       word ptr [edx + 0x108], cx
00482acd: mov       dword ptr [edx + 0x10c], ebx
00482ad3: mov       bx, word ptr [eax + 0x12]
00482ad7: mov       word ptr [eax + 0x10], si
00482adb: inc       ebx
00482adc: mov       word ptr [eax + 0x12], bx
00482ae0: jmp       0x482eb5
00482ae5: xor       edx, edx
00482ae7: mov       dx, si
00482aea: mov       eax, edx
00482aec: shl       eax, 4
00482aef: add       eax, edx
00482af1: shl       eax, 2
00482af4: add       eax, edx
00482af6: mov       edx, dword ptr [0x4e19a0]
00482afc: shl       eax, 2
00482aff: add       eax, edx
00482b01: xor       edx, edx
00482b03: mov       dl, byte ptr [eax]
00482b05: mov       eax, edx
00482b07: shl       eax, 2
00482b0a: xor       ebx, ebx
00482b0c: sub       eax, edx
00482b0e: mov       bx, si
00482b11: shl       eax, 5
00482b14: mov       edx, ebx
00482b16: mov       eax, dword ptr [eax + 0x51b68c]
00482b1c: call      0x4832b1
00482b21: xor       edx, edx
00482b23: mov       dx, si
00482b26: mov       eax, edx
00482b28: shl       eax, 4
00482b2b: add       eax, edx
00482b2d: shl       eax, 2
00482b30: add       eax, edx
00482b32: mov       edx, dword ptr [0x4e19a0]
00482b38: shl       eax, 2
00482b3b: add       eax, edx
00482b3d: xor       edx, edx
00482b3f: mov       dl, byte ptr [eax]
00482b41: mov       eax, edx
00482b43: shl       eax, 2
00482b46: sub       eax, edx
00482b48: shl       eax, 5
00482b4b: mov       edx, dword ptr [eax + 0x51b690]
00482b51: xor       eax, eax
00482b53: mov       ax, si
00482b56: call      0x4838d1
00482b5b: jmp       0x482eb5
00482b60: xor       edx, edx
00482b62: mov       dx, si
00482b65: mov       eax, edx
00482b67: shl       eax, 4
00482b6a: add       eax, edx
00482b6c: shl       eax, 2
00482b6f: add       eax, edx
00482b71: mov       edx, dword ptr [0x4e19a0]
00482b77: shl       eax, 2
00482b7a: add       edx, eax
00482b7c: xor       ebx, ebx
00482b7e: mov       bl, byte ptr [edx]
00482b80: mov       eax, ebx
00482b82: shl       eax, 2
00482b85: sub       eax, ebx
00482b87: shl       eax, 5
00482b8a: mov       ebx, dword ptr [eax + 0x51b68c]
00482b90: mov       eax, ebx
00482b92: shl       eax, 5
00482b95: mov       edi, esi
00482b97: add       eax, 0x51a9e0
00482b9c: je        0x482bbc
00482b9e: mov       cx, word ptr [eax + 0x10]
00482ba2: mov       word ptr [edx + 0x108], cx
00482ba9: mov       dword ptr [edx + 0x10c], ebx
00482baf: mov       dx, word ptr [eax + 0x12]
00482bb3: mov       word ptr [eax + 0x10], si
00482bb7: inc       edx
00482bb8: mov       word ptr [eax + 0x12], dx
00482bbc: xor       edx, edx
00482bbe: mov       dx, si
00482bc1: mov       eax, edx
00482bc3: shl       eax, 4
00482bc6: add       eax, edx
00482bc8: shl       eax, 2
00482bcb: add       eax, edx
00482bcd: mov       edx, dword ptr [0x4e19a0]
00482bd3: shl       eax, 2
00482bd6: add       eax, edx
00482bd8: xor       edx, edx
00482bda: xor       ebx, ebx
00482bdc: mov       dl, byte ptr [eax]
00482bde: mov       bl, byte ptr [eax + 1]
00482be1: mov       eax, edx
00482be3: shl       eax, 2
00482be6: sub       eax, edx
00482be8: shl       eax, 5
00482beb: mov       edx, dword ptr [eax + 0x51b6b4]
00482bf1: cmp       edx, -1
00482bf4: je        0x482c0f
00482bf6: mov       eax, edx
00482bf8: shl       eax, 5
00482bfb: xor       ecx, ecx
00482bfd: mov       cl, byte ptr [eax + 0x51a9fa]
00482c03: cmp       ecx, ebx
00482c05: je        0x482c0f
00482c07: mov       edx, dword ptr [eax + 0x51a9e4]
00482c0d: jmp       0x482bf1
00482c0f: cmp       edx, -1
00482c12: je        0x482c32
00482c14: push      0
00482c16: push      0
00482c18: xor       ebx, ebx
00482c1a: push      0
00482c1c: mov       bx, si
00482c1f: push      0
00482c21: mov       eax, ebx
00482c23: call      0x442045
00482c28: mov       edx, 0x17
00482c2d: jmp       0x482d20
00482c32: push      0
00482c34: push      0
00482c36: xor       ebx, ebx
00482c38: push      0
00482c3a: mov       bx, si
00482c3d: push      0
00482c3f: mov       eax, ebx
00482c41: call      0x442045
00482c46: mov       edx, 9
00482c4b: jmp       0x482d20
00482c50: test      ecx, ecx
00482c52: je        0x482eb5
00482c58: mov       eax, dword ptr [ecx + 0xc]
00482c5b: cmp       eax, -1
00482c5e: je        0x482c7c
00482c60: mov       edx, eax
00482c62: xor       eax, eax
00482c64: mov       ax, si
00482c67: mov       ebx, 0xffffffff
00482c6c: call      0x48873f
00482c71: mov       eax, dword ptr [ebp - 0x1c]
00482c74: mov       edx, dword ptr [ecx + 0xc]
00482c77: call      0x488cea
00482c7c: xor       edx, edx
00482c7e: mov       eax, edi
00482c80: mov       dx, si
00482c83: call      0x4832b1
00482c88: cmp       dword ptr [ecx + 0x1c], 0
00482c8c: je        0x482eb5
00482c92: cmp       dword ptr [ecx + 8], -1
00482c96: je        0x482eb5
00482c9c: test      byte ptr [ecx + 0x1c], 1
00482ca0: je        0x482cb4
00482ca2: mov       edx, 1
00482ca7: mov       eax, dword ptr [ecx + 8]
00482caa: call      0x47da54
00482caf: jmp       0x482eb5
00482cb4: mov       edx, 0xffffffff
00482cb9: jmp       0x482ca7
00482cbb: xor       ebx, ebx
00482cbd: mov       bx, si
00482cc0: mov       eax, ebx
00482cc2: shl       eax, 4
00482cc5: add       eax, ebx
00482cc7: shl       eax, 2
00482cca: add       eax, ebx
00482ccc: mov       edx, dword ptr [0x4e19a0]
00482cd2: shl       eax, 2
00482cd5: add       eax, edx
00482cd7: xor       edx, edx
00482cd9: mov       dl, byte ptr [eax]
00482cdb: mov       eax, edx
00482cdd: shl       eax, 2
00482ce0: sub       eax, edx
00482ce2: shl       eax, 5
00482ce5: mov       edx, dword ptr [eax + 0x51b664]
00482ceb: mov       eax, ebx
00482ced: call      0x4838d1
00482cf2: mov       eax, ebx
00482cf4: call      0x442025
00482cf9: and       eax, 0xff
00482cfe: test      byte ptr [eax*4 + 0x4989f9], 2
00482d06: je        0x482eb5
00482d0c: push      0
00482d0e: push      0
00482d10: push      0
00482d12: push      0
00482d14: mov       eax, ebx
00482d16: call      0x442045
00482d1b: mov       edx, 0x10
00482d20: and       eax, 0xff
00482d25: xor       ecx, ecx
00482d27: call      0x47d920
00482d2c: jmp       0x482eb5
00482d31: xor       ebx, ebx
00482d33: mov       bx, si
00482d36: mov       ecx, ebx
00482d38: shl       ecx, 4
00482d3b: add       ecx, ebx
00482d3d: shl       ecx, 2
00482d40: mov       eax, dword ptr [0x4e19a0]
00482d45: add       ecx, ebx
00482d47: mov       edx, ebx
00482d49: shl       ecx, 2
00482d4c: xor       edx, ebx
00482d4e: mov       dl, byte ptr [ecx + eax]
00482d51: mov       eax, edx
00482d53: shl       eax, 2
00482d56: sub       eax, edx
00482d58: shl       eax, 5
00482d5b: mov       edx, ebx
00482d5d: mov       eax, dword ptr [eax + 0x51b68c]
00482d63: call      0x4832b1
00482d68: mov       eax, dword ptr [0x4e19a0]
00482d6d: xor       edx, edx
00482d6f: mov       dl, byte ptr [ecx + eax]
00482d72: jmp       0x482cdb
00482d77: test      ecx, ecx
00482d79: je        0x482eb5
00482d7f: xor       eax, eax
00482d81: mov       al, byte ptr [ecx + 0x1b]
00482d84: cmp       eax, 0xff
00482d89: je        0x482eb5
00482d8f: mov       eax, dword ptr [eax*4 + 0x498e94]
00482d96: mov       eax, dword ptr [eax]
00482d98: mov       dword ptr [ebp - 0x14], eax
00482d9b: test      eax, eax
00482d9d: je        0x482eb5
00482da3: xor       eax, eax
00482da5: and       edx, 0xffff
00482dab: mov       ax, si
00482dae: call      dword ptr [ebp - 0x14]
00482db1: jmp       0x482eb5
00482db6: test      ecx, ecx
00482db8: je        0x482eb5
00482dbe: xor       eax, eax
00482dc0: mov       al, byte ptr [ecx + 0x1b]
00482dc3: cmp       eax, 0xff
00482dc8: je        0x482eb5
00482dce: mov       eax, dword ptr [eax*4 + 0x498e94]
00482dd5: mov       eax, dword ptr [eax + 0xc]
00482dd8: mov       dword ptr [ebp - 0xc], eax
00482ddb: test      eax, eax
00482ddd: je        0x482eb5
00482de3: xor       eax, eax
00482de5: and       edx, 0xffff
00482deb: mov       ax, si
00482dee: call      dword ptr [ebp - 0xc]
00482df1: jmp       0x482eb5
00482df6: test      ecx, ecx
00482df8: je        0x482eb5
00482dfe: xor       eax, eax
00482e00: mov       al, byte ptr [ecx + 0x1b]
00482e03: cmp       eax, 0xff
00482e08: je        0x482eb5
00482e0e: mov       eax, dword ptr [eax*4 + 0x498e94]
00482e15: mov       eax, dword ptr [eax + 8]
00482e18: mov       dword ptr [ebp - 0x18], eax
00482e1b: test      eax, eax
00482e1d: je        0x482eb5
00482e23: xor       eax, eax
00482e25: and       edx, 0xffff
00482e2b: mov       ax, si
00482e2e: call      dword ptr [ebp - 0x18]
00482e31: jmp       0x482eb5
00482e36: test      ecx, ecx
00482e38: je        0x482eb5
00482e3e: xor       eax, eax
00482e40: mov       al, byte ptr [ecx + 0x1b]
00482e43: cmp       eax, 0xff
00482e48: je        0x482e65
00482e4a: mov       eax, dword ptr [eax*4 + 0x498e94]
00482e51: mov       eax, dword ptr [eax + 4]
00482e54: mov       dword ptr [ebp - 8], eax
00482e57: test      eax, eax
00482e59: je        0x482e65
00482e5b: xor       eax, eax
00482e5d: xor       edx, edx
00482e5f: mov       ax, si
00482e62: call      dword ptr [ebp - 8]
00482e65: mov       eax, dword ptr [ecx + 0xc]
00482e68: cmp       eax, -1
00482e6b: je        0x482eb5
00482e6d: mov       ebx, 1
00482e72: mov       edx, eax
00482e74: mov       eax, dword ptr [ebp - 0x1c]
00482e77: call      0x488cea
00482e7c: jmp       0x482eb5
00482e7e: test      ecx, ecx
00482e80: je        0x482eb5
00482e82: xor       eax, eax
00482e84: mov       al, byte ptr [ecx + 0x1b]
00482e87: cmp       eax, 0xff
00482e8c: je        0x482eab
00482e8e: mov       eax, dword ptr [eax*4 + 0x498e94]
00482e95: mov       eax, dword ptr [eax + 0x10]
00482e98: mov       dword ptr [ebp - 0x10], eax
00482e9b: test      eax, eax
00482e9d: je        0x482eb5
00482e9f: xor       eax, eax
00482ea1: xor       edx, edx
00482ea3: mov       ax, si
00482ea6: call      dword ptr [ebp - 0x10]
00482ea9: jmp       0x482eb5
00482eab: xor       eax, eax
00482ead: mov       ax, si
00482eb0: call      0x453b84
00482eb5: mov       esp, ebp
00482eb7: pop       ebp
00482eb8: pop       edi
00482eb9: pop       esi
00482eba: pop       ecx
00482ebb: ret       

; MAJSympathie 0x475118..0x475267
00475118: push      ecx
00475119: push      esi
0047511a: push      edi
0047511b: push      ebp
0047511c: sub       esp, 0x10
0047511f: mov       ecx, eax
00475121: cmp       eax, edx
00475123: je        0x47525f
00475129: cmp       eax, 4
0047512c: jae       0x47525f
00475132: cmp       edx, 4
00475135: jae       0x47525f
0047513b: shl       eax, 4
0047513e: cmp       byte ptr [eax + 0x51a990], 0
00475145: jne       0x47525f
0047514b: mov       eax, edx
0047514d: shl       eax, 4
00475150: cmp       byte ptr [eax + 0x51a990], 0
00475157: jne       0x47525f
0047515d: mov       eax, ebx
0047515f: shl       eax, 4
00475162: mov       ebx, dword ptr [eax + 0x497290]
00475168: inc       ebx
00475169: mov       esi, dword ptr [eax + 0x497294]
0047516f: mov       dword ptr [eax + 0x497290], ebx
00475175: cmp       ebx, esi
00475177: jb        0x47525f
0047517d: xor       ebx, ebx
0047517f: xor       edi, edi
00475181: mov       bl, byte ptr [eax + 0x49728c]
00475187: mov       dword ptr [eax + 0x497290], edi
0047518d: cmp       ebx, 1
00475190: jne       0x47520c
00475196: mov       edi, eax
00475198: xor       esi, esi
0047519a: mov       ebp, 0x32
0047519f: jmp       0x4751ab
004751a1: inc       esi
004751a2: cmp       esi, 4
004751a5: jge       0x47525f
004751ab: xor       ecx, ecx
004751ad: jmp       0x4751d3
004751af: cmp       ebx, -0x32
004751b2: jge       0x4751b9
004751b4: mov       ebx, 0xffffffce
004751b9: movsx     ebx, bx
004751bc: xor       edx, edx
004751be: xor       eax, eax
004751c0: mov       dl, byte ptr [esp + 8]
004751c4: mov       al, byte ptr [esp + 0xc]
004751c8: call      0x46dc90
004751cd: inc       ecx
004751ce: cmp       ecx, 4
004751d1: jge       0x4751a1
004751d3: cmp       esi, ecx
004751d5: je        0x4751cd
004751d7: mov       dword ptr [esp + 0xc], esi
004751db: mov       dword ptr [esp + 8], ecx
004751df: mov       ebx, dword ptr [edi + 0x497288]
004751e5: cmp       esi, 4
004751e8: jae       0x4751cd
004751ea: cmp       ecx, 4
004751ed: jae       0x4751cd
004751ef: xor       edx, edx
004751f1: xor       eax, eax
004751f3: mov       dl, byte ptr [esp + 8]
004751f7: mov       al, byte ptr [esp + 0xc]
004751fb: call      0x46dc6c
00475200: cwde      
00475201: add       ebx, eax
00475203: cmp       ebx, 0x32
00475206: jle       0x4751af
00475208: mov       ebx, ebp
0047520a: jmp       0x4751b9
0047520c: mov       dword ptr [esp + 4], ecx
00475210: mov       dword ptr [esp], edx
00475213: mov       ebx, dword ptr [eax + 0x497288]
00475219: cmp       ecx, 4
0047521c: jae       0x47525f
0047521e: cmp       edx, 4
00475221: jae       0x47525f
00475223: xor       edx, edx
00475225: xor       eax, eax
00475227: mov       dl, byte ptr [esp]
0047522a: mov       al, byte ptr [esp + 4]
0047522e: call      0x46dc6c
00475233: cwde      
00475234: add       ebx, eax
00475236: cmp       ebx, 0x32
00475239: jle       0x475242
0047523b: mov       ebx, 0x32
00475240: jmp       0x47524c
00475242: cmp       ebx, -0x32
00475245: jge       0x47524c
00475247: mov       ebx, 0xffffffce
0047524c: movsx     ebx, bx
0047524f: xor       edx, edx
00475251: xor       eax, eax
00475253: mov       dl, byte ptr [esp]
00475256: mov       al, byte ptr [esp + 4]
0047525a: call      0x46dc90
0047525f: add       esp, 0x10
00475262: pop       ebp
00475263: pop       edi
00475264: pop       esi
00475265: pop       ecx
00475266: ret       

; PlayerResetAllie 0x46d8cb..0x46d927
0046d8cb: push      ebx
0046d8cc: push      ecx
0046d8cd: mov       bl, al
0046d8cf: cmp       al, dl
0046d8d1: je        0x46d924
0046d8d3: xor       eax, eax
0046d8d5: mov       al, bl
0046d8d7: cmp       eax, 4
0046d8da: jg        0x46d924
0046d8dc: xor       ecx, ecx
0046d8de: mov       cl, dl
0046d8e0: cmp       ecx, 4
0046d8e3: jg        0x46d924
0046d8e5: mov       bh, 1
0046d8e7: shl       bh, cl
0046d8e9: mov       ecx, eax
0046d8eb: shl       eax, 2
0046d8ee: add       eax, ecx
0046d8f0: mov       ecx, dword ptr [0x5080a8]
0046d8f6: mov       dh, byte ptr [ecx + eax*4 + 6]
0046d8fa: not       dh
0046d8fc: or        dh, bh
0046d8fe: not       dh
0046d900: mov       byte ptr [ecx + eax*4 + 6], dh
0046d904: cmp       bl, byte ptr [0x508041]
0046d90a: jne       0x46d924
0046d90c: xor       ah, ah
0046d90e: mov       al, dl
0046d910: add       eax, 0x192
0046d915: xor       edx, edx
0046d917: mov       dx, ax
0046d91a: mov       eax, 0xa
0046d91f: call      0x46994b
0046d924: pop       ecx
0046d925: pop       ebx
0046d926: ret       

; PlayerAAttaqueSet 0x46d600..0x46d628
0046d600: push      ebx
0046d601: and       eax, 0xff
0046d606: cmp       eax, 4
0046d609: jge       0x46d627
0046d60b: xor       ebx, ebx
0046d60d: mov       bl, dl
0046d60f: cmp       ebx, 4
0046d612: jge       0x46d627
0046d614: mov       edx, eax
0046d616: shl       eax, 2
0046d619: add       edx, eax
0046d61b: shl       edx, 2
0046d61e: mov       eax, ebx
0046d620: inc       dword ptr [edx + eax*4 + 0x508044]
0046d627: pop       ebx

; MessageBoxSet 0x46994b..0x469b85
0046994b: push      ebx
0046994c: push      ecx
0046994d: push      esi
0046994e: push      edi
0046994f: sub       esp, 8
00469952: mov       cl, al
00469954: mov       eax, edx
00469956: cmp       byte ptr [0x507d58], 0
0046995d: jne       0x469b7d
00469963: xor       edx, edx
00469965: mov       dx, word ptr [0x507d56]
0046996c: mov       ebx, edx
0046996e: shl       ebx, 6
00469971: add       ebx, edx
00469973: shl       ebx, 2
00469976: sub       ebx, edx
00469978: mov       byte ptr [ebx*2 + 0x4e7754], cl
0046997f: mov       word ptr [ebx*2 + 0x4e7756], ax
00469987: xor       ebx, ebx
00469989: mov       bx, ax
0046998c: mov       ecx, 0x64
00469991: mov       edx, ebx
00469993: mov       eax, ebx
00469995: sar       edx, 0x1f
00469998: idiv      ecx
0046999a: mov       ecx, 0xa
0046999f: mov       esi, eax
004699a1: mov       edx, ebx
004699a3: mov       eax, ebx
004699a5: sar       edx, 0x1f
004699a8: idiv      ecx
004699aa: mov       edi, 0xa
004699af: mov       ecx, eax
004699b1: mov       edx, ebx
004699b3: mov       eax, ebx
004699b5: sar       edx, 0x1f
004699b8: idiv      edi
004699ba: add       edx, 0x30
004699bd: cmp       ebx, 0x3e8
004699c3: jl        0x469a1b
004699c5: mov       byte ptr [esp + 3], dl
004699c9: mov       eax, ecx
004699cb: xor       edx, edx
004699cd: mov       dx, ax
004699d0: mov       eax, edx
004699d2: sar       edx, 0x1f
004699d5: idiv      edi
004699d7: add       edx, 0x30
004699da: mov       eax, esi
004699dc: mov       byte ptr [esp + 2], dl
004699e0: xor       edx, edx
004699e2: mov       dx, ax
004699e5: mov       eax, edx
004699e7: sar       edx, 0x1f
004699ea: idiv      edi
004699ec: add       edx, 0x30
004699ef: mov       ecx, 0x3e8
004699f4: mov       byte ptr [esp + 1], dl
004699f8: mov       edx, ebx
004699fa: mov       eax, ebx
004699fc: sar       edx, 0x1f
004699ff: idiv      ecx
00469a01: xor       edx, edx
00469a03: mov       dx, ax
00469a06: mov       eax, edx
00469a08: sar       edx, 0x1f
00469a0b: idiv      edi
00469a0d: xor       bl, bl
00469a0f: add       edx, 0x30
00469a12: mov       byte ptr [esp + 4], bl
00469a16: mov       byte ptr [esp], dl
00469a19: jmp       0x469a4e
00469a1b: mov       byte ptr [esp + 2], dl
00469a1f: mov       eax, ecx
00469a21: xor       edx, edx
00469a23: mov       dx, ax
00469a26: mov       eax, edx
00469a28: sar       edx, 0x1f
00469a2b: idiv      edi
00469a2d: add       edx, 0x30
00469a30: mov       eax, esi
00469a32: mov       byte ptr [esp + 1], dl
00469a36: xor       edx, edx
00469a38: mov       dx, ax
00469a3b: mov       eax, edx
00469a3d: sar       edx, 0x1f
00469a40: idiv      edi
00469a42: add       edx, 0x30
00469a45: mov       byte ptr [esp], dl
00469a48: xor       dh, dh
00469a4a: mov       byte ptr [esp + 3], dh
00469a4e: xor       edx, edx
00469a50: mov       dx, word ptr [0x507d56]
00469a57: mov       ebx, edx
00469a59: shl       ebx, 6
00469a5c: add       ebx, edx
00469a5e: shl       ebx, 2
00469a61: sub       ebx, edx
00469a63: add       ebx, ebx
00469a65: push      0x509094
00469a6a: add       ebx, 0x4e7754
00469a70: push      0xfa
00469a75: add       ebx, 0x106
00469a7b: push      ebx
00469a7c: push      0x494aec
00469a81: lea       eax, [esp + 0x10]
00469a85: push      eax
00469a86: push      0x494aed
00469a8b: call      dword ptr cs:[0x5231b0]
00469a92: xor       edx, edx
00469a94: mov       dx, word ptr [0x507d56]
00469a9b: mov       ebx, edx
00469a9d: shl       ebx, 6
00469aa0: add       ebx, edx
00469aa2: shl       ebx, 2
00469aa5: sub       ebx, edx
00469aa7: add       ebx, ebx
00469aa9: push      0x509094
00469aae: add       ebx, 0x4e7754
00469ab4: push      0xfa
00469ab9: add       ebx, 4
00469abc: push      ebx
00469abd: push      0x494af7
00469ac2: lea       eax, [esp + 0x10]
00469ac6: push      eax
00469ac7: push      0x494af8
00469acc: call      dword ptr cs:[0x5231b0]
00469ad3: xor       edx, edx
00469ad5: mov       dx, word ptr [0x507d56]
00469adc: mov       ebx, edx
00469ade: shl       ebx, 6
00469ae1: add       ebx, edx
00469ae3: shl       ebx, 2
00469ae6: sub       ebx, edx
00469ae8: add       ebx, ebx
00469aea: add       ebx, 0x4e7754
00469af0: mov       dl, 0x2a
00469af2: mov       ecx, ebx
00469af4: lea       esi, [ebx + 4]
00469af7: mov       al, byte ptr [esi]
00469af9: cmp       al, dl
00469afb: je        0x469b0f
00469afd: cmp       al, 0
00469aff: je        0x469b0d
00469b01: inc       esi
00469b02: mov       al, byte ptr [esi]
00469b04: cmp       al, dl
00469b06: je        0x469b0f
00469b08: inc       esi
00469b09: cmp       al, 0
00469b0b: jne       0x469af7
00469b0d: sub       esi, esi
00469b0f: mov       eax, esi
00469b11: test      esi, esi
00469b13: je        0x469b2d
00469b15: mov       edx, esi
00469b17: mov       eax, ebx
00469b19: inc       edx
00469b1a: add       eax, 4
00469b1f: sub       edx, eax
00469b21: mov       word ptr [ebx + 0x102], dx
00469b28: mov       byte ptr [esi], 0
00469b2b: jmp       0x469b36
00469b2d: mov       word ptr [ebx + 0x102], 0xffff
00469b36: xor       eax, eax
00469b38: mov       ax, word ptr [0x507d56]
00469b3e: mov       ebx, eax
00469b40: shl       ebx, 6
00469b43: add       ebx, eax
00469b45: shl       ebx, 2
00469b48: sub       ebx, eax
00469b4a: mov       word ptr [ebx*2 + 0x4e7858], 0x190
00469b54: lea       edx, [eax + 1]
00469b57: mov       ebx, 0x100
00469b5c: mov       eax, edx
00469b5e: sar       edx, 0x1f
00469b61: idiv      ebx
00469b63: mov       bx, word ptr [0x507d54]
00469b6a: mov       word ptr [0x507d56], dx
00469b71: cmp       dx, bx
00469b74: jne       0x469b7d
00469b76: mov       byte ptr [0x507d58], 1
00469b7d: add       esp, 8
00469b80: pop       edi
00469b81: pop       esi
00469b82: pop       ecx
00469b83: pop       ebx
00469b84: ret       

; SetDyingEngin 0x444938..0x444dad
00444938: push      ebx
00444939: push      ecx
0044493a: push      edx
0044493b: push      esi
0044493c: push      edi
0044493d: push      ebp
0044493e: mov       edi, eax
00444940: xor       edx, edx
00444942: mov       dx, ax
00444945: mov       eax, edx
00444947: shl       eax, 4
0044494a: add       eax, edx
0044494c: shl       eax, 2
0044494f: add       eax, edx
00444951: mov       esi, dword ptr [0x4e19a0]
00444957: shl       eax, 2
0044495a: add       esi, eax
0044495c: xor       eax, eax
0044495e: mov       al, byte ptr [esi + 2]
00444961: test      eax, eax
00444963: je        0x44496e
00444965: cmp       eax, 4
00444968: je        0x44496e
0044496a: mov       al, 1
0044496c: jmp       0x444970
0044496e: xor       al, al
00444970: test      al, al
00444972: je        0x444c47
00444978: xor       ecx, ecx
0044497a: mov       cx, di
0044497d: mov       ebp, ecx
0044497f: shl       ebp, 4
00444982: add       ebp, ecx
00444984: shl       ebp, 2
00444987: add       ebp, ecx
00444989: mov       eax, dword ptr [0x4e19a0]
0044498e: shl       ebp, 2
00444991: mov       al, byte ptr [eax + ebp + 0xdc]
00444998: mov       edx, 2
0044499d: and       eax, 0xff
004449a2: call      0x467d97
004449a7: test      al, al
004449a9: jne       0x444c47
004449af: mov       edx, 0x44
004449b4: mov       eax, ecx
004449b6: xor       ebx, ebx
004449b8: call      0x4829c8
004449bd: lea       eax, [esi + 0x104]
004449c3: call      0x48aac0
004449c8: mov       ebx, dword ptr [0x4e19a0]
004449ce: xor       edx, edx
004449d0: add       ebx, ebp
004449d2: xor       eax, eax
004449d4: mov       dl, byte ptr [0x508041]
004449da: mov       ax, word ptr [ebx + 8]
004449de: call      0x4766f0
004449e3: test      al, al
004449e5: je        0x444a20
004449e7: mov       eax, ecx
004449e9: call      0x440c5d
004449ee: mov       edx, dword ptr [ebx + 0x104]
004449f4: mov       byte ptr [ebx + 0xf9], 0
004449fb: cmp       edx, -1
004449fe: jne       0x444a20
00444a00: push      eax
00444a01: xor       edx, edx
00444a03: xor       ecx, ecx
00444a05: mov       dl, byte ptr [ebx + 1]
00444a08: lea       eax, [ebx + 0x104]
00444a0e: shl       edx, 0x10
00444a11: mov       ebx, eax
00444a13: mov       eax, 0x50
00444a18: or        dh, 5
00444a1b: call      0x48aa79
00444a20: xor       edx, edx
00444a22: mov       dx, di
00444a25: mov       eax, edx
00444a27: shl       eax, 4
00444a2a: add       eax, edx
00444a2c: shl       eax, 2
00444a2f: add       eax, edx
00444a31: mov       edx, dword ptr [0x4e19a0]
00444a37: mov       cl, 4
00444a39: mov       ebx, edi
00444a3b: mov       al, byte ptr [edx + eax*4 + 2]
00444a3f: and       eax, 0xff
00444a44: je        0x444a4f
00444a46: cmp       eax, 4
00444a49: je        0x444a4f
00444a4b: mov       al, 1
00444a4d: jmp       0x444a51
00444a4f: xor       al, al
00444a51: test      al, al
00444a53: je        0x444a9d
00444a55: xor       edx, edx
00444a57: mov       dx, bx
00444a5a: mov       eax, edx
00444a5c: shl       eax, 4
00444a5f: add       eax, edx
00444a61: shl       eax, 2
00444a64: add       edx, eax
00444a66: mov       eax, dword ptr [0x4e19a0]
00444a6b: shl       edx, 2
00444a6e: mov       byte ptr [edx + eax + 2], cl
00444a72: cmp       bx, word ptr [0x496304]
00444a79: jne       0x444a9d
00444a7b: xor       ah, ah
00444a7d: xor       ebx, ebx
00444a7f: mov       byte ptr [0x4e0f36], ah
00444a85: mov       dword ptr [0x4e0f3c], ebx
00444a8b: mov       ebx, 0xffff
00444a90: mov       byte ptr [0x4e0f37], ah
00444a96: mov       word ptr [0x496304], bx
00444a9d: xor       edx, edx
00444a9f: mov       dx, di
00444aa2: mov       eax, edx
00444aa4: shl       eax, 4
00444aa7: add       eax, edx
00444aa9: shl       eax, 2
00444aac: add       eax, edx
00444aae: mov       edx, dword ptr [0x4e19a0]
00444ab4: shl       eax, 2
00444ab7: add       eax, edx
00444ab9: mov       ecx, edi
00444abb: lea       ebx, [eax + 0xa]
00444abe: mov       ax, word ptr [ebx]
00444ac1: and       eax, 0xffff
00444ac6: je        0x444ad6
00444ac8: xor       eax, eax
00444aca: xor       edx, edx
00444acc: mov       ax, cx
00444acf: call      0x443dfc
00444ad4: jmp       0x444abe
00444ad6: xor       edx, edx
00444ad8: mov       dx, di
00444adb: mov       eax, edx
00444add: shl       eax, 4
00444ae0: add       eax, edx
00444ae2: shl       eax, 2
00444ae5: add       eax, edx
00444ae7: mov       edx, dword ptr [0x4e19a0]
00444aed: mov       cl, 4
00444aef: mov       ebx, edi
00444af1: mov       al, byte ptr [edx + eax*4 + 2]
00444af5: and       eax, 0xff
00444afa: je        0x444b05
00444afc: cmp       eax, 4
00444aff: je        0x444b05
00444b01: mov       al, 1
00444b03: jmp       0x444b07
00444b05: xor       al, al
00444b07: test      al, al
00444b09: je        0x444b58
00444b0b: xor       edx, edx
00444b0d: mov       dx, bx
00444b10: mov       eax, edx
00444b12: shl       eax, 4
00444b15: add       eax, edx
00444b17: shl       eax, 2
00444b1a: add       edx, eax
00444b1c: mov       eax, dword ptr [0x4e19a0]
00444b21: shl       edx, 2
00444b24: mov       byte ptr [edx + eax + 2], cl
00444b28: mov       dx, word ptr [0x496304]
00444b2f: cmp       bx, dx
00444b32: jne       0x444b58
00444b34: xor       bh, dh
00444b36: xor       cl, cl
00444b38: xor       ebp, ebp
00444b3a: mov       byte ptr [0x4e0f36], bh
00444b40: mov       byte ptr [0x4e0f37], cl
00444b46: mov       ebx, 0xffff
00444b4b: mov       dword ptr [0x4e0f3c], ebp
00444b51: mov       word ptr [0x496304], bx
00444b58: xor       ebx, ebx
00444b5a: mov       byte ptr [esi + 0xa4], 0
00444b61: mov       bx, di
00444b64: mov       word ptr [esi + 0xc2], 0
00444b6d: mov       eax, ebx
00444b6f: xor       edx, edx
00444b71: call      0x472648
00444b76: mov       eax, ebx
00444b78: mov       dx, word ptr [esi + 8]
00444b7c: call      0x442eac
00444b81: mov       ax, word ptr [esi + 8]
00444b85: mov       cx, word ptr [esi + 0x7c]
00444b89: cmp       ax, cx
00444b8c: je        0x444b9a
00444b8e: xor       edx, edx
00444b90: mov       eax, ebx
00444b92: mov       dx, cx
00444b95: call      0x442eac
00444b9a: xor       edx, edx
00444b9c: mov       dx, di
00444b9f: mov       eax, edx
00444ba1: shl       eax, 4
00444ba4: add       eax, edx
00444ba6: shl       eax, 2
00444ba9: add       edx, eax
00444bab: mov       eax, dword ptr [0x4e19a0]
00444bb0: shl       edx, 2
00444bb3: mov       al, byte ptr [edx + eax + 1]
00444bb7: sub       al, 0xb
00444bb9: cmp       al, 6
00444bbb: ja        0x444bce
00444bbd: and       eax, 0xff
00444bc2: jmp       dword ptr cs:[eax*4 + 0x44491c]
00444bca: mov       al, 1
00444bcc: jmp       0x444bd0
00444bce: xor       al, al
00444bd0: test      al, al
00444bd2: je        0x44f29d
00444bd8: xor       eax, eax
00444bda: mov       al, byte ptr [esi + 1]
00444bdd: cmp       eax, 0x10
00444be0: je        0x444c1f
00444be2: mov       eax, 0x41
00444be7: call      0x4704dc
00444bec: test      al, 1
00444bee: jne       0x444c0e
00444bf0: push      0
00444bf2: push      -0x20
00444bf4: push      -0x20
00444bf6: xor       edx, edx
00444bf8: push      0
00444bfa: mov       eax, 0x12
00444bff: mov       dx, word ptr [esi + 8]
00444c03: push      0
00444c05: xor       ecx, ecx
00444c07: mov       ebx, edx
00444c09: jmp       0x444da3
00444c0e: push      0
00444c10: push      -0x20
00444c12: push      -0x20
00444c14: xor       edx, edx
00444c16: push      0
00444c18: mov       eax, 0x13
00444c1d: jmp       0x444bff
00444c1f: xor       eax, eax
00444c21: mov       al, byte ptr [esi + 0xab]
00444c27: neg       eax
00444c29: push      0
00444c2b: cwde      
00444c2c: push      eax
00444c2d: push      0
00444c2f: xor       edx, edx
00444c31: push      0
00444c33: xor       ecx, ecx
00444c35: mov       dx, word ptr [esi + 8]
00444c39: push      0
00444c3b: mov       ebx, edx
00444c3d: mov       eax, 0x22
00444c42: jmp       0x444da3
00444c47: xor       ebx, ebx
00444c49: mov       bx, di
00444c4c: mov       ecx, ebx
00444c4e: shl       ecx, 4
00444c51: add       ecx, ebx
00444c53: shl       ecx, 2
00444c56: add       ecx, ebx
00444c58: mov       eax, dword ptr [0x4e19a0]
00444c5d: shl       ecx, 2
00444c60: mov       al, byte ptr [ecx + eax + 0xdc]
00444c67: mov       edx, 2
00444c6c: and       eax, 0xff
00444c71: call      0x467d97
00444c76: test      al, al
00444c78: je        0x44f29d
00444c7e: lea       eax, [esi + 0x104]
00444c84: call      0x48aac0
00444c89: mov       eax, dword ptr [0x4e19a0]
00444c8e: mov       cl, byte ptr [ecx + eax + 0x72]
00444c92: mov       eax, ebx
00444c94: xor       edx, edx
00444c96: call      0x472648
00444c9b: mov       eax, ebx
00444c9d: mov       dx, word ptr [esi + 8]
00444ca1: call      0x442eac
00444ca6: mov       ax, word ptr [esi + 8]
00444caa: cmp       ax, word ptr [esi + 0x7c]
00444cae: je        0x444cbd
00444cb0: xor       edx, edx
00444cb2: mov       eax, ebx
00444cb4: mov       dx, word ptr [esi + 0x7c]
00444cb8: call      0x442eac
00444cbd: xor       edx, edx
00444cbf: mov       dx, di
00444cc2: mov       eax, edx
00444cc4: shl       eax, 4
00444cc7: add       eax, edx
00444cc9: shl       eax, 2
00444ccc: mov       ebx, edi
00444cce: add       edx, eax
00444cd0: mov       eax, dword ptr [0x4e19a0]
00444cd5: shl       edx, 2
00444cd8: xor       ch, ch
00444cda: mov       al, byte ptr [edx + eax + 2]
00444cde: and       eax, 0xff
00444ce3: je        0x444cee
00444ce5: cmp       eax, 4
00444ce8: je        0x444cee
00444cea: mov       al, 1
00444cec: jmp       0x444cf0
00444cee: xor       al, al
00444cf0: test      al, al
00444cf2: je        0x444d3b
00444cf4: xor       edx, edx
00444cf6: mov       dx, bx
00444cf9: mov       eax, edx
00444cfb: shl       eax, 4
00444cfe: add       eax, edx
00444d00: shl       eax, 2
00444d03: add       edx, eax
00444d05: mov       eax, dword ptr [0x4e19a0]
00444d0a: shl       edx, 2
00444d0d: mov       byte ptr [edx + eax + 2], ch
00444d11: cmp       bx, word ptr [0x496304]
00444d18: jne       0x444d3b
00444d1a: mov       eax, 0xffff
00444d1f: xor       dh, dh
00444d21: xor       edi, edi
00444d23: mov       byte ptr [0x4e0f36], dh
00444d29: mov       byte ptr [0x4e0f37], dh
00444d2f: mov       dword ptr [0x4e0f3c], edi
00444d35: mov       word ptr [0x496304], ax
00444d3b: test      cl, cl
00444d3d: je        0x44f29d
00444d43: mov       edx, 5
00444d48: xor       ebx, ebx
00444d4a: xor       eax, eax
00444d4c: mov       bx, word ptr [esi + 8]
00444d50: mov       al, byte ptr [esi]
00444d52: call      0x46a388
00444d57: xor       ebx, ebx
00444d59: mov       bl, byte ptr [esi]
00444d5b: cmp       ebx, 0xc8
00444d61: je        0x444d8a
00444d63: cmp       ebx, 4
00444d66: je        0x444d8a
00444d68: xor       dh, dh
00444d6a: xor       ah, ah
00444d6c: mov       dl, byte ptr [esi + 0xbb]
00444d72: mov       al, byte ptr [esi + 0xf5]
00444d78: add       eax, edx
00444d7a: xor       edx, edx
00444d7c: mov       dx, ax
00444d7f: xor       eax, eax
00444d81: mov       ax, word ptr [esi + 8]
00444d85: call      0x476e82
00444d8a: push      0
00444d8c: push      0
00444d8e: push      0
00444d90: xor       edx, edx
00444d92: push      0
00444d94: mov       eax, 0x1f
00444d99: mov       dx, word ptr [esi + 8]
00444d9d: push      0
00444d9f: xor       ecx, ecx
00444da1: mov       ebx, edx
00444da3: call      0x46e44c
00444da8: jmp       0x44f29d

; EnginSetLevelExperience 0x44fb20..0x44fd4b
0044fb20: push      ebx
0044fb21: push      ecx
0044fb22: push      esi
0044fb23: push      edi
0044fb24: sub       esp, 4
0044fb27: xor       esi, esi
0044fb29: mov       si, ax
0044fb2c: mov       ebx, esi
0044fb2e: shl       ebx, 4
0044fb31: add       ebx, esi
0044fb33: shl       ebx, 2
0044fb36: xor       eax, eax
0044fb38: lea       ecx, [esi + ebx]
0044fb3b: mov       ebx, dword ptr [0x4e19a0]
0044fb41: shl       ecx, 2
0044fb44: mov       al, dl
0044fb46: add       ebx, ecx
0044fb48: cmp       eax, 5
0044fb4b: jl        0x44fd21
0044fb51: jmp       0x44507b
0044fb56: mov       eax, dword ptr [0x4e19a0]
0044fb5b: mov       al, byte ptr [ecx + eax + 1]
0044fb5f: mov       cl, al
0044fb61: cmp       al, 0xf
0044fb63: jb        0x44fb85
0044fb65: jbe       0x44fb81
0044fb67: cmp       al, 0x14
0044fb69: jb        0x44fb79
0044fb6b: cmp       al, 0x16
0044fb6d: jbe       0x44fb81
0044fb6f: cmp       al, 0x18
0044fb71: jbe       0x44fb81
0044fb73: cmp       al, 0x19
0044fb75: je        0x44fb81
0044fb77: jmp       0x44fb99
0044fb79: cmp       al, 0x10
0044fb7b: jbe       0x44fb81
0044fb7d: cmp       al, 0x12
0044fb7f: jb        0x44fb99
0044fb81: mov       al, 1
0044fb83: jmp       0x44fb9b
0044fb85: cmp       al, 3
0044fb87: jb        0x44fb81
0044fb89: jbe       0x44fb81
0044fb8b: cmp       al, 8
0044fb8d: jb        0x44fb99
0044fb8f: jbe       0x44fb81
0044fb91: cmp       al, 0xb
0044fb93: jb        0x44fb99
0044fb95: cmp       al, 0xc
0044fb97: jbe       0x44fb81
0044fb99: xor       al, al
0044fb9b: test      al, al
0044fb9d: je        0x44fbab
0044fb9f: mov       byte ptr [ebx + 0xf7], 1
0044fba6: jmp       0x44507b
0044fbab: xor       edx, edx
0044fbad: mov       dl, byte ptr [ebx + 1]
0044fbb0: mov       ecx, edx
0044fbb2: shl       ecx, 2
0044fbb5: sub       ecx, edx
0044fbb7: shl       ecx, 3
0044fbba: add       ecx, edx
0044fbbc: xor       edx, edx
0044fbbe: mov       dx, word ptr [ecx*2 + 0x4965dc]
0044fbc6: mov       ecx, 0x64
0044fbcb: mov       eax, edx
0044fbcd: sar       edx, 0x1f
0044fbd0: idiv      ecx
0044fbd2: mov       byte ptr [ebx + 0xf8], al
0044fbd8: jmp       0x44507b
0044fbdd: mov       byte ptr [ebx + 0xf6], 1
0044fbe4: jmp       0x44507b
0044fbe9: cmp       byte ptr [ebx + 0x72], 0
0044fbed: je        0x44fc9d
0044fbf3: mov       eax, esi
0044fbf5: call      0x457058
0044fbfa: mov       byte ptr [ebx + 0xf5], 1
0044fc01: mov       ebx, dword ptr [0x4e19a0]
0044fc07: xor       edx, edx
0044fc09: mov       ax, word ptr [ecx + ebx + 8]
0044fc0e: mov       dx, ax
0044fc11: mov       eax, esi
0044fc13: call      0x442cb4
0044fc18: mov       byte ptr [ecx + ebx + 0x72], 1
0044fc1d: mov       eax, dword ptr [0x4e19a0]
0044fc22: add       ecx, eax
0044fc24: xor       ebx, ebx
0044fc26: mov       bl, byte ptr [ecx]
0044fc28: mov       di, word ptr [ecx + 8]
0044fc2c: cmp       ebx, 0xc8
0044fc32: je        0x44fc85
0044fc34: cmp       ebx, 4
0044fc37: je        0x44fc85
0044fc39: xor       dh, dh
0044fc3b: xor       ah, ah
0044fc3d: mov       dl, byte ptr [ecx + 0xbb]
0044fc43: mov       al, byte ptr [ecx + 0xf5]
0044fc49: add       edx, 2
0044fc4c: xor       esi, esi
0044fc4e: add       eax, edx
0044fc50: xor       edx, edx
0044fc52: mov       si, di
0044fc55: mov       dx, ax
0044fc58: mov       eax, esi
0044fc5a: call      0x476851
0044fc5f: xor       ah, ah
0044fc61: mov       al, byte ptr [ecx + 0xbb]
0044fc67: mov       dword ptr [esp], eax
0044fc6a: mov       edx, dword ptr [esp]
0044fc6d: mov       al, byte ptr [ecx + 0xf5]
0044fc73: xor       ebx, ebx
0044fc75: add       eax, edx
0044fc77: xor       edx, edx
0044fc79: mov       bl, byte ptr [ecx]
0044fc7b: mov       dx, ax
0044fc7e: mov       eax, esi
0044fc80: call      0x476cb3
0044fc85: mov       edx, 4
0044fc8a: xor       ebx, ebx
0044fc8c: xor       eax, eax
0044fc8e: mov       bx, di
0044fc91: mov       al, byte ptr [ecx]
0044fc93: call      0x46a388
0044fc98: jmp       0x44507b
0044fc9d: mov       byte ptr [ebx + 0xf5], 1
0044fca4: jmp       0x44507b
0044fca9: mov       eax, dword ptr [0x4e19a0]
0044fcae: mov       cl, byte ptr [ecx + eax + 1]
0044fcb2: cmp       cl, 0xf
0044fcb5: jb        0x44fcdd
0044fcb7: jbe       0x44fcd9
0044fcb9: cmp       cl, 0x14
0044fcbc: jb        0x44fccf
0044fcbe: cmp       cl, 0x16
0044fcc1: jbe       0x44fcd9
0044fcc3: cmp       cl, 0x18
0044fcc6: jbe       0x44fcd9
0044fcc8: cmp       cl, 0x19
0044fccb: je        0x44fcd9
0044fccd: jmp       0x44fcf5
0044fccf: cmp       cl, 0x10
0044fcd2: jbe       0x44fcd9
0044fcd4: cmp       cl, 0x12
0044fcd7: jb        0x44fcf5
0044fcd9: mov       al, 1
0044fcdb: jmp       0x44fcf7
0044fcdd: cmp       cl, 3
0044fce0: jb        0x44fcd9
0044fce2: jbe       0x44fcd9
0044fce4: cmp       cl, 8
0044fce7: jb        0x44fcf5
0044fce9: jbe       0x44fcd9
0044fceb: cmp       cl, 0xb
0044fcee: jb        0x44fcf5
0044fcf0: cmp       cl, 0xc
0044fcf3: jbe       0x44fcd9
0044fcf5: xor       al, al
0044fcf7: test      al, al
0044fcf9: jne       0x44fbab
0044fcff: xor       edx, edx
0044fd01: mov       dl, byte ptr [ebx + 1]
0044fd04: mov       ecx, edx
0044fd06: shl       ecx, 2
0044fd09: sub       ecx, edx
0044fd0b: shl       ecx, 3
0044fd0e: add       ecx, edx
0044fd10: xor       edx, edx
0044fd12: mov       dx, word ptr [ecx*2 + 0x4965dc]
0044fd1a: add       edx, edx
0044fd1c: jmp       0x44fbc6
0044fd21: mov       al, byte ptr [ebx + 0xaf]
0044fd27: and       al, 0x1f
0044fd29: mov       ah, dl
0044fd2b: shl       ah, 5
0044fd2e: or        al, ah
0044fd30: mov       byte ptr [ebx + 0xaf], al
0044fd36: cmp       dl, 4
0044fd39: ja        0x44507b
0044fd3f: xor       eax, eax
0044fd41: mov       al, dl
0044fd43: jmp       dword ptr cs:[eax*4 + 0x44fb0c]

; EnginNextEtape 0x45442c..0x456c34
0045442c: push      ebx
0045442d: push      ecx
0045442e: push      edx
0045442f: push      esi
00454430: push      edi
00454431: push      ebp
00454432: sub       esp, 0x64
00454435: mov       edi, eax
00454437: xor       ebx, ebx
00454439: mov       bx, ax
0045443c: mov       eax, ebx
0045443e: shl       eax, 4
00454441: add       eax, ebx
00454443: shl       eax, 2
00454446: add       eax, ebx
00454448: mov       esi, dword ptr [0x4e19a0]
0045444e: shl       eax, 2
00454451: add       esi, eax
00454453: xor       eax, eax
00454455: mov       al, byte ptr [esi + 2]
00454458: test      eax, eax
0045445a: setne     al
0045445d: test      al, al
0045445f: je        0x454498
00454461: mov       al, byte ptr [esi]
00454463: mov       byte ptr [esp + 0x58], al
00454467: mov       al, byte ptr [esi + 1]
0045446a: mov       edx, dword ptr [esi + 0x104]
00454470: mov       byte ptr [esp + 0x60], al
00454474: cmp       edx, -1
00454477: je        0x454491
00454479: mov       eax, ebx
0045447b: call      0x440c5d
00454480: lea       ebx, [esi + 0x104]
00454486: mov       edx, eax
00454488: mov       eax, ebx
0045448a: call      0x48aacf
0045448f: jmp       0x454498
00454491: mov       byte ptr [esi + 0xf9], 0
00454498: xor       edx, edx
0045449a: mov       dx, di
0045449d: mov       eax, edx
0045449f: shl       eax, 4
004544a2: add       eax, edx
004544a4: shl       eax, 2
004544a7: add       eax, edx
004544a9: mov       edx, dword ptr [0x4e19a0]
004544af: mov       al, byte ptr [edx + eax*4 + 2]
004544b3: and       eax, 0xff
004544b8: je        0x4544c3
004544ba: cmp       eax, 4
004544bd: je        0x4544c3
004544bf: mov       al, 1
004544c1: jmp       0x4544c5
004544c3: xor       al, al
004544c5: test      al, al
004544c7: je        0x456c1c
004544cd: xor       eax, eax
004544cf: mov       al, byte ptr [esi + 1]
004544d2: cmp       eax, 0x10
004544d5: jne       0x454530
004544d7: xor       edx, edx
004544d9: mov       dx, di
004544dc: mov       eax, edx
004544de: shl       eax, 4
004544e1: add       eax, edx
004544e3: shl       eax, 2
004544e6: add       eax, edx
004544e8: mov       ebx, dword ptr [0x4e19a0]
004544ee: shl       eax, 2
004544f1: add       ebx, eax
004544f3: mov       ah, byte ptr [ebx + 0xa9]
004544f9: inc       ah
004544fb: mov       dl, byte ptr [ebx + 0xa7]
00454501: mov       byte ptr [ebx + 0xa9], ah
00454507: cmp       ah, dl
00454509: jne       0x454530
0045450b: xor       edx, edx
0045450d: mov       dl, byte ptr [ebx + 0xa4]
00454513: xor       ecx, ecx
00454515: inc       edx
00454516: mov       cl, byte ptr [ebx + 0xa5]
0045451c: mov       eax, edx
0045451e: sar       edx, 0x1f
00454521: idiv      ecx
00454523: mov       byte ptr [ebx + 0xa9], 0
0045452a: mov       byte ptr [ebx + 0xa4], dl
00454530: xor       edx, edx
00454532: mov       dx, di
00454535: mov       eax, edx
00454537: shl       eax, 4
0045453a: add       eax, edx
0045453c: shl       eax, 2
0045453f: add       eax, edx
00454541: mov       ecx, dword ptr [0x4e19a0]
00454547: shl       eax, 2
0045454a: add       ecx, eax
0045454c: xor       ebx, ebx
0045454e: mov       bl, byte ptr [ecx + 1]
00454551: mov       eax, ebx
00454553: shl       eax, 2
00454556: sub       eax, ebx
00454558: shl       eax, 3
0045455b: add       eax, ebx
0045455d: movzx     ebp, word ptr [eax*2 + 0x4965de]
00454565: xor       eax, eax
00454567: mov       edx, 3
0045456c: mov       al, byte ptr [ecx]
0045456e: call      0x428cc0
00454573: and       eax, 0xffff
00454578: sub       ebp, eax
0045457a: xor       eax, eax
0045457c: mov       ax, word ptr [ecx + 0x102]
00454583: cmp       eax, ebp
00454585: jge       0x454591
00454587: mov       edx, eax
00454589: inc       edx
0045458a: mov       word ptr [ecx + 0x102], dx
00454591: mov       dh, byte ptr [esp + 0x60]
00454595: cmp       dh, 0x10
00454598: jb        0x45459f
0045459a: cmp       dh, 0x11
0045459d: jbe       0x4545a7
0045459f: xor       al, al
004545a1: test      al, al
004545a3: jne       0x4545f3
004545a5: jmp       0x4545af
004545a7: mov       al, 1
004545a9: jmp       0x4545a1
004545ab: mov       al, 1
004545ad: jmp       0x4545c8
004545af: mov       al, byte ptr [esp + 0x60]
004545b3: sub       al, 0xb
004545b5: cmp       al, 5
004545b7: ja        0x4545c6
004545b9: and       eax, 0xff
004545be: jmp       dword ptr cs:[eax*4 + 0x45432c]
004545c6: xor       al, al
004545c8: test      al, al
004545ca: je        0x4545f3
004545cc: cmp       dword ptr [esi + 0x104], -1
004545d3: je        0x4545f3
004545d5: mov       ax, word ptr [esi + 0x7e]
004545d9: cmp       ax, word ptr [esi + 8]
004545dd: jne       0x4545f3
004545df: cmp       byte ptr [esi + 0xf9], 0
004545e6: je        0x4545f3
004545e8: lea       eax, [esi + 0x104]
004545ee: call      0x48aac0
004545f3: xor       eax, eax
004545f5: mov       al, byte ptr [esp + 0x60]
004545f9: cmp       eax, 0x10
004545fc: jne       0x454687
00454602: cmp       dword ptr [esi + 0x104], -1
00454609: jne       0x454687
0045460f: xor       ecx, ecx
00454611: mov       cx, di
00454614: mov       eax, ecx
00454616: shl       eax, 4
00454619: add       eax, ecx
0045461b: shl       eax, 2
0045461e: mov       ebx, dword ptr [0x4e19a0]
00454624: add       eax, ecx
00454626: mov       edx, ecx
00454628: shl       eax, 2
0045462b: xor       edx, ecx
0045462d: add       ebx, eax
0045462f: xor       eax, eax
00454631: mov       dl, byte ptr [0x508041]
00454637: mov       ax, word ptr [ebx + 8]
0045463b: call      0x4766f0
00454640: test      al, al
00454642: je        0x454680
00454644: mov       eax, ecx
00454646: call      0x440c5d
0045464b: mov       ebp, dword ptr [ebx + 0x104]
00454651: mov       byte ptr [ebx + 0xf9], 1
00454658: cmp       ebp, -1
0045465b: jne       0x454680
0045465d: mov       ecx, 1
00454662: xor       edx, edx
00454664: push      eax
00454665: mov       dl, byte ptr [ebx + 1]
00454668: lea       eax, [ebx + 0x104]
0045466e: shl       edx, 0x10
00454671: mov       ebx, eax
00454673: mov       eax, 0x50
00454678: or        dh, 8
0045467b: call      0x48aa79
00454680: mov       byte ptr [esi + 0xf9], 1
00454687: xor       eax, eax
00454689: mov       al, byte ptr [esi + 2]
0045468c: cmp       eax, 0xe
0045468f: je        0x4547e0
00454695: xor       eax, eax
00454697: mov       edx, dword ptr [0x508f7c]
0045469d: mov       ax, di
004546a0: add       eax, edx
004546a2: test      al, 0x1f
004546a4: jne       0x4547e0
004546aa: xor       eax, eax
004546ac: mov       al, byte ptr [esp + 0x58]
004546b0: cmp       eax, 0xc8
004546b5: jne       0x4546bc
004546b7: jmp       0x4547e0
004546bc: xor       edx, edx
004546be: mov       dx, di
004546c1: mov       eax, edx
004546c3: shl       eax, 4
004546c6: add       eax, edx
004546c8: shl       eax, 2
004546cb: add       edx, eax
004546cd: mov       eax, dword ptr [0x4e19a0]
004546d2: shl       edx, 2
004546d5: mov       al, byte ptr [edx + eax + 1]
004546d9: cmp       al, 0xf
004546db: jb        0x4546fd
004546dd: jbe       0x4546f9
004546df: cmp       al, 0x14
004546e1: jb        0x4546f1
004546e3: cmp       al, 0x16
004546e5: jbe       0x4546f9
004546e7: cmp       al, 0x18
004546e9: jbe       0x4546f9
004546eb: cmp       al, 0x19
004546ed: je        0x4546f9
004546ef: jmp       0x454711
004546f1: cmp       al, 0x10
004546f3: jbe       0x4546f9
004546f5: cmp       al, 0x12
004546f7: jb        0x454711
004546f9: mov       al, 1
004546fb: jmp       0x454713
004546fd: cmp       al, 3
004546ff: jb        0x4546f9
00454701: jbe       0x4546f9
00454703: cmp       al, 8
00454705: jb        0x454711
00454707: jbe       0x4546f9
00454709: cmp       al, 0xb
0045470b: jb        0x454711
0045470d: cmp       al, 0xc
0045470f: jbe       0x4546f9
00454711: xor       al, al
00454713: test      al, al
00454715: je        0x4547e0
0045471b: xor       eax, eax
0045471d: mov       al, byte ptr [esp + 0x58]
00454721: call      0x46d817
00454726: mov       byte ptr [esp + 0x50], al
0045472a: xor       eax, eax
0045472c: mov       al, byte ptr [esi + 2]
0045472f: cmp       eax, 1
00454732: je        0x4547e0
00454738: cmp       eax, 0x13
0045473b: jne       0x454746
0045473d: jmp       0x4547e0
00454742: mov       al, 1
00454744: jmp       0x454758
00454746: mov       cl, byte ptr [esp + 0x60]
0045474a: cmp       cl, 0xe
0045474d: jb        0x454756
0045474f: jbe       0x454742
00454751: cmp       cl, 0x10
00454754: je        0x454742
00454756: xor       al, al
00454758: test      al, al
0045475a: je        0x45477e
0045475c: xor       edx, edx
0045475e: mov       dx, di
00454761: mov       eax, edx
00454763: shl       eax, 4
00454766: add       eax, edx
00454768: shl       eax, 2
0045476b: add       eax, edx
0045476d: mov       edx, dword ptr [0x4e19a0]
00454773: mov       al, byte ptr [edx + eax*4 + 0xda]
0045477a: test      al, al
0045477c: jne       0x454794
0045477e: mov       ah, byte ptr [esp + 0x60]
00454782: cmp       ah, 0xe
00454785: jb        0x45478e
00454787: jbe       0x4547c6
00454789: cmp       ah, 0x10
0045478c: je        0x4547c6
0045478e: xor       al, al
00454790: test      al, al
00454792: jne       0x4547e0
00454794: xor       ecx, ecx
00454796: mov       cx, di
00454799: mov       eax, ecx
0045479b: xor       ebx, ebx
0045479d: call      0x453f74
004547a2: mov       bx, ax
004547a5: cmp       ebx, 0xffff
004547ab: je        0x4547e0
004547ad: xor       eax, eax
004547af: mov       al, byte ptr [esp + 0x50]
004547b3: cmp       eax, 2
004547b6: jne       0x4547ca
004547b8: mov       edx, 0x49
004547bd: mov       eax, ecx
004547bf: call      0x4829c8
004547c4: jmp       0x4547e0
004547c6: mov       al, 1
004547c8: jmp       0x454790
004547ca: xor       eax, eax
004547cc: mov       al, byte ptr [esi + 2]
004547cf: cmp       eax, 7
004547d2: jne       0x4547e0
004547d4: mov       edx, 1
004547d9: mov       eax, ecx
004547db: call      0x445a36
004547e0: xor       ebx, ebx
004547e2: mov       bx, di
004547e5: mov       eax, ebx
004547e7: shl       eax, 4
004547ea: add       eax, ebx
004547ec: shl       eax, 2
004547ef: mov       edx, dword ptr [0x4e19a0]
004547f5: add       eax, ebx
004547f7: mov       al, byte ptr [edx + eax*4 + 0xdc]
004547fe: mov       edx, 2
00454803: and       eax, 0xff
00454808: call      0x467d97
0045480d: test      al, al
0045480f: je        0x454855
00454811: mov       eax, 2
00454816: call      0x47474f
0045481b: xor       ecx, ecx
0045481d: xor       edx, edx
0045481f: mov       cx, ax
00454822: mov       eax, dword ptr [0x508f7c]
00454827: div       ecx
00454829: test      edx, edx
0045482b: jne       0x454855
0045482d: mov       cx, word ptr [esi + 0x9a]
00454834: xor       eax, eax
00454836: dec       ecx
00454837: mov       ax, cx
0045483a: mov       word ptr [esi + 0x9a], cx
00454841: test      eax, eax
00454843: jne       0x454855
00454845: mov       eax, ebx
00454847: call      0x444938
0045484c: jmp       0x454ccd
00454851: mov       al, 1
00454853: jmp       0x45486b
00454855: mov       al, byte ptr [esi + 1]
00454858: cmp       al, 0x19
0045485a: ja        0x454869
0045485c: and       eax, 0xff
00454861: jmp       dword ptr cs:[eax*4 + 0x454344]
00454869: xor       al, al
0045486b: test      al, al
0045486d: je        0x454994
00454873: xor       ebx, ebx
00454875: mov       bx, di
00454878: mov       ecx, ebx
0045487a: shl       ecx, 4
0045487d: add       ecx, ebx
0045487f: shl       ecx, 2
00454882: add       ecx, ebx
00454884: mov       eax, dword ptr [0x4e19a0]
00454889: shl       ecx, 2
0045488c: mov       al, byte ptr [ecx + eax + 0xdc]
00454893: mov       edx, 2
00454898: and       eax, 0xff
0045489d: call      0x467d97
004548a2: test      al, al
004548a4: jne       0x454994
004548aa: mov       eax, ebx
004548ac: call      0x452cc8
004548b1: mov       eax, dword ptr [0x4e19a0]
004548b6: add       ecx, eax
004548b8: xor       eax, eax
004548ba: mov       al, byte ptr [ecx + 2]
004548bd: test      eax, eax
004548bf: je        0x4548ca
004548c1: cmp       eax, 4
004548c4: je        0x4548ca
004548c6: mov       al, 1
004548c8: jmp       0x4548cc
004548ca: xor       al, al
004548cc: test      al, al
004548ce: je        0x454ccd
004548d4: xor       eax, eax
004548d6: mov       ax, word ptr [esi + 4]
004548da: cmp       eax, 4
004548dd: je        0x454994
004548e3: xor       edx, edx
004548e5: mov       dx, di
004548e8: mov       eax, edx
004548ea: shl       eax, 4
004548ed: add       eax, edx
004548ef: shl       eax, 2
004548f2: add       eax, edx
004548f4: mov       edx, dword ptr [0x4e19a0]
004548fa: shl       eax, 2
004548fd: add       edx, eax
004548ff: xor       eax, eax
00454901: mov       al, byte ptr [edx + 2]
00454904: test      eax, eax
00454906: je        0x454911
00454908: cmp       eax, 4
0045490b: je        0x454911
0045490d: mov       al, 1
0045490f: jmp       0x454913
00454911: xor       al, al
00454913: test      al, al
00454915: je        0x454994
0045491b: xor       ecx, ecx
0045491d: mov       cx, di
00454920: mov       eax, ecx
00454922: shl       eax, 4
00454925: add       eax, ecx
00454927: shl       eax, 2
0045492a: add       eax, ecx
0045492c: mov       edx, dword ptr [0x4e19a0]
00454932: shl       eax, 2
00454935: add       eax, edx
00454937: mov       dl, byte ptr [eax + 0x72]
0045493a: test      dl, dl
0045493c: je        0x454994
0045493e: xor       edx, edx
00454940: mov       dx, word ptr [eax + 4]
00454944: test      edx, edx
00454946: sete      dl
00454949: test      dl, dl
0045494b: je        0x454994
0045494d: mov       edx, dword ptr [esi + 0x83]
00454953: sar       edx, 0x18
00454956: test      edx, edx
00454958: jne       0x454994
0045495a: mov       edx, dword ptr [esi + 0x84]
00454960: sar       edx, 0x18
00454963: test      edx, edx
00454965: jne       0x454994
00454967: mov       al, byte ptr [eax]
00454969: and       eax, 0xff
0045496e: call      0x46d817
00454973: and       eax, 0xff
00454978: cmp       eax, 2
0045497b: jne       0x45498d
0045497d: mov       edx, 0x4b
00454982: mov       eax, ecx
00454984: xor       ebx, ebx
00454986: call      0x4829c8
0045498b: jmp       0x454994
0045498d: mov       eax, ecx
0045498f: call      0x453b84
00454994: xor       edx, edx
00454996: mov       dx, di
00454999: mov       eax, edx
0045499b: shl       eax, 4
0045499e: add       eax, edx
004549a0: shl       eax, 2
004549a3: add       eax, edx
004549a5: mov       edx, dword ptr [0x4e19a0]
004549ab: shl       eax, 2
004549ae: add       eax, edx
004549b0: mov       dl, byte ptr [eax + 1]
004549b3: and       edx, 0xff
004549b9: cmp       edx, 0x11
004549bc: jne       0x454b3c
004549c2: mov       dl, byte ptr [eax]
004549c4: mov       dword ptr [esp + 0x28], edi
004549c8: mov       byte ptr [esp + 0x4c], dl
004549cc: and       edx, 0xff
004549d2: mov       dx, word ptr [edx*8 + 0x4e1a14]
004549da: and       edx, 0xffff
004549e0: jne       0x454b3c
004549e6: mov       cl, 0x1e
004549e8: mov       ebx, edi
004549ea: mov       al, byte ptr [eax + 2]
004549ed: and       eax, 0xff
004549f2: je        0x4549fd
004549f4: cmp       eax, 4
004549f7: je        0x4549fd
004549f9: mov       al, 1
004549fb: jmp       0x4549ff
004549fd: xor       al, al
004549ff: test      al, al
00454a01: je        0x454a4f
00454a03: xor       edx, edx
00454a05: mov       dx, bx
00454a08: mov       eax, edx
00454a0a: shl       eax, 4
00454a0d: add       eax, edx
00454a0f: shl       eax, 2
00454a12: add       edx, eax
00454a14: mov       eax, dword ptr [0x4e19a0]
00454a19: shl       edx, 2
00454a1c: mov       byte ptr [edx + eax + 2], cl
00454a20: mov       ax, word ptr [0x496304]
00454a26: cmp       bx, ax
00454a29: jne       0x454a4f
00454a2b: xor       bl, al
00454a2d: mov       byte ptr [0x4e0f36], bl
00454a33: xor       bh, ah
00454a35: mov       edx, 0xffff
00454a3a: mov       byte ptr [0x4e0f37], bh
00454a40: xor       ebx, ebx
00454a42: mov       word ptr [0x496304], dx
00454a49: mov       dword ptr [0x4e0f3c], ebx
00454a4f: xor       ebx, ebx
00454a51: xor       ecx, ecx
00454a53: mov       bl, byte ptr [esp + 0x4c]
00454a57: mov       cx, word ptr [esp + 0x28]
00454a5c: xor       edx, edx
00454a5e: mov       eax, ecx
00454a60: mov       dx, word ptr [ebx*8 + 0x4e1a1a]
00454a68: call      0x4457d3
00454a6d: mov       eax, ecx
00454a6f: shl       eax, 4
00454a72: add       eax, ecx
00454a74: shl       eax, 2
00454a77: mov       edx, dword ptr [0x4e19a0]
00454a7d: add       eax, ecx
00454a7f: mov       ax, word ptr [edx + eax*4 + 0x7c]
00454a84: cmp       ax, word ptr [ebx*8 + 0x4e1a1a]
00454a8c: je        0x454aa8
00454a8e: xor       edx, edx
00454a90: mov       dx, ax
00454a93: mov       eax, edx
00454a95: sar       edx, 0x1f
00454a98: shl       edx, 8
00454a9b: sbb       eax, edx
00454a9d: sar       eax, 8
00454aa0: test      eax, eax
00454aa2: jne       0x454b3c
00454aa8: xor       edx, edx
00454aaa: mov       dx, word ptr [esp + 0x28]
00454aaf: mov       eax, edx
00454ab1: call      0x457058
00454ab6: mov       eax, edx
00454ab8: shl       eax, 4
00454abb: add       eax, edx
00454abd: shl       eax, 2
00454ac0: mov       ebx, edx
00454ac2: add       eax, edx
00454ac4: mov       edx, dword ptr [0x4e19a0]
00454aca: xor       cl, cl
00454acc: mov       al, byte ptr [edx + eax*4 + 2]
00454ad0: and       eax, 0xff
00454ad5: je        0x454ae0
00454ad7: cmp       eax, 4
00454ada: je        0x454ae0
00454adc: mov       al, 1
00454ade: jmp       0x454ae2
00454ae0: xor       al, al
00454ae2: test      al, al
00454ae4: je        0x454b2c
00454ae6: xor       edx, edx
00454ae8: mov       dx, bx
00454aeb: mov       eax, edx
00454aed: shl       eax, 4
00454af0: add       eax, edx
00454af2: shl       eax, 2
00454af5: add       eax, edx
00454af7: mov       edx, dword ptr [0x4e19a0]
00454afd: mov       byte ptr [edx + eax*4 + 2], cl
00454b01: cmp       bx, word ptr [0x496304]
00454b08: jne       0x454b2c
00454b0a: xor       cl, cl
00454b0c: mov       edx, 0xffff
00454b11: mov       byte ptr [0x4e0f36], cl
00454b17: mov       byte ptr [0x4e0f37], cl
00454b1d: xor       ecx, ecx
00454b1f: mov       word ptr [0x496304], dx
00454b26: mov       dword ptr [0x4e0f3c], ecx
00454b2c: xor       eax, eax
00454b2e: mov       al, byte ptr [esp + 0x4c]
00454b32: mov       word ptr [eax*8 + 0x4e1a18], 0xffff
00454b3c: xor       ebx, ebx
00454b3e: mov       bx, di
00454b41: mov       eax, ebx
00454b43: shl       eax, 4
00454b46: add       eax, ebx
00454b48: shl       eax, 2
00454b4b: mov       edx, dword ptr [0x4e19a0]
00454b51: add       eax, ebx
00454b53: mov       al, byte ptr [edx + eax*4 + 0x72]
00454b57: test      al, al
00454b59: je        0x454b72
00454b5b: xor       eax, eax
00454b5d: mov       al, byte ptr [esi + 2]
00454b60: cmp       eax, 4
00454b63: je        0x454b72
00454b65: xor       edx, edx
00454b67: mov       eax, ebx
00454b69: mov       dx, word ptr [esi + 8]
00454b6d: call      0x442cb4
00454b72: xor       edx, edx
00454b74: mov       dx, di
00454b77: mov       ebx, edx
00454b79: shl       ebx, 4
00454b7c: add       ebx, edx
00454b7e: shl       ebx, 2
00454b81: add       ebx, edx
00454b83: mov       eax, dword ptr [0x4e19a0]
00454b88: shl       ebx, 2
00454b8b: mov       al, byte ptr [ebx + eax + 0xdc]
00454b92: mov       edx, 1
00454b97: and       eax, 0xff
00454b9c: call      0x467d97
00454ba1: test      al, al
00454ba3: je        0x454bef
00454ba5: mov       eax, dword ptr [0x4e19a0]
00454baa: add       eax, ebx
00454bac: mov       esi, dword ptr [eax + 0xe4]
00454bb2: add       eax, 4
00454bb5: dec       esi
00454bb6: mov       dword ptr [eax + 0xe0], esi
00454bbc: mov       eax, dword ptr [0x4e19a0]
00454bc1: add       ebx, eax
00454bc3: lea       eax, [ebx + 4]
00454bc6: mov       ax, word ptr [eax + 0xe0]
00454bcd: and       eax, 0xffff
00454bd2: jne       0x454ccd
00454bd8: lea       eax, [ebx + 0xdc]
00454bde: mov       edx, 1
00454be3: xor       ebx, ebx
00454be5: call      0x467d71
00454bea: jmp       0x454ccd
00454bef: mov       eax, dword ptr [0x4e19a0]
00454bf4: mov       al, byte ptr [ebx + eax + 0xdc]
00454bfb: mov       edx, 3
00454c00: and       eax, 0xff
00454c05: call      0x467d97
00454c0a: test      al, al
00454c0c: je        0x454c4f
00454c0e: mov       eax, dword ptr [0x4e19a0]
00454c13: add       eax, ebx
00454c15: mov       ebp, dword ptr [eax + 0xec]
00454c1b: add       eax, 0xc
00454c1e: dec       ebp
00454c1f: mov       dword ptr [eax + 0xe0], ebp
00454c25: mov       eax, dword ptr [0x4e19a0]
00454c2a: add       ebx, eax
00454c2c: lea       eax, [ebx + 0xc]
00454c2f: mov       ax, word ptr [eax + 0xe0]
00454c36: and       eax, 0xffff
00454c3b: jne       0x454c4f
00454c3d: lea       eax, [ebx + 0xdc]
00454c43: mov       edx, 3
00454c48: xor       ebx, ebx
00454c4a: call      0x467d71
00454c4f: xor       edx, edx
00454c51: mov       dx, di
00454c54: mov       eax, edx
00454c56: shl       eax, 4
00454c59: add       eax, edx
00454c5b: shl       eax, 2
00454c5e: add       edx, eax
00454c60: mov       eax, dword ptr [0x4e19a0]
00454c65: shl       edx, 2
00454c68: mov       al, byte ptr [edx + eax + 1]
00454c6c: cmp       al, 0xc
00454c6e: jb        0x454c76
00454c70: jbe       0x454c8f
00454c72: cmp       al, 0xf
00454c74: je        0x454c8f
00454c76: xor       al, al
00454c78: test      al, al
00454c7a: je        0x456c1c
00454c80: xor       eax, eax
00454c82: mov       ax, di
00454c85: call      0x4484a7
00454c8a: jmp       0x456c1c
00454c8f: mov       al, 1
00454c91: jmp       0x454c78
00454c93: xor       eax, eax
00454c95: mov       ax, word ptr [esi + 0xc0]
00454c9c: cmp       eax, 0xffff
00454ca1: je        0x455554
00454ca7: xor       eax, eax
00454ca9: mov       ax, word ptr [esi + 0xc0]
00454cb0: call      0x41a70b
00454cb5: test      al, al
00454cb7: je        0x455554
00454cbd: xor       eax, eax
00454cbf: xor       edx, edx
00454cc1: mov       ax, di
00454cc4: mov       dx, word ptr [esi + 0x7e]
00454cc8: call      0x4457d3
00454ccd: add       esp, 0x64
00454cd0: jmp       0x44f29d
00454cd5: xor       edx, edx
00454cd7: mov       dx, di
00454cda: mov       eax, edx
00454cdc: shl       eax, 4
00454cdf: add       eax, edx
00454ce1: shl       eax, 2
00454ce4: add       eax, edx
00454ce6: mov       edx, dword ptr [0x4e19a0]
00454cec: mov       al, byte ptr [edx + eax*4 + 1]
00454cf0: and       eax, 0xff
00454cf5: cmp       eax, 6
00454cf8: jne       0x454d56
00454cfa: mov       bx, word ptr [esi + 0xc0]
00454d01: xor       edx, edx
00454d03: mov       dx, bx
00454d06: mov       eax, edx
00454d08: shl       eax, 4
00454d0b: add       eax, edx
00454d0d: shl       eax, 2
00454d10: add       edx, eax
00454d12: mov       eax, dword ptr [0x4e19a0]
00454d17: shl       edx, 2
00454d1a: mov       al, byte ptr [edx + eax + 2]
00454d1e: and       eax, 0xff
00454d23: je        0x454d50
00454d25: xor       edx, edx
00454d27: mov       dx, bx
00454d2a: mov       eax, edx
00454d2c: shl       eax, 4
00454d2f: add       eax, edx
00454d31: shl       eax, 2
00454d34: add       edx, eax
00454d36: mov       eax, dword ptr [0x4e19a0]
00454d3b: shl       edx, 2
00454d3e: mov       al, byte ptr [edx + eax + 2]
00454d42: and       eax, 0xff
00454d47: cmp       eax, 4
00454d4a: je        0x454d50
00454d4c: mov       al, 1
00454d4e: jmp       0x454d52
00454d50: xor       al, al
00454d52: test      al, al
00454d54: je        0x454d97
00454d56: xor       edx, edx
00454d58: mov       dx, di
00454d5b: mov       eax, edx
00454d5d: shl       eax, 4
00454d60: add       eax, edx
00454d62: shl       eax, 2
00454d65: add       edx, eax
00454d67: mov       eax, dword ptr [0x4e19a0]
00454d6c: shl       edx, 2
00454d6f: mov       al, byte ptr [edx + eax + 1]
00454d73: and       eax, 0xff
00454d78: cmp       eax, 7
00454d7b: jne       0x455554
00454d81: xor       eax, eax
00454d83: mov       ax, word ptr [esi + 0xc0]
00454d8a: call      0x41a70b
00454d8f: test      al, al
00454d91: je        0x455554
00454d97: xor       eax, eax
00454d99: xor       edx, edx
00454d9b: mov       ax, di
00454d9e: mov       dx, word ptr [esi + 0x7e]
00454da2: call      0x4457d3
00454da7: mov       word ptr [esi + 0xc0], 0xffff
00454db0: jmp       0x454ccd
00454db5: xor       eax, eax
00454db7: mov       ax, word ptr [esi + 0xc0]
00454dbe: call      0x41a70b
00454dc3: test      al, al
00454dc5: jne       0x454ddd
00454dc7: xor       eax, eax
00454dc9: mov       ax, word ptr [esi + 0xc0]
00454dd0: call      0x41a08c
00454dd5: cmp       al, byte ptr [esi]
00454dd7: je        0x454ebf
00454ddd: xor       ecx, ecx
00454ddf: mov       cx, di
00454de2: mov       ebp, ecx
00454de4: shl       ebp, 4
00454de7: add       ebp, ecx
00454de9: shl       ebp, 2
00454dec: add       ebp, ecx
00454dee: mov       ebx, dword ptr [0x4e19a0]
00454df4: shl       ebp, 2
00454df7: add       ebx, ebp
00454df9: mov       al, byte ptr [ebx + 0x72]
00454dfc: test      al, al
00454dfe: jne       0x454ea6
00454e04: mov       ax, word ptr [ebx + 8]
00454e08: xor       edx, edx
00454e0a: mov       dx, ax
00454e0d: mov       eax, ecx
00454e0f: call      0x442cb4
00454e14: mov       byte ptr [ebx + 0x72], 1
00454e18: mov       ecx, dword ptr [0x4e19a0]
00454e1e: add       ecx, ebp
00454e20: xor       ebx, ebx
00454e22: mov       ax, word ptr [ecx + 8]
00454e26: mov       bl, byte ptr [ecx]
00454e28: mov       dword ptr [esp + 0x24], eax
00454e2c: cmp       ebx, 0xc8
00454e32: je        0x454e91
00454e34: cmp       ebx, 4
00454e37: je        0x454e91
00454e39: xor       ah, ah
00454e3b: mov       al, byte ptr [ecx + 0xbb]
00454e41: add       eax, 2
00454e46: mov       dword ptr [esp + 0x48], eax
00454e4a: xor       ah, ah
00454e4c: mov       edx, dword ptr [esp + 0x48]
00454e50: mov       al, byte ptr [ecx + 0xf5]
00454e56: add       eax, edx
00454e58: xor       edx, edx
00454e5a: movzx     ebp, word ptr [esp + 0x24]
00454e5f: mov       dx, ax
00454e62: mov       eax, ebp
00454e64: call      0x476851
00454e69: xor       ah, ah
00454e6b: mov       al, byte ptr [ecx + 0xbb]
00454e71: mov       dword ptr [esp + 0x48], eax
00454e75: mov       edx, dword ptr [esp + 0x48]
00454e79: mov       al, byte ptr [ecx + 0xf5]
00454e7f: xor       ebx, ebx
00454e81: add       eax, edx
00454e83: xor       edx, edx
00454e85: mov       bl, byte ptr [ecx]
00454e87: mov       dx, ax
00454e8a: mov       eax, ebp
00454e8c: call      0x476cb3
00454e91: mov       edx, 4
00454e96: xor       ebx, ebx
00454e98: xor       eax, eax
00454e9a: mov       bx, word ptr [esp + 0x24]
00454e9f: mov       al, byte ptr [ecx]
00454ea1: call      0x46a388
00454ea6: xor       eax, eax
00454ea8: xor       edx, edx
00454eaa: mov       ax, di
00454ead: mov       dx, word ptr [esi + 0x7e]
00454eb1: mov       word ptr [esi + 0xc0], 0xffff
00454eba: jmp       0x4550b4
00454ebf: xor       eax, eax
00454ec1: mov       al, byte ptr [esi + 0x82]
00454ec7: cmp       eax, 2
00454eca: jne       0x455554
00454ed0: xor       eax, eax
00454ed2: mov       ax, word ptr [esi + 0x80]
00454ed9: call      0x41a70b
00454ede: test      al, al
00454ee0: jne       0x454ef8
00454ee2: xor       eax, eax
00454ee4: mov       ax, word ptr [esi + 0x80]
00454eeb: call      0x41a08c
00454ef0: cmp       al, byte ptr [esi]
00454ef2: je        0x455554
00454ef8: xor       ecx, ecx
00454efa: mov       cx, di
00454efd: mov       ebp, ecx
00454eff: shl       ebp, 4
00454f02: add       ebp, ecx
00454f04: shl       ebp, 2
00454f07: add       ebp, ecx
00454f09: mov       ebx, dword ptr [0x4e19a0]
00454f0f: shl       ebp, 2
00454f12: add       ebx, ebp
00454f14: mov       al, byte ptr [ebx + 0x72]
00454f17: test      al, al
00454f19: jne       0x454ea6
00454f1b: mov       ax, word ptr [ebx + 8]
00454f1f: xor       edx, edx
00454f21: mov       dx, ax
00454f24: mov       eax, ecx
00454f26: call      0x442cb4
00454f2b: mov       byte ptr [ebx + 0x72], 1
00454f2f: mov       ecx, dword ptr [0x4e19a0]
00454f35: add       ecx, ebp
00454f37: xor       ebx, ebx
00454f39: mov       ax, word ptr [ecx + 8]
00454f3d: mov       bl, byte ptr [ecx]
00454f3f: mov       dword ptr [esp + 0x44], eax
00454f43: cmp       ebx, 0xc8
00454f49: je        0x454f9a
00454f4b: cmp       ebx, 4
00454f4e: je        0x454f9a
00454f50: xor       ah, ah
00454f52: xor       dh, dh
00454f54: mov       al, byte ptr [ecx + 0xbb]
00454f5a: mov       dl, byte ptr [ecx + 0xf5]
00454f60: add       eax, 2
00454f65: add       eax, edx
00454f67: xor       edx, edx
00454f69: movzx     ebp, word ptr [esp + 0x44]
00454f6e: mov       dx, ax
00454f71: mov       eax, ebp
00454f73: call      0x476851
00454f78: xor       ebx, ebx
00454f7a: xor       dh, dh
00454f7c: xor       ah, ah
00454f7e: mov       dl, byte ptr [ecx + 0xf5]
00454f84: mov       al, byte ptr [ecx + 0xbb]
00454f8a: add       eax, edx
00454f8c: xor       edx, edx
00454f8e: mov       bl, byte ptr [ecx]
00454f90: mov       dx, ax
00454f93: mov       eax, ebp
00454f95: call      0x476cb3
00454f9a: mov       edx, 4
00454f9f: xor       ebx, ebx
00454fa1: xor       eax, eax
00454fa3: mov       bx, word ptr [esp + 0x44]
00454fa8: jmp       0x454e9f
00454fad: xor       eax, eax
00454faf: mov       al, byte ptr [esi + 0x82]
00454fb5: cmp       eax, 2
00454fb8: jne       0x455554
00454fbe: xor       eax, eax
00454fc0: mov       ax, word ptr [esi + 0x80]
00454fc7: call      0x41a70b
00454fcc: test      al, al
00454fce: jne       0x454fe6
00454fd0: xor       eax, eax
00454fd2: mov       ax, word ptr [esi + 0x80]
00454fd9: call      0x41a08c
00454fde: cmp       al, byte ptr [esi]
00454fe0: je        0x455554
00454fe6: xor       ecx, ecx
00454fe8: mov       cx, di
00454feb: mov       ebp, ecx
00454fed: shl       ebp, 4
00454ff0: add       ebp, ecx
00454ff2: shl       ebp, 2
00454ff5: add       ebp, ecx
00454ff7: mov       ebx, dword ptr [0x4e19a0]
00454ffd: shl       ebp, 2
00455000: add       ebx, ebp
00455002: mov       al, byte ptr [ebx + 0x72]
00455005: test      al, al
00455007: jne       0x4550a9
0045500d: mov       ax, word ptr [ebx + 8]
00455011: xor       edx, edx
00455013: mov       dx, ax
00455016: mov       eax, ecx
00455018: call      0x442cb4
0045501d: mov       byte ptr [ebx + 0x72], 1
00455021: mov       ecx, dword ptr [0x4e19a0]
00455027: add       ecx, ebp
00455029: xor       ebx, ebx
0045502b: mov       ax, word ptr [ecx + 8]
0045502f: mov       bl, byte ptr [ecx]
00455031: mov       dword ptr [esp + 0x40], eax
00455035: cmp       ebx, 0xc8
0045503b: je        0x455094
0045503d: cmp       ebx, 4
00455040: je        0x455094
00455042: xor       ah, ah
00455044: mov       al, byte ptr [ecx + 0xbb]
0045504a: add       eax, 2
0045504f: mov       dword ptr [esp + 0x48], eax
00455053: xor       ah, ah
00455055: mov       edx, dword ptr [esp + 0x48]
00455059: mov       al, byte ptr [ecx + 0xf5]
0045505f: add       eax, edx
00455061: xor       edx, edx
00455063: movzx     ebp, word ptr [esp + 0x40]
00455068: mov       dx, ax
0045506b: mov       eax, ebp
0045506d: call      0x476851
00455072: xor       ebx, ebx
00455074: xor       dh, dh
00455076: xor       ah, ah
00455078: mov       dl, byte ptr [ecx + 0xf5]
0045507e: mov       al, byte ptr [ecx + 0xbb]
00455084: add       eax, edx
00455086: xor       edx, edx
00455088: mov       bl, byte ptr [ecx]
0045508a: mov       dx, ax
0045508d: mov       eax, ebp
0045508f: call      0x476cb3
00455094: mov       edx, 4
00455099: xor       ebx, ebx
0045509b: xor       eax, eax
0045509d: mov       bx, word ptr [esp + 0x40]
004550a2: mov       al, byte ptr [ecx]
004550a4: call      0x46a388
004550a9: xor       eax, eax
004550ab: xor       edx, edx
004550ad: mov       ax, di
004550b0: mov       dx, word ptr [esi + 0x7e]
004550b4: call      0x4457d3
004550b9: mov       byte ptr [esi + 0x82], 0
004550c0: mov       word ptr [esi + 0x80], 0xffff
004550c9: jmp       0x454ccd
004550ce: xor       eax, eax
004550d0: mov       al, byte ptr [esi + 0x82]
004550d6: cmp       eax, 2
004550d9: jne       0x455554
004550df: xor       eax, eax
004550e1: mov       ax, word ptr [esi + 0x80]
004550e8: call      0x41a70b
004550ed: test      al, al
004550ef: jne       0x455107
004550f1: xor       eax, eax
004550f3: mov       ax, word ptr [esi + 0x80]
004550fa: call      0x41a08c
004550ff: cmp       al, byte ptr [esi]
00455101: je        0x455554
00455107: xor       edx, edx
00455109: mov       dx, di
0045510c: mov       eax, edx
0045510e: shl       eax, 4
00455111: add       eax, edx
00455113: shl       eax, 2
00455116: add       eax, edx
00455118: mov       edx, dword ptr [0x4e19a0]
0045511e: mov       al, byte ptr [edx + eax*4 + 0x72]
00455122: test      al, al
00455124: jne       0x4550a9
00455126: xor       eax, eax
00455128: mov       al, byte ptr [esi + 1]
0045512b: cmp       eax, 7
0045512e: jne       0x45513e
00455130: xor       eax, eax
00455132: mov       ax, word ptr [esi + 0xb2]
00455139: call      0x4754de
0045513e: xor       ecx, ecx
00455140: mov       cx, di
00455143: mov       ebp, ecx
00455145: shl       ebp, 4
00455148: add       ebp, ecx
0045514a: shl       ebp, 2
0045514d: mov       ebx, dword ptr [0x4e19a0]
00455153: add       ebp, ecx
00455155: mov       edx, ecx
00455157: shl       ebp, 2
0045515a: xor       edx, ecx
0045515c: mov       ax, word ptr [ebx + ebp + 8]
00455161: mov       dx, ax
00455164: mov       eax, ecx
00455166: call      0x442cb4
0045516b: mov       byte ptr [ebx + ebp + 0x72], 1
00455170: mov       ecx, dword ptr [0x4e19a0]
00455176: add       ecx, ebp
00455178: xor       ebx, ebx
0045517a: mov       ax, word ptr [ecx + 8]
0045517e: mov       bl, byte ptr [ecx]
00455180: mov       dword ptr [esp + 0x30], eax
00455184: cmp       ebx, 0xc8
0045518a: je        0x4551e3
0045518c: cmp       ebx, 4
0045518f: je        0x4551e3
00455191: xor       ah, ah
00455193: mov       al, byte ptr [ecx + 0xbb]
00455199: add       eax, 2
0045519e: mov       dword ptr [esp + 0x48], eax
004551a2: xor       ah, ah
004551a4: mov       edx, dword ptr [esp + 0x48]
004551a8: mov       al, byte ptr [ecx + 0xf5]
004551ae: add       eax, edx
004551b0: xor       edx, edx
004551b2: movzx     ebp, word ptr [esp + 0x30]
004551b7: mov       dx, ax
004551ba: mov       eax, ebp
004551bc: call      0x476851
004551c1: xor       ebx, ebx
004551c3: xor       dh, dh
004551c5: xor       ah, ah
004551c7: mov       dl, byte ptr [ecx + 0xf5]
004551cd: mov       al, byte ptr [ecx + 0xbb]
004551d3: add       eax, edx
004551d5: xor       edx, edx
004551d7: mov       bl, byte ptr [ecx]
004551d9: mov       dx, ax
004551dc: mov       eax, ebp
004551de: call      0x476cb3
004551e3: mov       edx, 4
004551e8: xor       ebx, ebx
004551ea: xor       eax, eax
004551ec: mov       bx, word ptr [esp + 0x30]
004551f1: jmp       0x4550a2
004551f6: xor       eax, eax
004551f8: mov       ax, word ptr [esi + 0xc0]
004551ff: call      0x41a70b
00455204: test      al, al
00455206: jne       0x454d97
0045520c: xor       eax, eax
0045520e: mov       ax, word ptr [esi + 0xc0]
00455215: call      0x41a08c
0045521a: and       eax, 0xff
0045521f: cmp       eax, 0xc8
00455224: je        0x454d97
0045522a: xor       eax, eax
0045522c: mov       ax, word ptr [esi + 0xc0]
00455233: call      0x41a08c
00455238: cmp       al, byte ptr [esi]
0045523a: jne       0x455554
00455240: jmp       0x454d97
00455245: xor       eax, eax
00455247: mov       ax, word ptr [esi + 0xb8]
0045524e: cmp       eax, 0xffff
00455253: je        0x45527c
00455255: call      0x41a70b
0045525a: test      al, al
0045525c: jne       0x45527c
0045525e: xor       eax, eax
00455260: mov       ax, word ptr [esi + 0xb8]
00455267: call      0x41a08c
0045526c: and       eax, 0xff
00455271: cmp       eax, 0xc8
00455276: jne       0x455554
0045527c: xor       ecx, ecx
0045527e: mov       cx, di
00455281: mov       eax, ecx
00455283: shl       eax, 4
00455286: add       eax, ecx
00455288: shl       eax, 2
0045528b: mov       edx, dword ptr [0x4e19a0]
00455291: add       eax, ecx
00455293: mov       al, byte ptr [edx + eax*4]
00455296: and       eax, 0xff
0045529b: call      0x46d817
004552a0: and       eax, 0xff
004552a5: cmp       eax, 2
004552a8: jne       0x4552bd
004552aa: mov       edx, 0x4a
004552af: mov       eax, ecx
004552b1: xor       ebx, ebx
004552b3: call      0x4829c8
004552b8: jmp       0x455554
004552bd: xor       edx, edx
004552bf: mov       eax, ecx
004552c1: mov       dx, word ptr [esi + 0x7e]
004552c5: call      0x4457d3
004552ca: mov       word ptr [esi + 0xb8], 0xffff
004552d3: jmp       0x455554
004552d8: xor       eax, eax
004552da: mov       ax, word ptr [esi + 0xb8]
004552e1: cmp       eax, 0xffff
004552e6: je        0x45535c
004552ec: xor       edx, edx
004552ee: mov       dx, ax
004552f1: mov       eax, edx
004552f3: shl       eax, 4
004552f6: add       eax, edx
004552f8: shl       eax, 2
004552fb: add       eax, edx
004552fd: mov       edx, dword ptr [0x4e19a0]
00455303: shl       eax, 2
00455306: add       edx, eax
00455308: xor       eax, eax
0045530a: mov       al, byte ptr [edx + 2]
0045530d: test      eax, eax
0045530f: je        0x45531a
00455311: cmp       eax, 4
00455314: je        0x45531a
00455316: mov       al, 1
00455318: jmp       0x45531c
0045531a: xor       al, al
0045531c: test      al, al
0045531e: je        0x45535c
00455320: mov       ax, word ptr [esi + 0xb8]
00455327: xor       edx, edx
00455329: mov       dx, ax
0045532c: mov       eax, edx
0045532e: shl       eax, 4
00455331: add       eax, edx
00455333: shl       eax, 2
00455336: add       eax, edx
00455338: mov       edx, dword ptr [0x4e19a0]
0045533e: shl       eax, 2
00455341: add       edx, eax
00455343: mov       al, byte ptr [edx]
00455345: and       eax, 0xff
0045534a: cmp       eax, 0xc8
0045534f: je        0x45535c
00455351: mov       al, byte ptr [edx + 0x72]
00455354: test      al, al
00455356: jne       0x455554
0045535c: xor       ecx, ecx
0045535e: mov       cx, di
00455361: mov       eax, ecx
00455363: shl       eax, 4
00455366: add       eax, ecx
00455368: shl       eax, 2
0045536b: mov       edx, dword ptr [0x4e19a0]
00455371: add       eax, ecx
00455373: mov       al, byte ptr [edx + eax*4]
00455376: and       eax, 0xff
0045537b: call      0x46d817
00455380: and       eax, 0xff
00455385: cmp       eax, 2
00455388: je        0x4552aa
0045538e: jmp       0x4552bd
00455393: mov       al, byte ptr [esi + 0xb7]
00455399: cmp       al, 1
0045539b: jb        0x455554
004553a1: jbe       0x4552d8
004553a7: cmp       al, 3
004553a9: je        0x455245
004553af: jmp       0x455554
004553b4: xor       eax, eax
004553b6: mov       ax, word ptr [esi + 0xc0]
004553bd: cmp       eax, 0xffff
004553c2: je        0x455429
004553c4: xor       eax, eax
004553c6: mov       ax, word ptr [esi + 0xc0]
004553cd: call      0x41a70b
004553d2: test      al, al
004553d4: jne       0x454d97
004553da: xor       eax, eax
004553dc: mov       al, byte ptr [esi + 1]
004553df: cmp       eax, 0xa
004553e2: je        0x45520c
004553e8: xor       eax, eax
004553ea: mov       ax, word ptr [esi + 0xc0]
004553f1: call      0x41a08c
004553f6: cmp       al, byte ptr [esi]
004553f8: je        0x455554
004553fe: xor       eax, eax
00455400: mov       ax, word ptr [esi + 0xc0]
00455407: call      0x41a08c
0045540c: and       eax, 0xff
00455411: cmp       eax, 0xc8
00455416: jne       0x454d97
0045541c: xor       eax, eax
0045541e: mov       al, byte ptr [esi + 1]
00455421: cmp       eax, 9
00455424: jmp       0x454d91
00455429: xor       eax, eax
0045542b: mov       ax, word ptr [esi + 0xb8]
00455432: cmp       eax, 0xffff
00455437: je        0x455554
0045543d: xor       edx, edx
0045543f: mov       dx, ax
00455442: mov       ebx, eax
00455444: mov       eax, edx
00455446: shl       eax, 4
00455449: add       eax, edx
0045544b: shl       eax, 2
0045544e: add       edx, eax
00455450: mov       eax, dword ptr [0x4e19a0]
00455455: shl       edx, 2
00455458: mov       al, byte ptr [edx + eax + 2]
0045545c: and       eax, 0xff
00455461: je        0x45548c
00455463: xor       edx, edx
00455465: mov       dx, bx
00455468: mov       eax, edx
0045546a: shl       eax, 4
0045546d: add       eax, edx
0045546f: shl       eax, 2
00455472: add       eax, edx
00455474: mov       edx, dword ptr [0x4e19a0]
0045547a: mov       al, byte ptr [edx + eax*4 + 2]
0045547e: and       eax, 0xff
00455483: cmp       eax, 4
00455486: je        0x45548c
00455488: mov       al, 1
0045548a: jmp       0x45548e
0045548c: xor       al, al
0045548e: test      al, al
00455490: jne       0x45549e
00455492: xor       eax, eax
00455494: xor       edx, edx
00455496: mov       ax, di
00455499: jmp       0x4567b7
0045549e: mov       ax, word ptr [esi + 0xb8]
004554a5: xor       edx, edx
004554a7: mov       dx, ax
004554aa: mov       eax, edx
004554ac: shl       eax, 4
004554af: add       eax, edx
004554b1: shl       eax, 2
004554b4: add       eax, edx
004554b6: mov       edx, dword ptr [0x4e19a0]
004554bc: mov       bl, byte ptr [esi]
004554be: mov       al, byte ptr [edx + eax*4]
004554c1: cmp       al, bl
004554c3: je        0x455554
004554c9: and       eax, 0xff
004554ce: cmp       eax, 0xc8
004554d3: je        0x455554
004554d9: jmp       0x455492
004554db: mov       dx, word ptr [esi + 0xa0]
004554e2: mov       eax, edx
004554e4: cmp       dx, 0xf
004554e8: jb        0x455526
004554ea: jbe       0x454cd5
004554f0: cmp       dx, 0x15
004554f4: jb        0x45550e
004554f6: jbe       0x454c93
004554fc: cmp       dx, 0x17
00455500: jb        0x455554
00455502: jbe       0x4551f6
00455508: cmp       dx, 0x18
0045550c: jmp       0x45554e
0045550e: cmp       dx, 0x12
00455512: jb        0x455554
00455514: jbe       0x454fad
0045551a: cmp       dx, 0x14
0045551e: je        0x454db5
00455524: jmp       0x455554
00455526: cmp       dx, 5
0045552a: jb        0x45554a
0045552c: jbe       0x4550ce
00455532: cmp       dx, 0xb
00455536: jb        0x455554
00455538: jbe       0x454c93
0045553e: cmp       dx, 0xd
00455542: je        0x4553b4
00455548: jmp       0x455554
0045554a: cmp       dx, 1
0045554e: je        0x455393
00455554: xor       eax, eax
00455556: mov       ax, word ptr [esi + 0xc2]
0045555d: cmp       eax, 0xffff
00455562: jne       0x45556e
00455564: mov       ax, word ptr [esi + 8]
00455568: cmp       ax, word ptr [esi + 0x7e]
0045556c: jne       0x4555a7
0045556e: xor       eax, eax
00455570: mov       ax, word ptr [esi + 0xc2]
00455577: cmp       eax, 0xffff
0045557c: je        0x45558d
0045557e: xor       edx, edx
00455580: mov       dx, word ptr [esi + 8]
00455584: call      0x42381f
00455589: test      al, al
0045558b: je        0x4555a7
0045558d: mov       eax, dword ptr [esi + 0x83]
00455593: sar       eax, 0x18
00455596: test      eax, eax
00455598: jne       0x4555a7
0045559a: mov       eax, dword ptr [esi + 0x84]
004555a0: sar       eax, 0x18
004555a3: test      eax, eax
004555a5: je        0x4555b6
004555a7: xor       eax, eax
004555a9: mov       ax, di
004555ac: call      0x44930c
004555b1: jmp       0x454ccd
004555b6: mov       ax, word ptr [esi + 0xc2]
004555bd: cmp       eax, 0xffff
004555c2: jne       0x455674
004555c8: xor       eax, eax
004555ca: mov       ax, word ptr [esi + 0x7e]
004555ce: call      0x476038
004555d3: and       eax, 0xff
004555d8: cmp       eax, 1
004555db: jne       0x455674
004555e1: xor       eax, eax
004555e3: mov       ax, word ptr [esi + 0x7e]
004555e7: xor       ecx, ecx
004555e9: call      0x476662
004555ee: mov       ax, word ptr [esi + 0x76]
004555f2: mov       cx, di
004555f5: mov       word ptr [esi + 4], ax
004555f9: mov       eax, ecx
004555fb: shl       eax, 4
004555fe: add       eax, ecx
00455600: mov       edx, ecx
00455602: shl       eax, 2
00455605: mov       word ptr [esi + 0x74], 0
0045560b: add       eax, ecx
0045560d: mov       ebx, dword ptr [0x4e19a0]
00455613: shl       eax, 2
00455616: xor       edx, ecx
00455618: add       ebx, eax
0045561a: xor       eax, eax
0045561c: mov       dl, byte ptr [0x508041]
00455622: mov       ax, word ptr [ebx + 8]
00455626: call      0x4766f0
0045562b: test      al, al
0045562d: je        0x455665
0045562f: mov       eax, ecx
00455631: call      0x440c5d
00455636: mov       ebp, dword ptr [ebx + 0x104]
0045563c: mov       byte ptr [ebx + 0xf9], 0
00455643: cmp       ebp, -1
00455646: jne       0x455665
00455648: push      eax
00455649: xor       edx, edx
0045564b: xor       ecx, ecx
0045564d: mov       dl, byte ptr [ebx + 1]
00455650: lea       eax, [ebx + 0x104]
00455656: shl       edx, 0x10
00455659: mov       ebx, eax
0045565b: mov       eax, 0x50
00455660: call      0x48aa79
00455665: xor       eax, eax
00455667: mov       ax, di
0045566a: call      0x45315f
0045566f: jmp       0x454ccd
00455674: xor       eax, eax
00455676: mov       ax, word ptr [esi + 0xc2]
0045567d: cmp       eax, 0xffff
00455682: je        0x45573d
00455688: call      0x41a4f4
0045568d: and       eax, 0xff
00455692: cmp       eax, 3
00455695: jne       0x45573d
0045569b: xor       eax, eax
0045569d: mov       ax, word ptr [esi + 0xc2]
004556a4: call      0x41a08c
004556a9: cmp       al, byte ptr [esi]
004556ab: jne       0x45573d
004556b1: xor       eax, eax
004556b3: xor       ecx, ecx
004556b5: mov       al, byte ptr [esi]
004556b7: xor       ebx, ebx
004556b9: push      eax
004556ba: xor       edx, edx
004556bc: mov       eax, 1
004556c1: call      0x4676e5
004556c6: test      al, al
004556c8: je        0x45573d
004556ca: mov       edx, 1
004556cf: xor       ebx, ebx
004556d1: mov       eax, edx
004556d3: mov       bl, byte ptr [esi]
004556d5: xor       ecx, ecx
004556d7: call      0x4235bd
004556dc: mov       ax, word ptr [esi + 0x76]
004556e0: mov       cx, di
004556e3: mov       word ptr [esi + 4], ax
004556e7: mov       eax, ecx
004556e9: shl       eax, 4
004556ec: add       eax, ecx
004556ee: mov       edx, ecx
004556f0: shl       eax, 2
004556f3: mov       word ptr [esi + 0x74], 0
004556f9: add       eax, ecx
004556fb: mov       ebx, dword ptr [0x4e19a0]
00455701: shl       eax, 2
00455704: xor       edx, ecx
00455706: add       ebx, eax
00455708: xor       eax, eax
0045570a: mov       dl, byte ptr [0x508041]
00455710: mov       ax, word ptr [ebx + 8]
00455714: call      0x4766f0
00455719: test      al, al
0045571b: je        0x455665
00455721: mov       eax, ecx
00455723: call      0x440c5d
00455728: mov       esi, dword ptr [ebx + 0x104]
0045572e: mov       byte ptr [ebx + 0xf9], 0
00455735: cmp       esi, -1
00455738: jmp       0x455646
0045573d: mov       ecx, 0x43
00455742: movzx     ebp, di
00455745: xor       edx, edx
00455747: xor       eax, eax
00455749: push      ebp
0045574a: mov       ebx, ecx
0045574c: mov       dl, byte ptr [esi + 0xbb]
00455752: mov       ax, word ptr [esi + 0x7c]
00455756: call      0x477b74
0045575b: xor       ecx, ecx
0045575d: mov       ebx, eax
0045575f: mov       cx, ax
00455762: mov       eax, ebp
00455764: shl       eax, 4
00455767: add       eax, ebp
00455769: shl       eax, 2
0045576c: add       eax, ebp
0045576e: shl       eax, 2
00455771: cmp       ecx, 0xffff
00455777: je        0x455837
0045577d: mov       byte ptr [esi + 2], 0x13
00455781: mov       edx, dword ptr [0x4e19a0]
00455787: add       eax, edx
00455789: mov       word ptr [eax + 0x7e], bx
0045578d: cmp       di, word ptr [0x496304]
00455794: jne       0x4557b8
00455796: mov       esi, 0xffff
0045579b: xor       bl, bl
0045579d: xor       edx, edx
0045579f: mov       byte ptr [0x4e0f36], bl
004557a5: mov       byte ptr [0x4e0f37], bl
004557ab: mov       dword ptr [0x4e0f3c], edx
004557b1: mov       word ptr [0x496304], si
004557b8: xor       ecx, ecx
004557ba: mov       cx, di
004557bd: mov       byte ptr [eax + 0x88], 0
004557c4: mov       eax, ecx
004557c6: shl       eax, 4
004557c9: add       eax, ecx
004557cb: shl       eax, 2
004557ce: mov       ebx, dword ptr [0x4e19a0]
004557d4: add       eax, ecx
004557d6: mov       edx, ecx
004557d8: shl       eax, 2
004557db: xor       edx, ecx
004557dd: add       ebx, eax
004557df: xor       eax, eax
004557e1: mov       dl, byte ptr [0x508041]
004557e7: mov       ax, word ptr [ebx + 8]
004557eb: call      0x4766f0
004557f0: test      al, al
004557f2: je        0x454ccd
004557f8: mov       eax, ecx
004557fa: call      0x440c5d
004557ff: mov       ecx, dword ptr [ebx + 0x104]
00455805: mov       byte ptr [ebx + 0xf9], 0
0045580c: cmp       ecx, -1
0045580f: jne       0x454ccd
00455815: push      eax
00455816: xor       edx, edx
00455818: xor       ecx, ecx
0045581a: mov       dl, byte ptr [ebx + 1]
0045581d: lea       eax, [ebx + 0x104]
00455823: shl       edx, 0x10
00455826: mov       ebx, eax
00455828: mov       eax, 0x50
0045582d: call      0x48aa79
00455832: jmp       0x454ccd
00455837: mov       dl, byte ptr [esi]
00455839: cmp       dl, byte ptr [0x508041]
0045583f: jne       0x455665
00455845: xor       edx, edx
00455847: mov       dx, word ptr [esi + 0x74]
0045584b: cmp       edx, 1
0045584e: jne       0x455665
00455854: mov       ebx, dword ptr [0x4e19a0]
0045585a: xor       edx, edx
0045585c: add       ebx, eax
0045585e: xor       eax, eax
00455860: mov       dl, byte ptr [0x508041]
00455866: mov       ax, word ptr [ebx + 8]
0045586a: call      0x4766f0
0045586f: test      al, al
00455871: je        0x455665
00455877: mov       eax, ebp
00455879: call      0x440c5d
0045587e: mov       ebp, dword ptr [ebx + 0x104]
00455884: mov       byte ptr [ebx + 0xf9], 0
0045588b: cmp       ebp, -1
0045588e: jne       0x455665
00455894: push      eax
00455895: xor       edx, edx
00455897: xor       ecx, ecx
00455899: mov       dl, byte ptr [ebx + 1]
0045589c: lea       eax, [ebx + 0x104]
004558a2: shl       edx, 0x10
004558a5: mov       ebx, eax
004558a7: mov       eax, 0x50
004558ac: or        dh, 0xc
004558af: jmp       0x455660
004558b4: xor       eax, eax
004558b6: mov       ax, word ptr [esi + 0xc0]
004558bd: cmp       eax, 0xffff
004558c2: je        0x454ccd
004558c8: call      0x41a70b
004558cd: test      al, al
004558cf: jne       0x454cbd
004558d5: xor       eax, eax
004558d7: mov       ax, di
004558da: call      0x449530
004558df: jmp       0x454ccd
004558e4: xor       eax, eax
004558e6: mov       ax, word ptr [esi + 0xc0]
004558ed: cmp       eax, 0xffff
004558f2: je        0x4559b2
004558f8: xor       eax, eax
004558fa: mov       ax, word ptr [esi + 0xc0]
00455901: call      0x41a70b
00455906: test      al, al
00455908: jne       0x454d97
0045590e: xor       eax, eax
00455910: mov       al, byte ptr [esi + 1]
00455913: cmp       eax, 0xa
00455916: jne       0x455965
00455918: xor       eax, eax
0045591a: mov       ax, word ptr [esi + 0xc0]
00455921: call      0x41a08c
00455926: and       eax, 0xff
0045592b: cmp       eax, 0xc8
00455930: je        0x454d97
00455936: xor       eax, eax
00455938: mov       ax, word ptr [esi + 0xc0]
0045593f: call      0x41a08c
00455944: cmp       al, byte ptr [esi]
00455946: jne       0x4559a3
00455948: xor       eax, eax
0045594a: mov       ax, word ptr [esi + 0xc0]
00455951: call      0x41a4f4
00455956: and       eax, 0xff
0045595b: cmp       eax, 0x10
0045595e: jne       0x4559a3
00455960: jmp       0x454d97
00455965: xor       eax, eax
00455967: mov       ax, word ptr [esi + 0xc0]
0045596e: call      0x41a08c
00455973: cmp       al, byte ptr [esi]
00455975: je        0x4559a3
00455977: xor       eax, eax
00455979: mov       ax, word ptr [esi + 0xc0]
00455980: call      0x41a08c
00455985: and       eax, 0xff
0045598a: cmp       eax, 0xc8
0045598f: jne       0x454d97
00455995: xor       eax, eax
00455997: mov       al, byte ptr [esi + 1]
0045599a: cmp       eax, 9
0045599d: jne       0x454d97
004559a3: xor       eax, eax
004559a5: mov       ax, di
004559a8: call      0x449716
004559ad: jmp       0x454ccd
004559b2: xor       eax, eax
004559b4: mov       ax, word ptr [esi + 0xb8]
004559bb: cmp       eax, 0xffff
004559c0: je        0x454ccd
004559c6: xor       edx, edx
004559c8: mov       dx, ax
004559cb: mov       ebx, eax
004559cd: mov       eax, edx
004559cf: shl       eax, 4
004559d2: add       eax, edx
004559d4: shl       eax, 2
004559d7: add       eax, edx
004559d9: mov       edx, dword ptr [0x4e19a0]
004559df: mov       al, byte ptr [edx + eax*4 + 2]
004559e3: and       eax, 0xff
004559e8: je        0x455a13
004559ea: xor       edx, edx
004559ec: mov       dx, bx
004559ef: mov       eax, edx
004559f1: shl       eax, 4
004559f4: add       eax, edx
004559f6: shl       eax, 2
004559f9: add       eax, edx
004559fb: mov       edx, dword ptr [0x4e19a0]
00455a01: mov       al, byte ptr [edx + eax*4 + 2]
00455a05: and       eax, 0xff
00455a0a: cmp       eax, 4
00455a0d: je        0x455a13
00455a0f: mov       al, 1
00455a11: jmp       0x455a15
00455a13: xor       al, al
00455a15: test      al, al
00455a17: je        0x455492
00455a1d: mov       ax, word ptr [esi + 0xb8]
00455a24: xor       edx, edx
00455a26: mov       dx, ax
00455a29: mov       eax, edx
00455a2b: shl       eax, 4
00455a2e: add       eax, edx
00455a30: shl       eax, 2
00455a33: add       eax, edx
00455a35: mov       edx, dword ptr [0x4e19a0]
00455a3b: mov       al, byte ptr [edx + eax*4]
00455a3e: cmp       al, byte ptr [esi]
00455a40: je        0x455a52
00455a42: and       eax, 0xff
00455a47: cmp       eax, 0xc8
00455a4c: jne       0x455492
00455a52: xor       eax, eax
00455a54: mov       ax, di
00455a57: call      0x44a2ed
00455a5c: jmp       0x454ccd
00455a61: mov       al, byte ptr [esi + 0x90]
00455a67: cmp       al, byte ptr [esi + 0x91]
00455a6d: je        0x455a7e
00455a6f: xor       eax, eax
00455a71: mov       ax, di
00455a74: call      0x448599
00455a79: jmp       0x454ccd
00455a7e: xor       edx, edx
00455a80: mov       dx, di
00455a83: mov       eax, edx
00455a85: shl       eax, 4
00455a88: add       eax, edx
00455a8a: shl       eax, 2
00455a8d: mov       cl, 7
00455a8f: add       edx, eax
00455a91: mov       eax, dword ptr [0x4e19a0]
00455a96: shl       edx, 2
00455a99: mov       ebx, edi
00455a9b: mov       al, byte ptr [edx + eax + 2]
00455a9f: and       eax, 0xff
00455aa4: je        0x455ad1
00455aa6: xor       edx, edx
00455aa8: mov       dx, di
00455aab: mov       eax, edx
00455aad: shl       eax, 4
00455ab0: add       eax, edx
00455ab2: shl       eax, 2
00455ab5: add       edx, eax
00455ab7: mov       eax, dword ptr [0x4e19a0]
00455abc: shl       edx, 2
00455abf: mov       al, byte ptr [edx + eax + 2]
00455ac3: and       eax, 0xff
00455ac8: cmp       eax, 4
00455acb: je        0x455ad1
00455acd: mov       al, 1
00455acf: jmp       0x455ad3
00455ad1: xor       al, al
00455ad3: test      al, al
00455ad5: je        0x454ccd
00455adb: xor       edx, edx
00455add: mov       dx, di
00455ae0: mov       eax, edx
00455ae2: shl       eax, 4
00455ae5: add       eax, edx
00455ae7: shl       eax, 2
00455aea: add       eax, edx
00455aec: mov       edx, dword ptr [0x4e19a0]
00455af2: mov       byte ptr [edx + eax*4 + 2], cl
00455af6: cmp       di, word ptr [0x496304]
00455afd: jne       0x454ccd
00455b03: xor       al, al
00455b05: xor       ebx, ebx
00455b07: mov       byte ptr [0x4e0f36], al
00455b0c: mov       dword ptr [0x4e0f3c], ebx
00455b12: mov       ebx, 0xffff
00455b17: mov       byte ptr [0x4e0f37], al
00455b1c: mov       word ptr [0x496304], bx
00455b23: jmp       0x454ccd
00455b28: xor       eax, eax
00455b2a: mov       ax, word ptr [esi + 0xc0]
00455b31: call      0x41a70b
00455b36: test      al, al
00455b38: jne       0x455b50
00455b3a: xor       eax, eax
00455b3c: mov       ax, word ptr [esi + 0xc0]
00455b43: call      0x41a08c
00455b48: cmp       al, byte ptr [esi]
00455b4a: je        0x455c17
00455b50: xor       ecx, ecx
00455b52: mov       cx, di
00455b55: mov       ebp, ecx
00455b57: shl       ebp, 4
00455b5a: add       ebp, ecx
00455b5c: shl       ebp, 2
00455b5f: add       ebp, ecx
00455b61: mov       ebx, dword ptr [0x4e19a0]
00455b67: shl       ebp, 2
00455b6a: add       ebx, ebp
00455b6c: mov       al, byte ptr [ebx + 0x72]
00455b6f: test      al, al
00455b71: jne       0x454ea6
00455b77: mov       ax, word ptr [ebx + 8]
00455b7b: xor       edx, edx
00455b7d: mov       dx, ax
00455b80: mov       eax, ecx
00455b82: call      0x442cb4
00455b87: mov       byte ptr [ebx + 0x72], 1
00455b8b: mov       ecx, dword ptr [0x4e19a0]
00455b91: add       ecx, ebp
00455b93: xor       ebx, ebx
00455b95: mov       ax, word ptr [ecx + 8]
00455b99: mov       bl, byte ptr [ecx]
00455b9b: mov       dword ptr [esp + 0x3c], eax
00455b9f: cmp       ebx, 0xc8
00455ba5: je        0x455c04
00455ba7: cmp       ebx, 4
00455baa: je        0x455c04
00455bac: xor       ah, ah
00455bae: mov       al, byte ptr [ecx + 0xbb]
00455bb4: add       eax, 2
00455bb9: mov       dword ptr [esp + 0x48], eax
00455bbd: xor       ah, ah
00455bbf: mov       edx, dword ptr [esp + 0x48]
00455bc3: mov       al, byte ptr [ecx + 0xf5]
00455bc9: add       eax, edx
00455bcb: xor       edx, edx
00455bcd: movzx     ebp, word ptr [esp + 0x3c]
00455bd2: mov       dx, ax
00455bd5: mov       eax, ebp
00455bd7: call      0x476851
00455bdc: xor       ah, ah
00455bde: mov       al, byte ptr [ecx + 0xbb]
00455be4: mov       dword ptr [esp + 0x48], eax
00455be8: mov       edx, dword ptr [esp + 0x48]
00455bec: mov       al, byte ptr [ecx + 0xf5]
00455bf2: xor       ebx, ebx
00455bf4: add       eax, edx
00455bf6: xor       edx, edx
00455bf8: mov       bl, byte ptr [ecx]
00455bfa: mov       dx, ax
00455bfd: mov       eax, ebp
00455bff: call      0x476cb3
00455c04: mov       edx, 4
00455c09: xor       ebx, ebx
00455c0b: xor       eax, eax
00455c0d: mov       bx, word ptr [esp + 0x3c]
00455c12: jmp       0x454e9f
00455c17: xor       eax, eax
00455c19: mov       al, byte ptr [esi + 0x82]
00455c1f: cmp       eax, 2
00455c22: jne       0x455d17
00455c28: xor       eax, eax
00455c2a: mov       ax, word ptr [esi + 0x80]
00455c31: call      0x41a70b
00455c36: test      al, al
00455c38: jne       0x455c50
00455c3a: xor       eax, eax
00455c3c: mov       ax, word ptr [esi + 0x80]
00455c43: call      0x41a08c
00455c48: cmp       al, byte ptr [esi]
00455c4a: je        0x455d17
00455c50: xor       ecx, ecx
00455c52: mov       cx, di
00455c55: mov       ebp, ecx
00455c57: shl       ebp, 4
00455c5a: add       ebp, ecx
00455c5c: shl       ebp, 2
00455c5f: add       ebp, ecx
00455c61: mov       ebx, dword ptr [0x4e19a0]
00455c67: shl       ebp, 2
00455c6a: add       ebx, ebp
00455c6c: mov       al, byte ptr [ebx + 0x72]
00455c6f: test      al, al
00455c71: jne       0x454ea6
00455c77: mov       ax, word ptr [ebx + 8]
00455c7b: xor       edx, edx
00455c7d: mov       dx, ax
00455c80: mov       eax, ecx
00455c82: call      0x442cb4
00455c87: mov       byte ptr [ebx + 0x72], 1
00455c8b: mov       ecx, dword ptr [0x4e19a0]
00455c91: add       ecx, ebp
00455c93: xor       ebx, ebx
00455c95: mov       ax, word ptr [ecx + 8]
00455c99: mov       bl, byte ptr [ecx]
00455c9b: mov       dword ptr [esp + 0x10], eax
00455c9f: cmp       ebx, 0xc8
00455ca5: je        0x455d04
00455ca7: cmp       ebx, 4
00455caa: je        0x455d04
00455cac: xor       ah, ah
00455cae: mov       al, byte ptr [ecx + 0xbb]
00455cb4: add       eax, 2
00455cb9: mov       dword ptr [esp + 0x48], eax
00455cbd: xor       ah, ah
00455cbf: mov       edx, dword ptr [esp + 0x48]
00455cc3: mov       al, byte ptr [ecx + 0xf5]
00455cc9: add       eax, edx
00455ccb: xor       edx, edx
00455ccd: movzx     ebp, word ptr [esp + 0x10]
00455cd2: mov       dx, ax
00455cd5: mov       eax, ebp
00455cd7: call      0x476851
00455cdc: xor       ah, ah
00455cde: mov       al, byte ptr [ecx + 0xbb]
00455ce4: mov       dword ptr [esp + 0x48], eax
00455ce8: mov       edx, dword ptr [esp + 0x48]
00455cec: mov       al, byte ptr [ecx + 0xf5]
00455cf2: xor       ebx, ebx
00455cf4: add       eax, edx
00455cf6: xor       edx, edx
00455cf8: mov       bl, byte ptr [ecx]
00455cfa: mov       dx, ax
00455cfd: mov       eax, ebp
00455cff: call      0x476cb3
00455d04: mov       edx, 4
00455d09: xor       ebx, ebx
00455d0b: xor       eax, eax
00455d0d: mov       bx, word ptr [esp + 0x10]
00455d12: jmp       0x454e9f
00455d17: xor       eax, eax
00455d19: mov       ax, di
00455d1c: call      0x44e35c
00455d21: jmp       0x454ccd
00455d26: xor       eax, eax
00455d28: mov       al, byte ptr [esi + 0x82]
00455d2e: cmp       eax, 2
00455d31: jne       0x455e23
00455d37: xor       eax, eax
00455d39: mov       ax, word ptr [esi + 0x80]
00455d40: call      0x41a70b
00455d45: test      al, al
00455d47: jne       0x455d5f
00455d49: xor       eax, eax
00455d4b: mov       ax, word ptr [esi + 0x80]
00455d52: call      0x41a08c
00455d57: cmp       al, byte ptr [esi]
00455d59: je        0x455e23
00455d5f: movzx     ebp, di
00455d62: mov       ecx, ebp
00455d64: shl       ecx, 4
00455d67: add       ecx, ebp
00455d69: shl       ecx, 2
00455d6c: add       ecx, ebp
00455d6e: mov       ebx, dword ptr [0x4e19a0]
00455d74: shl       ecx, 2
00455d77: add       ebx, ecx
00455d79: mov       al, byte ptr [ebx + 0x72]
00455d7c: test      al, al
00455d7e: jne       0x4550a9
00455d84: mov       ax, word ptr [ebx + 8]
00455d88: xor       edx, edx
00455d8a: mov       dx, ax
00455d8d: mov       eax, ebp
00455d8f: call      0x442cb4
00455d94: mov       byte ptr [ebx + 0x72], 1
00455d98: mov       eax, dword ptr [0x4e19a0]
00455d9d: add       ecx, eax
00455d9f: xor       ebx, ebx
00455da1: mov       ax, word ptr [ecx + 8]
00455da5: mov       bl, byte ptr [ecx]
00455da7: mov       dword ptr [esp + 0x38], eax
00455dab: cmp       ebx, 0xc8
00455db1: je        0x455e10
00455db3: cmp       ebx, 4
00455db6: je        0x455e10
00455db8: xor       ah, ah
00455dba: mov       al, byte ptr [ecx + 0xbb]
00455dc0: add       eax, 2
00455dc5: mov       dword ptr [esp + 0x48], eax
00455dc9: xor       ah, ah
00455dcb: mov       edx, dword ptr [esp + 0x48]
00455dcf: mov       al, byte ptr [ecx + 0xf5]
00455dd5: add       eax, edx
00455dd7: xor       edx, edx
00455dd9: movzx     ebp, word ptr [esp + 0x38]
00455dde: mov       dx, ax
00455de1: mov       eax, ebp
00455de3: call      0x476851
00455de8: xor       ah, ah
00455dea: mov       al, byte ptr [ecx + 0xbb]
00455df0: mov       dword ptr [esp + 0x48], eax
00455df4: mov       edx, dword ptr [esp + 0x48]
00455df8: mov       al, byte ptr [ecx + 0xf5]
00455dfe: xor       ebx, ebx
00455e00: add       eax, edx
00455e02: xor       edx, edx
00455e04: mov       bl, byte ptr [ecx]
00455e06: mov       dx, ax
00455e09: mov       eax, ebp
00455e0b: call      0x476cb3
00455e10: mov       edx, 4
00455e15: xor       ebx, ebx
00455e17: xor       eax, eax
00455e19: mov       bx, word ptr [esp + 0x38]
00455e1e: jmp       0x4550a2
00455e23: xor       eax, eax
00455e25: mov       ax, di
00455e28: call      0x44f2d4
00455e2d: jmp       0x454ccd
00455e32: mov       ax, word ptr [esi + 8]
00455e36: cmp       ax, word ptr [esi + 0x7e]
00455e3a: jne       0x4555a7
00455e40: xor       eax, eax
00455e42: mov       al, byte ptr [esi + 2]
00455e45: cmp       eax, 0x10
00455e48: jne       0x455fa6
00455e4e: xor       eax, eax
00455e50: mov       ax, word ptr [esi + 8]
00455e54: call      0x476038
00455e59: mov       dh, al
00455e5b: mov       dl, al
00455e5d: xor       eax, eax
00455e5f: mov       ax, word ptr [esi + 8]
00455e63: call      0x4766b1
00455e68: test      al, al
00455e6a: je        0x455f1b
00455e70: lea       eax, [esi + 0xa]
00455e73: xor       ebx, ebx
00455e75: mov       bx, word ptr [eax + 0x66]
00455e79: inc       ebx
00455e7a: mov       ax, word ptr [eax + 2]
00455e7e: and       eax, 0xffff
00455e83: cmp       ebx, eax
00455e85: setle     al
00455e88: test      al, al
00455e8a: je        0x455f1b
00455e90: xor       eax, eax
00455e92: mov       al, byte ptr [esi + 1]
00455e95: cmp       eax, 7
00455e98: jne       0x455ea3
00455e9a: xor       eax, eax
00455e9c: mov       al, dh
00455e9e: cmp       eax, 2
00455ea1: je        0x455ec8
00455ea3: xor       eax, eax
00455ea5: mov       al, byte ptr [esi + 1]
00455ea8: cmp       eax, 5
00455eab: jne       0x455eb6
00455ead: xor       eax, eax
00455eaf: mov       al, dl
00455eb1: cmp       eax, 1
00455eb4: je        0x455ec8
00455eb6: xor       eax, eax
00455eb8: mov       al, byte ptr [esi + 1]
00455ebb: cmp       eax, 6
00455ebe: jne       0x455f1b
00455ec0: xor       eax, eax
00455ec2: mov       al, dl
00455ec4: test      eax, eax
00455ec6: jne       0x455f1b
00455ec8: xor       eax, eax
00455eca: xor       ch, ch
00455ecc: mov       ax, word ptr [esi + 8]
00455ed0: xor       edx, edx
00455ed2: call      0x476662
00455ed7: mov       dx, di
00455eda: mov       cl, al
00455edc: mov       eax, edx
00455ede: shl       eax, 4
00455ee1: add       eax, edx
00455ee3: shl       eax, 2
00455ee6: add       eax, edx
00455ee8: mov       edx, dword ptr [0x4e19a0]
00455eee: shl       eax, 2
00455ef1: add       eax, edx
00455ef3: mov       dx, word ptr [eax + 0x70]
00455ef7: add       eax, 0xa
00455efa: inc       edx
00455efb: mov       word ptr [eax + 0x66], dx
00455eff: xor       ebx, ebx
00455f01: mov       dx, word ptr [eax]
00455f04: mov       bx, dx
00455f07: mov       edx, ebx
00455f09: mov       byte ptr [ebx + eax + 0x42], 2
00455f0e: mov       word ptr [eax + edx*2 + 6], cx
00455f13: inc       word ptr [eax]
00455f16: jmp       0x454ccd
00455f1b: xor       edx, edx
00455f1d: mov       dx, di
00455f20: mov       eax, edx
00455f22: shl       eax, 4
00455f25: add       eax, edx
00455f27: shl       eax, 2
00455f2a: add       eax, edx
00455f2c: mov       edx, dword ptr [0x4e19a0]
00455f32: shl       eax, 2
00455f35: add       edx, eax
00455f37: xor       eax, eax
00455f39: mov       cl, 7
00455f3b: mov       al, byte ptr [edx + 2]
00455f3e: mov       ebx, edi
00455f40: test      eax, eax
00455f42: je        0x455f4d
00455f44: cmp       eax, 4
00455f47: je        0x455f4d
00455f49: mov       al, 1
00455f4b: jmp       0x455f4f
00455f4d: xor       al, al
00455f4f: test      al, al
00455f51: je        0x455f98
00455f53: xor       edx, edx
00455f55: mov       dx, bx
00455f58: mov       eax, edx
00455f5a: shl       eax, 4
00455f5d: add       eax, edx
00455f5f: shl       eax, 2
00455f62: add       eax, edx
00455f64: mov       edx, dword ptr [0x4e19a0]
00455f6a: mov       byte ptr [edx + eax*4 + 2], cl
00455f6e: cmp       bx, word ptr [0x496304]
00455f75: jne       0x455f98
00455f77: mov       edi, 0xffff
00455f7c: xor       ch, ch
00455f7e: xor       eax, eax
00455f80: mov       byte ptr [0x4e0f36], ch
00455f86: mov       byte ptr [0x4e0f37], ch
00455f8c: mov       dword ptr [0x4e0f3c], eax
00455f91: mov       word ptr [0x496304], di
00455f98: mov       word ptr [esi + 0xb2], 0xffff
00455fa1: jmp       0x454ccd
00455fa6: cmp       eax, 0x11
00455fa9: jne       0x454ccd
00455faf: xor       ebx, ebx
00455fb1: xor       ecx, ecx
00455fb3: xor       edx, edx
00455fb5: mov       cx, di
00455fb8: mov       bx, word ptr [esi + 0x84]
00455fbf: mov       dl, byte ptr [esi + 0x82]
00455fc5: mov       eax, ecx
00455fc7: call      0x4438d8
00455fcc: xor       edx, edx
00455fce: mov       eax, ecx
00455fd0: mov       dx, word ptr [esi + 0x7c]
00455fd4: call      0x4457d3
00455fd9: mov       byte ptr [esi + 0x82], 0
00455fe0: jmp       0x455f98
00455fe2: xor       eax, eax
00455fe4: mov       ax, word ptr [esi + 0xc0]
00455feb: call      0x41a70b
00455ff0: test      al, al
00455ff2: jne       0x454d97
00455ff8: xor       eax, eax
00455ffa: mov       ax, word ptr [esi + 0xc0]
00456001: call      0x41a08c
00456006: and       eax, 0xff
0045600b: cmp       eax, 0xc8
00456010: je        0x454d97
00456016: xor       eax, eax
00456018: mov       ax, word ptr [esi + 0xc0]
0045601f: call      0x41a08c
00456024: cmp       al, byte ptr [esi]
00456026: je        0x454d97
0045602c: xor       edx, edx
0045602e: xor       eax, eax
00456030: mov       dx, word ptr [esi + 8]
00456034: mov       ax, word ptr [esi + 0xc0]
0045603b: call      0x42381f
00456040: test      al, al
00456042: jne       0x4560b5
00456044: mov       ax, word ptr [esi + 0x7e]
00456048: cmp       ax, word ptr [esi + 8]
0045604c: jne       0x4555a7
00456052: xor       eax, eax
00456054: mov       ax, word ptr [esi + 0xc0]
0045605b: xor       edx, edx
0045605d: call      0x41aee2
00456062: mov       dx, di
00456065: mov       ebx, eax
00456067: mov       eax, edx
00456069: shl       eax, 4
0045606c: add       eax, edx
0045606e: shl       eax, 2
00456071: add       edx, eax
00456073: mov       eax, dword ptr [0x4e19a0]
00456078: shl       edx, 2
0045607b: add       eax, edx
0045607d: mov       word ptr [eax + 0x7e], bx
00456081: cmp       di, word ptr [0x496304]
00456088: jne       0x4560a9
0045608a: xor       dl, dl
0045608c: mov       byte ptr [0x4e0f36], dl
00456092: mov       byte ptr [0x4e0f37], dl
00456098: xor       edx, edx
0045609a: mov       dword ptr [0x4e0f3c], edx
004560a0: mov       word ptr [0x496304], 0xffff
004560a9: mov       byte ptr [eax + 0x88], 0
004560b0: jmp       0x4555a7
004560b5: xor       eax, eax
004560b7: mov       ax, word ptr [esi + 0xc0]
004560be: xor       edx, edx
004560c0: call      0x41a08c
004560c5: mov       dx, di
004560c8: mov       cl, al
004560ca: mov       eax, edx
004560cc: shl       eax, 4
004560cf: add       eax, edx
004560d1: shl       eax, 2
004560d4: add       eax, edx
004560d6: mov       edx, dword ptr [0x4e19a0]
004560dc: xor       ebx, ebx
004560de: mov       al, byte ptr [edx + eax*4]
004560e1: mov       edx, 0x64
004560e6: mov       byte ptr [esp + 0x5c], al
004560ea: mov       byte ptr [esp + 0x54], al
004560ee: movzx     ebp, al
004560f1: mov       dword ptr [esp + 0xc], edx
004560f5: mov       bl, byte ptr [ebp + 0x4e19bc]
004560fb: xor       eax, eax
004560fd: xor       edx, edx
004560ff: call      0x4704dc
00456104: div       dword ptr [esp + 0xc]
00456108: cmp       edx, ebx
0045610a: jbe       0x4561d6
00456110: xor       eax, eax
00456112: mov       al, byte ptr [ebp + 0x4e19bc]
00456118: cmp       eax, 5
0045611b: jl        0x45612a
0045611d: mov       ah, al
0045611f: sub       ah, 5
00456122: mov       byte ptr [ebp + 0x4e19bc], ah
00456128: jmp       0x456132
0045612a: xor       al, al
0045612c: mov       byte ptr [ebp + 0x4e19bc], al
00456132: xor       edx, edx
00456134: mov       dx, di
00456137: mov       eax, edx
00456139: call      0x457058
0045613e: mov       eax, edx
00456140: shl       eax, 4
00456143: add       eax, edx
00456145: shl       eax, 2
00456148: add       eax, edx
0045614a: mov       edx, dword ptr [0x4e19a0]
00456150: xor       bl, bl
00456152: mov       al, byte ptr [edx + eax*4 + 2]
00456156: and       eax, 0xff
0045615b: je        0x456166
0045615d: cmp       eax, 4
00456160: je        0x456166
00456162: mov       al, 1
00456164: jmp       0x456168
00456166: xor       al, al
00456168: test      al, al
0045616a: je        0x4561b2
0045616c: xor       edx, edx
0045616e: mov       dx, di
00456171: mov       eax, edx
00456173: shl       eax, 4
00456176: add       eax, edx
00456178: shl       eax, 2
0045617b: add       eax, edx
0045617d: mov       edx, dword ptr [0x4e19a0]
00456183: mov       byte ptr [edx + eax*4 + 2], bl
00456187: cmp       di, word ptr [0x496304]
0045618e: jne       0x4561b2
00456190: mov       ecx, 0xffff
00456195: xor       dl, dl
00456197: xor       esi, esi
00456199: mov       byte ptr [0x4e0f36], dl
0045619f: mov       byte ptr [0x4e0f37], dl
004561a5: mov       dword ptr [0x4e0f3c], esi
004561ab: mov       word ptr [0x496304], cx
004561b2: mov       al, byte ptr [esp + 0x54]
004561b6: cmp       al, byte ptr [0x508041]
004561bc: jne       0x454ccd
004561c2: mov       edx, 0x1f6
004561c7: mov       eax, 0xa
004561cc: call      0x46994b
004561d1: jmp       0x454ccd
004561d6: xor       eax, eax
004561d8: mov       ebx, 0xa
004561dd: mov       ax, word ptr [esi + 0xc4]
004561e4: mov       dword ptr [esp + 0x2c], ebx
004561e8: cmp       eax, 3
004561eb: je        0x4562bc
004561f1: mov       ebx, 3
004561f6: xor       edx, edx
004561f8: xor       eax, eax
004561fa: mov       dl, byte ptr [esp + 0x5c]
004561fe: mov       al, cl
00456200: call      0x475118
00456205: mov       ebx, esp
00456207: xor       eax, eax
00456209: lea       edx, [esp + 4]
0045620d: mov       al, cl
0045620f: lea       ecx, [esp + 0x18]
00456213: push      eax
00456214: mov       dword ptr [esp + 0x10], eax
00456218: lea       eax, [esp + 6]
0045621c: call      0x46769d
00456221: mov       edx, 3
00456226: mov       eax, ebp
00456228: call      0x461222
0045622d: mov       dword ptr [esp + 0x48], eax
00456231: mov       bl, byte ptr [esi + 0xc4]
00456237: and       ebx, 0xff
0045623d: mov       ecx, 3
00456242: mov       edx, ebx
00456244: mov       eax, ebx
00456246: sar       edx, 0x1f
00456249: idiv      ecx
0045624b: movzx     esi, dl
0045624e: xor       edx, edx
00456250: mov       dx, word ptr [esp + esi*2]
00456254: mov       eax, edx
00456256: sar       edx, 0x1f
00456259: sub       eax, edx
0045625b: sar       eax, 1
0045625d: xor       edx, edx
0045625f: mov       ebx, dword ptr [esp + 0xc]
00456263: mov       dx, ax
00456266: mov       eax, esi
00456268: call      0x4235bd
0045626d: xor       edx, edx
0045626f: mov       dx, word ptr [esp + esi*2]
00456273: mov       eax, edx
00456275: sar       edx, 0x1f
00456278: sub       eax, edx
0045627a: sar       eax, 1
0045627c: xor       ebx, ebx
0045627e: mov       bx, word ptr [esp + 0x48]
00456283: mov       ecx, ebx
00456285: xor       edx, edx
00456287: mov       ebx, ebp
00456289: mov       dx, ax
0045628c: mov       eax, esi
0045628e: call      0x42340f
00456293: mov       al, byte ptr [esp + 0x5c]
00456297: xor       esi, esi
00456299: mov       bh, byte ptr [0x508041]
0045629f: mov       dword ptr [esp + 0x2c], esi
004562a3: cmp       al, bh
004562a5: jne       0x456324
004562ab: mov       edx, 0x1f5
004562b0: mov       eax, 0xa
004562b5: call      0x46994b
004562ba: jmp       0x456324
004562bc: mov       ebx, 4
004562c1: xor       edx, edx
004562c3: xor       eax, eax
004562c5: mov       dl, byte ptr [esp + 0x5c]
004562c9: mov       al, cl
004562cb: call      0x475118
004562d0: xor       ebx, ebx
004562d2: mov       bl, cl
004562d4: mov       eax, ebx
004562d6: xor       ecx, ecx
004562d8: call      0x4717b1
004562dd: mov       cl, al
004562df: mov       edx, ecx
004562e1: mov       eax, ebp
004562e3: call      0x4717c2
004562e8: mov       esi, eax
004562ea: mov       edx, ecx
004562ec: mov       eax, ebx
004562ee: call      0x4717c2
004562f3: cmp       si, ax
004562f6: jae       0x456324
004562f8: mov       al, byte ptr [esp + 0x5c]
004562fc: cmp       al, byte ptr [0x508041]
00456302: jne       0x456313
00456304: mov       edx, 0x1f5
00456309: mov       eax, 0xa
0045630e: call      0x46994b
00456313: xor       eax, eax
00456315: mov       al, byte ptr [esp + 0x54]
00456319: xor       ecx, ecx
0045631b: call      0x47149d
00456320: mov       dword ptr [esp + 0x2c], ecx
00456324: xor       eax, eax
00456326: mov       ax, word ptr [esp + 0x2c]
0045632b: cmp       eax, 0xa
0045632e: je        0x45634d
00456330: xor       ebx, ebx
00456332: mov       bl, byte ptr [esp + 0x54]
00456336: xor       edx, edx
00456338: mov       dl, byte ptr [ebx + 0x4e19bc]
0045633e: mov       eax, edx
00456340: sar       edx, 0x1f
00456343: sub       eax, edx
00456345: sar       eax, 1
00456347: mov       byte ptr [ebx + 0x4e19bc], al
0045634d: xor       edx, edx
0045634f: mov       dx, di
00456352: mov       eax, edx
00456354: call      0x457058
00456359: mov       eax, edx
0045635b: shl       eax, 4
0045635e: add       eax, edx
00456360: shl       eax, 2
00456363: add       eax, edx
00456365: mov       edx, dword ptr [0x4e19a0]
0045636b: xor       bl, bl
0045636d: mov       al, byte ptr [edx + eax*4 + 2]
00456371: and       eax, 0xff
00456376: je        0x456381
00456378: cmp       eax, 4
0045637b: je        0x456381
0045637d: mov       al, 1
0045637f: jmp       0x456383
00456381: xor       al, al
00456383: test      al, al
00456385: je        0x454ccd
0045638b: xor       edx, edx
0045638d: mov       dx, di
00456390: mov       eax, edx
00456392: shl       eax, 4
00456395: add       eax, edx
00456397: shl       eax, 2
0045639a: add       eax, edx
0045639c: mov       edx, dword ptr [0x4e19a0]
004563a2: mov       byte ptr [edx + eax*4 + 2], bl
004563a6: cmp       di, word ptr [0x496304]
004563ad: jne       0x454ccd
004563b3: xor       cl, cl
004563b5: mov       edx, 0xffff
004563ba: mov       byte ptr [0x4e0f36], cl
004563c0: mov       byte ptr [0x4e0f37], cl
004563c6: xor       ecx, ecx
004563c8: mov       word ptr [0x496304], dx
004563cf: mov       dword ptr [0x4e0f3c], ecx
004563d5: jmp       0x454ccd
004563da: mov       ax, word ptr [esi + 0x7e]
004563de: cmp       ax, word ptr [esi + 8]
004563e2: jne       0x4555a7
004563e8: mov       al, byte ptr [esi + 0x91]
004563ee: cmp       al, byte ptr [esi + 0x90]
004563f4: jne       0x455a6f
004563fa: xor       eax, eax
004563fc: mov       ax, di
004563ff: call      0x448194
00456404: test      al, al
00456406: jne       0x456447
00456408: xor       edx, edx
0045640a: mov       dx, di
0045640d: mov       eax, edx
0045640f: shl       eax, 4
00456412: add       eax, edx
00456414: shl       eax, 2
00456417: add       eax, edx
00456419: mov       ebx, dword ptr [0x4e19a0]
0045641f: shl       eax, 2
00456422: add       ebx, eax
00456424: xor       edx, edx
00456426: mov       dl, byte ptr [ebx + 0xa4]
0045642c: xor       ecx, ecx
0045642e: inc       edx
0045642f: mov       cl, byte ptr [ebx + 0xa5]
00456435: mov       eax, edx
00456437: sar       edx, 0x1f
0045643a: idiv      ecx
0045643c: mov       byte ptr [ebx + 0xa4], dl
00456442: jmp       0x454ccd
00456447: xor       edx, edx
00456449: mov       dx, di
0045644c: mov       eax, edx
0045644e: shl       eax, 4
00456451: add       eax, edx
00456453: shl       eax, 2
00456456: add       eax, edx
00456458: mov       edx, dword ptr [0x4e19a0]
0045645e: mov       cl, 7
00456460: mov       ebx, edi
00456462: mov       al, byte ptr [edx + eax*4 + 2]
00456466: and       eax, 0xff
0045646b: je        0x456496
0045646d: xor       edx, edx
0045646f: mov       dx, di
00456472: mov       eax, edx
00456474: shl       eax, 4
00456477: add       eax, edx
00456479: shl       eax, 2
0045647c: add       eax, edx
0045647e: mov       edx, dword ptr [0x4e19a0]
00456484: mov       al, byte ptr [edx + eax*4 + 2]
00456488: and       eax, 0xff
0045648d: cmp       eax, 4
00456490: je        0x456496
00456492: mov       al, 1
00456494: jmp       0x456498
00456496: xor       al, al
00456498: test      al, al
0045649a: je        0x454ccd
004564a0: xor       edx, edx
004564a2: mov       dx, di
004564a5: mov       eax, edx
004564a7: shl       eax, 4
004564aa: add       eax, edx
004564ac: shl       eax, 2
004564af: add       eax, edx
004564b1: mov       edx, dword ptr [0x4e19a0]
004564b7: mov       byte ptr [edx + eax*4 + 2], cl
004564bb: cmp       di, word ptr [0x496304]
004564c2: jne       0x454ccd
004564c8: mov       edi, 0xffff
004564cd: xor       dh, dh
004564cf: xor       ecx, ecx
004564d1: mov       byte ptr [0x4e0f36], dh
004564d7: mov       byte ptr [0x4e0f37], dh
004564dd: mov       dword ptr [0x4e0f3c], ecx
004564e3: mov       word ptr [0x496304], di
004564ea: jmp       0x454ccd
004564ef: xor       eax, eax
004564f1: mov       al, byte ptr [esi + 0x89]
004564f7: test      eax, eax
004564f9: je        0x456511
004564fb: xor       eax, eax
004564fd: mov       ax, word ptr [esi + 0xc0]
00456504: call      0x41a70b
00456509: test      al, al
0045650b: jne       0x454cbd
00456511: xor       eax, eax
00456513: mov       ax, di
00456516: call      0x44ab60
0045651b: jmp       0x454ccd
00456520: xor       eax, eax
00456522: mov       ax, di
00456525: call      0x44a706
0045652a: jmp       0x454ccd
0045652f: xor       edx, edx
00456531: mov       dx, di
00456534: mov       eax, edx
00456536: shl       eax, 4
00456539: add       eax, edx
0045653b: shl       eax, 2
0045653e: add       edx, eax
00456540: mov       eax, dword ptr [0x4e19a0]
00456545: shl       edx, 2
00456548: mov       al, byte ptr [edx + eax + 1]
0045654c: and       eax, 0xff
00456551: cmp       eax, 6
00456554: jne       0x4565b4
00456556: mov       bx, word ptr [esi + 0xc0]
0045655d: xor       edx, edx
0045655f: mov       dx, bx
00456562: mov       eax, edx
00456564: shl       eax, 4
00456567: add       eax, edx
00456569: shl       eax, 2
0045656c: add       eax, edx
0045656e: mov       edx, dword ptr [0x4e19a0]
00456574: mov       al, byte ptr [edx + eax*4 + 2]
00456578: and       eax, 0xff
0045657d: je        0x4565aa
0045657f: xor       edx, edx
00456581: mov       dx, bx
00456584: mov       eax, edx
00456586: shl       eax, 4
00456589: add       eax, edx
0045658b: shl       eax, 2
0045658e: add       edx, eax
00456590: mov       eax, dword ptr [0x4e19a0]
00456595: shl       edx, 2
00456598: mov       al, byte ptr [edx + eax + 2]
0045659c: and       eax, 0xff
004565a1: cmp       eax, 4
004565a4: je        0x4565aa
004565a6: mov       al, 1
004565a8: jmp       0x4565ac
004565aa: xor       al, al
004565ac: test      al, al
004565ae: je        0x454d97
004565b4: xor       edx, edx
004565b6: mov       dx, di
004565b9: mov       eax, edx
004565bb: shl       eax, 4
004565be: add       eax, edx
004565c0: shl       eax, 2
004565c3: add       edx, eax
004565c5: mov       eax, dword ptr [0x4e19a0]
004565ca: shl       edx, 2
004565cd: mov       al, byte ptr [edx + eax + 1]
004565d1: and       eax, 0xff
004565d6: cmp       eax, 7
004565d9: jne       0x4565f1
004565db: xor       eax, eax
004565dd: mov       ax, word ptr [esi + 0xc0]
004565e4: call      0x41a70b
004565e9: test      al, al
004565eb: jne       0x454d97
004565f1: xor       eax, eax
004565f3: mov       ax, di
004565f6: call      0x44b5f5
004565fb: jmp       0x454ccd
00456600: xor       eax, eax
00456602: mov       al, byte ptr [esi + 0x82]
00456608: cmp       eax, 2
0045660b: jne       0x45672c
00456611: xor       eax, eax
00456613: mov       ax, word ptr [esi + 0x80]
0045661a: call      0x41a70b
0045661f: test      al, al
00456621: jne       0x456639
00456623: xor       eax, eax
00456625: mov       ax, word ptr [esi + 0x80]
0045662c: call      0x41a08c
00456631: cmp       al, byte ptr [esi]
00456633: je        0x45672c
00456639: xor       edx, edx
0045663b: mov       dx, di
0045663e: mov       eax, edx
00456640: shl       eax, 4
00456643: add       eax, edx
00456645: shl       eax, 2
00456648: add       eax, edx
0045664a: mov       edx, dword ptr [0x4e19a0]
00456650: mov       al, byte ptr [edx + eax*4 + 0x72]
00456654: test      al, al
00456656: jne       0x4550a9
0045665c: xor       eax, eax
0045665e: mov       al, byte ptr [esi + 1]
00456661: cmp       eax, 7
00456664: jne       0x456674
00456666: xor       eax, eax
00456668: mov       ax, word ptr [esi + 0xb2]
0045666f: call      0x4754de
00456674: xor       ecx, ecx
00456676: mov       cx, di
00456679: mov       ebp, ecx
0045667b: shl       ebp, 4
0045667e: add       ebp, ecx
00456680: shl       ebp, 2
00456683: mov       ebx, dword ptr [0x4e19a0]
00456689: add       ebp, ecx
0045668b: mov       edx, ecx
0045668d: shl       ebp, 2
00456690: xor       edx, ecx
00456692: mov       ax, word ptr [ebx + ebp + 8]
00456697: mov       dx, ax
0045669a: mov       eax, ecx
0045669c: call      0x442cb4
004566a1: mov       byte ptr [ebx + ebp + 0x72], 1
004566a6: mov       ecx, dword ptr [0x4e19a0]
004566ac: add       ecx, ebp
004566ae: xor       ebx, ebx
004566b0: mov       ax, word ptr [ecx + 8]
004566b4: mov       bl, byte ptr [ecx]
004566b6: mov       dword ptr [esp + 0x34], eax
004566ba: cmp       ebx, 0xc8
004566c0: je        0x456719
004566c2: cmp       ebx, 4
004566c5: je        0x456719
004566c7: xor       ah, ah
004566c9: mov       al, byte ptr [ecx + 0xbb]
004566cf: add       eax, 2
004566d4: mov       dword ptr [esp + 0x48], eax
004566d8: xor       ah, ah
004566da: mov       edx, dword ptr [esp + 0x48]
004566de: mov       al, byte ptr [ecx + 0xf5]
004566e4: add       eax, edx
004566e6: xor       edx, edx
004566e8: movzx     ebp, word ptr [esp + 0x34]
004566ed: mov       dx, ax
004566f0: mov       eax, ebp
004566f2: call      0x476851
004566f7: xor       ebx, ebx
004566f9: xor       dh, dh
004566fb: xor       ah, ah
004566fd: mov       dl, byte ptr [ecx + 0xf5]
00456703: mov       al, byte ptr [ecx + 0xbb]
00456709: add       eax, edx
0045670b: xor       edx, edx
0045670d: mov       bl, byte ptr [ecx]
0045670f: mov       dx, ax
00456712: mov       eax, ebp
00456714: call      0x476cb3
00456719: mov       edx, 4
0045671e: xor       ebx, ebx
00456720: xor       eax, eax
00456722: mov       bx, word ptr [esp + 0x34]
00456727: jmp       0x4550a2
0045672c: xor       eax, eax
0045672e: mov       ax, di
00456731: call      0x44bc74
00456736: jmp       0x454ccd
0045673b: xor       eax, eax
0045673d: mov       ax, word ptr [esi + 0xb8]
00456744: cmp       eax, 0xffff
00456749: je        0x456772
0045674b: call      0x41a70b
00456750: test      al, al
00456752: jne       0x456772
00456754: xor       eax, eax
00456756: mov       ax, word ptr [esi + 0xb8]
0045675d: call      0x41a08c
00456762: and       eax, 0xff
00456767: cmp       eax, 0xc8
0045676c: jne       0x45689e
00456772: xor       ecx, ecx
00456774: mov       cx, di
00456777: mov       eax, ecx
00456779: shl       eax, 4
0045677c: add       eax, ecx
0045677e: shl       eax, 2
00456781: mov       edx, dword ptr [0x4e19a0]
00456787: add       eax, ecx
00456789: mov       al, byte ptr [edx + eax*4]
0045678c: and       eax, 0xff
00456791: call      0x46d817
00456796: and       eax, 0xff
0045679b: cmp       eax, 2
0045679e: jne       0x4567b3
004567a0: mov       edx, 0x4a
004567a5: mov       eax, ecx
004567a7: xor       ebx, ebx
004567a9: call      0x4829c8
004567ae: jmp       0x454ccd
004567b3: xor       edx, edx
004567b5: mov       eax, ecx
004567b7: mov       dx, word ptr [esi + 0x7e]
004567bb: call      0x4457d3
004567c0: mov       word ptr [esi + 0xb8], 0xffff
004567c9: jmp       0x454ccd
004567ce: xor       eax, eax
004567d0: mov       ax, word ptr [esi + 0xb8]
004567d7: cmp       eax, 0xffff
004567dc: je        0x45684f
004567e2: xor       edx, edx
004567e4: mov       dx, ax
004567e7: mov       eax, edx
004567e9: shl       eax, 4
004567ec: add       eax, edx
004567ee: shl       eax, 2
004567f1: add       eax, edx
004567f3: mov       edx, dword ptr [0x4e19a0]
004567f9: shl       eax, 2
004567fc: add       edx, eax
004567fe: xor       eax, eax
00456800: mov       al, byte ptr [edx + 2]
00456803: test      eax, eax
00456805: je        0x456810
00456807: cmp       eax, 4
0045680a: je        0x456810
0045680c: mov       al, 1
0045680e: jmp       0x456812
00456810: xor       al, al
00456812: test      al, al
00456814: je        0x45684f
00456816: mov       ax, word ptr [esi + 0xb8]
0045681d: xor       edx, edx
0045681f: mov       dx, ax
00456822: mov       eax, edx
00456824: shl       eax, 4
00456827: add       eax, edx
00456829: shl       eax, 2
0045682c: add       edx, eax
0045682e: mov       eax, dword ptr [0x4e19a0]
00456833: shl       edx, 2
00456836: add       eax, edx
00456838: mov       dl, byte ptr [eax]
0045683a: and       edx, 0xff
00456840: cmp       edx, 0xc8
00456846: je        0x45684f
00456848: mov       al, byte ptr [eax + 0x72]
0045684b: test      al, al
0045684d: jne       0x45689e
0045684f: xor       ecx, ecx
00456851: mov       cx, di
00456854: mov       eax, ecx
00456856: shl       eax, 4
00456859: add       eax, ecx
0045685b: shl       eax, 2
0045685e: mov       edx, dword ptr [0x4e19a0]
00456864: add       eax, ecx
00456866: mov       al, byte ptr [edx + eax*4]
00456869: and       eax, 0xff
0045686e: call      0x46d817
00456873: and       eax, 0xff
00456878: cmp       eax, 2
0045687b: je        0x4567a0
00456881: jmp       0x4567b3
00456886: mov       al, byte ptr [esi + 0xb7]
0045688c: cmp       al, 1
0045688e: jb        0x45689e
00456890: jbe       0x4567ce
00456896: cmp       al, 3
00456898: je        0x45673b
0045689e: xor       eax, eax
004568a0: mov       ax, di
004568a3: call      0x451914
004568a8: jmp       0x454ccd
004568ad: xor       edx, edx
004568af: mov       dx, di
004568b2: mov       eax, edx
004568b4: shl       eax, 4
004568b7: add       eax, edx
004568b9: shl       eax, 2
004568bc: mov       cl, 7
004568be: add       edx, eax
004568c0: mov       eax, dword ptr [0x4e19a0]
004568c5: shl       edx, 2
004568c8: mov       ebx, edi
004568ca: mov       al, byte ptr [edx + eax + 2]
004568ce: and       eax, 0xff
004568d3: je        0x4568fe
004568d5: xor       edx, edx
004568d7: mov       dx, di
004568da: mov       eax, edx
004568dc: shl       eax, 4
004568df: add       eax, edx
004568e1: shl       eax, 2
004568e4: add       eax, edx
004568e6: mov       edx, dword ptr [0x4e19a0]
004568ec: mov       al, byte ptr [edx + eax*4 + 2]
004568f0: and       eax, 0xff
004568f5: cmp       eax, 4
004568f8: je        0x4568fe
004568fa: mov       al, 1
004568fc: jmp       0x456900
004568fe: xor       al, al
00456900: test      al, al
00456902: je        0x454ccd
00456908: xor       edx, edx
0045690a: mov       dx, di
0045690d: mov       eax, edx
0045690f: shl       eax, 4
00456912: add       eax, edx
00456914: shl       eax, 2
00456917: add       eax, edx
00456919: mov       edx, dword ptr [0x4e19a0]
0045691f: mov       byte ptr [edx + eax*4 + 2], cl
00456923: cmp       di, word ptr [0x496304]
0045692a: jne       0x454ccd
00456930: mov       esi, 0xffff
00456935: xor       bl, bl
00456937: xor       edx, edx
00456939: mov       byte ptr [0x4e0f36], bl
0045693f: mov       byte ptr [0x4e0f37], bl
00456945: mov       dword ptr [0x4e0f3c], edx
0045694b: mov       word ptr [0x496304], si
00456952: jmp       0x454ccd
00456957: xor       eax, eax
00456959: mov       ax, di
0045695c: call      0x447b2f
00456961: jmp       0x454ccd
00456966: xor       edx, edx
00456968: mov       dx, di
0045696b: mov       eax, edx
0045696d: shl       eax, 4
00456970: add       eax, edx
00456972: shl       eax, 2
00456975: add       eax, edx
00456977: mov       ebx, dword ptr [0x4e19a0]
0045697d: shl       eax, 2
00456980: add       ebx, eax
00456982: mov       al, byte ptr [ebx + 1]
00456985: cmp       al, 8
00456987: jb        0x4569af
00456989: jbe       0x4569b1
0045698b: cmp       al, 0x12
0045698d: jb        0x4569a2
0045698f: jbe       0x4569b1
00456991: cmp       al, 0x17
00456993: jb        0x4569b1
00456995: cmp       al, 0x18
00456997: jbe       0x4569b1
00456999: cmp       al, 0x19
0045699b: je        0x4569b1
0045699d: jmp       0x454ccd
004569a2: cmp       al, 0xa
004569a4: jbe       0x4569b1
004569a6: cmp       al, 0x11
004569a8: je        0x456957
004569aa: jmp       0x454ccd
004569af: cmp       al, 4
004569b1: mov       eax, 0x24
004569b6: mov       ecx, 0xc8
004569bb: xor       edx, edx
004569bd: call      0x4704dc
004569c2: div       ecx
004569c4: test      edx, edx
004569c6: jne       0x454ccd
004569cc: mov       dl, byte ptr [ebx + 0x91]
004569d2: mov       ecx, 0x10
004569d7: mov       eax, edx
004569d9: sar       edx, 0x1f
004569dc: idiv      ecx
004569de: inc       edx
004569df: mov       byte ptr [ebx + 0x90], dl
004569e5: mov       byte ptr [ebx + 0x91], dl
004569eb: jmp       0x454ccd
004569f0: mov       al, 1
004569f2: test      al, al
004569f4: jne       0x456b2f
004569fa: xor       eax, eax
004569fc: mov       al, byte ptr [esi + 0xa4]
00456a02: test      eax, eax
00456a04: jne       0x456a38
00456a06: xor       ebx, ebx
00456a08: mov       bx, di
00456a0b: mov       eax, ebx
00456a0d: xor       edx, edx
00456a0f: call      0x472648
00456a14: mov       eax, ebx
00456a16: mov       dx, word ptr [esi + 8]
00456a1a: call      0x442eac
00456a1f: mov       ax, word ptr [esi + 8]
00456a23: mov       cx, word ptr [esi + 0x7c]
00456a27: cmp       ax, cx
00456a2a: je        0x456a38
00456a2c: xor       edx, edx
00456a2e: mov       eax, ebx
00456a30: mov       dx, cx
00456a33: call      0x442eac
00456a38: xor       edx, edx
00456a3a: mov       dx, di
00456a3d: mov       eax, edx
00456a3f: shl       eax, 4
00456a42: add       eax, edx
00456a44: shl       eax, 2
00456a47: add       eax, edx
00456a49: mov       ebx, dword ptr [0x4e19a0]
00456a4f: shl       eax, 2
00456a52: add       ebx, eax
00456a54: xor       ecx, ecx
00456a56: xor       edx, edx
00456a58: mov       cl, byte ptr [ebx + 0xdb]
00456a5e: mov       dl, byte ptr [ebx + 0xa4]
00456a64: lea       eax, [ecx - 1]
00456a67: cmp       edx, eax
00456a69: je        0x456a79
00456a6b: inc       edx
00456a6c: mov       eax, edx
00456a6e: sar       edx, 0x1f
00456a71: idiv      ecx
00456a73: mov       byte ptr [ebx + 0xa4], dl
00456a79: inc       word ptr [esi + 0xc2]
00456a80: xor       eax, eax
00456a82: mov       ax, word ptr [esi + 0xc2]
00456a89: cmp       eax, 0x14a
00456a8e: jl        0x454ccd
00456a94: xor       ebx, ebx
00456a96: mov       bx, di
00456a99: mov       eax, ebx
00456a9b: shl       eax, 4
00456a9e: add       eax, ebx
00456aa0: shl       eax, 2
00456aa3: lea       edx, [ebx + eax]
00456aa6: mov       eax, dword ptr [0x4e19a0]
00456aab: shl       edx, 2
00456aae: lea       ecx, [eax + edx]
00456ab1: mov       eax, ebx
00456ab3: call      0x472648
00456ab8: mov       eax, dword ptr [0x4e19a0]
00456abd: add       eax, edx
00456abf: mov       dword ptr [esp + 0x14], edi
00456ac3: lea       ebx, [eax + 0xa]
00456ac6: mov       ax, word ptr [ebx]
00456ac9: and       eax, 0xffff
00456ace: je        0x456b13
00456ad0: xor       eax, eax
00456ad2: xor       edx, edx
00456ad4: mov       ax, di
00456ad7: call      0x443dfc
00456adc: jmp       0x456ac6
00456ade: xor       al, al
00456ae0: jmp       0x4569f2
00456ae5: xor       edx, edx
00456ae7: mov       dx, di
00456aea: mov       eax, edx
00456aec: shl       eax, 4
00456aef: add       eax, edx
00456af1: shl       eax, 2
00456af4: add       eax, edx
00456af6: mov       edx, dword ptr [0x4e19a0]
00456afc: mov       al, byte ptr [edx + eax*4 + 1]
00456b00: sub       al, 0xb
00456b02: cmp       al, 6
00456b04: ja        0x456ade
00456b06: and       eax, 0xff
00456b0b: jmp       dword ptr cs:[eax*4 + 0x4543ac]
00456b13: mov       ax, word ptr [esp + 0x14]
00456b18: call      0x457058
00456b1d: mov       word ptr [ecx + 0x9a], 0
00456b26: mov       byte ptr [esi + 2], 0
00456b2a: jmp       0x454ccd
00456b2f: xor       edx, edx
00456b31: mov       dx, di
00456b34: mov       ebx, edx
00456b36: shl       ebx, 4
00456b39: add       ebx, edx
00456b3b: shl       ebx, 2
00456b3e: add       ebx, edx
00456b40: mov       eax, dword ptr [0x4e19a0]
00456b45: shl       ebx, 2
00456b48: mov       al, byte ptr [ebx + eax + 0xdc]
00456b4f: mov       edx, 2
00456b54: and       eax, 0xff
00456b59: call      0x467d97
00456b5e: test      al, al
00456b60: jne       0x456bb7
00456b62: mov       eax, dword ptr [0x4e19a0]
00456b67: xor       edx, edx
00456b69: mov       al, byte ptr [ebx + eax + 1]
00456b6d: mov       dl, al
00456b6f: mov       eax, edx
00456b71: shl       eax, 2
00456b74: sub       eax, edx
00456b76: shl       eax, 3
00456b79: add       edx, eax
00456b7b: add       edx, edx
00456b7d: mov       ax, word ptr [edx + 0x4965b0]
00456b84: mov       dword ptr [esp + 0x1c], eax
00456b88: mov       ax, word ptr [edx + 0x4965b4]
00456b8f: mov       dword ptr [esp + 0x1c], eax
00456b93: mov       ax, word ptr [edx + 0x4965b2]
00456b9a: xor       ebx, ebx
00456b9c: mov       dword ptr [esp + 0x20], eax
00456ba0: jmp       0x456bb0
00456ba2: xor       eax, eax
00456ba4: xor       edx, edx
00456ba6: mov       ax, word ptr [esi + 8]
00456baa: inc       ebx
00456bab: call      0x47605d
00456bb0: cmp       bx, word ptr [esp + 0x20]
00456bb5: jb        0x456ba2
00456bb7: xor       edx, edx
00456bb9: mov       dx, di
00456bbc: mov       eax, edx
00456bbe: shl       eax, 4
00456bc1: add       eax, edx
00456bc3: shl       eax, 2
00456bc6: lea       ebx, [edx + eax]
00456bc9: mov       eax, dword ptr [0x4e19a0]
00456bce: shl       ebx, 2
00456bd1: add       eax, ebx
00456bd3: mov       dword ptr [esp + 8], eax
00456bd7: mov       eax, edx
00456bd9: call      0x472648
00456bde: mov       eax, dword ptr [0x4e19a0]
00456be3: add       ebx, eax
00456be5: mov       ecx, edi
00456be7: add       ebx, 0xa
00456bea: mov       ax, word ptr [ebx]
00456bed: and       eax, 0xffff
00456bf2: je        0x456c02
00456bf4: xor       eax, eax
00456bf6: xor       edx, edx
00456bf8: mov       ax, di
00456bfb: call      0x443dfc
00456c00: jmp       0x456bea
00456c02: mov       ax, cx
00456c05: call      0x457058
00456c0a: mov       eax, dword ptr [esp + 8]
00456c0e: mov       word ptr [eax + 0x9a], 0
00456c17: jmp       0x456b26
00456c1c: mov       al, byte ptr [esi + 2]
00456c1f: cmp       al, 0x18
00456c21: ja        0x454ccd
00456c27: and       eax, 0xff
00456c2c: jmp       dword ptr cs:[eax*4 + 0x4543c8]

; CalculEnginNextEtape 0x456db5..0x456f0a
00456db5: push      ebx
00456db6: push      ecx
00456db7: push      edx
00456db8: push      esi
00456db9: xor       edx, edx
00456dbb: xor       cl, cl
00456dbd: mov       word ptr [0x4e1a38], dx
00456dc4: mov       word ptr [0x4e1a3a], dx
00456dcb: xor       esi, esi
00456dcd: jmp       0x456df7
00456dcf: xor       ebx, ebx
00456dd1: mov       bl, cl
00456dd3: imul      ebx, ebx, 0x34
00456dd6: inc       eax
00456dd7: mov       word ptr [ebx + edx*2 + 0x4e1a3c], si
00456ddf: xor       edx, edx
00456de1: mov       dx, ax
00456de4: cmp       edx, 0x1a
00456de7: jl        0x456dcf
00456de9: xor       edx, edx
00456deb: mov       dl, cl
00456ded: inc       cl
00456def: mov       word ptr [edx*2 + 0x4e1928], si
00456df7: xor       eax, eax
00456df9: mov       al, cl
00456dfb: cmp       eax, 4
00456dfe: jge       0x456e04
00456e00: mov       eax, esi
00456e02: jmp       0x456ddf
00456e04: xor       ecx, ecx
00456e06: xor       ebx, ebx
00456e08: mov       word ptr [0x4e1930], cx
00456e0f: jmp       0x456eb3
00456e14: xor       al, al
00456e16: test      al, al
00456e18: je        0x456ea8
00456e1e: xor       eax, eax
00456e20: mov       ax, bx
00456e23: imul      eax, eax, 0x114
00456e29: mov       edx, dword ptr [0x4e19a0]
00456e2f: add       edx, eax
00456e31: mov       al, byte ptr [edx + 1]
00456e34: mov       cl, al
00456e36: mov       ah, byte ptr [edx]
00456e38: xor       edx, edx
00456e3a: mov       dl, ah
00456e3c: mov       ch, ah
00456e3e: cmp       edx, 0xc8
00456e44: je        0x456e5b
00456e46: cmp       edx, 4
00456e49: je        0x456e5b
00456e4b: imul      edx, edx, 0x34
00456e4e: and       eax, 0xff
00456e53: inc       word ptr [edx + eax*2 + 0x4e1a3c]
00456e5b: xor       edx, edx
00456e5d: mov       eax, 1
00456e62: mov       dx, bx
00456e65: call      0x47fbfd
00456e6a: xor       eax, eax
00456e6c: mov       al, cl
00456e6e: cmp       eax, 0x11
00456e71: je        0x456e8b
00456e73: cmp       ch, byte ptr [0x508041]
00456e79: je        0x456e84
00456e7b: inc       word ptr [0x4e1a38]
00456e82: jmp       0x456e8b
00456e84: inc       word ptr [0x4e1a3a]
00456e8b: xor       edx, edx
00456e8d: mov       dl, ch
00456e8f: cmp       edx, 0xc8
00456e95: je        0x456ea8
00456e97: xor       eax, eax
00456e99: mov       al, cl
00456e9b: cmp       eax, 5
00456e9e: je        0x456ea8
00456ea0: inc       word ptr [edx*2 + 0x4e1928]
00456ea8: xor       eax, eax
00456eaa: mov       ax, bx
00456ead: call      0x45442c
00456eb2: inc       ebx
00456eb3: xor       eax, eax
00456eb5: mov       ax, bx
00456eb8: cmp       eax, 0x320
00456ebd: jge       0x45179d
00456ec3: imul      eax, eax, 0x114
00456ec9: mov       edx, dword ptr [0x4e19a0]
00456ecf: mov       al, byte ptr [edx + eax + 2]
00456ed3: and       eax, 0xff
00456ed8: setne     al
00456edb: test      al, al
00456edd: je        0x456eb2
00456edf: xor       eax, eax
00456ee1: mov       ax, bx
00456ee4: imul      eax, eax, 0x114
00456eea: mov       dl, byte ptr [edx + eax + 2]
00456eee: and       edx, 0xff
00456ef4: je        0x456e14
00456efa: cmp       edx, 4
00456efd: je        0x456e14
00456f03: mov       al, 1
00456f05: jmp       0x456e16

; EnginInfligeDegat 0x4502f0..0x450874
004502f0: push      esi
004502f1: push      edi
004502f2: push      ebp
004502f3: sub       esp, 0x2c
004502f6: mov       edi, eax
004502f8: mov       byte ptr [esp + 0x1c], dl
004502fc: mov       dword ptr [esp + 0x14], ebx
00450300: mov       bl, cl
00450302: xor       eax, eax
00450304: mov       ax, di
00450307: mov       dword ptr [esp + 8], eax
0045030b: mov       edx, eax
0045030d: shl       eax, 4
00450310: add       eax, edx
00450312: shl       eax, 2
00450315: mov       ebp, dword ptr [0x4e19a0]
0045031b: add       eax, edx
0045031d: xor       ecx, ecx
0045031f: shl       eax, 2
00450322: mov       cx, word ptr [esp + 0x14]
00450327: lea       esi, [eax + ebp]
0045032a: mov       eax, ecx
0045032c: shl       eax, 4
0045032f: add       eax, ecx
00450331: shl       eax, 2
00450334: add       eax, ecx
00450336: shl       eax, 2
00450339: mov       dword ptr [esp + 4], eax
0045033d: add       ebp, eax
0045033f: mov       ax, word ptr [esi + 0x7c]
00450343: mov       dword ptr [esp + 0x10], eax
00450347: mov       ah, byte ptr [esp + 0x1c]
0045034b: cmp       ah, 4
0045034e: jb        0x450588
00450354: jbe       0x4504c6
0045035a: cmp       ah, 8
0045035d: jb        0x45059c
00450363: jbe       0x450475
00450369: cmp       ah, 9
0045036c: je        0x450494
00450372: jmp       0x45059c
00450377: mov       al, byte ptr [esi + 1]
0045037a: xor       ebx, ebx
0045037c: mov       bl, al
0045037e: mov       eax, ecx
00450380: call      0x41a4f4
00450385: mov       edx, 1
0045038a: and       eax, 0xff
0045038f: call      0x418b8a
00450394: mov       edx, 0x4c
00450399: mov       byte ptr [esp + 0x20], al
0045039d: mov       eax, ecx
0045039f: mov       ebx, ecx
004503a1: call      0x41a08c
004503a6: mov       byte ptr [esp + 0x28], al
004503aa: mov       eax, dword ptr [esp + 8]
004503ae: call      0x4829c8
004503b3: jmp       0x45059c
004503b8: mov       al, byte ptr [esi + 1]
004503bb: xor       ebx, ebx
004503bd: mov       byte ptr [esp + 0x24], al
004503c1: mov       al, byte ptr [ebp + 1]
004503c4: mov       bl, al
004503c6: mov       eax, ebx
004503c8: mov       edx, dword ptr [0x4e199c]
004503ce: shl       eax, 2
004503d1: add       eax, edx
004503d3: xor       edx, edx
004503d5: mov       eax, dword ptr [eax]
004503d7: mov       dl, byte ptr [esp + 0x24]
004503db: mov       al, byte ptr [edx + eax]
004503de: mov       ah, byte ptr [ebp + 0xf7]
004503e4: add       ah, al
004503e6: mov       byte ptr [esp + 0x20], ah
004503ea: xor       eax, eax
004503ec: mov       edx, 5
004503f1: mov       al, byte ptr [ebp]
004503f4: call      0x428cc0
004503f9: mov       dh, byte ptr [esp + 0x20]
004503fd: mov       ecx, dword ptr [esp + 4]
00450401: add       dh, al
00450403: mov       eax, dword ptr [0x4e19a0]
00450408: add       eax, ecx
0045040a: xor       ebx, ebx
0045040c: mov       byte ptr [esp + 0x20], dh
00450410: mov       dx, word ptr [eax + 0x7c]
00450414: mov       bx, dx
00450417: mov       al, byte ptr [eax]
00450419: xor       edx, edx
0045041b: mov       ecx, 0xa
00450420: mov       dl, al
00450422: mov       eax, 2
00450427: call      0x4500e4
0045042c: test      al, al
0045042e: je        0x45043f
00450430: mov       bl, byte ptr [esp + 0x20]
00450434: mov       al, byte ptr [0x4965ac]
00450439: add       bl, al
0045043b: mov       byte ptr [esp + 0x20], bl
0045043f: mov       edx, 0x48
00450444: xor       ecx, ecx
00450446: xor       eax, eax
00450448: mov       cx, word ptr [esp + 0x14]
0045044d: mov       ax, di
00450450: mov       ebx, ecx
00450452: call      0x4829c8
00450457: mov       eax, ecx
00450459: shl       eax, 4
0045045c: add       eax, ecx
0045045e: shl       eax, 2
00450461: mov       edx, dword ptr [0x4e19a0]
00450467: add       eax, ecx
00450469: mov       al, byte ptr [edx + eax*4]
0045046c: mov       byte ptr [esp + 0x28], al
00450470: jmp       0x45059c
00450475: mov       eax, dword ptr [0x4e199c]
0045047a: mov       dl, byte ptr [esi + 1]
0045047d: add       eax, 0x68
00450480: and       edx, 0xff
00450486: mov       eax, dword ptr [eax]
00450488: mov       al, byte ptr [edx + eax]
0045048b: mov       byte ptr [esp + 0x20], al
0045048f: jmp       0x45059c
00450494: mov       ax, word ptr [esi + 0x9a]
0045049b: xor       edx, edx
0045049d: mov       dx, ax
004504a0: mov       eax, edx
004504a2: sar       edx, 0x1f
004504a5: sub       eax, edx
004504a7: sar       eax, 1
004504a9: mov       byte ptr [esp + 0x20], al
004504ad: mov       eax, dword ptr [esp + 0x1d]
004504b1: sar       eax, 0x18
004504b4: test      eax, eax
004504b6: jne       0x45059c
004504bc: mov       byte ptr [esp + 0x20], 1
004504c1: jmp       0x45059c
004504c6: xor       eax, eax
004504c8: mov       al, bl
004504ca: cmp       eax, 0x1d
004504cd: jne       0x4504da
004504cf: mov       al, byte ptr [0x49716c]
004504d4: mov       byte ptr [esp + 0x20], al
004504d8: jmp       0x4504fe
004504da: cmp       eax, 0x1e
004504dd: jne       0x4504fe
004504df: mov       al, byte ptr [0x49716e]
004504e4: jmp       0x4504d4
004504e6: mov       word ptr [ecx], 1
004504eb: mov       word ptr [edx], 1
004504f0: jmp       0x45053a
004504f2: mov       word ptr [ecx], 2
004504f7: mov       word ptr [edx], 2
004504fc: jmp       0x45053a
004504fe: xor       eax, eax
00450500: mov       ax, di
00450503: mov       dword ptr [esp], eax
00450506: mov       ebx, dword ptr [esp]
00450509: shl       eax, 4
0045050c: add       eax, ebx
0045050e: shl       eax, 2
00450511: add       eax, ebx
00450513: mov       ebx, dword ptr [0x4e19a0]
00450519: shl       eax, 2
0045051c: add       eax, ebx
0045051e: lea       ecx, [esp + 0x18]
00450522: lea       edx, [esp + 0xc]
00450526: mov       al, byte ptr [eax + 1]
00450529: cmp       al, 0x19
0045052b: ja        0x45053a
0045052d: and       eax, 0xff
00450532: jmp       dword ptr cs:[eax*4 + 0x450288]
0045053a: xor       eax, eax
0045053c: mov       ax, word ptr [esp + 0x18]
00450541: cmp       eax, 2
00450544: jne       0x45056a
00450546: xor       eax, eax
00450548: mov       ax, word ptr [esp + 0xc]
0045054d: cmp       eax, 2
00450550: jne       0x45056a
00450552: mov       edx, dword ptr [esp + 0x1d]
00450556: sar       edx, 0x18
00450559: mov       eax, edx
0045055b: sar       edx, 0x1f
0045055e: shl       edx, 2
00450561: sbb       eax, edx
00450563: sar       eax, 2
00450566: mov       byte ptr [esp + 0x20], al
0045056a: xor       edx, edx
0045056c: mov       dx, word ptr [esp + 0x14]
00450571: mov       eax, edx
00450573: shl       eax, 4
00450576: add       eax, edx
00450578: shl       eax, 2
0045057b: add       eax, edx
0045057d: mov       edx, dword ptr [0x4e19a0]
00450583: jmp       0x450469
00450588: cmp       ah, 1
0045058b: jb        0x45059c
0045058d: jbe       0x4503b8
00450593: cmp       ah, 3
00450596: je        0x450377
0045059c: mov       bh, byte ptr [esp + 0x20]
004505a0: sub       bh, byte ptr [esi + 0xf6]
004505a6: mov       edx, 6
004505ab: mov       byte ptr [esp + 0x20], bh
004505af: xor       eax, eax
004505b1: xor       ebx, ebx
004505b3: mov       al, byte ptr [ebp]
004505b6: mov       bl, byte ptr [ebp + 1]
004505b9: mov       cl, byte ptr [esp + 0x20]
004505bd: call      0x428cc0
004505c2: sub       cl, al
004505c4: mov       byte ptr [esp + 0x20], cl
004505c8: mov       eax, dword ptr [esp + 0x1d]
004505cc: sar       eax, 0x18
004505cf: test      eax, eax
004505d1: jge       0x4505d8
004505d3: mov       byte ptr [esp + 0x20], 1
004505d8: xor       ebx, ebx
004505da: mov       bx, di
004505dd: mov       eax, ebx
004505df: shl       eax, 4
004505e2: add       eax, ebx
004505e4: shl       eax, 2
004505e7: mov       ebp, dword ptr [0x4e19a0]
004505ed: add       eax, ebx
004505ef: mov       edx, ebx
004505f1: shl       eax, 2
004505f4: xor       edx, ebx
004505f6: add       ebp, eax
004505f8: xor       eax, eax
004505fa: mov       dl, byte ptr [0x508041]
00450600: mov       ax, word ptr [ebp + 8]
00450604: call      0x4766f0
00450609: test      al, al
0045060b: je        0x450644
0045060d: mov       eax, ebx
0045060f: call      0x440c5d
00450614: mov       edx, dword ptr [ebp + 0x104]
0045061a: mov       byte ptr [ebp + 0xf9], 0
00450621: cmp       edx, -1
00450624: jne       0x450644
00450626: push      eax
00450627: xor       edx, edx
00450629: lea       ebx, [ebp + 0x104]
0045062f: mov       dl, byte ptr [ebp + 1]
00450632: xor       ecx, ecx
00450634: shl       edx, 0x10
00450637: mov       eax, 0x50
0045063c: or        dh, 1
0045063f: call      0x48aa79
00450644: xor       edx, edx
00450646: mov       dx, di
00450649: mov       eax, edx
0045064b: shl       eax, 4
0045064e: add       eax, edx
00450650: shl       eax, 2
00450653: add       eax, edx
00450655: mov       edx, dword ptr [0x4e19a0]
0045065b: mov       al, byte ptr [edx + eax*4 + 0xdc]
00450662: mov       edx, 3
00450667: and       eax, 0xff
0045066c: call      0x467d97
00450671: test      al, al
00450673: je        0x450679
00450675: dec       byte ptr [esp + 0x20]
00450679: mov       eax, dword ptr [esp + 0x1d]
0045067d: xor       edx, edx
0045067f: sar       eax, 0x18
00450682: mov       dx, word ptr [esi + 0x9a]
00450689: cmp       edx, eax
0045068b: jle       0x4506a1
0045068d: movsx     ax, byte ptr [esp + 0x20]
00450693: sub       edx, eax
00450695: mov       word ptr [esi + 0x9a], dx
0045069c: jmp       0x45084f
004506a1: xor       eax, eax
004506a3: mov       al, byte ptr [esp + 0x1c]
004506a7: cmp       eax, 1
004506aa: je        0x4506b1
004506ac: jmp       0x450754
004506b1: xor       edx, edx
004506b3: mov       dx, word ptr [esp + 0x14]
004506b8: mov       eax, edx
004506ba: shl       eax, 4
004506bd: add       eax, edx
004506bf: shl       eax, 2
004506c2: add       eax, edx
004506c4: mov       edx, dword ptr [0x4e19a0]
004506ca: mov       al, byte ptr [edx + eax*4 + 1]
004506ce: cmp       al, 6
004506d0: jb        0x4506e4
004506d2: cmp       al, 7
004506d4: jbe       0x4506e6
004506d6: cmp       al, 9
004506d8: jb        0x4506e6
004506da: cmp       al, 0xa
004506dc: jbe       0x4506e6
004506de: cmp       al, 0x19
004506e0: je        0x4506e6
004506e2: jmp       0x4506ea
004506e4: cmp       al, 3
004506e6: mov       al, 1
004506e8: jmp       0x4506ec
004506ea: xor       al, al
004506ec: test      al, al
004506ee: je        0x450754
004506f0: xor       ebx, ebx
004506f2: mov       bx, word ptr [esp + 0x14]
004506f7: mov       eax, ebx
004506f9: shl       eax, 4
004506fc: add       eax, ebx
004506fe: shl       eax, 2
00450701: add       eax, ebx
00450703: mov       edx, dword ptr [0x4e19a0]
00450709: shl       eax, 2
0045070c: add       eax, edx
0045070e: mov       dl, byte ptr [eax + 0xaf]
00450714: and       dl, 0x1f
00450717: add       dl, 0xa
0045071a: mov       dh, byte ptr [eax + 0xaf]
00450720: xor       ecx, ecx
00450722: shr       dh, 5
00450725: mov       cl, dl
00450727: cmp       ecx, 0xa
0045072a: jl        0x450744
0045072c: and       byte ptr [eax + 0xaf], 0xe0
00450733: mov       al, dh
00450735: inc       al
00450737: xor       edx, edx
00450739: mov       dl, al
0045073b: mov       eax, ebx
0045073d: call      0x44fb20
00450742: jmp       0x450754
00450744: add       dl, 0xa
00450747: shl       dh, 5
0045074a: add       dh, dl
0045074c: add       dl, dh
0045074e: mov       byte ptr [eax + 0xaf], dl
00450754: xor       edx, edx
00450756: mov       dx, di
00450759: mov       eax, edx
0045075b: shl       eax, 4
0045075e: add       eax, edx
00450760: shl       eax, 2
00450763: mov       word ptr [esi + 0x9a], 0
0045076c: add       edx, eax
0045076e: mov       eax, dword ptr [0x4e19a0]
00450773: shl       edx, 2
00450776: mov       al, byte ptr [edx + eax + 1]
0045077a: and       eax, 0xff
0045077f: cmp       eax, 1
00450782: jne       0x4507a3
00450784: push      0
00450786: push      0
00450788: push      0
0045078a: xor       edx, edx
0045078c: push      0
0045078e: mov       eax, 6
00450793: mov       dx, word ptr [esp + 0x20]
00450798: push      0
0045079a: xor       ecx, ecx
0045079c: mov       ebx, edx
0045079e: call      0x46e44c
004507a3: xor       edx, edx
004507a5: mov       dx, di
004507a8: mov       eax, edx
004507aa: call      0x444938
004507af: mov       eax, edx
004507b1: shl       eax, 4
004507b4: add       eax, edx
004507b6: shl       eax, 2
004507b9: add       edx, eax
004507bb: mov       eax, dword ptr [0x4e19a0]
004507c0: shl       edx, 2
004507c3: mov       al, byte ptr [edx + eax + 1]
004507c7: cmp       al, 0xc
004507c9: jb        0x4507e1
004507cb: cmp       al, 0xd
004507cd: jbe       0x4507d9
004507cf: cmp       al, 0xf
004507d1: jb        0x4507d9
004507d3: jbe       0x4507d9
004507d5: cmp       al, 0x11
004507d7: ja        0x4507dd
004507d9: xor       al, al
004507db: jmp       0x4507ed
004507dd: mov       al, 1
004507df: jmp       0x4507ed
004507e1: cmp       al, 3
004507e3: jb        0x4507dd
004507e5: jbe       0x4507d9
004507e7: cmp       al, 0xb
004507e9: je        0x4507d9
004507eb: jmp       0x4507dd
004507ed: test      al, al
004507ef: je        0x45081c
004507f1: xor       edx, edx
004507f3: mov       dx, di
004507f6: mov       eax, edx
004507f8: shl       eax, 4
004507fb: add       eax, edx
004507fd: shl       eax, 2
00450800: xor       ecx, ecx
00450802: add       eax, edx
00450804: mov       edx, dword ptr [0x4e19a0]
0045080a: mov       cl, byte ptr [esp + 0x28]
0045080e: mov       al, byte ptr [edx + eax*4]
00450811: and       eax, 0xff
00450816: mov       edx, ecx
00450818: xor       ebx, ebx
0045081a: jmp       0x45084a
0045081c: xor       edx, edx
0045081e: mov       dx, di
00450821: mov       eax, edx
00450823: shl       eax, 4
00450826: add       eax, edx
00450828: shl       eax, 2
0045082b: xor       ecx, ecx
0045082d: add       edx, eax
0045082f: mov       eax, dword ptr [0x4e19a0]
00450834: shl       edx, 2
00450837: mov       cl, byte ptr [esp + 0x28]
0045083b: mov       al, byte ptr [edx + eax]
0045083e: mov       ebx, 1
00450843: and       eax, 0xff
00450848: mov       edx, ecx
0045084a: call      0x475118
0045084f: add       esp, 0x2c
00450852: pop       ebp
00450853: pop       edi
00450854: pop       esi
00450855: ret       
00450856: mov       eax, eax
00450858: push      cs
00450859: push      cs
0045085a: inc       ebp
0045085b: add       byte ptr [esi], cl
0045085d: push      cs
0045085e: inc       ebp
0045085f: add       byte ptr [esi], cl
00450861: push      cs
00450862: inc       ebp
00450863: add       byte ptr [esi], cl
00450865: push      cs
00450866: inc       ebp
00450867: add       byte ptr [esi], cl
00450869: push      cs
0045086a: inc       ebp
0045086b: add       byte ptr [esi], cl
0045086d: push      cs
0045086e: inc       ebp
0045086f: add       byte ptr [esi], cl
00450871: push      cs
00450872: inc       ebp

; InfligeDegat 0x450874..0x4510dd
00450874: push      esi
00450875: push      edi
00450876: push      ebp
00450877: sub       esp, 0x24
0045087a: push      eax
0045087b: mov       byte ptr [esp + 0x18], dl
0045087f: mov       esi, ebx
00450881: mov       byte ptr [esp + 0xc], cl
00450885: cmp       byte ptr [esp + 0x38], 0
0045088a: jne       0x45089b
0045088c: xor       eax, eax
0045088e: mov       ax, word ptr [esp]
00450892: call      0x41b54a
00450897: mov       edi, eax
00450899: jmp       0x4508a0
0045089b: mov       edi, 0xffff
004508a0: movzx     ebp, di
004508a3: cmp       ebp, 0xffff
004508a9: je        0x450a9d
004508af: xor       eax, eax
004508b1: mov       al, byte ptr [esp + 0x18]
004508b5: mov       ecx, 2
004508ba: cmp       eax, 1
004508bd: jne       0x450925
004508bf: xor       eax, eax
004508c1: mov       ax, si
004508c4: mov       dword ptr [esp + 4], eax
004508c8: mov       edx, eax
004508ca: shl       eax, 4
004508cd: add       eax, edx
004508cf: shl       eax, 2
004508d2: add       eax, edx
004508d4: mov       esi, dword ptr [0x4e19a0]
004508da: shl       eax, 2
004508dd: add       esi, eax
004508df: xor       ebx, ebx
004508e1: mov       al, byte ptr [esi + 1]
004508e4: mov       bl, al
004508e6: mov       edx, dword ptr [0x4e199c]
004508ec: mov       eax, ebx
004508ee: mov       eax, dword ptr [edx + eax*4]
004508f1: add       eax, 0x1a
004508f4: xor       ch, ch
004508f6: mov       al, byte ptr [eax]
004508f8: mov       cl, al
004508fa: xor       eax, eax
004508fc: mov       edx, 5
00450901: mov       al, byte ptr [esi]
00450903: call      0x428cc0
00450908: mov       ebx, dword ptr [esp + 4]
0045090c: add       ecx, eax
0045090e: mov       al, byte ptr [esi]
00450910: mov       edx, 4
00450915: mov       byte ptr [esp + 0x14], al
00450919: mov       eax, ebp
0045091b: call      0x484808
00450920: jmp       0x4509b2
00450925: cmp       eax, 3
00450928: jne       0x450960
0045092a: mov       eax, ebp
0045092c: xor       ebx, ebx
0045092e: call      0x41a4f4
00450933: mov       bl, al
00450935: and       esi, 0xffff
0045093b: mov       eax, esi
0045093d: call      0x41a4f4
00450942: mov       edx, 3
00450947: and       eax, 0xff
0045094c: call      0x418b8a
00450951: mov       ecx, eax
00450953: mov       eax, esi
00450955: call      0x41a08c
0045095a: mov       byte ptr [esp + 0x14], al
0045095e: jmp       0x4509b2
00450960: cmp       eax, 4
00450963: jne       0x4509b2
00450965: xor       edx, edx
00450967: mov       dx, si
0045096a: mov       eax, edx
0045096c: shl       eax, 4
0045096f: add       eax, edx
00450971: shl       eax, 2
00450974: add       eax, edx
00450976: mov       edx, dword ptr [0x4e19a0]
0045097c: mov       al, byte ptr [edx + eax*4]
0045097f: mov       byte ptr [esp + 0x14], al
00450983: xor       eax, eax
00450985: mov       al, byte ptr [esp + 0xc]
00450989: cmp       eax, 0x1d
0045098c: jne       0x450999
0045098e: xor       edx, edx
00450990: mov       dx, word ptr [0x49716c]
00450997: jmp       0x4509a7
00450999: cmp       eax, 0x1e
0045099c: jne       0x4509b2
0045099e: xor       edx, edx
004509a0: mov       dx, word ptr [0x49716e]
004509a7: mov       eax, edx
004509a9: sar       edx, 0x1f
004509ac: sub       eax, edx
004509ae: sar       eax, 1
004509b0: mov       ecx, eax
004509b2: xor       ebx, ebx
004509b4: xor       edx, edx
004509b6: xor       eax, eax
004509b8: mov       bl, byte ptr [esp + 0x14]
004509bc: mov       dx, cx
004509bf: mov       ax, di
004509c2: call      0x41a2c1
004509c7: mov       eax, 0x21
004509cc: call      0x4704dc
004509d1: test      al, 1
004509d3: jne       0x4509e6
004509d5: push      0
004509d7: push      0
004509d9: push      0
004509db: xor       edx, edx
004509dd: push      0
004509df: mov       eax, 0xf
004509e4: jmp       0x4509f5
004509e6: push      0
004509e8: push      0
004509ea: push      0
004509ec: xor       edx, edx
004509ee: push      0
004509f0: mov       eax, 0x10
004509f5: mov       dx, word ptr [esp + 0x10]
004509fa: push      0
004509fc: xor       ecx, ecx
004509fe: mov       ebx, edx
00450a00: call      0x46e44c
00450a05: xor       ecx, ecx
00450a07: mov       cx, di
00450a0a: movzx     esi, byte ptr [esp + 0x14]
00450a0f: mov       eax, ecx
00450a11: xor       edx, edx
00450a13: call      0x41a08c
00450a18: mov       dl, al
00450a1a: mov       eax, esi
00450a1c: call      0x46d838
00450a21: test      al, al
00450a23: je        0x450a7f
00450a25: mov       eax, ecx
00450a27: movzx     ebp, byte ptr [esp + 0x14]
00450a2c: call      0x41a08c
00450a31: mov       ebx, 0xa
00450a36: and       eax, 0xff
00450a3b: mov       edx, ebp
00450a3d: call      0x475118
00450a42: mov       eax, ecx
00450a44: call      0x41a08c
00450a49: mov       ebx, 6
00450a4e: and       eax, 0xff
00450a53: mov       edx, ebp
00450a55: call      0x475118
00450a5a: mov       eax, ecx
00450a5c: xor       edx, edx
00450a5e: call      0x41a08c
00450a63: mov       dl, al
00450a65: mov       eax, esi
00450a67: call      0x46d8cb
00450a6c: mov       eax, ecx
00450a6e: call      0x41a08c
00450a73: and       eax, 0xff
00450a78: mov       edx, esi
00450a7a: call      0x46d8cb
00450a7f: xor       eax, eax
00450a81: mov       ax, di
00450a84: xor       edx, edx
00450a86: call      0x41a08c
00450a8b: mov       dl, al
00450a8d: xor       eax, eax
00450a8f: mov       al, byte ptr [esp + 0x14]
00450a93: call      0x46d600
00450a98: jmp       0x4510d5
00450a9d: mov       edx, ebp
00450a9f: xor       ebx, ebx
00450aa1: xor       eax, eax
00450aa3: mov       bl, byte ptr [esp + 0x38]
00450aa7: mov       ax, word ptr [esp]
00450aab: call      0x4465df
00450ab0: xor       edx, edx
00450ab2: mov       dx, ax
00450ab5: mov       edi, eax
00450ab7: cmp       edx, ebp
00450ab9: je        0x4510d5
00450abf: mov       eax, edx
00450ac1: shl       eax, 4
00450ac4: add       eax, edx
00450ac6: shl       eax, 2
00450ac9: add       eax, edx
00450acb: mov       ecx, dword ptr [0x4e19a0]
00450ad1: shl       eax, 2
00450ad4: add       ecx, eax
00450ad6: mov       al, byte ptr [ecx + 1]
00450ad9: mov       byte ptr [esp + 0x1c], al
00450add: mov       al, byte ptr [ecx]
00450adf: mov       ebx, ecx
00450ae1: mov       byte ptr [esp + 0x20], al
00450ae5: and       eax, 0xff
00450aea: cmp       eax, 0xc8
00450aef: je        0x450b47
00450af1: call      0x46d817
00450af6: and       eax, 0xff
00450afb: cmp       eax, 1
00450afe: jne       0x450b47
00450b00: xor       eax, eax
00450b02: mov       al, byte ptr [ecx + 2]
00450b05: cmp       eax, 5
00450b08: je        0x450b0f
00450b0a: cmp       eax, 0x12
00450b0d: jne       0x450b47
00450b0f: xor       edx, edx
00450b11: xor       eax, eax
00450b13: mov       dl, byte ptr [ebx]
00450b15: mov       ax, word ptr [ebx + 8]
00450b19: call      0x4539f3
00450b1e: and       eax, 0xffff
00450b23: cmp       eax, 0xffff
00450b28: je        0x450d8a
00450b2e: xor       edx, edx
00450b30: call      0x41aee2
00450b35: mov       dx, ax
00450b38: xor       eax, eax
00450b3a: mov       ax, di
00450b3d: call      0x4457d3
00450b42: jmp       0x450d8a
00450b47: xor       eax, eax
00450b49: mov       al, byte ptr [esp + 0x20]
00450b4d: cmp       eax, 0xc8
00450b52: jne       0x450b59
00450b54: jmp       0x450d8a
00450b59: mov       dl, byte ptr [esp + 0x1c]
00450b5d: cmp       dl, 0xf
00450b60: jb        0x450b88
00450b62: jbe       0x450b84
00450b64: cmp       dl, 0x14
00450b67: jb        0x450b7a
00450b69: cmp       dl, 0x16
00450b6c: jbe       0x450b84
00450b6e: cmp       dl, 0x18
00450b71: jbe       0x450b84
00450b73: cmp       dl, 0x19
00450b76: je        0x450b84
00450b78: jmp       0x450ba0
00450b7a: cmp       dl, 0x10
00450b7d: jbe       0x450b84
00450b7f: cmp       dl, 0x12
00450b82: jb        0x450ba0
00450b84: mov       al, 1
00450b86: jmp       0x450ba2
00450b88: cmp       dl, 3
00450b8b: jb        0x450b84
00450b8d: jbe       0x450b84
00450b8f: cmp       dl, 8
00450b92: jb        0x450ba0
00450b94: jbe       0x450b84
00450b96: cmp       dl, 0xb
00450b99: jb        0x450ba0
00450b9b: cmp       dl, 0xc
00450b9e: jbe       0x450b84
00450ba0: xor       al, al
00450ba2: test      al, al
00450ba4: je        0x450ce4
00450baa: xor       edx, edx
00450bac: mov       dx, di
00450baf: mov       eax, edx
00450bb1: shl       eax, 4
00450bb4: add       eax, edx
00450bb6: shl       eax, 2
00450bb9: add       edx, eax
00450bbb: mov       eax, dword ptr [0x4e19a0]
00450bc0: shl       edx, 2
00450bc3: mov       al, byte ptr [edx + eax + 0xdc]
00450bca: mov       edx, 1
00450bcf: and       eax, 0xff
00450bd4: call      0x467d97
00450bd9: test      al, al
00450bdb: jne       0x450ce4
00450be1: xor       eax, eax
00450be3: mov       al, byte ptr [esp + 0x18]
00450be7: cmp       eax, 1
00450bea: jne       0x450ce4
00450bf0: xor       edx, edx
00450bf2: mov       dx, si
00450bf5: mov       eax, edx
00450bf7: shl       eax, 4
00450bfa: add       eax, edx
00450bfc: shl       eax, 2
00450bff: add       eax, edx
00450c01: mov       edx, dword ptr [0x4e19a0]
00450c07: mov       al, byte ptr [edx + eax*4 + 1]
00450c0b: and       eax, 0xff
00450c10: cmp       eax, 0x11
00450c13: je        0x450c1a
00450c15: cmp       eax, 0xa
00450c18: jne       0x450c1e
00450c1a: xor       al, al
00450c1c: jmp       0x450c35
00450c1e: cmp       eax, 0x10
00450c21: jne       0x450c33
00450c23: mov       cl, byte ptr [esp + 0x1c]
00450c27: cmp       cl, 2
00450c2a: jb        0x450c1a
00450c2c: jbe       0x450c33
00450c2e: cmp       cl, 8
00450c31: jne       0x450c1a
00450c33: mov       al, 1
00450c35: test      al, al
00450c37: je        0x450ce4
00450c3d: xor       ecx, ecx
00450c3f: mov       cx, si
00450c42: mov       eax, ecx
00450c44: shl       eax, 4
00450c47: add       eax, ecx
00450c49: shl       eax, 2
00450c4c: lea       edx, [ecx + eax]
00450c4f: mov       eax, dword ptr [0x4e19a0]
00450c54: shl       edx, 2
00450c57: mov       al, byte ptr [edx + eax]
00450c5a: mov       ah, byte ptr [esp + 0x20]
00450c5e: cmp       al, ah
00450c60: je        0x450ce4
00450c66: xor       edx, edx
00450c68: mov       dl, ah
00450c6a: mov       eax, edx
00450c6c: call      0x46d817
00450c71: and       eax, 0xff
00450c76: cmp       eax, 1
00450c79: jne       0x450cb5
00450c7b: xor       eax, eax
00450c7d: mov       al, byte ptr [ebx + 2]
00450c80: cmp       eax, 7
00450c83: je        0x450c9b
00450c85: mov       eax, dword ptr [0x508f7c]
00450c8a: sub       eax, dword ptr [ebx + 0x110]
00450c90: cmp       eax, 0xfa
00450c95: jbe       0x450d8a
00450c9b: xor       ebx, ebx
00450c9d: xor       edx, edx
00450c9f: xor       eax, eax
00450ca1: mov       dl, byte ptr [esp + 0x18]
00450ca5: mov       bx, si
00450ca8: mov       ax, di
00450cab: call      0x445a36
00450cb0: jmp       0x450d8a
00450cb5: mov       eax, edx
00450cb7: call      0x46d817
00450cbc: and       eax, 0xff
00450cc1: cmp       eax, 2
00450cc4: jne       0x450d8a
00450cca: xor       eax, eax
00450ccc: mov       al, byte ptr [ebx + 2]
00450ccf: cmp       eax, 7
00450cd2: jne       0x450d8a
00450cd8: mov       ebx, ecx
00450cda: xor       edx, edx
00450cdc: xor       eax, eax
00450cde: mov       dl, byte ptr [esp + 0x18]
00450ce2: jmp       0x450ca8
00450ce4: xor       eax, eax
00450ce6: mov       al, byte ptr [esp + 0x18]
00450cea: cmp       eax, 3
00450ced: jne       0x450cff
00450cef: xor       eax, eax
00450cf1: mov       ax, si
00450cf4: call      0x41aee2
00450cf9: mov       dword ptr [esp + 8], eax
00450cfd: jmp       0x450d2d
00450cff: cmp       eax, 1
00450d02: jne       0x450d22
00450d04: xor       edx, edx
00450d06: mov       dx, si
00450d09: mov       eax, edx
00450d0b: shl       eax, 4
00450d0e: add       eax, edx
00450d10: shl       eax, 2
00450d13: add       eax, edx
00450d15: mov       edx, dword ptr [0x4e19a0]
00450d1b: mov       ax, word ptr [edx + eax*4 + 0x7c]
00450d20: jmp       0x450cf9
00450d22: cmp       eax, 4
00450d25: jne       0x450d2d
00450d27: xor       edx, edx
00450d29: mov       dword ptr [esp + 8], edx
00450d2d: xor       ebx, ebx
00450d2f: mov       bx, di
00450d32: mov       ecx, ebx
00450d34: shl       ecx, 4
00450d37: add       ecx, ebx
00450d39: shl       ecx, 2
00450d3c: mov       eax, dword ptr [0x4e19a0]
00450d41: add       ecx, ebx
00450d43: mov       edx, ebx
00450d45: shl       ecx, 2
00450d48: xor       edx, ebx
00450d4a: mov       ax, word ptr [ecx + eax + 0x7c]
00450d4f: mov       dx, ax
00450d52: xor       eax, eax
00450d54: mov       ax, word ptr [esp + 8]
00450d59: call      0x477042
00450d5e: xor       edx, edx
00450d60: mov       dl, al
00450d62: mov       eax, dword ptr [0x4e19a0]
00450d67: mov       ax, word ptr [ecx + eax + 0x7c]
00450d6c: and       eax, 0xffff
00450d71: call      0x4770ee
00450d76: xor       edx, edx
00450d78: mov       dx, ax
00450d7b: cmp       edx, 0xffff
00450d81: je        0x450d8a
00450d83: mov       eax, ebx
00450d85: jmp       0x450b3d
00450d8a: xor       ecx, ecx
00450d8c: xor       ebx, ebx
00450d8e: xor       edx, edx
00450d90: xor       eax, eax
00450d92: mov       cl, byte ptr [esp + 0xc]
00450d96: mov       dl, byte ptr [esp + 0x18]
00450d9a: mov       bx, si
00450d9d: mov       ax, di
00450da0: call      0x4502f0
00450da5: mov       dl, byte ptr [esp + 0x1c]
00450da9: mov       al, 1
00450dab: cmp       dl, 0xe
00450dae: jb        0x450dca
00450db0: jbe       0x450dd9
00450db2: cmp       dl, 0x12
00450db5: jb        0x450dd9
00450db7: jbe       0x450de4
00450db9: cmp       dl, 0x17
00450dbc: jb        0x450de4
00450dbe: cmp       dl, 0x18
00450dc1: jbe       0x450de4
00450dc3: cmp       dl, 0x19
00450dc6: je        0x450dd9
00450dc8: jmp       0x450de6
00450dca: cmp       dl, 6
00450dcd: jb        0x450ddd
00450dcf: cmp       dl, 8
00450dd2: jbe       0x450de4
00450dd4: cmp       dl, 0xb
00450dd7: jb        0x450de4
00450dd9: xor       al, al
00450ddb: jmp       0x450de6
00450ddd: cmp       dl, 3
00450de0: jb        0x450de4
00450de2: jbe       0x450dd9
00450de4: mov       al, 1
00450de6: test      al, al
00450de8: je        0x450e16
00450dea: push      0
00450dec: push      0
00450dee: push      0
00450df0: xor       edx, edx
00450df2: push      0
00450df4: mov       eax, 0xe
00450df9: mov       dx, word ptr [esp + 0x10]
00450dfe: push      0
00450e00: xor       ecx, ecx
00450e02: mov       ebx, edx
00450e04: call      0x46e44c
00450e09: jmp       0x4510b8
00450e0e: mov       al, 1
00450e10: jmp       0x450e2d
00450e12: xor       al, al
00450e14: jmp       0x450e2d
00450e16: mov       al, byte ptr [esp + 0x1c]
00450e1a: sub       al, 0xb
00450e1c: cmp       al, 6
00450e1e: ja        0x450e12
00450e20: and       eax, 0xff
00450e25: jmp       dword ptr cs:[eax*4 + 0x450858]
00450e2d: test      al, al
00450e2f: je        0x4510b8
00450e35: xor       eax, eax
00450e37: mov       al, byte ptr [esp + 0x1c]
00450e3b: xor       dl, dl
00450e3d: cmp       eax, 0x10
00450e40: jne       0x450e44
00450e42: mov       dl, 1
00450e44: mov       eax, 0x22
00450e49: call      0x4704dc
00450e4e: test      al, 1
00450e50: jne       0x450e6f
00450e52: xor       eax, eax
00450e54: mov       al, dl
00450e56: push      eax
00450e57: push      0
00450e59: push      0
00450e5b: xor       edx, edx
00450e5d: push      0
00450e5f: xor       ecx, ecx
00450e61: mov       dx, word ptr [esp + 0x10]
00450e66: push      0
00450e68: mov       eax, 0xf
00450e6d: jmp       0x450e02
00450e6f: xor       eax, eax
00450e71: mov       al, dl
00450e73: push      eax
00450e74: push      0
00450e76: push      0
00450e78: xor       edx, edx
00450e7a: push      0
00450e7c: xor       ecx, ecx
00450e7e: mov       dx, word ptr [esp + 0x10]
00450e83: push      0
00450e85: mov       eax, 0x10
00450e8a: jmp       0x450e02
00450e8f: xor       edx, edx
00450e91: xor       eax, eax
00450e93: mov       dx, di
00450e96: mov       ax, si
00450e99: mov       esi, edx
00450e9b: xor       ecx, ecx
00450e9d: shl       esi, 4
00450ea0: call      0x41a08c
00450ea5: add       esi, edx
00450ea7: mov       bl, al
00450ea9: shl       esi, 2
00450eac: mov       byte ptr [esp + 0x10], al
00450eb0: add       esi, edx
00450eb2: mov       eax, dword ptr [0x4e19a0]
00450eb7: shl       esi, 2
00450eba: xor       edx, edx
00450ebc: mov       al, byte ptr [esi + eax]
00450ebf: mov       cl, bl
00450ec1: mov       dl, al
00450ec3: mov       eax, ecx
00450ec5: call      0x46d838
00450eca: test      al, al
00450ecc: je        0x450f2a
00450ece: mov       eax, dword ptr [0x4e19a0]
00450ed3: movzx     ebp, bl
00450ed6: mov       al, byte ptr [esi + eax]
00450ed9: mov       ebx, 0xa
00450ede: and       eax, 0xff
00450ee3: mov       edx, ebp
00450ee5: call      0x475118
00450eea: mov       eax, dword ptr [0x4e19a0]
00450eef: mov       al, byte ptr [esi + eax]
00450ef2: mov       ebx, 6
00450ef7: and       eax, 0xff
00450efc: mov       edx, ebp
00450efe: call      0x475118
00450f03: mov       eax, dword ptr [0x4e19a0]
00450f08: xor       edx, edx
00450f0a: mov       al, byte ptr [esi + eax]
00450f0d: mov       dl, al
00450f0f: mov       eax, ecx
00450f11: call      0x46d8cb
00450f16: mov       eax, dword ptr [0x4e19a0]
00450f1b: mov       al, byte ptr [esi + eax]
00450f1e: and       eax, 0xff
00450f23: mov       edx, ecx
00450f25: call      0x46d8cb
00450f2a: xor       edx, edx
00450f2c: mov       dx, di
00450f2f: mov       eax, edx
00450f31: shl       eax, 4
00450f34: add       eax, edx
00450f36: shl       eax, 2
00450f39: add       eax, edx
00450f3b: mov       edx, dword ptr [0x4e19a0]
00450f41: mov       al, byte ptr [edx + eax*4]
00450f44: xor       edx, edx
00450f46: mov       dl, al
00450f48: xor       eax, eax
00450f4a: mov       al, byte ptr [esp + 0x10]
00450f4e: jmp       0x450a93
00450f53: xor       edx, edx
00450f55: mov       dx, si
00450f58: mov       eax, edx
00450f5a: shl       eax, 4
00450f5d: add       eax, edx
00450f5f: shl       eax, 2
00450f62: add       eax, edx
00450f64: xor       edx, edx
00450f66: mov       dx, di
00450f69: mov       esi, edx
00450f6b: shl       esi, 4
00450f6e: add       esi, edx
00450f70: shl       esi, 2
00450f73: add       esi, edx
00450f75: mov       ecx, dword ptr [0x4e19a0]
00450f7b: shl       esi, 2
00450f7e: mov       bl, byte ptr [ecx + eax*4]
00450f81: mov       al, byte ptr [ecx + esi]
00450f84: xor       ecx, ecx
00450f86: xor       edx, edx
00450f88: mov       cl, bl
00450f8a: mov       dl, al
00450f8c: mov       eax, ecx
00450f8e: mov       byte ptr [esp + 0x24], bl
00450f92: call      0x46d838
00450f97: test      al, al
00450f99: je        0x450ff7
00450f9b: mov       eax, dword ptr [0x4e19a0]
00450fa0: movzx     ebp, bl
00450fa3: mov       al, byte ptr [esi + eax]
00450fa6: mov       ebx, 0xa
00450fab: and       eax, 0xff
00450fb0: mov       edx, ebp
00450fb2: call      0x475118
00450fb7: mov       eax, dword ptr [0x4e19a0]
00450fbc: mov       al, byte ptr [esi + eax]
00450fbf: mov       ebx, 6
00450fc4: and       eax, 0xff
00450fc9: mov       edx, ebp
00450fcb: call      0x475118
00450fd0: mov       eax, dword ptr [0x4e19a0]
00450fd5: xor       edx, edx
00450fd7: mov       al, byte ptr [esi + eax]
00450fda: mov       dl, al
00450fdc: mov       eax, ecx
00450fde: call      0x46d8cb
00450fe3: mov       eax, dword ptr [0x4e19a0]
00450fe8: mov       al, byte ptr [esi + eax]
00450feb: and       eax, 0xff
00450ff0: mov       edx, ecx
00450ff2: call      0x46d8cb
00450ff7: xor       edx, edx
00450ff9: mov       dx, di
00450ffc: mov       ebx, edx
00450ffe: shl       ebx, 4
00451001: add       ebx, edx
00451003: shl       ebx, 2
00451006: add       ebx, edx
00451008: mov       eax, dword ptr [0x4e19a0]
0045100d: shl       ebx, 2
00451010: xor       edx, edx
00451012: mov       al, byte ptr [ebx + eax]
00451015: mov       dl, al
00451017: xor       eax, eax
00451019: mov       al, byte ptr [esp + 0x24]
0045101d: call      0x46d600
00451022: mov       eax, dword ptr [0x4e19a0]
00451027: add       eax, ebx
00451029: mov       dl, byte ptr [eax]
0045102b: cmp       dl, byte ptr [esp + 0x24]
0045102f: je        0x4510d5
00451035: mov       cl, byte ptr [0x508041]
0045103b: mov       ebx, eax
0045103d: cmp       dl, cl
0045103f: jne       0x4510d5
00451045: mov       eax, dword ptr [0x4e19c0]
0045104a: mov       ecx, dword ptr [0x508f7c]
00451050: cmp       eax, ecx
00451052: ja        0x451065
00451054: mov       esi, dword ptr [0x4e19c0]
0045105a: mov       eax, ecx
0045105c: sub       eax, esi
0045105e: cmp       eax, 0xc8
00451063: jb        0x4510d5
00451065: xor       edx, edx
00451067: mov       eax, dword ptr [0x508f7c]
0045106c: mov       dx, di
0045106f: mov       dword ptr [0x4e19c0], eax
00451074: mov       eax, edx
00451076: shl       eax, 4
00451079: add       eax, edx
0045107b: shl       eax, 2
0045107e: add       edx, eax
00451080: mov       eax, dword ptr [0x4e19a0]
00451085: shl       edx, 2
00451088: mov       ax, word ptr [edx + eax + 0x7c]
0045108d: mov       word ptr [0x496acc], ax
00451093: xor       eax, eax
00451095: mov       al, byte ptr [ebx + 1]
00451098: push      0x100
0045109d: shl       eax, 0x10
004510a0: xor       ecx, ecx
004510a2: or        ah, 7
004510a5: mov       ebx, 0x496ac8
004510aa: mov       edx, eax
004510ac: mov       eax, 0x50
004510b1: call      0x48aa79
004510b6: jmp       0x4510d5
004510b8: mov       ch, byte ptr [esp + 0x18]
004510bc: cmp       ch, 3
004510bf: jb        0x4510cc
004510c1: jbe       0x450e8f
004510c7: cmp       ch, 4
004510ca: jmp       0x4510cf
004510cc: cmp       ch, 1
004510cf: je        0x450f53
004510d5: add       esp, 0x28
004510d8: jmp       0x4462aa
