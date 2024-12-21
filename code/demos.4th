# Demo snippets from p129-131 of main manual

┌─┬───┤SCR # 6├────────────────────────────────────────────────────┐
│0│0 VARIABLE CL 8 VARIABLE PH : OPEN EXX 0 COL ! 12 ROW ! 2 HGT ! │
│1│0 SROW ! 0 SCOL ! 128 SPN ! 0 PAPER 6 INK 32 LEN ! CLSV 0 INK   │
│2│1 LEN ! CLSV 32 LEN ! PWBLS EXX ;                               │
│3│: NXB CL @ 1+ DUP 64 = IF DROP 0 ENDIF DUP CL ! 31 + 64 MOD SCOL│
│4│! 1 LEN ! PWBLS 32 LEN ! ;                                      │
│5│: SL WRL1V PH @ 1- DUP 0= IF NXB DROP 8 ENDIF PH ! ;            │
│6│: GO 6 INK 0 PAPER 0 BORDER 1 BRIGHT CLS 14 ROW ! 1 COL !       │
│7│6 PAPER 31 LEN ! 4 HGT ! SETAV OPEN 6 INK ' SL INT-ON ;         │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 7├────────────────────────────────────────────────────┐
│0│: DEM1 5 HGT ! 10 LEN ! 8 ROW ! 9 COL ! WRL1V ;                 │
│1│: DEM2 100 0 DO DEM1 LOOP ;                                     │
│2│: DEM3 10 HGT ! 5 LEN ! -3 NPX ! 2 ROW ! 12 COL ! WCRV ;        │
│3│: DEM4 4 HGT ! 4 LEN ! 5 ROW ! 10 COL ! INVV ;                  │
│4│: DEM5 COL ! ROW ! SPN ! PUTBLS ;                               │
│5│: DEM6 29 SPN ! 10 ROW ! 11 COL ! WRR1M PUTBLS ;                │
│6│: DEM7 1 FLASH 6 INK 2 PAPER 10 HGT ! 5 LEN ! 13 ROW ! 17 COL ! │
│7│SETAV 0 FLASH 7 INK 1 PAPER ;                                   │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 8├────────────────────────────────────────────────────┐
│0│: DEM8 28 SPN ! 2 INK 1 BRIGHT 0 PAPER SETAM PUTBLS ;           │
│1│: DEM9 100 RND . ;                                              │
│2│: DEM10 7 RND INK 34 SPN ! SETAM 10 ROW ! 10 COL ! PUTBLS ;     │
│3│: DEM11 24 SP1 ! 13 SP2 ! 7 SCOL ! 6 SROW ! GWBLM 10 ROW !      │
│4│10 COL ! ATTON PUTBLS ;                                         │
│5│: DEM12 43 SP1 ! 27 SP2 ! COPXRM 10 ROW ! 10 COL ! 27 SPN !     │
│6│ATTON PUTBLS ;                                                  │
│7│: DEM13 7 SPN ! INVM 10 ROW ! 10 COL ! PUTBLS ;                 │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 9├────────────────────────────────────────────────────┐
│0│: DEM14 45 SP1 ! 24 SP2 ! DSPM 45 SPN ! 10 COL ! 10 ROW !       │
│1│PUTBLS ;                                                        │
│2│: DEM15 255 1 DO I SPN ! TEST 1 = IF I SPACE DPTR @ U. SPACE    │ 
│3│LEN ? SPACE HGT ? SPACE CR THEN LOOP ;                          │
│4│                                                                │
│5│                                                                │
│6│                                                                │
│7│                                                                │
└─┴────────────────────────────────────────────────────────────────┘
