
; PlayerGetSympathie 0x46dc6c..0x46dc90
0046dc6c: push      ebx
0046dc6d: mov       bl, dl
0046dc6f: xor       edx, edx
0046dc71: mov       dl, al
0046dc73: mov       eax, edx
0046dc75: shl       eax, 2
0046dc78: add       eax, edx
0046dc7a: mov       edx, dword ptr [0x5080a8]
0046dc80: shl       eax, 2
0046dc83: add       edx, eax
0046dc85: xor       eax, eax
0046dc87: mov       al, bl
0046dc89: mov       ax, word ptr [edx + eax*2 + 0xc]
0046dc8e: pop       ebx
0046dc8f: ret       

; PlayerSetSympathie 0x46dc90..0x46dcb4
0046dc90: push      ecx
0046dc91: mov       cl, dl
0046dc93: xor       edx, edx
0046dc95: mov       dl, al
0046dc97: mov       eax, edx
0046dc99: shl       eax, 2
0046dc9c: add       eax, edx
0046dc9e: mov       edx, dword ptr [0x5080a8]
0046dca4: shl       eax, 2
0046dca7: add       edx, eax
0046dca9: xor       eax, eax
0046dcab: mov       al, cl
0046dcad: mov       word ptr [edx + eax*2 + 0xc], bx
0046dcb2: pop       ecx
0046dcb3: ret       

; iaProbReturnTo 0x47da54..0x47da7a
0047da54: push      ebx
0047da55: mov       ebx, edx
0047da57: mov       edx, eax
0047da59: shl       eax, 2
0047da5c: sub       eax, edx
0047da5e: shl       eax, 5
0047da61: add       eax, 0x512320
0047da66: mov       byte ptr [eax + 0x5e], 0
0047da6a: mov       byte ptr [eax + 0x5f], 1
0047da6e: mov       dword ptr [eax + 0x14], 0
0047da75: mov       dword ptr [eax + 0x54], ebx
0047da78: pop       ebx
0047da79: ret       

; iagWarUnlockTargetAfterDeath 0x48873f..0x48884d
0048873f: push      ebx
00488740: push      ecx
00488741: push      esi
00488742: push      edi
00488743: mov       edi, eax
00488745: mov       ebx, edx
00488747: cmp       eax, 0xffff
0048874c: je        0x488848
00488752: mov       edx, eax
00488754: shl       eax, 4
00488757: add       eax, edi
00488759: shl       eax, 2
0048875c: add       eax, edi
0048875e: mov       esi, dword ptr [0x4e19a0]
00488764: shl       eax, 2
00488767: add       esi, eax
00488769: xor       edx, edi
0048876b: mov       dl, byte ptr [esi]
0048876d: mov       eax, edx
0048876f: shl       eax, 4
00488772: add       eax, edx
00488774: shl       eax, 2
00488777: mov       edx, eax
00488779: shl       eax, 6
0048877c: add       eax, edx
0048877e: mov       edx, 0x51bcfc
00488783: add       edx, eax
00488785: mov       eax, ebx
00488787: shl       eax, 4
0048878a: add       eax, ebx
0048878c: add       edx, 0x28
0048878f: shl       eax, 4
00488792: mov       si, word ptr [esi + 0xb8]
00488799: add       edx, eax
0048879b: xor       eax, eax
0048879d: mov       ax, si
004887a0: cmp       eax, 0xffff
004887a5: je        0x488848
004887ab: lea       ebx, [edx + 0x10]
004887ae: xor       eax, eax
004887b0: jmp       0x4887b6
004887b2: add       ebx, 8
004887b5: inc       eax
004887b6: xor       ecx, ecx
004887b8: mov       cx, word ptr [edx + 0xe]
004887bc: cmp       eax, ecx
004887be: jge       0x488848
004887c4: mov       cx, word ptr [ebx]
004887c7: cmp       si, cx
004887ca: jne       0x4887b2
004887cc: mov       edx, ecx
004887ce: mov       ecx, edi
004887d0: shl       ecx, 4
004887d3: add       ecx, edi
004887d5: shl       ecx, 2
004887d8: add       ecx, edi
004887da: shl       ecx, 2
004887dd: test      dh, 0x80
004887e0: je        0x4887f2
004887e2: mov       eax, dword ptr [0x4e19a0]
004887e7: mov       al, byte ptr [ecx + eax + 1]
004887eb: mov       edx, 0x1a
004887f0: jmp       0x48881a
004887f2: and       edx, 0xffff
004887f8: mov       eax, edx
004887fa: shl       eax, 4
004887fd: add       eax, edx
004887ff: shl       eax, 2
00488802: add       edx, eax
00488804: mov       eax, dword ptr [0x4e19a0]
00488809: shl       edx, 2
0048880c: mov       dl, byte ptr [edx + eax + 1]
00488810: and       edx, 0xff
00488816: mov       al, byte ptr [ecx + eax + 1]
0048881a: and       eax, 0xff
0048881f: call      0x44f98a
00488824: and       eax, 0xff
00488829: xor       ecx, ecx
0048882b: mov       cx, word ptr [ebx + 2]
0048882f: mov       edx, eax
00488831: cmp       ecx, eax
00488833: jge       0x488840
00488835: mov       word ptr [ebx + 2], 0
0048883b: pop       edi
0048883c: pop       esi
0048883d: pop       ecx
0048883e: pop       ebx
0048883f: ret       
00488840: mov       esi, ecx
00488842: sub       esi, eax
00488844: mov       word ptr [ebx + 2], si
00488848: pop       edi
00488849: pop       esi
0048884a: pop       ecx
0048884b: pop       ebx
0048884c: ret       

; iagWarProbReturnTo 0x488cea..0x488d21
00488cea: push      ecx
00488ceb: push      esi
00488cec: mov       ecx, edx
00488cee: mov       edx, eax
00488cf0: shl       eax, 4
00488cf3: add       eax, edx
00488cf5: shl       eax, 2
00488cf8: mov       esi, eax
00488cfa: shl       esi, 6
00488cfd: mov       edx, ecx
00488cff: add       esi, eax
00488d01: mov       eax, edx
00488d03: shl       eax, 4
00488d06: add       eax, edx
00488d08: shl       eax, 4
00488d0b: mov       eax, dword ptr [esi + eax + 0x51bd2c]
00488d12: cmp       eax, -1
00488d15: je        0x488d1e
00488d17: mov       edx, ebx
00488d19: call      0x47da54
00488d1e: pop       esi
00488d1f: pop       ecx
00488d20: ret       

; iabTouche_AjouteEnnemiOuNeChangePasDeCibleOuAlerteConflit 0x489bc8..0x489c36
00489bc8: push      ebx
00489bc9: push      ecx
00489bca: push      esi
00489bcb: push      edi
00489bcc: mov       edi, eax
00489bce: shl       edi, 4
00489bd1: add       edi, eax
00489bd3: shl       edi, 2
00489bd6: add       edi, eax
00489bd8: mov       eax, dword ptr [0x4e19a0]
00489bdd: shl       edi, 2
00489be0: add       eax, edi
00489be2: mov       ecx, dword ptr [eax + 0x10c]
00489be8: shl       ecx, 5
00489beb: add       ecx, 0x51a9e0
00489bf1: je        0x489c31
00489bf3: mov       ebx, dword ptr [ecx + 0xc]
00489bf6: cmp       ebx, -1
00489bf9: je        0x489c31
00489bfb: mov       esi, ebx
00489bfd: mov       al, byte ptr [eax]
00489bff: and       eax, 0xff
00489c04: mov       ebx, edx
00489c06: mov       edx, esi
00489c08: call      0x487b78
00489c0d: and       eax, 0xff
00489c12: cmp       eax, 1
00489c15: jne       0x489c31
00489c17: mov       eax, dword ptr [0x4e19a0]
00489c1c: mov       edx, dword ptr [ecx + 0xc]
00489c1f: mov       al, byte ptr [edi + eax]
00489c22: mov       ebx, 0xffffffff
00489c27: and       eax, 0xff
00489c2c: call      0x488cea
00489c31: pop       edi
00489c32: pop       esi
00489c33: pop       ecx
00489c34: pop       ebx
00489c35: ret       
