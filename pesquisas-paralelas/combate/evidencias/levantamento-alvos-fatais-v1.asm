
; iagWarRemoveEnnemyFromBattle 0x487e2a..0x487eef
00487e2a: push      ecx
00487e2b: push      esi
00487e2c: push      edi
00487e2d: sub       esp, 4
00487e30: mov       ecx, eax
00487e32: mov       esi, edx
00487e34: mov       dword ptr [esp], ebx
00487e37: test      byte ptr [esp + 1], 0x80
00487e3c: je        0x487e50
00487e3e: mov       eax, dword ptr [esp]
00487e41: and       ah, 0x7f
00487e44: and       eax, 0xffff
00487e49: call      0x41a08c
00487e4e: jmp       0x487e5b
00487e50: xor       eax, eax
00487e52: mov       ax, word ptr [esp]
00487e56: call      0x442045
00487e5b: and       eax, 0xff
00487e60: cmp       eax, ecx
00487e62: je        0x487ee8
00487e68: cmp       dword ptr [esp], 0xffff
00487e6f: je        0x487ee8
00487e75: mov       eax, ecx
00487e77: shl       eax, 4
00487e7a: add       eax, ecx
00487e7c: shl       eax, 2
00487e7f: mov       edx, eax
00487e81: shl       eax, 6
00487e84: mov       ebx, 0x51bcfc
00487e89: add       eax, edx
00487e8b: add       ebx, eax
00487e8d: mov       eax, esi
00487e8f: shl       eax, 4
00487e92: add       eax, esi
00487e94: lea       edx, [ebx + 0x28]
00487e97: shl       eax, 4
00487e9a: mov       edi, dword ptr [esp]
00487e9d: add       edx, eax
00487e9f: xor       ebx, ebx
00487ea1: lea       eax, [edx + 0x10]
00487ea4: jmp       0x487eaa
00487ea6: add       eax, 8
00487ea9: inc       ebx
00487eaa: xor       ecx, ecx
00487eac: mov       cx, word ptr [edx + 0xe]
00487eb0: cmp       ebx, ecx
00487eb2: jge       0x487ee8
00487eb4: xor       esi, esi
00487eb6: mov       si, word ptr [eax]
00487eb9: cmp       esi, edi
00487ebb: jne       0x487ea6
00487ebd: dec       ecx
00487ebe: cmp       ebx, ecx
00487ec0: jge       0x487ee4
00487ec2: mov       eax, ebx
00487ec4: shl       eax, 3
00487ec7: mov       ecx, ebx
00487ec9: add       eax, edx
00487ecb: jmp       0x487ed9
00487ecd: lea       edi, [eax + 0x10]
00487ed0: lea       esi, [eax + 0x18]
00487ed3: add       eax, 8
00487ed6: inc       ecx
00487ed7: movsd     dword ptr es:[edi], dword ptr [esi]
00487ed8: movsd     dword ptr es:[edi], dword ptr [esi]
00487ed9: xor       ebx, ebx
00487edb: mov       bx, word ptr [edx + 0xe]
00487edf: dec       ebx
00487ee0: cmp       ecx, ebx
00487ee2: jl        0x487ecd
00487ee4: dec       word ptr [edx + 0xe]
00487ee8: add       esp, 4
00487eeb: pop       edi
00487eec: pop       esi
00487eed: pop       ecx
00487eee: ret       

; None 0x487eef..0x48829d
00487eef: push      ebx
00487ef0: push      ecx
00487ef1: push      esi
00487ef2: push      edi
00487ef3: push      ebp
00487ef4: sub       esp, 0x14
00487ef7: push      eax
00487ef8: push      edx
00487ef9: mov       eax, dword ptr [eax]
00487efb: mov       edx, 0x51a9e0
00487f00: shl       eax, 5
00487f03: add       edx, eax
00487f05: mov       dword ptr [esp + 0xc], edx
00487f09: je        0x488100
00487f0f: mov       eax, dword ptr [esp + 0xc]
00487f13: xor       edx, edx
00487f15: mov       ebx, dword ptr [esp + 0xc]
00487f19: mov       dx, word ptr [eax + 0x10]
00487f1d: xor       eax, eax
00487f1f: mov       ax, word ptr [ebx + 0x12]
00487f23: test      eax, eax
00487f25: je        0x488100
00487f2b: cmp       edx, 0xffff
00487f31: je        0x488100
00487f37: mov       eax, dword ptr [esp]
00487f3a: mov       ebx, dword ptr [esp + 4]
00487f3e: shl       eax, 3
00487f41: add       eax, ebx
00487f43: xor       edi, edi
00487f45: mov       di, word ptr [eax + 0x12]
00487f49: mov       ax, word ptr [eax + 0x10]
00487f4d: and       eax, 0xffff
00487f52: mov       dword ptr [esp + 0x14], eax
00487f56: test      byte ptr [esp + 0x15], 0x80
00487f5b: je        0x487f92
00487f5d: mov       eax, dword ptr [esp + 0x14]
00487f61: xor       edx, edx
00487f63: and       ah, 0x7f
00487f66: mov       dx, ax
00487f69: mov       eax, edx
00487f6b: shl       eax, 4
00487f6e: add       eax, edx
00487f70: shl       eax, 2
00487f73: add       eax, edx
00487f75: shl       eax, 2
00487f78: add       eax, 0x49a0c8
00487f7d: xor       edx, edx
00487f7f: mov       dx, word ptr [eax + 0xa]
00487f83: mov       ax, word ptr [eax + 6]
00487f87: and       eax, 0xffff
00487f8c: sub       edx, eax
00487f8e: mov       eax, edx
00487f90: jmp       0x487fb8
00487f92: xor       edx, edx
00487f94: mov       dx, word ptr [esp + 0x14]
00487f99: mov       eax, edx
00487f9b: shl       eax, 4
00487f9e: add       eax, edx
00487fa0: shl       eax, 2
00487fa3: add       eax, edx
00487fa5: mov       edx, dword ptr [0x4e19a0]
00487fab: mov       ax, word ptr [edx + eax*4 + 0x9a]
00487fb3: and       eax, 0xffff
00487fb8: mov       dword ptr [esp + 8], eax
00487fbc: mov       eax, dword ptr [esp + 0x14]
00487fc0: mov       ecx, 1
00487fc5: and       ah, 0x7f
00487fc8: mov       dword ptr [esp + 0x10], ecx
00487fcc: mov       dword ptr [esp + 0x18], eax
00487fd0: jmp       0x487fd6
00487fd2: dec       dword ptr [esp + 0x10]
00487fd6: cmp       dword ptr [esp + 0x10], 0
00487fdb: jl        0x4880f0
00487fe1: cmp       edi, dword ptr [esp + 8]
00487fe5: jge       0x4880f0
00487feb: mov       eax, dword ptr [esp + 0xc]
00487fef: xor       ecx, ecx
00487ff1: mov       cx, word ptr [eax + 0x10]
00487ff5: cmp       ecx, 0xffff
00487ffb: je        0x487fd2
00487ffd: cmp       edi, dword ptr [esp + 8]
00488001: jge       0x487fd2
00488003: imul      esi, ecx, 0x114
00488009: mov       eax, dword ptr [0x4e19a0]
0048800e: add       esi, eax
00488010: xor       eax, eax
00488012: mov       ax, word ptr [esi + 0xb8]
00488019: cmp       eax, 0xffff
0048801e: jne       0x4880e2
00488024: cmp       dword ptr [esp + 0x10], 0
00488029: je        0x488062
0048802b: mov       dl, byte ptr [esp + 0x15]
0048802f: mov       eax, ecx
00488031: test      dl, 0x80
00488034: je        0x488044
00488036: xor       ebx, ebx
00488038: mov       bx, word ptr [esp + 0x18]
0048803d: mov       edx, 3
00488042: jmp       0x488050
00488044: xor       ebx, ebx
00488046: mov       bx, word ptr [esp + 0x14]
0048804b: mov       edx, 1
00488050: and       eax, 0xffff
00488055: call      0x446cb5
0048805a: test      al, al
0048805c: je        0x4880e2
00488062: imul      ebp, ecx, 0x114
00488068: test      byte ptr [esp + 0x15], 0x80
0048806d: je        0x488084
0048806f: mov       eax, dword ptr [0x4e19a0]
00488074: mov       al, byte ptr [eax + ebp + 1]
00488078: mov       edx, 0x1a
0048807d: and       eax, 0xff
00488082: jmp       0x4880a3
00488084: xor       eax, eax
00488086: mov       ax, word ptr [esp + 0x14]
0048808b: imul      eax, eax, 0x114
00488091: mov       ebx, dword ptr [0x4e19a0]
00488097: xor       edx, edx
00488099: mov       dl, byte ptr [ebx + eax + 1]
0048809d: xor       eax, eax
0048809f: mov       al, byte ptr [ebx + ebp + 1]
004880a3: call      0x44f98a
004880a8: and       eax, 0xff
004880ad: test      eax, eax
004880af: jle       0x4880e2
004880b1: mov       bl, byte ptr [esp + 0x15]
004880b5: add       edi, eax
004880b7: mov       eax, ecx
004880b9: test      bl, 0x80
004880bc: je        0x4880cc
004880be: xor       ebx, ebx
004880c0: mov       bx, word ptr [esp + 0x18]
004880c5: mov       edx, 3
004880ca: jmp       0x4880d8
004880cc: xor       ebx, ebx
004880ce: mov       bx, word ptr [esp + 0x14]
004880d3: mov       edx, 1
004880d8: and       eax, 0xffff
004880dd: call      0x445a36
004880e2: xor       ecx, ecx
004880e4: mov       cx, word ptr [esi + 0x108]
004880eb: jmp       0x487ff5
004880f0: mov       eax, dword ptr [esp]
004880f3: mov       edx, dword ptr [esp + 4]
004880f7: shl       eax, 3
004880fa: add       eax, edx
004880fc: mov       word ptr [eax + 0x12], di
00488100: add       esp, 0x1c
00488103: jmp       0x486a98
00488108: push      ebx
00488109: test      dh, 0x80
0048810c: je        0x48811d
0048810e: and       dh, 0x7f
00488111: xor       ebx, ebx
00488113: mov       bx, dx
00488116: mov       edx, 3
0048811b: jmp       0x488127
0048811d: xor       ebx, ebx
0048811f: mov       bx, dx
00488122: mov       edx, 1
00488127: and       eax, 0xffff
0048812c: call      0x445a36
00488131: pop       ebx
00488132: ret       
00488133: push      ebx
00488134: push      ecx
00488135: mov       ebx, edx
00488137: mov       ecx, eax
00488139: shl       ecx, 4
0048813c: add       ecx, eax
0048813e: shl       ecx, 2
00488141: add       ecx, eax
00488143: shl       ecx, 2
00488146: test      dh, 0x80
00488149: je        0x488160
0048814b: mov       eax, dword ptr [0x4e19a0]
00488150: mov       al, byte ptr [ecx + eax + 1]
00488154: mov       edx, 0x1a
00488159: and       eax, 0xff
0048815e: jmp       0x48818a
00488160: xor       edx, edx
00488162: mov       dx, bx
00488165: mov       eax, edx
00488167: shl       eax, 4
0048816a: add       eax, edx
0048816c: shl       eax, 2
0048816f: add       edx, eax
00488171: mov       eax, dword ptr [0x4e19a0]
00488176: shl       edx, 2
00488179: mov       dl, byte ptr [edx + eax + 1]
0048817d: add       ecx, eax
0048817f: xor       eax, eax
00488181: and       edx, 0xff
00488187: mov       al, byte ptr [ecx + 1]
0048818a: call      0x44f98a
0048818f: and       eax, 0xff
00488194: pop       ecx
00488195: pop       ebx
00488196: ret       
00488197: test      ah, 0x80
0048819a: je        0x4881ab
0048819c: and       ah, 0x7f
0048819f: and       eax, 0xffff
004881a4: call      0x41a08c
004881a9: jmp       0x4881b5
004881ab: and       eax, 0xffff
004881b0: call      0x442045
004881b5: and       eax, 0xff
004881ba: ret       
004881bb: push      edx
004881bc: test      ah, 0x80
004881bf: je        0x4881ea
004881c1: and       ah, 0x7f
004881c4: xor       edx, edx
004881c6: mov       dx, ax
004881c9: mov       eax, edx
004881cb: shl       eax, 4
004881ce: add       eax, edx
004881d0: shl       eax, 2
004881d3: add       eax, edx
004881d5: mov       al, byte ptr [eax*4 + 0x49a0d0]
004881dc: and       eax, 0xff
004881e1: mov       eax, dword ptr [eax*4 + 0x498d5c]
004881e8: pop       edx
004881e9: ret       
004881ea: xor       edx, edx
004881ec: mov       dx, ax
004881ef: mov       eax, edx
004881f1: shl       eax, 4
004881f4: add       eax, edx
004881f6: shl       eax, 2
004881f9: add       edx, eax
004881fb: mov       eax, dword ptr [0x4e19a0]
00488200: shl       edx, 2
00488203: mov       al, byte ptr [edx + eax + 1]
00488207: and       eax, 0xff
0048820c: mov       eax, dword ptr [eax*4 + 0x498cf4]
00488213: pop       edx
00488214: ret       
00488215: push      edx
00488216: test      ah, 0x80
00488219: je        0x48824c
0048821b: and       ah, 0x7f
0048821e: xor       edx, edx
00488220: mov       dx, ax
00488223: mov       eax, edx
00488225: shl       eax, 4
00488228: add       eax, edx
0048822a: shl       eax, 2
0048822d: add       eax, edx
0048822f: shl       eax, 2
00488232: add       eax, 0x49a0c8
00488237: xor       edx, edx
00488239: mov       dx, word ptr [eax + 0xa]
0048823d: mov       ax, word ptr [eax + 6]
00488241: and       eax, 0xffff
00488246: sub       edx, eax
00488248: mov       eax, edx
0048824a: pop       edx
0048824b: ret       
0048824c: xor       edx, edx
0048824e: mov       dx, ax
00488251: mov       eax, edx
00488253: shl       eax, 4
00488256: add       eax, edx
00488258: shl       eax, 2
0048825b: add       eax, edx
0048825d: mov       edx, dword ptr [0x4e19a0]
00488263: mov       ax, word ptr [edx + eax*4 + 0x9a]
0048826b: and       eax, 0xffff
00488270: pop       edx
00488271: ret       
00488272: push      ebx
00488273: test      dh, 0x80
00488276: je        0x488287
00488278: and       dh, 0x7f
0048827b: xor       ebx, ebx
0048827d: mov       bx, dx
00488280: mov       edx, 3
00488285: jmp       0x488291
00488287: xor       ebx, ebx
00488289: mov       bx, dx
0048828c: mov       edx, 1
00488291: and       eax, 0xffff
00488296: call      0x446cb5
0048829b: pop       ebx
0048829c: ret       

; iagWarNewTargetForUnit 0x48829d..0x48873f
0048829d: push      ebx
0048829e: push      ecx
0048829f: push      esi
004882a0: push      edi
004882a1: push      ebp
004882a2: sub       esp, 0x28
004882a5: push      eax
004882a6: push      edx
004882a7: mov       edx, eax
004882a9: shl       eax, 4
004882ac: add       eax, edx
004882ae: shl       eax, 2
004882b1: add       eax, edx
004882b3: mov       edx, dword ptr [0x4e19a0]
004882b9: mov       al, byte ptr [edx + eax*4]
004882bc: and       eax, 0xff
004882c1: mov       edx, dword ptr [esp + 4]
004882c5: mov       dword ptr [esp + 0x24], eax
004882c9: cmp       edx, 0xffff
004882cf: jne       0x4882db
004882d1: mov       ecx, 0xffff
004882d6: jmp       0x488735
004882db: mov       edx, eax
004882dd: shl       eax, 4
004882e0: add       eax, edx
004882e2: shl       eax, 2
004882e5: mov       edx, eax
004882e7: shl       eax, 6
004882ea: mov       ebx, 0x51bcfc
004882ef: add       eax, edx
004882f1: mov       edx, dword ptr [esp]
004882f4: add       ebx, eax
004882f6: mov       eax, edx
004882f8: shl       eax, 4
004882fb: add       eax, edx
004882fd: add       ebx, 0x28
00488300: shl       eax, 4
00488303: lea       ebp, [ebx + eax]
00488306: xor       eax, eax
00488308: mov       ax, word ptr [ebp + 0xe]
0048830c: test      eax, eax
0048830e: jne       0x488518
00488314: mov       eax, dword ptr [esp + 0x24]
00488318: mov       dword ptr [esp + 0x28], eax
0048831c: mov       eax, dword ptr [ebp + 4]
0048831f: mov       edx, eax
00488321: mov       ecx, 0x100
00488326: sar       edx, 0x1f
00488329: idiv      ecx
0048832b: mov       eax, dword ptr [ebp + 4]
0048832e: mov       ecx, edx
00488330: mov       edx, eax
00488332: sar       edx, 0x1f
00488335: shl       edx, 8
00488338: sbb       eax, edx
0048833a: sar       eax, 8
0048833d: xor       edx, edx
0048833f: mov       esi, ecx
00488341: mov       dx, word ptr [ebp + 0xc]
00488345: sub       esi, edx
00488347: mov       ebx, ebp
00488349: mov       edx, esi
0048834b: test      esi, esi
0048834d: jge       0x488351
0048834f: xor       edx, esi
00488351: mov       dword ptr [esp + 0xc], edx
00488355: xor       edx, edx
00488357: mov       esi, eax
00488359: mov       dx, word ptr [ebx + 0xc]
0048835d: sub       esi, edx
0048835f: mov       edx, esi
00488361: test      esi, esi
00488363: jge       0x488367
00488365: xor       edx, esi
00488367: mov       edi, edx
00488369: xor       edx, edx
0048836b: mov       dx, word ptr [ebx + 0xc]
0048836f: add       ecx, edx
00488371: cmp       ecx, 0x100
00488377: jl        0x48837e
00488379: mov       ecx, 0xff
0048837e: xor       edx, edx
00488380: mov       dx, word ptr [ebx + 0xc]
00488384: add       edx, eax
00488386: mov       dword ptr [esp + 0x14], ecx
0048838a: cmp       edx, 0x100
00488390: jl        0x488397
00488392: mov       edx, 0xff
00488397: mov       ebx, 0xffff
0048839c: mov       eax, edi
0048839e: shl       edx, 8
004883a1: xor       esi, esi
004883a3: mov       dword ptr [esp + 0x2c], ebx
004883a7: shl       eax, 8
004883aa: mov       dword ptr [esp + 0x20], edx
004883ae: mov       dword ptr [esp + 0x10], eax
004883b2: jmp       0x4883bc
004883b4: add       dword ptr [esp + 0x10], 0x100
004883bc: mov       eax, dword ptr [esp + 0x10]
004883c0: cmp       eax, dword ptr [esp + 0x20]
004883c4: jg        0x4884f9
004883ca: mov       ecx, dword ptr [esp + 0xc]
004883ce: mov       edi, ecx
004883d0: lea       ebx, [eax + ecx]
004883d3: jmp       0x4884b9
004883d8: mov       eax, 0xffff
004883dd: xor       ecx, ecx
004883df: mov       cx, ax
004883e2: cmp       ecx, 0xffff
004883e8: je        0x488435
004883ea: mov       eax, ecx
004883ec: call      0x443dad
004883f1: test      al, al
004883f3: je        0x488435
004883f5: mov       eax, ecx
004883f7: call      0x44113e
004883fc: and       eax, 0xffff
00488401: cmp       eax, ebx
00488403: jne       0x488435
00488405: xor       edx, edx
00488407: mov       eax, ecx
00488409: mov       dl, byte ptr [esp + 0x28]
0048840d: call      0x446fbf
00488412: test      al, al
00488414: je        0x488435
00488416: mov       eax, ecx
00488418: call      0x442025
0048841d: and       eax, 0xff
00488422: mov       eax, dword ptr [eax*4 + 0x498cf4]
00488429: cmp       eax, esi
0048842b: jle       0x488435
0048842d: mov       edx, ecx
0048842f: mov       esi, eax
00488431: mov       dword ptr [esp + 0x2c], edx
00488435: xor       eax, eax
00488437: mov       ax, bx
0048843a: mov       ecx, dword ptr [0x4e0f38]
00488440: add       eax, eax
00488442: add       ecx, eax
00488444: test      byte ptr [ecx + 1], 0x80
00488448: je        0x48845c
0048844a: mov       ax, word ptr [ecx]
0048844d: and       eax, 0x7fe0
00488452: and       eax, 0xffff
00488457: sar       eax, 5
0048845a: jmp       0x488461
0048845c: mov       eax, 0xffff
00488461: xor       ecx, ecx
00488463: mov       cx, ax
00488466: cmp       ecx, 0xffff
0048846c: je        0x4884b7
0048846e: mov       eax, ecx
00488470: call      0x41a735
00488475: test      al, al
00488477: je        0x4884b7
00488479: mov       eax, ecx
0048847b: call      0x41a70b
00488480: test      al, al
00488482: jne       0x4884b7
00488484: xor       edx, edx
00488486: mov       eax, ecx
00488488: mov       dl, byte ptr [esp + 0x28]
0048848c: call      0x41a61c
00488491: test      al, al
00488493: je        0x4884b7
00488495: mov       eax, ecx
00488497: call      0x41a4f4
0048849c: and       eax, 0xff
004884a1: mov       eax, dword ptr [eax*4 + 0x498d5c]
004884a8: cmp       eax, esi
004884aa: jle       0x4884b7
004884ac: mov       edx, ecx
004884ae: or        dh, 0x80
004884b1: mov       esi, eax
004884b3: mov       dword ptr [esp + 0x2c], edx
004884b7: inc       ebx
004884b8: inc       edi
004884b9: cmp       edi, dword ptr [esp + 0x14]
004884bd: jg        0x4883b4
004884c3: xor       eax, eax
004884c5: mov       ax, bx
004884c8: mov       ecx, dword ptr [0x4e0f38]
004884ce: add       eax, eax
004884d0: add       ecx, eax
004884d2: mov       ax, word ptr [ecx]
004884d5: xor       al, al
004884d7: and       ah, 0xc0
004884da: cmp       ax, 0x4000
004884de: jne       0x4883d8
004884e4: mov       ax, word ptr [ecx]
004884e7: and       eax, 0x3ff8
004884ec: and       eax, 0xffff
004884f1: sar       eax, 3
004884f4: jmp       0x4883dd
004884f9: xor       ebx, ebx
004884fb: mov       bx, word ptr [esp + 0x2c]
00488500: cmp       ebx, 0xffff
00488506: je        0x4882d1
0048850c: mov       edx, dword ptr [esp]
0048850f: mov       eax, dword ptr [esp + 0x24]
00488513: call      0x487b78
00488518: mov       eax, dword ptr [esp + 4]
0048851c: mov       edi, eax
0048851e: shl       edi, 4
00488521: add       edi, eax
00488523: mov       ebx, 1
00488528: shl       edi, 2
0048852b: mov       dword ptr [esp + 0x1c], ebx
0048852f: add       edi, eax
00488531: lea       eax, [ebp + 0x10]
00488534: shl       edi, 2
00488537: mov       dword ptr [esp + 8], eax
0048853b: jmp       0x488541
0048853d: dec       dword ptr [esp + 0x1c]
00488541: cmp       dword ptr [esp + 0x1c], 0
00488546: jl        0x488692
0048854c: mov       ecx, dword ptr [esp + 8]
00488550: xor       esi, esi
00488552: jmp       0x488558
00488554: add       ecx, 8
00488557: inc       esi
00488558: xor       eax, eax
0048855a: mov       ax, word ptr [ebp + 0xe]
0048855e: cmp       esi, eax
00488560: jge       0x48853d
00488562: xor       eax, eax
00488564: mov       ax, word ptr [ecx + 2]
00488568: mov       bx, word ptr [ecx]
0048856b: mov       dword ptr [esp + 0x18], eax
0048856f: test      bh, 0x80
00488572: je        0x48859d
00488574: and       bh, 0x7f
00488577: xor       eax, eax
00488579: mov       ax, bx
0048857c: imul      eax, eax, 0x114
00488582: mov       ebx, 0x49a0c8
00488587: add       ebx, eax
00488589: xor       eax, eax
0048858b: mov       ax, word ptr [ebx + 0xa]
0048858f: mov       bx, word ptr [ebx + 6]
00488593: and       ebx, 0xffff
00488599: sub       eax, ebx
0048859b: jmp       0x4885bb
0048859d: xor       eax, eax
0048859f: mov       ax, bx
004885a2: imul      eax, eax, 0x114
004885a8: mov       edx, dword ptr [0x4e19a0]
004885ae: mov       ax, word ptr [edx + eax + 0x9a]
004885b6: and       eax, 0xffff
004885bb: cmp       eax, dword ptr [esp + 0x18]
004885bf: jle       0x488554
004885c1: cmp       dword ptr [esp + 0x1c], 0
004885c6: je        0x488601
004885c8: mov       bx, word ptr [ecx]
004885cb: mov       eax, dword ptr [esp + 4]
004885cf: test      bh, 0x80
004885d2: je        0x4885e4
004885d4: and       bh, 0x7f
004885d7: and       ebx, 0xffff
004885dd: mov       edx, 3
004885e2: jmp       0x4885ef
004885e4: and       ebx, 0xffff
004885ea: mov       edx, 1
004885ef: and       eax, 0xffff
004885f4: call      0x446cb5
004885f9: test      al, al
004885fb: je        0x488554
00488601: mov       ax, word ptr [ecx]
00488604: test      ah, 0x80
00488607: je        0x48861e
00488609: mov       eax, dword ptr [0x4e19a0]
0048860e: mov       al, byte ptr [edi + eax + 1]
00488612: mov       edx, 0x1a
00488617: and       eax, 0xff
0048861c: jmp       0x48863b
0048861e: and       eax, 0xffff
00488623: imul      eax, eax, 0x114
00488629: mov       ebx, dword ptr [0x4e19a0]
0048862f: xor       edx, edx
00488631: mov       dl, byte ptr [ebx + eax + 1]
00488635: xor       eax, eax
00488637: mov       al, byte ptr [edi + ebx + 1]
0048863b: call      0x44f98a
00488640: and       eax, 0xff
00488645: mov       edx, eax
00488647: test      eax, eax
00488649: jle       0x488554
0048864f: mov       di, word ptr [ecx + 2]
00488653: mov       edx, dword ptr [esp + 4]
00488657: add       edi, eax
00488659: mov       ax, word ptr [ecx]
0048865c: mov       word ptr [ecx + 2], di
00488660: test      ah, 0x80
00488663: je        0x488679
00488665: and       ah, 0x7f
00488668: xor       ebx, ebx
0048866a: mov       bx, ax
0048866d: xor       eax, eax
0048866f: mov       ax, dx
00488672: mov       edx, 3
00488677: jmp       0x488688
00488679: xor       ebx, ebx
0048867b: mov       bx, ax
0048867e: xor       eax, eax
00488680: mov       ax, dx
00488683: mov       edx, 1
00488688: call      0x445a36
0048868d: jmp       0x488732
00488692: mov       edx, dword ptr [esp + 4]
00488696: mov       esi, edx
00488698: shl       esi, 4
0048869b: add       esi, edx
0048869d: mov       ecx, dword ptr [esp + 8]
004886a1: shl       esi, 2
004886a4: add       ebp, 0x12
004886a7: add       esi, edx
004886a9: mov       bx, word ptr [ecx]
004886ac: shl       esi, 2
004886af: test      bh, 0x80
004886b2: je        0x4886c4
004886b4: mov       eax, dword ptr [0x4e19a0]
004886b9: mov       al, byte ptr [esi + eax + 1]
004886bd: mov       edx, 0x1a
004886c2: jmp       0x4886eb
004886c4: xor       edx, edx
004886c6: mov       dx, bx
004886c9: mov       eax, edx
004886cb: shl       eax, 4
004886ce: add       eax, edx
004886d0: shl       eax, 2
004886d3: add       edx, eax
004886d5: mov       eax, dword ptr [0x4e19a0]
004886da: shl       edx, 2
004886dd: mov       dl, byte ptr [edx + eax + 1]
004886e1: and       edx, 0xff
004886e7: mov       al, byte ptr [esi + eax + 1]
004886eb: and       eax, 0xff
004886f0: call      0x44f98a
004886f5: and       eax, 0xff
004886fa: add       word ptr [ebp], ax
004886fe: mov       ax, word ptr [ecx]
00488701: mov       edx, dword ptr [esp + 4]
00488705: test      ah, 0x80
00488708: je        0x48871e
0048870a: and       ah, 0x7f
0048870d: xor       ebx, ebx
0048870f: mov       bx, ax
00488712: xor       eax, eax
00488714: mov       ax, dx
00488717: mov       edx, 3
0048871c: jmp       0x48872d
0048871e: xor       ebx, ebx
00488720: mov       bx, ax
00488723: xor       eax, eax
00488725: mov       ax, dx
00488728: mov       edx, 1
0048872d: call      0x445a36
00488732: mov       cx, word ptr [ecx]
00488735: mov       eax, ecx
00488737: add       esp, 0x30
0048873a: jmp       0x486a98
