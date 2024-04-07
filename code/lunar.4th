┌─┬───┤SCR # 6├────────────────────────────────────────────────────┐
│0│: COLOUR 0 ROW ! 16 COL ! 16 LEN ! 23 HGT ! 7 INK 1 BRIGHT      │
│1│SETAV ATTON ;                                                   │
│2│: VTSC COL ! 10 2 DO I ROW ! PUTBLS LOOP ;                      │
│3│: SCLE 26 SPN ! 18 VTSC 26 VTSC MIRM 21 VTSC 29 VTSC MIRM ;     │
│4│: VTCL ROW ! COL ! LEN ! HGT ! PAPER SETAV ;                    │
│5│: BARS 4 6 1 20 2 VTCL 2 2 1 20 8 VTCL 5 4  1 28 2 VTCL         │
│6│2 3 1 28 7 VTCL 5 1 16 16 14 VTCL ;                             │
│7│-->                                                             │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 7├────────────────────────────────────────────────────┐
│0│: LND 6 COL ! 17 ROW ! 44 SPN ! PUTBLS BEGIN 7 1 KB UNTIL       │
│1│20 ROW ! 43 SPN ! 7 COL ! 20 0 DO PUTXRS 100 100 BLEEP LOOP     │
│2│44 SPN ! 17 ROW ! 6 COL ! PUTXRS ;                              │
│3│: PTST SPN ! COL ! ROW ! PUTBLS ;                               │
│4│: BARST 14 23 31 PTST MIRM 14 24 31 PTST MIRM 6 28 28 PTST      │
│5│19 16 32 PTST 19 24 33 PTST ;                                   │
│6│: LETR 7 INK 0 PAPER 1 18 AT ." FUEL" 0 26 AT ." VERT" 1 26 AT  │
│7│." VEL" 11 20 AT ." HORZ VEL" ; -->                             │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 8├────────────────────────────────────────────────────┐
│0│: HRSC 32 16 DO 12 I 29 PTST 17 I 29 PTST LOOP 16 16 1 PTST ;   │
│1│: MARK 152 159 PLOT 7 0 DRAW 216 127 PLOT 7 0 DRAW 128 71 PLOT  │
│2│0 -7 DRAW ;                                                     │
│3│: PANEL 0 PAPER COLOUR SCLE BARS BARST HRSC LETR MARK ;         │
│4│: MAKE 128 SPN ! 3 HGT ! 128 LEN ! 0 SROW ! 128 SP2 ! ISPRITE   │
│5│16 0 DO I 10 + DUP SPN ! SP1 ! I 8 * SCOL ! GWBLM GWATTM DSPRITE│
│6│LOOP ;                          0 VARIABLE PH                   │
│7│256 VARIABLE SPD 0 VARIABLE DOWN 1008 VARIABLE FU -->           │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR # 9├────────────────────────────────────────────────────┐
│0│: S1 1023 AND 8 / SCOL ! 1 LEN ! PUTBLS 16 LEN ! ;              │
│1│: NBR PH @ S1 ;                 : NBL PH @ 128 + S1 ;           │
│2│: OPEN 0 PAPER 5 INK CLS 0 PH ! EXX 128 SPN ! 16 LEN ! 0 COL  ! │
│3│3 HGT ! 21 ROW ! 0 SCOL ! 0 SROW ! PWBLS PWATTS 2 HGT ! EXX     │
│4│0 PAPER 1008 FU ! 0 BORDER ;    : SH8 PH @ DUP 7 AND 0= ;       │
│5│: FUEL -1 FU +! ;               : SR SH8 IF NBR ENDIF ;         │
│6│: SL SH8 IF NBL ENDIF ;         : SH4 PH @ DUP 3 AND 0= ;       │
│7│: SF SPD +! ;                   : SS SPD @  ; -->               │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #10├────────────────────────────────────────────────────┐
│0│: POLL FU @ IF 8 1 KB IF SS -252 > MINUS SF FUEL ENDIF          │
│1│1 1 KB IF SS 256 < SF FUEL ENDIF ENDIF ;                        │
│2│: -P - PH ! POLL ;              : +P + PH ! POLL ;              │
│3│: SR1 SR WRR1V 1 -P ;           : SL1 SL WRL1V 1 +P ;           │
│4│: SR4 SH4 IF SR WRR4V 4 -P ELSE SR1 ENDIF DROP ;                │
│5│: SL4 SH4 IF SL WRL4V 4 +P ELSE SL1 ENDIF DROP ;                │
│6│: SO DOWN @ IF ELSE SS ABS 256 < IF POLL ENDIF ENDIF ;          │
│7│: SR8 SH8 IF NBR WRR8V 8 -P ELSE SR4 ENDIF DROP ; -->           │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #11├────────────────────────────────────────────────────┐
│0│: SL8 SH8 IF NBL WRL8V 8 +P ELSE SL4 ENDIF ;                    │
│1│: UR SS 200 > IF SR8 ELSE SR4 ENDIF ;                           │
│2│: LR SS 7 > IF SR1 ELSE SO ENDIF ;                              │
│3│: RT SS 100 > IF UR ELSE LR ENDIF ;                             │
│4│: UL SS -200 < IF SL8 ELSE SL4 ENDIF ;                          │
│5│: LL SS -7 < IF SL1 ELSE SO ENDIF ;                             │
│6│: LF SS -100 < IF UL ELSE LL ENDIF ;                            │
│7│: DEC SS 0< IF LF ELSE RT ENDIF ;                               │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #12├────────────────────────────────────────────────────┐
│0│: SET -1 NPX ! 3 LEN ! 6 HGT ! 107 100 DO I SP1 ! I 1+ DUP SP2 !│
│1│ SPN ! ISPRITE COPYM WCRM LOOP ;                                │
│2│40 VARIABLE XP 8 VARIABLE VEL                                   │
│3│: PREP 7 COL ! 0 DOWN ! 40 XP ! ;                               │
│4│: TICK VEL @ 255 > IF ELSE 1 VEL +! ENDIF ;                     │
│5│: THRUST FU @ IF 7 1 KB IF VEL @ -252 > IF -4 VEL +! FUEL       │
│6│ENDIF ENDIF ENDIF ;                                             │
│7│-->                                                             │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #13├────────────────────────────────────────────────────┐
│0│: MV VEL @ XP @ + DUP 5631 > IF DROP 5631 1 DOWN ! ENDIF DUP    │
│1│XP ! 32 / 8 /MOD 5 - ROW ! 7 AND 100 + SPN ! ROW @ 0< IF ADJM   │
│2│PWBLS ELSE VEL @ 0< IF 1 SROW ! ROW @ 15 > IF 4 HGT ! ELSE      │
│3│5 HGT ! ENDIF ELSE 0 SROW ! 5 HGT ! ENDIF ROW @ DUP SROW @ +    │
│4│ROW ! PWBLS ROW ! ENDIF ;                                       │
│5│                                                                │
│6│                                                                │
│7│-->                                                             │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #14├────────────────────────────────────────────────────┐
│0│: BANG DOWN @ DUP IF 19 ROW ! 43 SPN ! -5 NPX ! 7 HGT ! 3 LEN ! │
│1│40 10 DO PUTXRS I 20 + I DO J I BLEEP LOOP PUTXRS 17 ROW !      │
│2│SCRV 19 ROW ! 5 +LOOP SS ABS 8 < IF 21 ROW ! 45 SPN ! PUTBLS    │
│3│ENDIF ENDIF XP @ 5631 = IF DOWN @ 0= IF 7 COL ! LND 7 COL !     │
│4│MV 0 VEL ! ENDIF INT-OFF BEGIN 7 1 KB UNTIL                     │
│5│ ' DEC INT-ON ENDIF ;                                           │
│6│: OK 0 DOWN ! ;                                                 │
│7│-->                                                             │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #15├────────────────────────────────────────────────────┐
│0│: LAND SS ABS 8 < IF VEL @ 32 < IF PH @ 1023 AND 8 / CASE 12 OF │
│1│OK ENDOF 13 OF OK ENDOF 30 OF OK ENDOF 31 OF OK ENDOF 58 OF OK  │
│2│ENDOF 59 OF OK ENDOF 91 OF OK ENDOF 92 OF OK ENDOF ENDCASE      │
│3│ENDIF ENDIF BANG ;                                              │
│4│128 VARIABLE SX 32 VARIABLE SY 63 VARIABLE SFU                  │
│5│: XG SX +! 16 COL ! 13 ROW ! 1 HGT ! 16 LEN ! ;                 │
│6│: RSET1 7 COL ! 3 LEN ! ;       : WLEFT -1 XG WRR1V RSET1 ;     │
│7│: WRIGHT 1 XG WRL1V RSET1 ;     -->                             │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #16├────────────────────────────────────────────────────┐
│0│: XVEL SPD @ 256 + 4 / SX @ - DUP 0< IF WLEFT DROP ELSE 0 > IF  │
│1│WRIGHT ENDIF ENDIF ;                                            │
│2│: YG DUP MINUS NPX ! SY +! 27 COL ! 2 ROW ! 8 HGT ! 1 LEN !     │
│3│WCRV RSET1 ;                                                    │
│4│: WUP -1 YG ;                   : WDOWN 1 YG ;                  │
│5│: YVEL VEL @ 256 + 8 / SY @ - DUP 0< IF WUP DROP ELSE 0 > IF    │
│6│WDOWN ENDIF ENDIF ;                                             │
│7│-->                                                             │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #17├────────────────────────────────────────────────────┐
│0│: FVEL FU @ 16 / SFU @ - 0< IF 19 COL ! 2 ROW ! 8 HGT ! 1 LEN ! │
│1│-1 NPX ! -1 SFU   +! WCRV RSET1 ENDIF ;                         │
│2│0   VARIABLE LX                                                 │
│3│: MXG 18 ROW ! 16 COL ! 16 LEN ! 1 HGT ! ;                      │
│4│: MLEFT MXG WRL1V -1 LX +! ;    : MRIGHT MXG WRR1V 1 LX +! ;    │
│5│: MON PH @ 8 / LX @ - DUP 0 > IF DROP MRIGHT ELSE               │
│6│0< IF MLEFT ENDIF ENDIF RSET1 ;                                 │
│7│-->                                                             │
└─┴────────────────────────────────────────────────────────────────┘

┌─┬───┤SCR #18├────────────────────────────────────────────────────┐
│0│: OFF PANEL PREP ' DEC INT-ON BEGIN TICK THRUST MV MON XVEL     │
│1│YVEL FVEL MON LAND MON UNTIL INT-OFF ;                          │
│2│: TST 256 SPD ! 0 PH ! 1008 FU ! 40 XP ! 8 VEL ! 128 SX !       │
│3│32 SY ! 63 SFU ! 0 LX ! OPEN OFF ;                              │
│4│                                                                │
│5│                                                                │
│6│                                                                │
│7│                                                                │
└─┴────────────────────────────────────────────────────────────────┘