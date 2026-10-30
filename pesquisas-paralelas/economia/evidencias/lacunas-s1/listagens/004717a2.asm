; RechercheGetEtat; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x4717b1
004717a2  25ff000000               and      eax, 0xff
004717a7  c1e004                   shl      eax, 4
004717aa  dd80fc805000             fld      qword ptr [eax + 0x5080fc]
004717b0  c3                       ret      
