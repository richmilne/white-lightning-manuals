# Example code from p8,9 of Cheatsheet

┌─┬───┤SCR # 6├────────────────────────────────────────────────────┐
│0│: SETUP 0 COL ! 6 ROW ! 24 SPN ! CLS SETAM PUTBLS 2 HGT !       │
│1│32 LEN ! ;                                                      │
│2│: LEFT WRL1V ; : RIGHT WRR1V ;                                  │
│3│: KEYS 1 1 KB IF LEFT ENDIF 8 1 KB IF RIGHT ENDIF ;             │
│4│: TESTA ATTOFF SETUP BEGIN KEYS 8 2 KB UNTIL ;                  │
│5│: TESTB ATTOFF EXX SETUP EXX ' KEYS INT-ON ;                    │
│6│                                                                │
│7│                                                                │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 7├────────────────────────────────────────────────────┐
│0│: MAKE 62 SPN ! 4 HGT ! 4 LEN ! TEST 0= IF ISPRITE CLSM ENDIF ; │
│1│MAKE 1 SCOL ! 1 SROW ! 62 SP2 ! 24 SP1 ! GWBLM                  │
│2│: UP    7 1 KB IF ROW @  0 > MINUS ROW +! ENDIF ;               │
│3│: DOWN  8 1 KB IF ROW @ 20 <       ROW +! ENDIF ;               │
│4│: LEFT  1 1 KB IF COL @  0 > MINUS COL +! ENDIF ;               │
│5│: RIGHT 1 2 KB IF COL @ 28 <       COL +! ENDIF ;               │
│6│: TESTC 62 SPN ! 10 COL ! 10 ROW ! CLS BEGIN UP DOWN LEFT RIGHT │
│7│ADJM PWBLS 6 1 KB UNTIL ;                                       │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 8├────────────────────────────────────────────────────┐
│0│: SETUP 4 SPN ! 3 2 4 5 6 3 5 12 10 9 12 4 6 0 DO ROW ! COL !   │
│1│: PUTORS LOOP ; : KCHK KB DUP ROT OR SWAP ;                     │
│2│: UP 7 1 KCHK IF ROW @ 0 > MINUS ROW +! ENDIF ;                 │
│3│: DOWN 8 1 KCHK IF ROW @ 20 < ROW +! ENDIF ;                    │
│4│: LEFT 1 1 KCHK IF COL @ 0 > MINUS COL +! ENDIF ;               │
│5│: RIGHT 1 2 KCHK IF COL @ 28 < COL +! ENDIF ;                   │
│6│: TESTD CLS BEGIN COL @ ROW @ SETUP ROW ! COL ! 62 SPN !        │
│7│0 UP DOWN LEFT RIGHT IF ADJM  PWBLS ENDIF 6 1 KB UNTIL ;        │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 9├────────────────────────────────────────────────────┐
│0│: MAKE 2 HGT ! 3 LEN ! 104 100 DO I SPN ! ISPRITE CLSM LOOP ;   │
│1│: SET1 0 SROW ! 0 SCOL ! 24 SP1 ! 100 SP2 ! GWBLM ;             │
│2│: SET2 103 100 DO I SP1 ! I 1+ DUP SP2 ! SPN ! COPYM WRR1M      │
│3│WRR1M LOOP ;                                                    │
│4│: TESTE CLS 0 COL ! 4 0 DO I 100 + SPN ! I DUP + ROW ! PUTBLS   │
│5│LOOP 8 0 AT ;                                                   │
│6│: HPLOT 4 /MOD COL ! 100 + SPN ! PUTBLS ;                       │
│7│                                                                │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #10├────────────────────────────────────────────────────┐
│0│: MAKE 3 HGT ! 3 LEN ! 116 100 DO I SPN ! ISPRITE CLSM SETAM    │
│1│LOOP ;                                                          │
│2│: SET3 -2 NPX ! 104 100 DO I DUP 12 + SWAP DO I DUP 4 + DUP SP2 │
│3│! SPN ! SP1 ! GWBLM SCRM 4 +LOOP LOOP ;                         │
│4│: XYPUT 4 /MOD COL ! SWAP 4 /MOD ROW ! DUP + DUP + + 100 + SPN  │
│5│! ;                                                             │
│6│                                                                │
│7│                                                                │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #11├────────────────────────────────────────────────────┐
│0│0 VARIABLE TSPN 0 VARIABLE TCOL 0 VARIABLE TROW  0 VARIABLE XC  │
│1│0 VARIABLE YC 100 CONSTANT FSPN 0 VARIABLE FLAG                 │
│2│: PLOAD COL ! ROW ! SPN ! PUTXRS ;                              │
│3│: PSET TSPN @ TROW @ TCOL @ ;                                   │
│4│: PCAL 4 /MOD TCOL ! SWAP 4 /MOD TROW ! DUP + DUP + FSPN + +    │
│5│TSPN ! ;                                                        │
│6│: PLACE YC @ XC @ PCAL PSET PLOAD ;                             │
│7│: MOVE YC @ XC @ PCAL PSET PUTXRS PLOAD ;                       │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #12├────────────────────────────────────────────────────┐
│0│: KCHK KB DUP ROT OR SWAP ;                                     │
│1│: UP 7 1 KCHK IF YC @ 4 > MINUS YC +! ENDIF ;                   │
│2│: DOWN 8 1 KCHK IF YC @ 83 < YC +! ENDIF ;                      │
│3│: LEFT 1 1 KCHK IF XC @ 4 > MINUS XC +! ENDIF ;                 │
│4│: RIGHT 1 2 KCHK IF XC @ 115 < XC +! ENDIF ;                    │
│5│: KREAD 0 UP DOWN LEFT RIGHT ;                                  │
│6│: TESTF 10 XC ! 10 YC ! PLACE BEGIN KREAD IF MOVE ENDIF 6 1 KB  │
│7│UNTIL ;                                                         │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #13├────────────────────────────────────────────────────┐
│0│: TESTG KREAD IF MOVE ENDIF ;                                   │
│1│: TESTH 10 XC ! 10 YC ! EXX PLACE EXX ' TESTG INT-ON BEGIN 6 1  │
│2│KB UNTIL INT-OFF ;                                              │
│3│                                                                │
│4│                                                                │
│5│                                                                │
│6│                                                                │
│7│                                                                │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #14├────────────────────────────────────────────────────┐
│0│: STEP1 -1 COL +! -1 ROW +! SPN @ 117 SPN ! GETBLS ;            │
│1│: STEP2 1 SCOL ! 1 SROW ! 117 SP2 ! SP1 ! GWXRM ;               │
│2│: STEP3 116 SP2 ! TSPN SP1 ! COPYM ;                            │
│3│: STEP4 COL @ - SCOL ! ROW @ - SROW ! 117 SP2 ! 116             │
│4│SP1 ! PWNDM 116 SPN ! SCANM FLAG +! ;                           │
│5│: STEP5 SP1 ! GWXRM 117 SPN ! PUTBLS PSET COL ! ROW ! SPN !     │
│6│FLAG @ IF 100 100 BLEEP 0 FLAG ! ENDIF ;                        │
│7│: MOVE YC @ XC @ PCAL PSET STEP1 STEP2 STEP3 STEP4 STEP5 ;      │
└─┴────────────────────────────────────────────────────────────────┘
