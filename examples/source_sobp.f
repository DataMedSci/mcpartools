*$ CREATE SOURCE.FOR
*COPY SOURCE
*
*     Currently hardcoded for C-12 ions. /NBassler
*     Taken from https://github.com/DataMedSci/au-fluka-tools/blob/master/source_sampler.f
*
*===  source ===========================================================*
*
      SUBROUTINE SOURCE ( NOMORE )

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 1990-2006      by    Alfredo Ferrari & Paola Sala  *
*     All Rights Reserved.                                             *
*                                                                      *
*                                                                      *
*     New source for FLUKA9x-FLUKA200x:                                *
*                                                                      *
*     Created on 07 january 1990   by    Alfredo Ferrari & Paola Sala  *
*                                                   Infn - Milan       *
*                                                                      *
*     Last change on 03-mar-06     by    Alfredo Ferrari               *
*                                                                      *
*  This is just an example of a possible user written source routine.  *
*  note that the beam card still has some meaning - in the scoring the *
*  maximum momentum used in deciding the binning is taken from the     *
*  beam momentum.  Other beam card parameters are obsolete.            *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE '(BEAMCM)'
      INCLUDE '(FHEAVY)'
      INCLUDE '(FLKSTK)'
      INCLUDE '(IOIOCM)'
      INCLUDE '(LTCLCM)'
      INCLUDE '(PAPROP)'
      INCLUDE '(SOURCM)'
      INCLUDE '(SUMCOU)'
*
      INCLUDE '(CASLIM)'
*
c $FLUPRO/flutil/ldpm3qmd source_SAM.f -o flukadpm3_sam
      DOUBLE PRECISION ENERGY(65000), XPOS(65000), YPOS(65000)
      DOUBLE PRECISION FWHM(65000), PART(65000)
      INTEGER NWEIGHT


      SAVE ENERGY, XPOS, YPOS
      SAVE FWHM, PART
      SAVE NWEIGHT


      LOGICAL LFIRST
*
      SAVE LFIRST
      DATA LFIRST / .TRUE. /
*======================================================================*
*                                                                      *
*                 BASIC VERSION                                        *
*                                                                      *
*======================================================================*
      NOMORE = 0
*  +-------------------------------------------------------------------*
*  |  First call initializations:
      IF ( LFIRST ) THEN
*  |  *** The following 3 cards are mandatory ***
	 WRITE(LUNOUT,*) ' NB SOURCE_SAM4 INVOKED'
         TKESUM = ZERZER
         LFIRST = .FALSE.
         LUSSRC = .TRUE.

ccc only absolute path or
         OPEN(44, FILE = '../sobp.dat',
     $        STATUS = 'OLD')
         WRITE(LUNOUT,*) 'NB SOURCE ZPOS fixed to', ZBEAM


         NWEIGHT = 0
         WSUM = 0.0
         DO
*  fortran arrays start with 1
            NWEIGHT = NWEIGHT + 1
            IF (NWEIGHT .GT. 65000) THEN
               WRITE(LUNOUT,*) 'NB SOURCE ERROR: too many beamlets'
            ENDIF

            READ (44, 3, END=10 ) ENERGY(NWEIGHT),
     $           XPOS(NWEIGHT), YPOS(NWEIGHT),
     $           FWHM(NWEIGHT), PART(NWEIGHT)
 3          FORMAT(F10.4,F10.4,F10.4,F10.4,E10.4)
            WSUM = WSUM + PART(NWEIGHT)
            ENERGY(NWEIGHT) = ENERGY(NWEIGHT) * 12 ! FIX ME (c12 hardcoded)
         ENDDO
 10      CONTINUE
*        fix index
	 NWEIGHT = NWEIGHT - 1
         WRITE(LUNOUT,*) 'NB SOURCE beamlets found:', NWEIGHT
         WRITE(LUNOUT,*) 'NB SOURCE Particle sum (float) :', WSUM
         WRITE(LUNOUT,*) 'NB SOURCE TODO: particle sum is not exact.'

* check for gaussian, for future implementation
         IF ((Ldygss) .AND. (Ldxgss)) THEN
            WRITE(LUNOUT,*) 'NB SOURCE GAUSSIAN: TRUE'
         ELSE
            WRITE(LUNOUT,*) 'NB SOURCE GAUSSIAN: FALSE'
         ENDIF

      END IF

*** Sample a beamlet ****************************

      RAN = FLRNDM(111)

*     http://infohost.nmt.edu/tcc/help/lang/fortran/scaling.html
*     If you want an integer between i and j inclusive
*     use int(rand(0)*(j+1-i))+i
*     i hope hope FLRNDM [0,1[ ??
      NRAN = INT(RAN * NWEIGHT) + 1

*     If you want a real number in the interval [x,y),
*      use this expression:
*     (rand(0)*(y-x))+x

      IF ((NRAN .GT. NWEIGHT) .OR. (NRAN .LT. 1)) THEN
         WRITE(LUNOUT,*) 'NB SOURCE BOUND ERROR. NRAN, RAN:', NRAN, RAN
      END IF

      ENK = ENERGY(NRAN)
      XBEAM = XPOS(NRAN)
      YBEAM = YPOS(NRAN)
      XSPOT = FWHM(NRAN)/2.35482
      YSPOT = XSPOT

*      WRITE(LUNOUT,*) 'NB SOURCE SAM:', RAN,NRAN, ENK, XBEAM, YBEAM
*      WRITE(LUNOUT,*) 'NB SOURCE SAM2:', XSPOT,YSPOT, PART(NRAN)

*** End of beamlet sample ********************************************






*  +-------------------------------------------------------------------*
*  Push one source particle to the stack. Note that you could as well
*  push many but this way we reserve a maximum amount of space in the
*  stack for the secondaries to be generated
* Npflka is the stack counter: of course any time source is called it
* must be =0
      NPFLKA = NPFLKA + 1
* Wt is the weight of the particle
**      WTFLK  (NPFLKA) = ONEONE         set new weight
      WTFLK  (NPFLKA) = PART(NRAN)
      WEIPRI = WEIPRI + WTFLK (NPFLKA)
* Particle type (1=proton.....). Ijbeam is the type set by the BEAM
* card
*  +-------------------------------------------------------------------*
*  |  (Radioactive) isotope:
      IF ( IJBEAM .EQ. -2 .AND. LRDBEA ) THEN
         IARES  = IPROA
         IZRES  = IPROZ
         IISRES = IPROM
         CALL STISBM ( IARES, IZRES, IISRES )
         IJHION = IPROZ  * 1000 + IPROA
         IJHION = IJHION * 100 + KXHEAV
         IONID  = IJHION
         CALL DCDION ( IONID )
         CALL SETION ( IONID )
*  |
*  +-------------------------------------------------------------------*
*  |  Heavy ion:
      ELSE IF ( IJBEAM .EQ. -2 ) THEN
         IJHION = IPROZ  * 1000 + IPROA
         IJHION = IJHION * 100 + KXHEAV
         IONID  = IJHION
         CALL DCDION ( IONID )
         CALL SETION ( IONID )
         ILOFLK (NPFLKA) = IJHION
*  |  Flag this is prompt radiation
         LRADDC (NPFLKA) = .FALSE.
*  |
*  +-------------------------------------------------------------------*
*  |  Normal hadron:
      ELSE
         IONID = IJBEAM
         ILOFLK (NPFLKA) = IJBEAM
*  |  Flag this is prompt radiation
         LRADDC (NPFLKA) = .FALSE.
      END IF
*  |
*  +-------------------------------------------------------------------*
* From this point .....
* Particle generation (1 for primaries)
      LOFLK  (NPFLKA) = 1
* User dependent flag:
      LOUSE  (NPFLKA) = 0
* User dependent spare variables:
      DO 100 ISPR = 1, MKBMX1
         SPAREK (ISPR,NPFLKA) = ZERZER
 100  CONTINUE
* User dependent spare flags:
      DO 200 ISPR = 1, MKBMX2
         ISPARK (ISPR,NPFLKA) = 0
 200  CONTINUE
* Save the track number of the stack particle:
      ISPARK (MKBMX2,NPFLKA) = NPFLKA
      NPARMA = NPARMA + 1
      NUMPAR (NPFLKA) = NPARMA
      NEVENT (NPFLKA) = 0
      DFNEAR (NPFLKA) = +ZERZER
* ... to this point: don't change anything
* Particle age (s)
      AGESTK (NPFLKA) = +ZERZER
      AKNSHR (NPFLKA) = -TWOTWO
* Group number for "low" energy neutrons, set to 0 anyway
      IGROUP (NPFLKA) = 0
****************************************************************

*sample a gaussian position
*      IF (Ldygss) THEN
      CALL FLNRR2 (RGAUS1, RGAUS2)
      XFLK   (NPFLKA) = XBEAM + XSPOT * RGAUS1
      YFLK   (NPFLKA) = YBEAM + YSPOT * RGAUS2
      ZFLK   (NPFLKA) = ZBEAM

*      WRITE(LUNOUT,*) 'NB SOURCE gaussian sampled'

* Cosines (tx,ty,tz) (fix along z axis)

      TXFLK  (NPFLKA) = ZERZER
      TYFLK  (NPFLKA) = ZERZER
      TZFLK  (NPFLKA) = ONEONE
*      WRITE(LUNOUT,*) 'NB SOURCE cosines set'
*********************************************************************
* Particle momentum
*      PMOFLK (NPFLKA) = PBEAM
*      WRITE(LUNOUT,*) 'NB SOURCE mark',AM (IONID)
       CALL FLNRRN(RGAUSS)
       PMOFLK (NPFLKA) = SQRT ( ENK* ( ENK
     &     + TWOTWO * AM (IONID) ))
     &     +DPBEAM*RGAUSS/2.35482


* Kinetic energy of the particle (GeV)
* set energy
      TKEFLK (NPFLKA) = SQRT(PMOFLK(NPFLKA)**2 + AM(IONID)**2)
     &      -AM(IONID)

*      WRITE(LUNOUT,*) 'NB SOURCE set ekin'


* Polarization cosines:
      TXPOL  (NPFLKA) = -TWOTWO
      TYPOL  (NPFLKA) = +ZERZER
      TZPOL  (NPFLKA) = +ZERZER
*      WRITE(LUNOUT,*) 'NB SOURCE pol set'
*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
*  Calculate the total kinetic energy of the primaries: don't change
      IF ( ILOFLK (NPFLKA) .EQ. -2 .OR. ILOFLK (NPFLKA) .GT. 100000 )
     &   THEN
         TKESUM = TKESUM + TKEFLK (NPFLKA) * WTFLK (NPFLKA)
      ELSE IF ( ILOFLK (NPFLKA) .NE. 0 ) THEN
         TKESUM = TKESUM + ( TKEFLK (NPFLKA) + AMDISC (ILOFLK(NPFLKA)) )
     &          * WTFLK (NPFLKA)
      ELSE
         TKESUM = TKESUM + TKEFLK (NPFLKA) * WTFLK (NPFLKA)
      END IF
      RADDLY (NPFLKA) = ZERZER

*      WRITE(LUNOUT,*) 'NB SOURCE mark'

*  Here we ask for the region number of the hitting point.
*     NREG (NPFLKA) = ...
*  The following line makes the starting region search much more
*  robust if particles are starting very close to a boundary:
      CALL GEOCRS ( TXFLK (NPFLKA), TYFLK (NPFLKA), TZFLK (NPFLKA) )
      CALL GEOREG ( XFLK  (NPFLKA), YFLK  (NPFLKA), ZFLK  (NPFLKA),
     &              NRGFLK(NPFLKA), IDISC )
*      WRITE(LUNOUT,*) 'NB SOURCE mark2'
*  Do not change these cards:
      CALL GEOHSM ( NHSPNT (NPFLKA), 1, -11, MLATTC )
      NLATTC (NPFLKA) = MLATTC
      CMPATH (NPFLKA) = ZERZER
      CALL SOEVSV


*      WRITE(LUNOUT,*) 'NB SOURCE END'
      CLOSE(44)
      RETURN
*=== End of subroutine Source =========================================*
      END