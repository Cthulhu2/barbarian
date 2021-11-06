SCREEN 13
SCREEN _NEWIMAGE(320, 200, 32)
_SCREENMOVE _MIDDLE
_TITLE "BARBARIAN AMIGA"
_ICON _LOADIMAGE("AMIGA/menu/icone.gif")

'********************************************************************
'*                                                                  *
'*                                                                  *
'*                               BARBARIAN                          *
'*                                                                  *
'*                          palace software 1988                    *
'*                                                                  *
'*             remake of AMIGA 500 version by FL in 2012            *
'*                                                                  *
'*             other versions : http://barbarian.1987.free.fr       *
'*                                                                  *
'*                                                                  *
'*                   run this BASIC prog only with QB64             *
'*                          http://www.qb64.net                     *
'*                                                                  *
'*                                                                  *
'********************************************************************



pleinecran$ = "non"
repetermusique$ = "non"
credits$ = "non"
scoreA = 0
scoreB = 0
memoire$ = "non"
country$ = "europe"


' logo
logo:

IF country$ = "USA" THEN
    decor = _LOADIMAGE("AMIGA/menu/titreDS.png")
    _PUTIMAGE , decor
    _DISPLAY
    SLEEP 4
END IF



decor = _LOADIMAGE("AMIGA/menu/titre.png")
_PUTIMAGE , decor

IF country$ = "USA" THEN decor = _LOADIMAGE("AMIGA/menu/logoDS.png"): _PUTIMAGE (46, 10), decor

_DISPLAY


' mise en mmoire des sons

IF memoire$ = "non" THEN

    memoire$ = "oui"

    epee = _SNDOPEN("AMIGA/sound/epee.ogg", "sync")
    tombe = _SNDOPEN("AMIGA/sound/tombe.ogg", "sync")
    roule = _SNDOPEN("AMIGA/sound/roule.ogg", "sync")
    touche = _SNDOPEN("AMIGA/sound/touche.ogg", "sync")
    touche2 = _SNDOPEN("AMIGA/sound/touche2.ogg", "sync")
    touche3 = _SNDOPEN("AMIGA/sound/touche3.ogg", "sync")
    attente = _SNDOPEN("AMIGA/sound/attente.ogg", "sync")
    tete = _SNDOPEN("AMIGA/sound/tete.ogg", "sync")
    teteX = _SNDOPEN("AMIGA/sound/tete2.ogg", "sync")
    decapite = _SNDOPEN("AMIGA/sound/decapite.ogg", "sync")
    cling = _SNDOPEN("AMIGA/sound/block1.ogg", "sync")
    cling2 = _SNDOPEN("AMIGA/sound/block2.ogg", "sync")
    cling3 = _SNDOPEN("AMIGA/sound/block3.ogg", "sync")
    coupdetete = _SNDOPEN("AMIGA/sound/coupdetete.ogg", "sync")
    coupdepied = _SNDOPEN("AMIGA/sound/coupdepied.ogg", "sync")
    feu = _SNDOPEN("AMIGA/sound/feu.ogg", "sync")
    mortdecap = _SNDOPEN("AMIGA/sound/mortdecap.ogg", "sync")
    mortKO = _SNDOPEN("AMIGA/sound/mortKO.ogg", "sync")
    prepare = _SNDOPEN("AMIGA/sound/prepare.ogg", "sync")
    protege = _SNDOPEN("AMIGA/sound/protege.ogg", "sync")
    grogne1 = _SNDOPEN("AMIGA/sound/grogne1.ogg", "sync")
    grogne2 = _SNDOPEN("AMIGA/sound/grogne2.ogg", "sync")



    ' chargement sprites joueur A

    deboutA = _LOADIMAGE("AMIGA/spritesA/debout.gif")
    assis1A = _LOADIMAGE("AMIGA/spritesA/assis1.gif")
    assis2A = _LOADIMAGE("AMIGA/spritesA/assis2.gif")
    attente1A = _LOADIMAGE("AMIGA/spritesA/attente1.gif")
    attente2A = _LOADIMAGE("AMIGA/spritesA/attente2.gif")
    attente3A = _LOADIMAGE("AMIGA/spritesA/attente3.gif")
    protegeHA = _LOADIMAGE("AMIGA/spritesA/protegeH.gif")
    cou2A = _LOADIMAGE("AMIGA/spritesA/cou2.gif")
    cou3A = _LOADIMAGE("AMIGA/spritesA/cou3.gif")
    devant1A = _LOADIMAGE("AMIGA/spritesA/devant1.gif")
    devant2A = _LOADIMAGE("AMIGA/spritesA/devant2.gif")
    devant3A = _LOADIMAGE("AMIGA/spritesA/devant3.gif")
    genou1A = _LOADIMAGE("AMIGA/spritesA/genou1.gif")
    genou3A = _LOADIMAGE("AMIGA/spritesA/genou3.gif")
    marche1A = _LOADIMAGE("AMIGA/spritesA/marche1.gif")
    marche2A = _LOADIMAGE("AMIGA/spritesA/marche2.gif")
    marche3A = _LOADIMAGE("AMIGA/spritesA/marche3.gif")
    saut1A = _LOADIMAGE("AMIGA/spritesA/saut1.gif")
    saut2A = _LOADIMAGE("AMIGA/spritesA/saut2.gif")
    vainqueur1A = _LOADIMAGE("AMIGA/spritesA/vainqueur1.gif")
    vainqueur2A = _LOADIMAGE("AMIGA/spritesA/vainqueur2.gif")
    vainqueur3A = _LOADIMAGE("AMIGA/spritesA/vainqueur3.gif")
    retourne1A = _LOADIMAGE("AMIGA/spritesA/retourne1.gif")
    retourne2A = _LOADIMAGE("AMIGA/spritesA/retourne2.gif")
    retourne3A = _LOADIMAGE("AMIGA/spritesA/retourne3.gif")
    front1A = _LOADIMAGE("AMIGA/spritesA/front1.gif")
    front2A = _LOADIMAGE("AMIGA/spritesA/front2.gif")
    front3A = _LOADIMAGE("AMIGA/spritesA/front3.gif")
    toile1A = _LOADIMAGE("AMIGA/spritesA/toile1.gif")
    toile2A = _LOADIMAGE("AMIGA/spritesA/toile2.gif")
    toile3A = _LOADIMAGE("AMIGA/spritesA/toile3.gif")
    toile4A = _LOADIMAGE("AMIGA/spritesA/toile4.gif")
    tombe1A = _LOADIMAGE("AMIGA/spritesA/tombe1.gif")
    tombe2A = _LOADIMAGE("AMIGA/spritesA/tombe2.gif")
    tombe3A = _LOADIMAGE("AMIGA/spritesA/tombe3.gif")
    protegeDA = _LOADIMAGE("AMIGA/spritesA/protegeD.gif")
    protegeHA = _LOADIMAGE("AMIGA/spritesA/protegeH.gif")
    couptete1A = _LOADIMAGE("AMIGA/spritesA/tete1.gif")
    couptete2A = _LOADIMAGE("AMIGA/spritesA/tete2.gif")
    touche1A = _LOADIMAGE("AMIGA/spritesA/touche2.gif")
    touche2A = _LOADIMAGE("AMIGA/spritesA/touche1.gif")
    touche3A = _LOADIMAGE("AMIGA/spritesA/touche2.gif")

    pied1A = _LOADIMAGE("AMIGA/spritesA/pied1.gif")
    pied2A = _LOADIMAGE("AMIGA/spritesA/pied2.gif")
    decap1A = _LOADIMAGE("AMIGA/spritesA/decap1.gif")
    decap2A = _LOADIMAGE("AMIGA/spritesA/decap2.gif")
    decap3A = _LOADIMAGE("AMIGA/spritesA/decap3.gif")
    decap4A = _LOADIMAGE("AMIGA/spritesA/decap4.gif")
    mort1A = _LOADIMAGE("AMIGA/spritesA/assis1.gif")
    mort2A = _LOADIMAGE("AMIGA/spritesA/mort2.gif")
    mort3A = _LOADIMAGE("AMIGA/spritesA/mort3.gif")
    mort4A = _LOADIMAGE("AMIGA/spritesA/mort4.gif")

    roulade1A = _LOADIMAGE("AMIGA/spritesA/roulade1.gif")
    roulade2A = _LOADIMAGE("AMIGA/spritesA/roulade2.gif")
    roulade3A = _LOADIMAGE("AMIGA/spritesA/roulade3.gif")
    roulade5A = _LOADIMAGE("AMIGA/spritesA/roulade5.gif")


    drax1B = _LOADIMAGE("AMIGA/sprites/drax1.gif")
    drax2B = _LOADIMAGE("AMIGA/sprites/drax2.gif")
    mariannaB = _LOADIMAGE("AMIGA/sprites/marianna.gif")

    ' gnome

    gnome1 = _LOADIMAGE("AMIGA/sprites/gnome1.gif")
    gnome2 = _LOADIMAGE("AMIGA/sprites/gnome2.gif")
    gnome3 = _LOADIMAGE("AMIGA/sprites/gnome3.gif")
    gnome4 = _LOADIMAGE("AMIGA/sprites/gnome4.gif")


    ' divers
    tachesang = _LOADIMAGE("AMIGA/sprites/sang.gif")
    spriteombre = _LOADIMAGE("AMIGA/spritesA/teteombre.gif")

    tete1A = _LOADIMAGE("AMIGA/spritesA/tetedecap1.gif")
    tete2A = _LOADIMAGE("AMIGA/spritesA/tetedecap2.gif")
    tete3A = _LOADIMAGE("AMIGA/spritesA/tetedecap3.gif")
    tete4A = _LOADIMAGE("AMIGA/spritesA/tetedecap4.gif")
    tete5A = _LOADIMAGE("AMIGA/spritesA/tetedecap5.gif")
    tete6A = _LOADIMAGE("AMIGA/spritesA/tetedecap6.gif")

    feu1 = _LOADIMAGE("AMIGA/sprites/feu1.gif"): _CLEARCOLOR _RGB(255, 0, 255), feu1
    feu2 = _LOADIMAGE("AMIGA/sprites/feu2.gif"): _CLEARCOLOR _RGB(255, 0, 255), feu2
    feu3 = _LOADIMAGE("AMIGA/sprites/feu3.gif"): _CLEARCOLOR _RGB(255, 0, 255), feu3

    gicle1 = _LOADIMAGE("AMIGA/sprites/gicle1.gif")
    gicle2 = _LOADIMAGE("AMIGA/sprites/gicle2.gif")
    gicle3 = _LOADIMAGE("AMIGA/sprites/gicle3.gif")

    serpent1 = _LOADIMAGE("AMIGA/stage/serpent1.gif")
    serpent2 = _LOADIMAGE("AMIGA/stage/serpent2.gif")
    serpent3 = _LOADIMAGE("AMIGA/stage/serpent3.gif")

END IF


IF pleinecran$ = "non" THEN SLEEP 2
IF pleinecran$ = "oui" THEN SLEEP 4



'                           menu, choix du decor

menu:
demo$ = "non"

DO: LOOP UNTIL INKEY$ = ""

SCREEN _NEWIMAGE(320, 200, 32): CLS
decor = _LOADIMAGE("AMIGA/menu/menu.png")
_PUTIMAGE , decor

IF country$ = "USA" THEN decor = _LOADIMAGE("AMIGA/menu/logoDS.png"): _PUTIMAGE (46, 10), decor
_DISPLAY

SLEEP

IF _KEYDOWN(48) THEN decor$ = "foret": demo$ = "oui": IA = 4: partie$ = "solo": sorcier$ = "non": GOTO variables
IF _KEYDOWN(49) THEN decor$ = "foret": IA = 0: partie$ = "solo": sorcier$ = "non": GOTO variables
IF _KEYDOWN(50) THEN IA = 0: partie$ = "vs": chronometre = 60: sorcier$ = "non": GOTO selectstage
IF _KEYDOWN(51) THEN GOTO options
IF _KEYDOWN(52) THEN GOTO controls
IF _KEYDOWN(53) THEN GOTO histoire
IF _KEYDOWN(54) THEN GOTO credits
IF _KEYDOWN(55) THEN SYSTEM ELSE GOTO menu



' selection du dcor
selectstage:

decor = _LOADIMAGE("AMIGA/menu/stage.png")
_PUTIMAGE , decor

IF country$ = "USA" THEN decor = _LOADIMAGE("AMIGA/menu/logoDS.png"): _PUTIMAGE (46, 10), decor

_DISPLAY

SLEEP


IF _KEYDOWN(49) THEN decor$ = "plaine": GOTO variables
IF _KEYDOWN(50) THEN decor$ = "foret": GOTO variables
IF _KEYDOWN(51) THEN decor$ = "trone": GOTO variables
IF _KEYDOWN(52) THEN decor$ = "arene": GOTO variables

IF _KEYDOWN(54) THEN GOTO menu ELSE GOTO selectstage


' menu options
options:

decor = _LOADIMAGE("AMIGA/menu/version.png")
_PUTIMAGE , decor

IF country$ = "USA" THEN decor = _LOADIMAGE("AMIGA/menu/logoDS.png"): _PUTIMAGE (46, 10), decor

_DISPLAY
SLEEP

IF _KEYDOWN(49) THEN country$ = "europe": GOTO optionssons

IF _KEYDOWN(50) THEN
    country$ = "USA": GOTO optionssons
ELSE GOTO options
END IF

optionssons:

decor = _LOADIMAGE("AMIGA/menu/display.png")
_PUTIMAGE , decor

IF country$ = "USA" THEN decor = _LOADIMAGE("AMIGA/menu/logoDS.png"): _PUTIMAGE (46, 10), decor

_DISPLAY
SLEEP

IF _KEYDOWN(49) THEN
    IF pleinecran$ = "oui" THEN GOTO menu
    pleinecran$ = "oui"
    _FULLSCREEN
    GOTO logo
END IF

IF _KEYDOWN(50) THEN
    IF pleinecran$ = "oui" THEN
        _FULLSCREEN _OFF
        pleinecran$ = "non"
    END IF
    GOTO logo
ELSE GOTO optionssons
END IF


credits:

SCREEN _NEWIMAGE(320, 200, 32)
CLS
decor = _LOADIMAGE("AMIGA/menu/team.png"): _PUTIMAGE (0, 0), decor
_FONT 8

LOCATE 2, 21: PRINT "     BARBARIAN      "
LOCATE 3, 21: PRINT "the ultimate warrior"
LOCATE 4, 21: PRINT "                    "
LOCATE 5, 21: PRINT "  Palace Software  "
LOCATE 6, 21: PRINT "         1987      "
LOCATE 7, 21: PRINT " AMIGA 500 version "
LOCATE 8, 21: PRINT "                    "
LOCATE 9, 21: PRINT "created and designed"
LOCATE 10, 21: PRINT "  by STEVE BROWN    "
LOCATE 11, 21: PRINT "                    "
LOCATE 12, 21: PRINT "     programmer     "
LOCATE 13, 21: PRINT " Richard Leinfellner"
LOCATE 14, 21: PRINT "                    "
LOCATE 15, 21: PRINT "  assistant artist  "
LOCATE 16, 21: PRINT "                    "
LOCATE 17, 21: PRINT "     GARY CARR      "
LOCATE 18, 21: PRINT "                    "
LOCATE 19, 21: PRINT "     JO WALKER      "
LOCATE 20, 21: PRINT "                    "
LOCATE 21, 21: PRINT "       music        "
LOCATE 22, 21: PRINT "   RICHARD JOSEPH "
LOCATE 23, 21: PRINT "                    "
LOCATE 24, 1: PRINT "FL clone http://barbarian.1987.free.fr";

_DISPLAY
SLEEP

IF _KEYDOWN(13) OR _KEYDOWN(27) THEN
    GOTO menu
ELSE credits$ = "oui": GOTO credits
END IF


controls:

SCREEN _NEWIMAGE(320, 200, 32)
CLS
_FONT 8

decor = _LOADIMAGE("AMIGA/menu/titre2.png")
_PUTIMAGE , decor

IF country$ = "USA" THEN decor = _LOADIMAGE("AMIGA/menu/logoDS.png"): _PUTIMAGE (46, 10), decor

decor = _LOADIMAGE("AMIGA/menu/playerA.png")
_PUTIMAGE (0, 0), decor

decor = _LOADIMAGE("AMIGA/menu/playerB.png")
_PUTIMAGE (280, 0), decor

COLOR _RGB(255, 238, 0): LOCATE 10, 14: PRINT "CONTROLS KEYS"

COLOR _RGB(255, 255, 255)
LOCATE 10, 1: PRINT "PLAYER A"
LOCATE 12, 1: PRINT "UP............"; CHR$(24)
LOCATE 13, 1: PRINT "DOWN.........."; CHR$(25)
LOCATE 14, 1: PRINT "LEFT.........."; CHR$(27)
LOCATE 15, 1: PRINT "RIGHT........."; CHR$(26)
LOCATE 17, 1: PRINT "ATTACK...SHIFT"
COLOR _RGB(255, 0, 0): LOCATE 18, 1: PRINT "   or GAMEPAD 1"

COLOR _RGB(255, 255, 255)
LOCATE 10, 27: PRINT "      PLAYER B"
LOCATE 12, 25: PRINT "UP.............I"
LOCATE 13, 25: PRINT "DOWN...........J"
LOCATE 14, 25: PRINT "LEFT...........K"
LOCATE 15, 25: PRINT "RIGHT..........L"
LOCATE 17, 25: PRINT "ATTACK.....SPACE"

COLOR _RGB(255, 0, 0): LOCATE 18, 27: PRINT " or GAMEPAD 2"

COLOR _RGB(255, 255, 255)
LOCATE 20, 10: PRINT "ABORT GAME...........ESC"
LOCATE 22, 10: PRINT "GOTO MENU..........ENTER"

_DISPLAY
SLEEP
IF _KEYDOWN(13) OR _KEYDOWN(27) THEN GOTO controls2 ELSE GOTO controls

controls2:
CLS
COLOR _RGB(255, 238, 0): LOCATE 2, 13: PRINT "MOVING CONTROLS"

decor = _LOADIMAGE("AMIGA/menu/controls1.gif")
_PUTIMAGE (100, 40), decor

COLOR _RGB(255, 255, 255)
LOCATE 5, 19: PRINT "jump";
LOCATE 7, 8: PRINT "protect";
LOCATE 8, 11: PRINT "head";
LOCATE 7, 27: PRINT "protect";
LOCATE 8, 27: PRINT "body";
LOCATE 12, 9: PRINT "move";
LOCATE 13, 9: PRINT "back"
LOCATE 12, 29: PRINT "move";
LOCATE 13, 29: PRINT "forward"
LOCATE 18, 11: PRINT "roll";
LOCATE 19, 11: PRINT "back";
LOCATE 18, 27: PRINT "roll";
LOCATE 19, 27: PRINT "front";
LOCATE 21, 18: PRINT "crouch"

_DISPLAY
SLEEP
IF _KEYDOWN(13) OR _KEYDOWN(27) THEN GOTO controls3 ELSE GOTO controls2


controls3:

CLS
COLOR _RGB(255, 238, 0): LOCATE 2, 13: PRINT "FIGHTING CONTROLS"
LOCATE 3, 13: PRINT "(with attack key)"

decor = _LOADIMAGE("AMIGA/menu/controls2.gif")
_PUTIMAGE (100, 40), decor

COLOR _RGB(255, 255, 255)
LOCATE 5, 16: PRINT "neck chop";
LOCATE 7, 9: PRINT "web of";
LOCATE 8, 9: PRINT "death";
LOCATE 7, 27: PRINT "head";
LOCATE 8, 27: PRINT "butt";
LOCATE 12, 7: PRINT "flying";
LOCATE 13, 9: PRINT "neck";
LOCATE 14, 9: PRINT "chop";
LOCATE 12, 29: PRINT "body";
LOCATE 13, 29: PRINT "chop";
LOCATE 18, 7: PRINT "overhead";
LOCATE 19, 11: PRINT "chop";
LOCATE 19, 27: PRINT "kick ";
LOCATE 21, 17: PRINT "leg chop";


_DISPLAY
SLEEP
IF _KEYDOWN(13) OR _KEYDOWN(27) THEN GOTO menu ELSE GOTO controls3


' histoire du jeu

histoire:
SCREEN 7
CLS
LOCATE 2, 1: PRINT "The evil sorcerer Drax desires "
LOCATE 3, 1: PRINT "Princess Marianna and has sworn "
LOCATE 4, 1: PRINT "to wreak an unspeakable doom on the"
LOCATE 5, 1: PRINT "people of the Jewelled City, unless"
LOCATE 6, 1: PRINT "she is delivred to him."
LOCATE 7, 1: PRINT "However, he has agreed that if a"
LOCATE 8, 1: PRINT "champion can be found who is able to "
LOCATE 9, 1: PRINT "defeat his 7 demonic guardians, the"
LOCATE 10, 1: PRINT "princess will be allowed to go free."
LOCATE 12, 1: PRINT "All seems lost as champion after "
LOCATE 13, 1: PRINT "champion is defeated."
LOCATE 15, 1: PRINT "Then, from the forgotten wastelands of"
LOCATE 16, 1: PRINT "the North, comes an unknown barbarian,"
LOCATE 17, 1: PRINT "a mighty warrior, wielding broadsword"
LOCATE 18, 1: PRINT "with deadly skill."
LOCATE 20, 1: PRINT "Can he vanquish the forces of Darkness "
LOCATE 21, 1: PRINT "and free the princess ?"
LOCATE 23, 1: PRINT "Only you can say ...";

_DISPLAY
SLEEP
IF _KEYDOWN(13) OR _KEYDOWN(27) THEN GOTO menu ELSE GOTO histoire




'                       entree des variables
variables:

yAttA = 17: xAttA = 15
yAttB = 17: xAttB = 27
yFA = 15: yFB = 15: ' front
yTA = 16: yTB = 16: ' tete
yMA = 18: yMB = 18: ' corps
yGA = 20: yGB = 20: ' genou
xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
xFB = xB: xTB = xB: xMB = xB: xGB = xB
sens$ = "normal"
joueurA$ = "debout"
joueurB$ = "debout"
decapiteA$ = "oui"
decapiteB$ = "oui"
vieA = 12
vieB = 12
temps = 1
reftemps = 1
attenteA = 1
attenteB = 1
entree$ = "oui":
xA = 1: xB = 36 'xA = 14 : xB=23  positions du milieu
sensimageA$ = "normal"
sensimageB$ = "normal"
Aoccupe$ = "non"
Boccupe$ = "non"
spriteavanceA = 0
spritereculeA = 0
spriteavanceB = 0
spritereculeB = 0
sangA$ = "non"
sangB$ = "non"
serpentA$ = "oui"
serpentB$ = "oui"
sangdecapA = 0
sangdecapB = 0
lancerintro$ = "oui"
lancerfin$ = "oui"
chrono = 1
ySPRt = 111
xSPRt = 0
xSPRt2 = 0
gnome$ = "non"
xGNOME = 1
numerotete = 1
numerognome = 1
football$ = "non"
sortieA$ = "non"
sortieB$ = "non"
protegeDA$ = "non"
protegeDB$ = "non"
protegeHA$ = "non"
protegeHB$ = "non"
tempsfini$ = "non"
gnometire$ = "oui"
bonusA$ = "non"
bonusB$ = "non"
infocoupB = 0
infoBdegatF = 0
infoBdegatT = 0
infoBdegatG = 0
infocoupA = 0
infoAdegatF = 0
infoAdegatT = 0
infoAdegatG = 0
jeu$ = "encours"
entreesorcier$ = "non"
sonrigole$ = "non"
gnomerigole$ = "non"
finiderigoler$ = "non"
transition$ = "non"
transitionfinie$ = "non"
attaqueA$ = "non"
attaqueB$ = "non"
sontouche = 0
soncling = 0
songrogne = 0


'                   ************************************
'                   *******AFFICHAGE DU DECOR **********
'                   ************************************
decor:

SCREEN _NEWIMAGE(320, 200, 32)
CLS

IF decor$ = "plaine" THEN
    decor = _LOADIMAGE("AMIGA/stage/plaine.gif")
    _PUTIMAGE , decor
    fond = _LOADIMAGE("AMIGA/stage/plaineFOND.gif")
    arbreG = _LOADIMAGE("AMIGA/stage/plaineARBREG.gif")
    arbreD = _LOADIMAGE("AMIGA/stage/plaineARBRED.gif")
END IF

IF decor$ = "foret" THEN
    decor = _LOADIMAGE("AMIGA/stage/foret.gif")
    _PUTIMAGE , decor
    fond = _LOADIMAGE("AMIGA/stage/foretFOND.gif")
    arbreG = _LOADIMAGE("AMIGA/stage/foretARBREG.gif")
    arbreD = _LOADIMAGE("AMIGA/stage/foretARBRED.gif")
END IF

IF decor$ = "trone" THEN
    decor = _LOADIMAGE("AMIGA/stage/trone.gif")
    _PUTIMAGE , decor
    fond = _LOADIMAGE("AMIGA/stage/troneFOND.gif")
    arbreG = _LOADIMAGE("AMIGA/stage/troneARBREG.gif")
    arbreD = _LOADIMAGE("AMIGA/stage/troneARBRED.gif")
END IF

IF decor$ = "arene" THEN
    decor = _LOADIMAGE("AMIGA/stage/arene.gif")
    _PUTIMAGE , decor
    fond = _LOADIMAGE("AMIGA/stage/areneFOND.gif")
    arbreG = _LOADIMAGE("AMIGA/stage/areneARBREG.gif")
    arbreD = _LOADIMAGE("AMIGA/stage/areneARBRED.gif")
END IF

IF country$ = "USA" THEN
    IF decor$ = "foret" OR decor$ = "plaine" THEN decor = _LOADIMAGE("AMIGA/stage/logoDS2.png")
    IF decor$ = "foret" THEN _PUTIMAGE (59, 16), decor
    IF decor$ = "plaine" THEN _PUTIMAGE (59, 14), decor
    IF decor$ = "arene" OR decor$ = "trone" THEN decor = _LOADIMAGE("AMIGA/stage/logoDS3.png")
    IF decor$ = "arene" OR decor$ = "trone" THEN _PUTIMAGE (59, 16), decor
END IF

' premier affichages

COLOR _RGB(0, 0, 0)
_FONT 8
_PRINTMODE _KEEPBACKGROUND

IF partie$ = "solo" AND demo$ = "non" THEN LOCATE 25, 16: PRINT "ONE  PLAYER";
IF partie$ = "vs" THEN LOCATE 25, 16: PRINT "TWO PLAYER";
IF demo$ = "oui" THEN LOCATE 25, 14: PRINT "DEMONSTRATION";

' pr-affichage du score
IF scoreA = 0 THEN LOCATE 8, 13: PRINT "00000"
IF scoreB = 0 THEN LOCATE 8, 24: PRINT "00000"

IF scoreA > 99999 THEN scoreA = 0: IF scoreB > 99999 THEN scoreB = 0

IF scoreA > 99 AND scoreA < 999 THEN
    LOCATE 8, 13: PRINT "00": LOCATE 8, 14: PRINT scoreA
END IF
IF scoreA > 999 AND scoreA < 9999 THEN
    LOCATE 8, 13: PRINT "0": LOCATE 8, 13: PRINT scoreA
END IF
IF scoreA > 9999 AND scoreA < 99999 THEN
    LOCATE 8, 12: PRINT scoreA
END IF

IF scoreB > 99 AND scoreB < 999 THEN
    LOCATE 8, 24: PRINT "00": LOCATE 8, 25: PRINT scoreB
END IF
IF scoreB > 999 AND scoreB < 9999 THEN
    LOCATE 8, 24: PRINT "0": LOCATE 8, 24: PRINT scoreB
END IF
IF scoreB > 9999 AND scoreB < 99999 THEN
    LOCATE 8, 23: PRINT scoreB
END IF

IF partie$ = "vs" THEN LOCATE 8, 19: PRINT chronometre
IF partie$ = "solo" THEN LOCATE 8, 20: PRINT "0": LOCATE 8, 20: PRINT IA
_PRINTMODE _FILLBACKGROUND


_DISPLAY

'                   ******************************************
'                   *******   CHARGEMENT SPRITES B  **********
'                   ******************************************

IF IA = 0 THEN AI$ = "0"
IF IA = 1 THEN AI$ = "1"
IF IA = 2 THEN AI$ = "2"
IF IA = 3 THEN AI$ = "3"
IF IA = 4 THEN AI$ = "4"
IF IA = 5 THEN AI$ = "5"
IF IA = 6 THEN AI$ = "6"
IF IA = 7 THEN AI$ = "7"

'spritesB" + AI$ + "/

deboutB = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/debout.gif")
assis1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/assis1.gif")
assis2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/assis2.gif")
attente1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/attente1.gif")
attente2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/attente2.gif")
attente3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/attente3.gif")
protegeHB = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/protegeH.gif")
cou2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/cou2.gif")
cou3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/cou3.gif")
devant1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/devant1.gif")
devant2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/devant2.gif")
devant3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/devant3.gif")
genou1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/genou1.gif")
genou3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/genou3.gif")
marche1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/marche1.gif")
marche2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/marche2.gif")
marche3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/marche3.gif")
saut1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/saut1.gif")
saut2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/saut2.gif")
vainqueur1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/vainqueur1.gif")
vainqueur2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/vainqueur2.gif")
vainqueur3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/vainqueur3.gif")
retourne1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/retourne1.gif")
retourne2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/retourne2.gif")
retourne3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/retourne3.gif")
front1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/front1.gif")
front2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/front2.gif")
front3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/front3.gif")
toile1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/toile1.gif")
toile2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/toile2.gif")
toile3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/toile3.gif")
toile4B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/toile4.gif")
tombe1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tombe1.gif")
tombe2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tombe2.gif")
tombe3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tombe3.gif")
protegeDB = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/protegeD.gif")
protegeHB = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/protegeH.gif")
couptete1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tete1.gif")
couptete2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tete2.gif")
touche1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/touche2.gif")
touche2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/touche1.gif")
touche3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/touche2.gif")
pied1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/pied1.gif")
pied2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/pied2.gif")
decap1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/decap1.gif")
decap2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/decap2.gif")
decap3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/decap3.gif")
decap4B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/decap4.gif")
mort1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/assis1.gif")
mort2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/mort2.gif")
mort3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/mort3.gif")
mort4B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/mort4.gif")
roulade1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/roulade1.gif")
roulade2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/roulade2.gif")
roulade3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/roulade3.gif")
roulade5B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/roulade5.gif")
tete1B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tetedecap1.gif")
tete2B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tetedecap2.gif")
tete3B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tetedecap3.gif")
tete4B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tetedecap4.gif")
tete5B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tetedecap5.gif")
tete6B = _LOADIMAGE("AMIGA/spritesB/spritesB" + AI$ + "/tetedecap6.gif")


'                   ************************************
'                   *******   DEBUT DU JEU    **********
'                   ************************************



DO
    debut:

    IF _KEYDOWN(27) THEN arret$ = "oui" ELSE arret$ = "non"

    temps = temps + 1


    '                    ************* scenes d'animation************

    IF sorcier$ = "oui" THEN GOTO degats


    IF bonusA$ = "oui" THEN
        scoreA = scoreA + 10: chronometre = chronometre - 1
        IF chronometre <= 0 THEN
            chronometre = 0: scoreA = scoreA - 10
            IF xB >= 37 THEN sortieA$ = "oui": Aoccupe$ = "non"
        END IF
    END IF

    IF bonusB$ = "oui" THEN
        scoreB = scoreB + 10: chronometre = chronometre - 1
        IF chronometre <= 0 THEN
            chronometre = 0: scoreB = scoreB - 10
            IF xA >= 37 THEN sortieB$ = "oui": Boccupe$ = "non"
        END IF
    END IF

    IF entree$ = "oui" THEN
        IF xA >= 13 OR xB <= 22 THEN entree$ = "non"
    END IF

    IF sortieA$ = "oui" THEN
        IF tempsfini$ = "non" THEN
            IF xA < 2 AND xB >= 37 THEN
                SLEEP 1
                IF partie$ = "solo" THEN '******* round solo gagn
                    IF demo$ = "oui" THEN
                        _SNDSTOP mortKO: _SNDSTOP mortdecap: GOTO menu
                        IA = 0: scoreA = 0: scoreB = 0
                    END IF
                    IA = IA + 1
                    IF IA > 7 THEN
                        IA = 7: sorcier$ = "oui"
                        sens$ = "inverse"
                        joueurB$ = "sorcier": joueurA$ = "deboutR"
                        xB = 8: xA = 36
                        entree$ = "non": sortieA$ = "non"
                        entreesorcier$ = "oui"
                        Boccupe$ = "oui":
                        reftempsB = temps:
                        GOTO debut
                    END IF
                    IF IA = 1 THEN decor$ = "plaine"
                    IF IA = 2 THEN decor$ = "foret"
                    IF IA = 3 THEN decor$ = "plaine"
                    IF IA = 4 THEN decor$ = "trone"
                    IF IA = 5 THEN decor$ = "arene"
                    IF IA = 6 THEN decor$ = "trone"
                    IF IA = 7 THEN decor$ = "arene"

                    GOTO variables
                END IF
                IF partie$ = "vs" THEN
                    chronometre = 60
                    IF decor$ = "plaine" THEN decor$ = "foret": GOTO variables
                    IF decor$ = "foret" THEN decor$ = "plaine": GOTO variables
                    IF decor$ = "trone" THEN decor$ = "arene": GOTO variables
                    IF decor$ = "arene" THEN decor$ = "trone": GOTO variables
                END IF
            END IF
        END IF

        IF tempsfini$ = "oui" THEN
            IF sens$ = "normal" THEN
                IF xA < 2 AND xB >= 37 THEN
                    SLEEP 1
                    chronometre = 60
                    GOTO variables
                END IF
            END IF
            IF sens$ = "inverse" THEN
                IF xB < 2 AND xA >= 37 THEN
                    SLEEP 1
                    chronometre = 60
                    GOTO variables
                END IF
            END IF

        END IF

        GOTO clavier
    END IF

    IF sortieB$ = "oui" THEN
        IF tempsfini$ = "non" THEN
            IF xA >= 37 AND xB >= 37 THEN
                SLEEP 1
                IF partie$ = "solo" THEN '********** partie solo finie
                    IF demo$ = "oui" THEN _SNDSTOP mortKO: _SNDSTOP mortdecap: GOTO menu
                    IA = 0: scoreA = 0: scoreB = 0
                    decor$ = "foret": GOTO variables
                END IF
                IF partie$ = "vs" THEN
                    chronometre = 60
                    IF decor$ = "plaine" THEN decor$ = "foret": GOTO variables
                    IF decor$ = "foret" THEN decor$ = "plaine": GOTO variables
                    IF decor$ = "trone" THEN decor$ = "arene": GOTO variables
                    IF decor$ = "arene" THEN decor$ = "trone": GOTO variables
                END IF
            END IF
        END IF
        GOTO clavierB
    END IF

    IF gnome$ = "oui" THEN GOTO gnome


    '                   ************************************
    '                   *******GESTION DES DEGATS***********
    '                   ************************************

    degats:

    'degats sur joueurA

    IF sorcier$ = "oui" THEN

        IF xA < 29 THEN
            IF xAttB > xTA AND xAttB <= xTA + 2 THEN
                IF yAttB = yTA THEN
                    gnome$ = "non"
                    IF jeu$ = "perdu" THEN GOTO gestion
                    joueurA$ = "mortSORCIER": Aoccupe$ = "oui": reftemps = temps: sangA$ = "non"
                    joueurB$ = "sorcierFINI": Boccupe$ = "oui": reftempsB = temps: sangB$ = "non"
                    jeu$ = "perdu"
                    GOTO gestion
                END IF
            END IF

            IF xAttB >= xGA AND xAttB <= xGA + 2 THEN
                IF yAttB = yGA THEN
                    gnome$ = "non"
                    IF jeu$ = "perdu" THEN GOTO gestion
                    joueurA$ = "mortSORCIER": Aoccupe$ = "oui": reftemps = temps: sangA$ = "non"
                    joueurB$ = "sorcierFINI": Boccupe$ = "oui": reftempsB = temps: sangB$ = "non"
                    jeu$ = "perdu"
                    GOTO gestion
                END IF
            END IF
        END IF

        IF Aoccupe$ = "oui" THEN GOTO gestion
        sangA$ = "non"

        GOTO clavier

    END IF


    IF sens$ = "normal" THEN
        IF xA < xB THEN
            IF xAttB <= xFA AND yAttB = yFA THEN
                IF joueurA$ = "protegeH" THEN joueurA$ = "clingH": GOTO gestion
                joueurA$ = "tombe": infoAdegatF = infoAdegatF + 1: GOTO gestion
            END IF

            IF xAttB <= xTA AND yAttB = yTA THEN
                IF joueurB$ = "coupdetete" THEN joueurA$ = "tombe": GOTO gestion
                joueurA$ = "touche": scoreB = scoreB + 250: infoAdegatT = infoAdegatT + 1: GOTO gestion
            END IF

            IF xAttB <= xMA AND yAttB = yMA THEN
                IF joueurA$ = "protegeD" THEN joueurA$ = "clingD": GOTO gestion
                joueurA$ = "touche": scoreB = scoreB + 250: GOTO gestion
            END IF

            IF xAttB <= xGA AND yAttB = yGA THEN
                IF joueurB$ = "araignee" THEN joueurA$ = "tombe": GOTO gestion
                IF joueurB$ = "rouladeAV" THEN joueurA$ = "tombe": GOTO gestion
                IF joueurA$ = "protegeD" THEN joueurA$ = "clingD": GOTO gestion
                IF joueurB$ = "coupdepied" THEN joueurA$ = "tombe": infoAdegatG = infoAdegatG + 1: GOTO gestion
                joueurA$ = "touche": scoreB = scoreB + 100: infoAdegatG = infoAdegatG + 1: GOTO gestion
            END IF
        END IF
    END IF

    IF sens$ = "inverse" THEN
        IF xA > xB THEN
            IF xAttB >= xFA AND yAttB = yFA THEN
                IF joueurA$ = "protegeHR" THEN joueurA$ = "clingH": GOTO gestion
                joueurA$ = "tombeR": GOTO gestion
            END IF

            IF xAttB >= xTA AND yAttB = yTA THEN
                IF joueurB$ = "coupdeteteR" THEN joueurA$ = "tombeR": GOTO gestion
                joueurA$ = "toucheR": scoreB = scoreB + 250: GOTO gestion
            END IF
            IF xAttB >= xMA AND yAttB = yMA THEN
                IF joueurA$ = "protegeDR" THEN joueurA$ = "clingD": GOTO gestion
                joueurA$ = "toucheR": scoreB = scoreB + 250: GOTO gestion
            END IF
            IF xAttB >= xGA AND yAttB = yGA THEN
                IF joueurB$ = "araigneeR" THEN joueurA$ = "tombeR": GOTO gestion
                IF joueurB$ = "rouladeAVR" THEN joueurA$ = "tombeR": GOTO gestion
                IF joueurA$ = "protegeDR" THEN joueurA$ = "clingD": GOTO gestion
                IF joueurB$ = "coupdepiedR" THEN joueurA$ = "tombeR": GOTO gestion
                joueurA$ = "toucheR": scoreB = scoreB + 100: GOTO gestion
            END IF
        END IF
    END IF


    IF Aoccupe$ = "oui" THEN GOTO gestion
    sangA$ = "non"


    '               *********************************************************
    '               ***************** evenements clavier ********************
    '               *********************************************************


    clavier:

    '                       remise a zero  du pav virtuel

    x1 = 7: y1 = 7
    levier1$ = "neutre"


    IF demo$ = "non" THEN
        '                       ENTREE DES TOUCHES

        IF _KEYDOWN(18432) OR STICK(1) < 65 THEN y1 = y1 - 1
        IF _KEYDOWN(20480) OR STICK(1) > 190 THEN y1 = y1 + 1
        IF _KEYDOWN(19712) OR STICK(0) > 190 THEN x1 = x1 + 1
        IF _KEYDOWN(19200) OR STICK(0) < 65 THEN x1 = x1 - 1

        IF _KEYDOWN(100303) OR STRIG(1) = -1 THEN attaqueA$ = "oui" ELSE attaqueA$ = "non"


        IF _KEYDOWN(118) THEN version$ = "oui" ELSE version$ = "non"





        '                       amplitude du pave virtuel
        IF y1 > 9 THEN y1 = 9
        IF y1 < 5 THEN y1 = 5
        IF x1 > 9 THEN x1 = 9
        IF x1 < 5 THEN x1 = 5


        '                        position du "levier"  virtuel

        IF sens$ = "normal" THEN
            IF (x1 <= 6 AND y1 <= 6) THEN levier1$ = "hautG"
            IF (x1 >= 8 AND y1 <= 6) THEN levier1$ = "hautD"
            IF (x1 <= 6 AND y1 >= 8) THEN levier1$ = "basG"
            IF (x1 >= 8 AND y1 >= 8) THEN levier1$ = "basD"
            IF (x1 <= 6 AND y1 = 7) THEN levier1$ = "gauche"
            IF (x1 >= 8 AND y1 = 7) THEN levier1$ = "droite"
            IF (x1 = 7 AND y1 >= 8) THEN levier1$ = "bas"
            IF (x1 = 7 AND y1 <= 6) THEN levier1$ = "haut"
        END IF

        IF sens$ = "inverse" THEN
            IF (x1 <= 6 AND y1 <= 6) THEN levier1$ = "hautD"
            IF (x1 >= 8 AND y1 <= 6) THEN levier1$ = "hautG"
            IF (x1 <= 6 AND y1 >= 8) THEN levier1$ = "basD"
            IF (x1 >= 8 AND y1 >= 8) THEN levier1$ = "basG"
            IF (x1 <= 6 AND y1 = 7) THEN levier1$ = "gauche"
            IF (x1 >= 8 AND y1 = 7) THEN levier1$ = "droite"
            IF (x1 = 7 AND y1 >= 8) THEN levier1$ = "bas"
            IF (x1 = 7 AND y1 <= 6) THEN levier1$ = "haut"
        END IF
    END IF
    '                       **********************************
    '                       ******* animations  auto *********
    '                       **********************************

    IF entree$ = "oui" THEN
        IF lancerintro$ = "oui" THEN _SNDPLAY prepare: lancerintro$ = "non"
        levier1$ = "droite": GOTO action
    END IF

    IF sortieA$ = "oui" THEN
        IF tempsfini$ = "oui" THEN
            IF sens$ = "inverse" THEN levier1$ = "droite": GOTO action
        END IF

        sens$ = "normal": levier1$ = "gauche": GOTO action
    END IF

    IF entreesorcier$ = "oui" THEN
        IF xA <= 33 THEN entreesorcier$ = "non": GOTO gestion
        levier1$ = "gauche": GOTO action
    END IF

    '                   ************************************
    '                   **********   MODE DEMO   ***********
    '                   ************************************



    IF demo$ = "oui" THEN

        IF sens$ = "normal" THEN
            distance = xB - xA

            IF distance >= 15 THEN '  quand trop loin
                joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
            END IF


            IF distance = 12 AND joueurB$ = "debout" THEN joueurA$ = "decapite": reftemps = temps: Aoccupe$ = "oui": GOTO gestion

            IF distance = 9 THEN
                IF attenteB > 100 THEN joueurA$ = "decapite": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF joueurB$ = "rouladeAR" THEN joueurA$ = "genou": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF Boccupe$ = "oui" THEN joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
            END IF

            IF distance < 9 AND distance > 6 THEN ' distance de combat 1

                ' pour se rapprocher
                IF joueurB$ = "rouladeAR" THEN joueurA$ = "genou": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF levier2$ = "gauche" THEN joueurA$ = "araignee": reftemps = temps: Aoccupe$ = "oui": GOTO gestion

                IF joueurB$ = "front" THEN joueurA$ = "protegeH": reftemps = temps: GOTO gestion


                'pour eviter les degats repetitifs
                IF infoAdegatG > 4 THEN
                    IF joueurB$ = "assis2" OR joueurB$ = "genou" THEN joueurA$ = "genou": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                END IF
                IF infoAdegatG > 2 THEN
                    IF joueurB$ = "assis2" OR joueurB$ = "genou" THEN joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                END IF

                IF infoAdegatT > 2 THEN
                    IF joueurB$ = "cou" THEN joueurA$ = "genou": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                END IF

                IF infoAdegatF > 2 THEN
                    IF joueurB$ = "front" THEN joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                END IF

                'pour alterner les attaques

                IF infocoupA = 0 THEN joueurA$ = "devant": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 1 THEN joueurA$ = "front": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 2 THEN joueurA$ = "araignee": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 3 THEN joueurA$ = "araignee": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 4 THEN joueurA$ = "cou": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 5 THEN levier1$ = "gauche": infocoupA = 0: GOTO action


            END IF
            IF distance <= 6 THEN

                IF joueurB$ = "devant" THEN joueurA$ = "protegeD": reftemps = temps: GOTO gestion

                IF infoAdegatG > 4 THEN
                    IF joueurB$ = "assis2" OR joueurB$ = "genou" THEN joueurA$ = "genou": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                END IF
                IF infoAdegatG > 2 THEN
                    IF joueurB$ = "coupdepied" THEN joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                    IF joueurB$ = "assis2" OR joueurB$ = "genou" THEN joueurA$ = "rouladeAV": reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                END IF

                IF infocoupA = 0 THEN joueurA$ = "coupdepied": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 1 THEN joueurA$ = "coupdetete": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 2 THEN joueurA$ = "araignee": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 3 THEN joueurA$ = "genou": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 4 THEN joueurA$ = "genou": infocoupA = infocoupA + 1: reftemps = temps: Aoccupe$ = "oui": GOTO gestion
                IF infocoupA = 5 THEN levier1$ = "gauche": infocoupA = 0: GOTO action


            END IF

        END IF


        IF sens$ = "inverse" THEN GOTO menu

    END IF





    '                       redirection suivant les touches

    IF levier1$ = "hautG" GOTO action
    IF levier1$ = "hautD" GOTO action

    IF levier1$ = "basG" GOTO action
    IF levier1$ = "basD" GOTO action
    IF levier1$ = "bas" GOTO action
    IF levier1$ = "haut" GOTO action
    IF levier1$ = "gauche" GOTO action
    IF levier1$ = "droite" GOTO action


    '                       action si aucune touche n'a ete touche

    spriteavanceA = 0
    spritereculeA = 0

    protegeDA$ = "non": protegeHA$ = "non"

    attenteA = attenteA + 1
    levier1$ = "neutre":

    ' pour se relever
    assisA$ = "non"
    IF joueurA$ = "assis2" THEN joueurA$ = "releve": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
    IF joueurA$ = "assis2R" THEN joueurA$ = "releveR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion


    'attente des 5 secondes
    IF sens$ = "normal" THEN
        IF attenteA > 250 THEN joueurA$ = "attente": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
    END IF
    IF sens$ = "inverse" THEN
        IF attenteA > 250 THEN joueurA$ = "attenteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
    END IF

    ' etat debout
    IF sens$ = "normal" THEN joueurA$ = "debout"
    IF sens$ = "inverse" THEN joueurA$ = "deboutR"


    GOTO gestion


    action:

    attenteA = 1 ' remise a zero de l'attente

    '               *********************************************************
    '               ***************** ACTIONS suivant clavier ***************
    '               *********************************************************



    '                       droite,gauche, decapite, devant (normal)


    IF sens$ = "normal" THEN
        IF levier1$ = "droite" THEN
            protegeDA$ = "non"
            IF spriteavanceA = 1 THEN joueurA$ = "avance1": GOTO gestion
            IF spriteavanceA = 2 THEN joueurA$ = "avance2": GOTO gestion
            IF spriteavanceA = 3 THEN joueurA$ = "avance3": GOTO gestion
            IF spriteavanceA = 4 THEN joueurA$ = "avance4": GOTO gestion
            joueurA$ = "avance": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" AND entree$ = "non" THEN joueurA$ = "devant": Aoccupe$ = "oui": reftemps = temps
        END IF

        IF levier1$ = "gauche" THEN
            protegeHA$ = "non"
            IF spritereculeA = 1 THEN joueurA$ = "recule1": GOTO gestion
            IF spritereculeA = 2 THEN joueurA$ = "recule2": GOTO gestion
            IF spritereculeA = 3 THEN joueurA$ = "recule3": GOTO gestion
            IF spritereculeA = 4 THEN joueurA$ = "recule4": GOTO gestion
            joueurA$ = "recule": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" AND sortieA$ = "non" THEN joueurA$ = "decapite": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF

    '                       droite, gauche, decapite, devant (inverse)

    IF sens$ = "inverse" THEN
        IF levier1$ = "droite" THEN
            protegeHA$ = "non"
            IF spritereculeA = 1 THEN joueurA$ = "recule1R": GOTO gestion
            IF spritereculeA = 2 THEN joueurA$ = "recule2R": GOTO gestion
            IF spritereculeA = 3 THEN joueurA$ = "recule3R": GOTO gestion
            IF spritereculeA = 4 THEN joueurA$ = "recule4R": GOTO gestion
            joueurA$ = "reculeR": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "decapiteR": Aoccupe$ = "oui": reftemps = temps:
        END IF

        IF levier1$ = "gauche" THEN
            protegeDA$ = "non"
            IF spriteavanceA = 1 THEN joueurA$ = "avance1R": GOTO gestion
            IF spriteavanceA = 2 THEN joueurA$ = "avance2R": GOTO gestion
            IF spriteavanceA = 3 THEN joueurA$ = "avance3R": GOTO gestion
            IF spriteavanceA = 4 THEN joueurA$ = "avance4R": GOTO gestion
            joueurA$ = "avanceR": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "devantR": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF

    '                           saute, attaque cou

    IF sens$ = "normal" THEN

        IF levier1$ = "haut" THEN
            protegeDA$ = "non": protegeHA$ = "non"
            joueurA$ = "saute": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        END IF
    END IF

    IF sens$ = "inverse" THEN
        IF levier1$ = "haut" THEN
            protegeDA$ = "non": protegeHA$ = "non"
            joueurA$ = "sauteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        END IF
    END IF



    '                               assis, attaque genou
    IF sens$ = "normal" THEN
        IF levier1$ = "bas" THEN
            IF assisA$ = "oui" THEN joueurA$ = "assis2": GOTO gestion
            joueurA$ = "assis": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        END IF
    END IF
    IF sens$ = "inverse" THEN
        IF levier1$ = "bas" THEN
            IF assisA$ = "oui" THEN joueurA$ = "assis2R": GOTO gestion
            joueurA$ = "assisR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        END IF
    END IF


    '                               roulade AV, coup de pied
    IF sens$ = "normal" THEN
        IF levier1$ = "basD" THEN
            joueurA$ = "rouladeAV": Aoccupe$ = "oui": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdepied": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF
    IF sens$ = "inverse" THEN
        IF levier1$ = "basD" THEN
            joueurA$ = "rouladeAVR": Aoccupe$ = "oui": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdepiedR": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF



    '                               roulade AR, coup sur front
    IF sens$ = "normal" THEN
        IF levier1$ = "basG" THEN
            joueurA$ = "rouladeAR": Aoccupe$ = "oui": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "front": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF
    IF sens$ = "inverse" THEN
        IF levier1$ = "basG" THEN
            joueurA$ = "rouladeARR": Aoccupe$ = "oui": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "frontR": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF

    '                                   protection Haute, araignee
    IF sens$ = "normal" THEN
        IF levier1$ = "hautG" THEN
            IF protegeHA$ = "oui" THEN joueurA$ = "protegeH": GOTO gestion
            joueurA$ = "protegeH1": Aoccupe$ = "oui": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "araignee": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF

    IF sens$ = "inverse" THEN
        IF levier1$ = "hautG" THEN
            IF protegeHA$ = "oui" THEN joueurA$ = "protegeHR": GOTO gestion
            joueurA$ = "protegeHR1": Aoccupe$ = "oui": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "araigneeR": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF


    '                                   protection devant, coup de tete
    IF sens$ = "normal" THEN
        IF levier1$ = "hautD" THEN
            IF protegeDA$ = "oui" THEN joueurA$ = "protegeD": GOTO gestion
            joueurA$ = "protegeD1": Aoccupe$ = "oui": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdetete": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF
    IF sens$ = "inverse" THEN
        IF levier1$ = "hautD" THEN
            IF protegeDA$ = "oui" THEN joueurA$ = "protegeDR": GOTO gestion
            joueurA$ = "protegeDR1": Aoccupe$ = "oui": reftemps = temps
            IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdeteteR": Aoccupe$ = "oui": reftemps = temps
        END IF
    END IF


    '               ********************************************
    '               *************GESTION DES ETATS**************
    '               ********************************************
    gestion:


    IF joueurA$ = "attente" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        IF temps > reftemps + 50 THEN Aoccupe$ = "non": attenteA = 1: joueurA$ = "debout": GOTO joueur2
        IF temps > reftemps + 37 THEN spriteA$ = "attente1": GOTO joueur2
        IF temps > reftemps + 30 THEN spriteA$ = "attente2": GOTO joueur2
        IF temps > reftemps + 23 THEN spriteA$ = "attente3": GOTO joueur2
        IF temps > reftemps + 15 THEN spriteA$ = "attente2": GOTO joueur2
        IF temps > reftemps + 8 THEN GOTO joueur2
        IF temps > reftemps + 7 THEN _SNDPLAY attente: spriteA$ = "attente1": GOTO joueur2
    END IF

    IF joueurA$ = "attenteR" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        IF temps > reftemps + 50 THEN Aoccupe$ = "non": attenteA = 1: joueurA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 37 THEN spriteA$ = "attente1R": GOTO joueur2
        IF temps > reftemps + 30 THEN spriteA$ = "attente2R": GOTO joueur2
        IF temps > reftemps + 23 THEN spriteA$ = "attente3R": GOTO joueur2
        IF temps > reftemps + 15 THEN spriteA$ = "attente2R": GOTO joueur2
        IF temps > reftemps + 8 THEN GOTO joueur2
        IF temps > reftemps + 7 THEN _SNDPLAY attente: spriteA$ = "attente1R": GOTO joueur2
    END IF


    IF joueurA$ = "debout" THEN
        spriteA$ = "debout"
        decapiteA$ = "oui"
        sangA$ = "non"
        xAttA = xA:: yAttA = 14
        yFA = 15: yTA = 16: yMA = 18: yGA = 20
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        IF demo$ = "oui" THEN
            IF temps > reftemps + 20 THEN Aoccupe$ = "non"
        END IF
    END IF

    IF joueurA$ = "deboutR" THEN
        spriteA$ = "deboutR"
        decapiteA$ = "oui"
        sangA$ = "non"
        xAttA = xFA + 4: yAttA = 14
        yFA = 15: yTA = 16: yMA = 18: yGA = 20
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
    END IF

    '                               avance

    IF joueurA$ = "avance" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        IF attaqueA$ = "oui" AND demo$ = "non" AND entree$ = "non" THEN joueurA$ = "devant": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        spriteA$ = "marche1": spriteavanceA = 1: xA = xA + 1
    END IF

    IF joueurA$ = "avance1" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        IF attaqueA$ = "oui" AND demo$ = "non" AND entree$ = "non" THEN joueurA$ = "devant": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 9 THEN xA = xA + 1: spriteA$ = "marche2": spriteavanceA = 2
    END IF


    IF joueurA$ = "avance2" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        spriteA$ = "marche2"
        IF attaqueA$ = "oui" AND demo$ = "non" AND entree$ = "non" THEN joueurA$ = "devant": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 18 THEN xA = xA + 1: spriteA$ = "marche3": spriteavanceA = 3
    END IF

    IF joueurA$ = "avance3" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        spriteA$ = "marche3"
        IF attaqueA$ = "oui" AND demo$ = "non" AND entree$ = "non" THEN joueurA$ = "devant": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 27 THEN xA = xA + 1: spriteA$ = "debout": spriteavanceA = 4
    END IF

    IF joueurA$ = "avance4" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        spriteA$ = "debout"
        IF attaqueA$ = "oui" AND demo$ = "non" AND entree$ = "non" THEN joueurA$ = "devant": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 36 THEN joueurA$ = "debout": reftemps = temps: spriteavanceA = 0
    END IF

    '                                avance inverse

    IF joueurA$ = "avanceR" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        xAttA = xA + 4
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "devantR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        spriteA$ = "marche1R": spriteavanceA = 1: xA = xA - 1
    END IF

    IF joueurA$ = "avance1R" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        xAttA = xA + 4
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "devantR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 9 THEN xA = xA - 1: spriteA$ = "marche2R": spriteavanceA = 2
    END IF


    IF joueurA$ = "avance2R" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        xAttA = xA + 4
        spriteA$ = "marche2R"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "devantR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 17 THEN xA = xA - 1: spriteA$ = "marche3R": spriteavanceA = 3
    END IF

    IF joueurA$ = "avance3R" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        xAttA = xA + 4
        spriteA$ = "marche3R"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "devantR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 27 THEN xA = xA - 1: spriteA$ = "deboutR": spriteavanceA = 4
    END IF

    IF joueurA$ = "avance4R" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        xAttA = xA + 4
        spriteA$ = "deboutR"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "devantR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 36 THEN joueurA$ = "deboutR": reftemps = temps: spriteavanceA = 0
    END IF

    '                               recule
    IF joueurA$ = "recule" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        IF attaqueA$ = "oui" AND demo$ = "non" AND sortieA$ = "non" THEN joueurA$ = "decapite": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        spriteA$ = "marche3": spritereculeA = 1: xA = xA - 1
    END IF

    IF joueurA$ = "recule1" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        IF attaqueA$ = "oui" AND demo$ = "non" AND sortieA$ = "non" THEN joueurA$ = "decapite": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 9 THEN xA = xA - 1: spriteA$ = "marche2": spritereculeA = 2
    END IF

    IF joueurA$ = "recule2" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        spriteA$ = "marche2"
        IF attaqueA$ = "oui" AND demo$ = "non" AND sortieA$ = "non" THEN joueurA$ = "decapite": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 18 THEN xA = xA - 1: spriteA$ = "marche1": spritereculeA = 3
    END IF

    IF joueurA$ = "recule3" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        spriteA$ = "marche1"
        IF attaqueA$ = "oui" AND demo$ = "non" AND sortieA$ = "non" THEN joueurA$ = "decapite": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 26 THEN xA = xA - 1: spriteA$ = "debout": spritereculeA = 4
    END IF

    IF joueurA$ = "recule4" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        spriteA$ = "debout"
        IF attaqueA$ = "oui" AND demo$ = "non" AND sortieA$ = "non" THEN joueurA$ = "decapite": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 36 THEN joueurA$ = "debout": reftemps = temps: spritereculeA = 0
    END IF

    '                               recule inverse

    IF joueurA$ = "reculeR" THEN
        xAttA = xA + 4
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "decapiteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        spriteA$ = "marche3R": spritereculeA = 1: xA = xA + 1
    END IF

    IF joueurA$ = "recule1R" THEN
        xAttA = xA + 4
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "decapiteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 9 THEN xA = xA + 1: spriteA$ = "marche2R": spritereculeA = 2
    END IF

    IF joueurA$ = "recule2R" THEN
        xAttA = xA + 4
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        spriteA$ = "marche2R"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "decapiteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 18 THEN xA = xA + 1: spriteA$ = "marche1R": spritereculeA = 3
    END IF

    IF joueurA$ = "recule3R" THEN
        xAttA = xA + 4
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        spriteA$ = "marche1R"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "decapiteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 26 THEN xA = xA + 1: spriteA$ = "deboutR": spritereculeA = 4
    END IF

    IF joueurA$ = "recule4R" THEN
        xAttA = xA + 4
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        spriteA$ = "deboutR"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "decapiteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 36 THEN joueurA$ = "deboutR": reftemps = temps: spritereculeA = 0
    END IF

    IF joueurA$ = "saute" THEN
        xAttA = xA: xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        decapiteA$ = "non"
        yGA = yMA: yAttA = 14
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "cou": Aoccupe$ = "oui": reftemps = temps: GOTO joueur2

        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "debout": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "debout": xMA = xA + 4: xGA = xA + 4: GOTO joueur2
        IF temps > reftemps + 30 THEN spriteA$ = "saut1": xMA = xA + 4: xGA = xA + 1: decapiteA$ = "oui": GOTO joueur2
        IF temps > reftemps + 13 THEN spriteA$ = "saut2": xMA = xA + 1: xGA = xA + 1: GOTO joueur2
        IF temps > reftemps + 2 THEN spriteA$ = "saut1": xMA = xA + 4: xGA = xA + 1
        spriteA$ = "saut1"
    END IF

    IF joueurA$ = "sauteR" THEN
        xAttA = xA + 4: xFA = xA: xTA = xA: xMA = xA: xGA = xA
        decapiteA$ = "non"
        yGA = yMA: yAttA = 14
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "couR": Aoccupe$ = "oui": reftemps = temps: GOTO joueur2

        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "deboutR": xMA = xA: xGA = xA: GOTO joueur2
        IF temps > reftemps + 30 THEN spriteA$ = "saut1R": xMA = xA: xGA = xA + 1: decapiteA$ = "oui": GOTO joueur2
        IF temps > reftemps + 13 THEN spriteA$ = "saut2R": xMA = xA + 3: xGA = xA + 3: GOTO joueur2
        IF temps > reftemps + 2 THEN spriteA$ = "saut1R": xMA = xA: xGA = xA + 3
        spriteA$ = "saut1R"
    END IF

    IF joueurA$ = "assis" THEN
        xAttA = xA
        xFA = xA: xTA = xA: xMA = xA: xGA = xA + 4
        spriteA$ = "assis1"
        IF temps > reftemps + 10 THEN joueurA$ = "assis2": GOTO joueur2
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "genou": Aoccupe$ = "oui": reftemps = temps
    END IF

    IF joueurA$ = "assis2" THEN
        Aoccupe$ = "non"
        assisA$ = "oui"
        xAttA = xA
        xFA = xA: xTA = xA: xMA = xA + 4: xGA = xA + 4
        spriteA$ = "assis2"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "genou": Aoccupe$ = "oui": reftemps = temps
        IF demo$ = "oui" THEN
            IF temps > reftemps + 20 THEN Aoccupe$ = "non"
            GOTO joueur2
        END IF

    END IF

    IF joueurA$ = "releve" THEN
        xAttA = xA: yAttA = 14
        xFA = xA: xTA = xA: xMA = xA + 4: xGA = xA + 4
        spriteA$ = "assis1"
        IF temps > reftemps + 10 THEN joueurA$ = "debout": Aoccupe$ = "non": GOTO joueur2
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "genou": Aoccupe$ = "oui": reftemps = temps
    END IF


    IF joueurA$ = "assisR" THEN
        xAttA = xA + 4
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA
        spriteA$ = "assis1R"
        IF temps > reftemps + 10 THEN joueurA$ = "assis2R": GOTO joueur2
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "genouR": Aoccupe$ = "oui": reftemps = temps
    END IF

    IF joueurA$ = "assis2R" THEN
        Aoccupe$ = "non"
        assisA$ = "oui"
        xAttA = xA + 4
        xFA = xA + 4: xTA = xA + 4: xMA = xA: xGA = xA
        spriteA$ = "assis2R"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "genouR": Aoccupe$ = "oui": reftemps = temps
    END IF

    IF joueurA$ = "releveR" THEN
        xAttA = xA + 4: yAttA = 14
        xFA = xA + 4: xTA = xA + 4: xMA = xA: xGA = xA
        spriteA$ = "assis1R"
        IF temps > reftemps + 10 THEN joueurA$ = "deboutR": Aoccupe$ = "non": GOTO joueur2
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "genouR": Aoccupe$ = "oui": reftemps = temps
    END IF

    IF joueurA$ = "rouladeAV" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yGA = 20: yAttA = yGA: xAttA = xA: yTA = yGA
        IF attaqueA$ = "oui" AND demo$ = "non" THEN yTA = 16: joueurA$ = "coupdepied": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 38 THEN
            spriteA$ = "debout": xTA = xA + 4: xMA = xA + 4: yTA = 16:
            Aoccupe$ = "non": xA = xA + 1: joueurA$ = "finderoulade": GOTO finderoulade
        END IF
        IF temps > reftemps + 33 THEN spriteA$ = "debout": GOTO joueur2
        IF temps > reftemps + 31 THEN GOTO joueur2
        IF temps > reftemps + 30 THEN xA = xA + 1: spriteA$ = "roulade6": GOTO joueur2
        IF temps > reftemps + 29 THEN GOTO joueur2
        IF temps > reftemps + 28 THEN xA = xA + 1: spriteA$ = "roulade5": GOTO joueur2
        IF temps > reftemps + 26 THEN GOTO joueur2
        IF temps > reftemps + 25 THEN xA = xA + 1: spriteA$ = "roulade5": GOTO joueur2
        IF temps > reftemps + 23 THEN GOTO joueur2
        IF temps > reftemps + 22 THEN xA = xA + 1: spriteA$ = "roulade4": GOTO joueur2
        IF temps > reftemps + 20 THEN GOTO joueur2
        IF temps > reftemps + 19 THEN xA = xA + 1: spriteA$ = "roulade4": GOTO joueur2
        IF temps > reftemps + 17 THEN GOTO joueur2
        IF temps > reftemps + 16 THEN xA = xA + 1: xAttA = xA + 5: spriteA$ = "roulade3": GOTO joueur2
        IF temps > reftemps + 14 THEN GOTO joueur2
        IF temps > reftemps + 13 THEN xA = xA + 1: xAttA = xA + 5: spriteA$ = "roulade3": GOTO joueur2
        IF temps > reftemps + 11 THEN GOTO joueur2
        IF temps > reftemps + 10 THEN xA = xA + 1: spriteA$ = "roulade2": GOTO joueur2
        IF temps > reftemps + 8 THEN GOTO joueur2
        IF temps > reftemps + 7 THEN xA = xA + 1: spriteA$ = "roulade2": GOTO joueur2
        IF temps > reftemps + 5 THEN GOTO joueur2
        IF temps > reftemps + 4 THEN xA = xA + 1: spriteA$ = "roulade1": GOTO joueur2
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN _SNDPLAY roule: xA = xA + 1: spriteA$ = "roulade1": GOTO joueur2

    END IF

    finderoulade:

    IF joueurA$ = "finderoulade" THEN
        IF xA < xB THEN
            joueurA$ = "debout"
            spriteA$ = "debout"
            xAttA = xA: yGA = 20: yAttA = 17
            xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
            yFA = 15: yTA = 16: yMA = 18: yGA = 20
            GOTO joueur2
        END IF
        IF xA > xB - 1 THEN
            joueurA$ = "retourne": yAttA = 14: Aoccupe$ = "oui": reftemps = temps
            joueurB$ = "retourne": yAttB = 14: Boccupe$ = "oui": reftempsB = temps
            GOTO affichage
        END IF

    END IF

    IF joueurA$ = "rouladeAVR" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yGA = 20: yAttA = yGA: xAttA = xA + 4: yTA = yGA
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdepiedR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 38 THEN
            spriteA$ = "deboutR": xTA = xA: xMA = xA:
            Aoccupe$ = "non": xA = xA - 1: joueurA$ = "finderouladeR": GOTO finderouladeR
        END IF
        IF temps > reftemps + 33 THEN yTA = 16: spriteA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 31 THEN GOTO joueur2
        IF temps > reftemps + 30 THEN xA = xA - 1: spriteA$ = "roulade6R": GOTO joueur2
        IF temps > reftemps + 29 THEN GOTO joueur2
        IF temps > reftemps + 28 THEN xA = xA - 1: spriteA$ = "roulade5R": GOTO joueur2
        IF temps > reftemps + 26 THEN GOTO joueur2
        IF temps > reftemps + 25 THEN xA = xA - 1: spriteA$ = "roulade5R": GOTO joueur2
        IF temps > reftemps + 23 THEN GOTO joueur2
        IF temps > reftemps + 22 THEN xA = xA - 1: spriteA$ = "roulade4R": GOTO joueur2
        IF temps > reftemps + 20 THEN GOTO joueur2
        IF temps > reftemps + 19 THEN xA = xA - 1: spriteA$ = "roulade4R": GOTO joueur2
        IF temps > reftemps + 17 THEN GOTO joueur2
        IF temps > reftemps + 16 THEN xA = xA - 1: xAttA = xA - 1: spriteA$ = "roulade3R": GOTO joueur2
        IF temps > reftemps + 14 THEN GOTO joueur2
        IF temps > reftemps + 13 THEN xA = xA - 1: xAttA = xA - 1: spriteA$ = "roulade3R": GOTO joueur2
        IF temps > reftemps + 11 THEN GOTO joueur2
        IF temps > reftemps + 10 THEN xA = xA - 1: spriteA$ = "roulade2R": GOTO joueur2
        IF temps > reftemps + 8 THEN GOTO joueur2
        IF temps > reftemps + 7 THEN xA = xA - 1: spriteA$ = "roulade2R": GOTO joueur2
        IF temps > reftemps + 5 THEN GOTO joueur2
        IF temps > reftemps + 4 THEN xA = xA - 1: spriteA$ = "roulade1R": GOTO joueur2
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN _SNDPLAY roule: xA = xA - 1: spriteA$ = "roulade1R": GOTO joueur2
    END IF

    finderouladeR:

    IF joueurA$ = "finderouladeR" THEN
        IF xA > xB THEN
            joueurA$ = "deboutR"
            spriteA$ = "deboutR"
            xAttA = xA + 4: yGA = 20: yAttA = 17
            xFA = xA: xTA = xA: xMA = xA: xGA = xA
            yFA = 15: yTA = 16: yMA = 18: yGA = 20
            GOTO joueur2
        END IF
        IF xA < xB + 1 THEN
            joueurA$ = "retourneR": yAttA = 14: Aoccupe$ = "oui": reftemps = temps
            joueurB$ = "retourneR": yAttB = 14: Boccupe$ = "oui": reftempsB = temps
            GOTO affichage
        END IF

    END IF

    IF joueurA$ = "rouladeAR" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yGA = 20: yAttA = yGA: xAttA = xA
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "front": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 38 THEN
            spriteA$ = "debout": xTA = xA + 4: xMA = xA + 4:
            Aoccupe$ = "non": joueurA$ = "debout": GOTO colision
        END IF
        IF temps > reftemps + 33 THEN spriteA$ = "debout": GOTO joueur2
        IF temps > reftemps + 30 THEN GOTO joueur2
        IF temps > reftemps + 29 THEN xA = xA - 1: spriteA$ = "roulade1": GOTO joueur2
        IF temps > reftemps + 27 THEN GOTO joueur2
        IF temps > reftemps + 26 THEN xA = xA - 1: spriteA$ = "roulade1": GOTO joueur2
        IF temps > reftemps + 24 THEN GOTO joueur2
        IF temps > reftemps + 23 THEN xA = xA - 1: spriteA$ = "roulade2": GOTO joueur2
        IF temps > reftemps + 21 THEN GOTO joueur2
        IF temps > reftemps + 20 THEN xA = xA - 1: spriteA$ = "roulade2": GOTO joueur2
        IF temps > reftemps + 18 THEN GOTO joueur2
        IF temps > reftemps + 17 THEN xA = xA - 1: spriteA$ = "roulade3": GOTO joueur2
        IF temps > reftemps + 15 THEN GOTO joueur2
        IF temps > reftemps + 14 THEN xA = xA - 1: spriteA$ = "roulade3": GOTO joueur2
        IF temps > reftemps + 12 THEN GOTO joueur2
        IF temps > reftemps + 11 THEN xA = xA - 1: spriteA$ = "roulade4": GOTO joueur2
        IF temps > reftemps + 9 THEN GOTO joueur2
        IF temps > reftemps + 8 THEN xA = xA - 1: spriteA$ = "roulade4": GOTO joueur2
        IF temps > reftemps + 6 THEN GOTO joueur2
        IF temps > reftemps + 5 THEN xA = xA - 1: spriteA$ = "roulade5": GOTO joueur2
        IF temps > reftemps + 3 THEN GOTO joueur2
        IF temps > reftemps + 2 THEN xA = xA - 1: spriteA$ = "roulade6": GOTO joueur2
        IF temps > reftemps + 1 THEN _SNDPLAY roule: spriteA$ = "roulade6": GOTO joueur2
    END IF

    IF joueurA$ = "rouladeARR" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yGA = 20: yAttA = yGA: xAttA = xA + 4
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "frontR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 38 THEN
            spriteA$ = "deboutR": xTA = xA: xMA = xA:
            Aoccupe$ = "non": joueurA$ = "deboutR": GOTO joueur2
        END IF
        IF temps > reftemps + 33 THEN spriteA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 30 THEN GOTO joueur2
        IF temps > reftemps + 29 THEN xA = xA + 1: spriteA$ = "roulade1R": GOTO joueur2
        IF temps > reftemps + 27 THEN GOTO joueur2
        IF temps > reftemps + 26 THEN xA = xA + 1: spriteA$ = "roulade2R": GOTO joueur2
        IF temps > reftemps + 24 THEN GOTO joueur2
        IF temps > reftemps + 23 THEN xA = xA + 1: spriteA$ = "roulade2R": GOTO joueur2
        IF temps > reftemps + 21 THEN GOTO joueur2
        IF temps > reftemps + 20 THEN xA = xA + 1: spriteA$ = "roulade3R": GOTO joueur2
        IF temps > reftemps + 18 THEN GOTO joueur2
        IF temps > reftemps + 17 THEN xA = xA + 1: spriteA$ = "roulade3R": GOTO joueur2
        IF temps > reftemps + 15 THEN GOTO joueur2
        IF temps > reftemps + 14 THEN xA = xA + 1: spriteA$ = "roulade4R": GOTO joueur2
        IF temps > reftemps + 12 THEN GOTO joueur2
        IF temps > reftemps + 11 THEN xA = xA + 1: spriteA$ = "roulade4R": GOTO joueur2
        IF temps > reftemps + 9 THEN GOTO joueur2
        IF temps > reftemps + 8 THEN xA = xA + 1: spriteA$ = "roulade5R": GOTO joueur2
        IF temps > reftemps + 6 THEN GOTO joueur2
        IF temps > reftemps + 5 THEN xA = xA + 1: spriteA$ = "roulade5R": GOTO joueur2
        IF temps > reftemps + 3 THEN GOTO joueur2
        IF temps > reftemps + 2 THEN xA = xA + 1: spriteA$ = "roulade6R": GOTO joueur2
        IF temps > reftemps + 1 THEN _SNDPLAY roule: spriteA$ = "roulade6R": GOTO joueur2
    END IF

    IF joueurA$ = "protegeH1" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        yGA = 20
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "araignee": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 5 THEN protegeHA$ = "oui": spriteA$ = "protegeH": Aoccupe$ = "non": GOTO joueur2
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN _SNDPLAY protege: xA = xA - 1: spriteA$ = "marche1": GOTO joueur2
    END IF

    IF joueurA$ = "protegeH" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        xAttA = xA
        yGA = 20
        spriteA$ = "protegeH"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "araignee": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
    END IF

    IF joueurA$ = "protegeHR1" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        xAttA = xA + 4
        yGA = 20
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "araigneeR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 5 THEN protegeHA$ = "oui": joueurA$ = "protegeHR": Aoccupe$ = "non": GOTO joueur2
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN _SNDPLAY protege: xA = xA + 1: spriteA$ = "marche1R": GOTO joueur2
    END IF

    IF joueurA$ = "protegeHR" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        xAttA = xA + 4
        yGA = 20
        spriteA$ = "protegeHR"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "araigneeR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
    END IF

    IF joueurA$ = "protegeD1" THEN
        xAttA = xA
        yGA = 20
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        decapiteA$ = "non"
        spriteA$ = "protegeH"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdetete": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 5 THEN joueurA$ = "protegeD": protegeDA$ = "oui": Aoccupe$ = "non"
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN _SNDPLAY protege
    END IF

    IF joueurA$ = "protegeD" THEN
        xAttA = xA
        yGA = 20
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        decapiteA$ = "non"
        spriteA$ = "protegeD"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdetete": Aoccupe$ = "oui": reftemps = temps
    END IF

    IF joueurA$ = "protegeDR1" THEN
        xAttA = xA + 4
        yGA = 20
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        decapiteA$ = "non"
        spriteA$ = "protegeHR"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdeteteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
        IF temps > reftemps + 5 THEN spriteA$ = "protegeDR": protegeDA$ = "oui": Aoccupe$ = "non"
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN _SNDPLAY protege
    END IF

    IF joueurA$ = "protegeDR" THEN
        xAttA = xA + 4
        yGA = 20
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        decapiteA$ = "non"
        spriteA$ = "protegeDR"
        IF attaqueA$ = "oui" AND demo$ = "non" THEN joueurA$ = "coupdeteteR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
    END IF

    IF joueurA$ = "cou" THEN '****attention au temps sinon il saute
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yGA = 20
        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "debout": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "cou2": xAttA = xA: GOTO joueur2
        IF temps > reftemps + 31 THEN xAttA = xA: GOTO joueur2
        IF temps > reftemps + 30 THEN
            spriteA$ = "cou3"
            IF joueurB$ = "cou" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xTA = xA: xAttA = xA + 7: GOTO joueur2
        END IF
        IF temps > reftemps + 16 THEN GOTO joueur2
        IF temps > reftemps + 15 THEN _SNDPLAY epee: spriteA$ = "cou2": yAttA = yTA: GOTO joueur2
        IF temps > reftemps + 4 THEN GOTO joueur2
        IF temps > reftemps + 3 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            spriteA$ = "cou1": GOTO joueur2
        END IF
    END IF

    IF joueurA$ = "couR" THEN '****attention au temps sinon il saute
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yGA = 20
        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "cou2R": xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 31 THEN xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 30 THEN
            spriteA$ = "cou3R"
            IF joueurB$ = "couR" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xTA = xA + 4: xAttA = xA - 3: GOTO joueur2
        END IF
        IF temps > reftemps + 16 THEN GOTO joueur2
        IF temps > reftemps + 15 THEN _SNDPLAY epee: spriteA$ = "cou2R": yAttA = yTA: GOTO joueur2
        IF temps > reftemps + 4 THEN GOTO joueur2
        IF temps > reftemps + 3 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            spriteA$ = "cou1R": GOTO joueur2
        END IF
    END IF

    IF joueurA$ = "devant" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yGA = 20
        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "debout": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "devant2": GOTO joueur2
        IF temps > reftemps + 21 THEN spriteA$ = "devant3": xAttA = xA: GOTO joueur2
        IF temps > reftemps + 20 THEN
            spriteA$ = "devant3"
            IF joueurB$ = "devant" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xMA = xA: xAttA = xA + 6: GOTO joueur2
        END IF
        IF temps > reftemps + 11 THEN GOTO joueur2
        IF temps > reftemps + 10 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteA$ = "devant2": yAttA = yMA: GOTO joueur2
        END IF
        spriteA$ = "devant1"
    END IF

    IF joueurA$ = "devantR" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yGA = 20
        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "devant2R": GOTO joueur2
        IF temps > reftemps + 21 THEN spriteA$ = "devant3R": xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 20 THEN
            spriteA$ = "devant3R"
            IF joueurB$ = "devantR" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xMA = xA + 4: xAttA = xA - 2: GOTO joueur2
        END IF
        IF temps > reftemps + 11 THEN GOTO joueur2
        IF temps > reftemps + 10 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteA$ = "devant2R": yAttA = yMA: GOTO joueur2
        END IF
        spriteA$ = "devant1R"
    END IF

    IF joueurA$ = "genou" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA + 4
        yGA = 20
        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "assis2": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "genou2": GOTO joueur2
        IF temps > reftemps + 21 THEN spriteA$ = "genou3": xAttA = xA: GOTO joueur2
        IF temps > reftemps + 20 THEN
            spriteA$ = "genou3":
            IF joueurB$ = "genou" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xGA = xA: xAttA = xA + 7: GOTO joueur2
        END IF
        IF temps > reftemps + 11 THEN GOTO joueur2
        IF temps > reftemps + 10 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteA$ = "genou2": yAttA = yGA: GOTO joueur2
        END IF
        spriteA$ = "genou1"
    END IF

    IF joueurA$ = "genouR" THEN
        yGA = 20
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA
        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "assis2R": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "genou2R": GOTO joueur2
        IF temps > reftemps + 21 THEN spriteA$ = "genou3R": xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 20 THEN
            spriteA$ = "genou3R"
            IF joueurB$ = "genouR" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xGA = xA + 4: xAttA = xA - 3: GOTO joueur2
        END IF
        IF temps > reftemps + 11 THEN GOTO joueur2
        IF temps > reftemps + 10 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteA$ = "genou2R": yAttA = yGA: GOTO joueur2
        END IF
        spriteA$ = "genou1R"
    END IF

    IF joueurA$ = "araignee" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA: xGA = xA + 4
        yAttA = yGA: xAttA = xA: yGA = 20
        IF temps > reftemps + 24 THEN Aoccupe$ = "non": joueurA$ = "debout": GOTO joueur2
        IF temps > reftemps + 19 THEN xAttA = xA: GOTO joueur2
        IF temps > reftemps + 18 THEN
            _SNDPLAY epee
            spriteA$ = "toile4"
            IF joueurB$ = "araignee" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xAttA = xA + 5: GOTO joueur2
        END IF
        IF temps > reftemps + 12 THEN spriteA$ = "toile3": xAttA = xA: GOTO joueur2
        IF temps > reftemps + 7 THEN GOTO joueur2
        IF temps > reftemps + 6 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteA$ = "toile2": xAttA = xA: GOTO joueur2
        END IF
        spriteA$ = "toile1"
    END IF

    IF joueurA$ = "araigneeR" THEN
        xFA = xA: xTA = xA: xMA = xA + 4: xGA = xA
        yAttA = yGA: xAttA = xA + 4: yGA = 20
        IF temps > reftemps + 24 THEN Aoccupe$ = "non": joueurA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 19 THEN xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 18 THEN
            _SNDPLAY epee
            spriteA$ = "toile4R"
            IF joueurB$ = "araigneeR" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xAttA = xA - 1: GOTO joueur2
        END IF
        IF temps > reftemps + 12 THEN spriteA$ = "toile3R": xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 7 THEN GOTO joueur2
        IF temps > reftemps + 6 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteA$ = "toile2R": xAttA = xA + 4: GOTO joueur2
        END IF
        spriteA$ = "toile1R"
    END IF

    IF joueurA$ = "coupdepied" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        spriteA$ = "pied1": yAttA = yGA: yGA = 20
        IF temps > reftemps + 15 THEN spriteA$ = "pied2": xAttA = xA + 5
        IF temps > reftemps + 16 THEN spriteA$ = "pied2": xAttA = xA
        IF temps > reftemps + 30 THEN spriteA$ = "pied1"
        IF temps > reftemps + 45 THEN spriteA$ = "debout"
        IF temps > reftemps + 50 THEN Aoccupe$ = "non": joueurA$ = "debout"
    END IF

    IF joueurA$ = "coupdepiedR" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        spriteA$ = "pied1R": yAttA = yGA: yGA = 20
        IF temps > reftemps + 15 THEN spriteA$ = "pied2R": xAttA = xA - 1
        IF temps > reftemps + 16 THEN spriteA$ = "pied2R": xAttA = xA + 4
        IF temps > reftemps + 30 THEN spriteA$ = "pied1R"
        IF temps > reftemps + 45 THEN spriteA$ = "deboutR"
        IF temps > reftemps + 50 THEN Aoccupe$ = "non": joueurA$ = "deboutR"
    END IF

    IF joueurA$ = "coupdetete" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yGA = 20
        IF temps > reftemps + 37 THEN Aoccupe$ = "non": spriteA$ = "debout": joueurA$ = "debout": GOTO joueur2
        IF temps > reftemps + 29 THEN GOTO joueur2
        IF temps > reftemps + 28 THEN xA = xA - 1: spriteA$ = "tete1": GOTO joueur2
        IF temps > reftemps + 20 THEN xAttA = xA: GOTO joueur2
        IF temps > reftemps + 19 THEN spriteA$ = "tete2": xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 18 THEN xA = xA + 1: spriteA$ = "tete2": xAttA = xA: GOTO joueur2
        IF temps > reftemps + 9 THEN spriteA$ = "tete1": yAttA = yTA: GOTO joueur2
        spriteA$ = "tete1"
    END IF

    IF joueurA$ = "coupdeteteR" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yGA = 20: yTA = 16
        IF temps > reftemps + 37 THEN Aoccupe$ = "non": spriteA$ = "deboutR": joueurA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 29 THEN GOTO joueur2
        IF temps > reftemps + 28 THEN xA = xA + 1: spriteA$ = "tete1R": GOTO joueur2
        IF temps > reftemps + 20 THEN xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 19 THEN spriteA$ = "tete2R": xAttA = xA: GOTO joueur2
        IF temps > reftemps + 18 THEN xA = xA - 1: spriteA$ = "tete2R": xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 9 THEN spriteA$ = "tete1R": yAttA = yTA: GOTO joueur2
        spriteA$ = "tete1R"
    END IF

    IF joueurA$ = "decapite" THEN
        decapiteA$ = "non"
        xFA = xA + 3: xTA = xA + 2: xMA = xA + 2: xGA = xA + 4
        IF temps > reftemps + 58 THEN Aoccupe$ = "non": spriteA$ = "debout": joueurA$ = "debout": GOTO joueur2
        IF temps > reftemps + 51 THEN spriteA$ = "cou2": xAttA = xA: GOTO joueur2
        IF temps > reftemps + 50 THEN spriteA$ = "cou3": xTA = xA: xAttA = xA + 6: GOTO joueur2
        IF temps > reftemps + 39 THEN spriteA$ = "cou3": yAttA = yTA: GOTO joueur2
        IF temps > reftemps + 33 THEN spriteA$ = "cou2": yAttA = yTA: GOTO joueur2
        IF temps > reftemps + 29 THEN spriteA$ = "cou1": yAttA = yTA: GOTO joueur2
        IF temps > reftemps + 25 THEN GOTO joueur2
        IF temps > reftemps + 24 THEN xA = xA + 1: GOTO joueur2
        IF temps > reftemps + 20 THEN spriteA$ = "retourne3": GOTO joueur2
        IF temps > reftemps + 19 THEN xA = xA + 1: GOTO joueur2
        IF temps > reftemps + 15 THEN spriteA$ = "retourne3": GOTO joueur2
        IF temps > reftemps + 14 THEN _SNDPLAY decapite: xA = xA + 1: GOTO joueur2
        IF temps > reftemps + 10 THEN spriteA$ = "retourne2": GOTO joueur2
        IF temps > reftemps + 9 THEN xA = xA + 1: GOTO joueur2
        IF temps > reftemps + 5 THEN spriteA$ = "retourne2": GOTO joueur2
        IF temps > reftemps + 4 THEN xA = xA + 1: GOTO joueur2
        IF temps > reftemps + 2 THEN spriteA$ = "retourne1": GOTO joueur2
        IF temps > reftemps + 1 THEN xA = xA + 1: spriteA$ = "retourne1": GOTO joueur2
    END IF

    IF joueurA$ = "decapiteR" THEN
        decapiteA$ = "non"
        xFA = xA + 1: xTA = xA + 2: xMA = xA + 2: xGA = xA
        IF temps > reftemps + 58 THEN Aoccupe$ = "non": spriteA$ = "deboutR": joueurA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 51 THEN spriteA$ = "cou2R": xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 50 THEN spriteA$ = "cou3R": xTA = xA + 4: xAttA = xA - 2: GOTO joueur2
        IF temps > reftemps + 39 THEN spriteA$ = "cou3R": yAttA = yTA: GOTO joueur2
        IF temps > reftemps + 33 THEN spriteA$ = "cou2R": yAttA = yTA: GOTO joueur2
        IF temps > reftemps + 29 THEN spriteA$ = "cou1R": yAttA = yTA: GOTO joueur2
        IF temps > reftemps + 25 GOTO joueur2
        IF temps > reftemps + 24 THEN xA = xA - 1: GOTO joueur2
        IF temps > reftemps + 20 THEN spriteA$ = "retourne3R": GOTO joueur2
        IF temps > reftemps + 19 THEN xA = xA - 1: GOTO joueur2
        IF temps > reftemps + 15 THEN spriteA$ = "retourne3R": GOTO joueur2
        IF temps > reftemps + 14 THEN _SNDPLAY decapite: xA = xA - 1: GOTO joueur2
        IF temps > reftemps + 10 THEN spriteA$ = "retourne2R": GOTO joueur2
        IF temps > reftemps + 9 THEN xA = xA - 1: GOTO joueur2
        IF temps > reftemps + 5 THEN spriteA$ = "retourne2R": GOTO joueur2
        IF temps > reftemps + 4 THEN xA = xA - 1: GOTO joueur2
        IF temps > reftemps + 2 THEN spriteA$ = "retourne1R": GOTO joueur2
        IF temps > reftemps + 1 THEN xA = xA - 1: spriteA$ = "retourne1R": GOTO joueur2
    END IF

    IF joueurA$ = "front" THEN
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yGA = 20
        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "debout": GOTO joueur2
        IF temps > reftemps + 30 THEN spriteA$ = "front2": GOTO joueur2
        IF temps > reftemps + 24 THEN spriteA$ = "front3": xAttA = xA: GOTO joueur2
        IF temps > reftemps + 23 THEN
            spriteA$ = "front3"
            IF joueurB$ = "front" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xFA = xA: xAttA = xA + 7: GOTO joueur2
        END IF
        IF temps > reftemps + 6 THEN GOTO joueur2
        IF temps > reftemps + 5 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteA$ = "front2": yAttA = yFA: GOTO joueur2
        END IF
        IF temps > reftemps + 3 THEN spriteA$ = "front1": GOTO joueur2
    END IF

    IF joueurA$ = "frontR" THEN
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yGA = 20
        IF temps > reftemps + 45 THEN Aoccupe$ = "non": joueurA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 30 THEN spriteA$ = "front2R": GOTO joueur2
        IF temps > reftemps + 24 THEN spriteA$ = "front3R": xAttA = xA + 4: GOTO joueur2
        IF temps > reftemps + 23 THEN
            spriteA$ = "front3R"
            IF joueurB$ = "frontR" THEN
                IF distance < 12 THEN
                    soncling = soncling + 1
                    IF soncling > 3 THEN soncling = 1
                    IF soncling = 1 THEN _SNDPLAY cling
                    IF soncling = 2 THEN _SNDPLAY cling2
                    IF soncling = 3 THEN _SNDPLAY cling3
                END IF
                GOTO joueur2
            END IF
            xFA = xA + 4: xAttA = xA - 3: GOTO joueur2
        END IF
        IF temps > reftemps + 6 THEN GOTO joueur2
        IF temps > reftemps + 5 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2

            _SNDPLAY epee: spriteA$ = "front2R": yAttA = yFA: GOTO joueur2
        END IF
        IF temps > reftemps + 3 THEN spriteA$ = "front1R": GOTO joueur2
    END IF

    IF joueurA$ = "retourne" THEN
        xAttA = xA: xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yAttA = 14:
        spriteA$ = "retourne1"
        IF temps > reftemps + 5 THEN spriteA$ = "retourne2"
        IF temps > reftemps + 10 THEN spriteA$ = "retourne3"
        IF temps > reftemps + 15 THEN joueurA$ = "deboutR": Aoccupe$ = "non": sens$ = "inverse"
    END IF

    IF joueurA$ = "retourneR" THEN
        xAttA = xA + 4: xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yAttA = 14:
        spriteA$ = "retourne1"
        IF temps > reftemps + 5 THEN spriteA$ = "retourne2"
        IF temps > reftemps + 10 THEN spriteA$ = "retourne3"
        IF temps > reftemps + 15 THEN joueurA$ = "debout": Aoccupe$ = "non": sens$ = "normal"
    END IF

    IF joueurA$ = "vainqueur" THEN
        spriteA$ = "vainqueur1"
        decapiteA$ = "oui"
        sangA$ = "non"
        xAttA = xA: yGA = 20: yAttA = 14
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        IF temps > reftemps + 18 THEN spriteA$ = "vainqueur2"
        IF temps > reftemps + 35 THEN spriteA$ = "vainqueur3"
        IF temps > reftemps + 85 THEN spriteA$ = "vainqueur2"
        IF temps > reftemps + 100 THEN spriteA$ = "vainqueur1"
    END IF

    IF joueurA$ = "vainqueurR" THEN
        spriteA$ = "vainqueur1R"
        decapiteA$ = "oui"
        sangA$ = "non"
        xAttA = xFA + 4: yGA = 20: yAttA = 14
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        IF temps > reftemps + 18 THEN spriteA$ = "vainqueur2R"
        IF temps > reftemps + 35 THEN spriteA$ = "vainqueur3R"
        IF temps > reftemps + 85 THEN spriteA$ = "vainqueur2R"
        IF temps > reftemps + 100 THEN spriteA$ = "vainqueur1R"
    END IF

    IF joueurA$ = "vainqueurKO" THEN
        decapiteA$ = "oui"
        sangA$ = "non"
        xAttA = xA: yGA = 20:
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4

        IF temps > reftemps + 230 THEN
            gnome$ = "oui": reftemps = temps
            xGNOME = 1
            xSPRt = 270
            GOTO affichage
        END IF

        IF temps > reftemps + 205 THEN spriteA$ = "vainqueur1": GOTO joueur2
        IF temps > reftemps + 195 THEN spriteA$ = "vainqueur2": GOTO joueur2
        IF temps > reftemps + 140 THEN spriteA$ = "vainqueur3": GOTO joueur2
        IF temps > reftemps + 123 THEN spriteA$ = "vainqueur2": GOTO joueur2
        IF temps > reftemps + 105 THEN spriteA$ = "vainqueur1": GOTO joueur2
        IF temps > reftemps + 100 THEN spriteA$ = "debout": GOTO joueur2
        IF temps > reftemps + 75 THEN spriteA$ = "pied1": spriteB$ = "mort4": GOTO joueur2
        IF temps > reftemps + 71 THEN GOTO joueur2
        IF temps > reftemps + 70 THEN
            spriteA$ = "pied2": spriteB$ = "mort3": xB = xB + 2: GOTO joueur2
        END IF
        IF temps > reftemps + 55 THEN spriteA$ = "pied1": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "debout": GOTO joueur2
        IF temps > reftemps + 36 THEN GOTO joueur2
        IF temps > reftemps + 35 THEN
            distance = xB - xA
            IF distance < 5 THEN spriteA$ = "marche3": xA = xA - 1
            IF distance > 5 THEN spriteA$ = "marche3": xA = xA + 1
            GOTO colision
        END IF
        IF temps > reftemps + 30 THEN spriteA$ = "debout": GOTO joueur2
        IF temps > reftemps + 23 THEN spriteA$ = "retourne3": GOTO joueur2
        IF temps > reftemps + 15 THEN spriteA$ = "retourne2": GOTO joueur2
        IF temps > reftemps + 8 THEN spriteA$ = "retourne1"
    END IF

    IF joueurA$ = "vainqueurKOR" THEN
        decapiteA$ = "oui"
        sangA$ = "non"
        xAttA = xFA + 4: yGA = 20
        xFA = xA: xTA = xA: xMA = xA: xGA = xA

        IF temps > reftemps + 230 THEN
            gnome$ = "oui": reftemps = temps
            xGNOME = 1
            xSPRt = 270
            GOTO affichage
        END IF

        IF temps > reftemps + 205 THEN spriteA$ = "vainqueur1R": GOTO joueur2
        IF temps > reftemps + 190 THEN spriteA$ = "vainqueur2R": GOTO joueur2
        IF temps > reftemps + 140 THEN spriteA$ = "vainqueur3R": GOTO joueur2
        IF temps > reftemps + 123 THEN spriteA$ = "vainqueur2R": GOTO joueur2
        IF temps > reftemps + 105 THEN spriteA$ = "vainqueur1R": GOTO joueur2
        IF temps > reftemps + 100 THEN spriteA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 75 THEN spriteA$ = "pied1R": spriteB$ = "mort4R": GOTO joueur2
        IF temps > reftemps + 71 THEN GOTO joueur2
        IF temps > reftemps + 70 THEN
            spriteA$ = "pied2R": spriteB$ = "mort3R": xB = xB - 2: GOTO joueur2
        END IF
        IF temps > reftemps + 55 THEN spriteA$ = "pied1R": GOTO joueur2
        IF temps > reftemps + 40 THEN spriteA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 36 THEN GOTO joueur2
        IF temps > reftemps + 35 THEN
            distance = xA - xB
            IF distance < 5 THEN spriteA$ = "marche3R": xA = xA + 1
            IF distance > 5 THEN spriteA$ = "marche3R": xA = xA - 1
            GOTO colision
        END IF
        IF temps > reftemps + 30 THEN spriteA$ = "deboutR": GOTO joueur2
        IF temps > reftemps + 23 THEN spriteA$ = "retourne3R": GOTO joueur2
        IF temps > reftemps + 15 THEN spriteA$ = "retourne2R": GOTO joueur2
        IF temps > reftemps + 8 THEN spriteA$ = "retourne1R"
    END IF


    '                               ******degats******
    IF joueurA$ = "touche" THEN
        attenteA = 0
        xAttA = xA
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yFA = 15: yTA = 16: yMA = 18: yGA = 20
        IF joueurB$ = "coupdepied" THEN joueurA$ = "tombe": GOTO gestion

        sangA$ = "oui"
        serpentA$ = "oui"

        IF joueurB$ = "decapite" AND decapiteA$ = "oui" THEN
            joueurA$ = "mortdecap": Aoccupe$ = "oui": reftemps = temps
            xSPRt = xA + 3: scoreB = scoreB + 250
            sangA$ = "non": GOTO mort
        END IF

        vieA = vieA - 1:
        IF vieA <= 0 THEN
            joueurA$ = "mort": Aoccupe$ = "oui": reftemps = temps: sangA$ = "oui": GOTO mort
        END IF

        sontouche = sontouche + 1
        IF sontouche > 3 THEN sontouche = 1
        IF sontouche = 1 THEN _SNDPLAY touche
        IF sontouche = 2 THEN _SNDPLAY touche2
        IF sontouche = 3 THEN _SNDPLAY touche3


        joueurA$ = "touche1": Aoccupe$ = "oui": reftemps = temps: decapiteA$ = "oui"
        GOTO joueur2
    END IF

    IF joueurA$ = "touche1" THEN
        attenteA = 0
        xAttA = xA
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        IF temps > reftemps + 20 THEN
            spriteA$ = "debout": Aoccupe$ = "non"
            joueurA$ = "debout": GOTO joueur2
        END IF
        IF temps > reftemps + 15 THEN spriteA$ = "touche4": GOTO joueur2 ' pour serpent
        IF temps > reftemps + 11 THEN GOTO joueur2
        IF temps > reftemps + 10 THEN xA = xA - 1: sangA$ = "non": spriteA$ = "touche3": GOTO joueur2
        IF temps > reftemps + 6 THEN GOTO joueur2
        IF temps > reftemps + 5 THEN xA = xA - 2: spriteA$ = "touche2": GOTO joueur2
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN xA = xA - 1: spriteA$ = "touche1": GOTO joueur2
        spriteA$ = "touche1"
    END IF

    IF joueurA$ = "toucheR" THEN
        attenteA = 0
        xAttA = xA + 4
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yFA = 15: yTA = 16: yMA = 18: yGA = 20
        IF joueurB$ = "coupdepiedR" THEN joueurA$ = "tombeR": GOTO gestion

        sangA$ = "oui"
        serpentA$ = "oui"

        IF joueurB$ = "decapiteR" AND decapiteA$ = "oui" THEN
            joueurA$ = "mortdecapR": Aoccupe$ = "oui": reftemps = temps
            xSPRt = xA + 3: scoreB = scoreB + 250
            sangA$ = "non": GOTO mort
        END IF

        vieA = vieA - 1
        IF vieA <= 0 THEN
            joueurA$ = "mortR": Aoccupe$ = "oui": reftemps = temps: sangA$ = "oui": GOTO mort
        END IF

        sontouche = sontouche + 1
        IF sontouche > 3 THEN sontouche = 1
        IF sontouche = 1 THEN _SNDPLAY touche
        IF sontouche = 2 THEN _SNDPLAY touche2
        IF sontouche = 3 THEN _SNDPLAY touche3


        joueurA$ = "touche1R": Aoccupe$ = "oui": reftemps = temps: decapiteA$ = "oui"
        GOTO joueur2

    END IF

    IF joueurA$ = "touche1R" THEN
        attenteA = 0
        xAttA = xA + 4
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        IF temps > reftemps + 20 THEN
            spriteA$ = "deboutR": Aoccupe$ = "non"
            joueurA$ = "deboutR": GOTO joueur2
        END IF
        IF temps > reftemps + 15 THEN spriteA$ = "touche4R": GOTO joueur2 'pour serpent
        IF temps > reftemps + 11 THEN GOTO joueur2
        IF temps > reftemps + 10 THEN xA = xA + 1: sangA$ = "non": spriteA$ = "touche3R": GOTO joueur2
        IF temps > reftemps + 6 THEN GOTO joueur2
        IF temps > reftemps + 5 THEN xA = xA + 2: spriteA$ = "touche2R": GOTO joueur2
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN xA = xA + 1: spriteA$ = "touche1R": GOTO joueur2
        spriteA$ = "touche1R"
    END IF

    IF joueurA$ = "tombe" THEN

        xAttA = xA
        attenteA = 0
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        yFA = 15: yTA = 16: yMA = 18: yGA = 20
        sangA$ = "oui"
        serpentA$ = "oui"

        vieA = vieA - 1: scoreB = scoreB + 100
        IF joueurB$ = "rouladeAV" THEN vieA = vieA + 1: sangA$ = "non": serpentA$ = "non": scoreB = scoreB - 100

        IF vieA <= 0 THEN
            joueurA$ = "mort": Aoccupe$ = "oui": reftemps = temps: sangA$ = "oui"
            IF joueurB$ = "coupdetete" OR joueurB$ = "coupdepied" THEN sangA$ = "non"
            GOTO mort
        END IF

        IF joueurB$ = "coupdetete" THEN scoreB = scoreB + 150: sangA$ = "non": _SNDPLAY coupdetete:


        IF joueurB$ = "coupdepied" THEN scoreB = scoreB + 150: sangA$ = "non": _SNDPLAY coupdepied


        joueurA$ = "tombe1": Aoccupe$ = "oui": reftemps = temps
        GOTO joueur2
    END IF


    IF joueurA$ = "tombe1" THEN
        xAttA = xA
        attenteA = 0
        xFA = xA: xTA = xA: xMA = xA: xGA = xA
        IF temps > reftemps + 25 THEN
            spriteA$ = "debout": xA = xA - 1: joueurA$ = "debout": Aoccupe$ = "non": GOTO joueur2
        END IF
        IF temps > reftemps + 20 THEN spriteA$ = "tombe4": GOTO joueur2
        IF temps > reftemps + 15 THEN spriteA$ = "tombe3": GOTO joueur2
        IF temps > reftemps + 10 THEN GOTO joueur2
        IF temps > reftemps + 9 THEN sangA$ = "non": xA = xA - 2: spriteA$ = "tombe2": GOTO joueur2
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN
            _SNDPLAY tombe
            IF joueurB$ = "coupdetete" THEN _SNDSTOP tombe
            xA = xA - 2: GOTO joueur2
        END IF
        spriteA$ = "tombe1"
    END IF

    IF joueurA$ = "tombeR" THEN
        xAttA = xA + 4
        attenteA = 0
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        yFA = 15: yTA = 16: yMA = 18: yGA = 20
        sangA$ = "oui"
        serpentA$ = "oui"

        vieA = vieA - 1: scoreB = scoreB + 100
        IF joueurB$ = "rouladeAVR" THEN vieA = vieA + 1: sangA$ = "non": serpentA$ = "non": scoreB = scoreB - 100

        IF vieA <= 0 THEN
            joueurA$ = "mortR": Aoccupe$ = "oui": reftemps = temps: sangA$ = "oui"
            IF joueurB$ = "coupdeteteR" OR joueurB$ = "coupdepiedR" THEN sangA$ = "non"
            GOTO mort
        END IF


        IF joueurB$ = "coupdeteteR" THEN _SNDPLAY coupdetete: scoreB = scoreB + 150: sangA$ = "non"

        IF joueurB$ = "coupdepiedR" THEN _SNDPLAY coupdepied: scoreB = scoreB + 150: sangA$ = "non"


        joueurA$ = "tombe1R": Aoccupe$ = "oui": reftemps = temps
        GOTO joueur2

    END IF

    IF joueurA$ = "tombe1R" THEN
        xAttA = xA + 4
        attenteA = 0
        xFA = xA + 4: xTA = xA + 4: xMA = xA + 4: xGA = xA + 4
        IF temps > reftemps + 25 THEN
            spriteA$ = "deboutR": xA = xA + 1: joueurA$ = "deboutR": Aoccupe$ = "non": GOTO joueur2
        END IF
        IF temps > reftemps + 20 THEN spriteA$ = "tombe4R": GOTO joueur2 ' pour serpent
        IF temps > reftemps + 15 THEN spriteA$ = "tombe3R": GOTO joueur2
        IF temps > reftemps + 10 THEN GOTO joueur2
        IF temps > reftemps + 9 THEN sangA$ = "non": xA = xA + 2: spriteA$ = "tombe2R": GOTO joueur2
        IF temps > reftemps + 2 THEN GOTO joueur2
        IF temps > reftemps + 1 THEN
            _SNDPLAY tombe
            IF joueurB$ = "coupdeteteR" THEN _SNDSTOP tombe
            xA = xA + 2: GOTO joueur2
        END IF
        spriteA$ = "tombe1R"
    END IF


    '                               bruit des epees  et decapitation loupee
    IF sens$ = "normal" THEN

        IF joueurA$ = "clingD" THEN

            IF joueurB$ = "decapite" AND decapiteA$ = "non" THEN joueurA$ = "touche": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
            IF joueurB$ = "genou" THEN joueurA$ = "touche": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
            IF distance < 12 THEN
                soncling = soncling + 1
                IF soncling > 3 THEN soncling = 1
                IF soncling = 1 THEN _SNDPLAY cling
                IF soncling = 2 THEN _SNDPLAY cling2
                IF soncling = 3 THEN _SNDPLAY cling3
            END IF
            joueurA$ = "protegeD": GOTO joueur2
        END IF

        IF joueurA$ = "clingH" THEN
            IF distance < 12 THEN
                soncling = soncling + 1
                IF soncling > 3 THEN soncling = 1
                IF soncling = 1 THEN _SNDPLAY cling
                IF soncling = 2 THEN _SNDPLAY cling2
                IF soncling = 3 THEN _SNDPLAY cling3
            END IF
            joueurA$ = "protegeH": GOTO joueur2
        END IF

    END IF

    IF sens$ = "inverse" THEN

        IF joueurA$ = "clingD" THEN
            IF joueurB$ = "decapiteR" AND decapiteA$ = "non" THEN joueurA$ = "toucheR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
            IF joueurB$ = "genouR" THEN joueurA$ = "toucheR": Aoccupe$ = "oui": reftemps = temps: GOTO gestion
            IF distance < 12 THEN
                soncling = soncling + 1
                IF soncling > 3 THEN soncling = 1
                IF soncling = 1 THEN _SNDPLAY cling
                IF soncling = 2 THEN _SNDPLAY cling2
                IF soncling = 3 THEN _SNDPLAY cling3
            END IF
            joueurA$ = "protegeDR": GOTO joueur2
        END IF

        IF joueurA$ = "clingH" THEN
            IF distance < 12 THEN
                soncling = soncling + 1
                IF soncling > 3 THEN soncling = 1
                IF soncling = 1 THEN _SNDPLAY cling
                IF soncling = 2 THEN _SNDPLAY cling2
                IF soncling = 3 THEN _SNDPLAY cling3
            END IF
            joueurA$ = "protegeHR": GOTO joueur2
        END IF

    END IF


    '                                   *************************************
    '                                   **********gestion de la mort*********
    '                                   *************************************

    mort:

    IF joueurA$ = "mort" THEN
        IF temps > reftemps + 16 THEN GOTO joueur2
        IF temps > reftemps + 15 THEN sangA$ = "non": spriteA$ = "mort2": GOTO joueur2
        IF temps > reftemps + 1 THEN spriteA$ = "mort1": GOTO joueur2
        spriteA$ = "mort1": joueurB$ = "vainqueurKO": Boccupe$ = "oui": reftempsB = temps
        IF lancerfin$ = "oui" THEN _SNDPLAY mortKO: lancerfin$ = "non"
    END IF

    IF joueurA$ = "mortR" THEN
        IF temps > reftemps + 16 THEN GOTO joueur2
        IF temps > reftemps + 15 THEN sangA$ = "non": spriteA$ = "mort2R": GOTO joueur2
        IF temps > reftemps + 1 THEN spriteA$ = "mort1R": GOTO joueur2
        spriteA$ = "mort1R":
        joueurB$ = "vainqueurKOR": Boccupe$ = "oui": reftempsB = temps
        IF lancerfin$ = "oui" THEN _SNDPLAY mortKO: lancerfin$ = "non"
    END IF

    IF joueurA$ = "mortdecap" THEN
        IF temps > reftemps + 80 THEN spriteA$ = "decap4": GOTO joueur2
        IF temps > reftemps + 70 THEN spriteA$ = "decap3": GOTO joueur2
        IF temps > reftemps + 55 THEN sangdecapA = 0: GOTO joueur2
        IF temps > reftemps + 50 THEN sangdecapA = 6: GOTO joueur2
        IF temps > reftemps + 45 THEN sangdecapA = 5: GOTO joueur2
        IF temps > reftemps + 40 THEN sangdecapA = 4: GOTO joueur2
        IF temps > reftemps + 35 THEN spriteA$ = "decap2": GOTO joueur2
        IF temps > reftemps + 20 THEN sangdecapA = 0: GOTO joueur2
        IF temps > reftemps + 15 THEN sangdecapA = 3: GOTO joueur2
        IF temps > reftemps + 10 THEN sangdecapA = 2: GOTO joueur2
        IF temps > reftemps + 5 THEN sangdecapA = 1: GOTO joueur2
        spriteA$ = "decap1": joueurB$ = "vainqueur": Boccupe$ = "oui": reftempsB = temps
        IF lancerfin$ = "oui" THEN _SNDPLAY mortdecap: lancerfin$ = "non"
    END IF

    IF joueurA$ = "mortdecapR" THEN
        IF temps > reftemps + 80 THEN spriteA$ = "decap4R": GOTO joueur2
        IF temps > reftemps + 70 THEN spriteA$ = "decap3R": GOTO joueur2
        IF temps > reftemps + 55 THEN sangdecapA = 0: GOTO joueur2
        IF temps > reftemps + 50 THEN sangdecapA = 6: GOTO joueur2
        IF temps > reftemps + 45 THEN sangdecapA = 5: GOTO joueur2
        IF temps > reftemps + 40 THEN sangdecapA = 4: GOTO joueur2
        IF temps > reftemps + 35 THEN spriteA$ = "decap2R": GOTO joueur2
        IF temps > reftemps + 20 THEN sangdecapA = 0: GOTO joueur2
        IF temps > reftemps + 15 THEN sangdecapA = 3: GOTO joueur2
        IF temps > reftemps + 10 THEN sangdecapA = 2: GOTO joueur2
        IF temps > reftemps + 5 THEN sangdecapA = 1: GOTO joueur2
        spriteA$ = "decap1R": joueurB$ = "vainqueurR": Boccupe$ = "oui": reftempsB = temps
        IF lancerfin$ = "oui" THEN _SNDPLAY mortdecap: lancerfin$ = "non"
    END IF

    IF joueurA$ = "mortSORCIER" THEN

        IF temps > reftemps + 86 THEN joueurA$ = "sorcierFINI": GOTO joueur2

        IF temps > reftemps + 85 THEN sangA$ = "non": spriteA$ = "mort4R": GOTO joueur2
        IF temps > reftemps + 71 THEN GOTO joueur2
        IF temps > reftemps + 70 THEN sangA$ = "non": spriteA$ = "mort3R": xA = xA + 2: GOTO joueur2
        IF temps > reftemps + 15 THEN sangA$ = "non": spriteA$ = "mort2R": GOTO joueur2
        IF temps > reftemps + 1 THEN spriteA$ = "mort1R": GOTO joueur2
        spriteA$ = "mort1R"

    END IF

    '                         **************************************
    '                         *********     joueur 2    ************
    '                         **************************************
    joueur2:
    'debut joueur 2

    IF sorcier$ = "oui" THEN sangB$ = "non"

    IF sorcier$ = "oui" THEN

        IF xA <= xB + 4 THEN
            joueurB$ = "marianna": joueurA$ = "fini"
            spriteB$ = "marianna": spriteA$ = "vainqueur3R"
            xB = 13: xA = 20
            Boccupe$ = "oui": Aoccupe$ = "oui"
            reftempsB = temps: reftempsB = temps
            jeu$ = "gagne"
            GOTO debut
        END IF


        IF Boccupe$ = "oui" THEN GOTO gestionB
        sangB$ = "non"

        GOTO clavierB

    END IF



    '                           ************degats sur joueurB************

    IF sens$ = "normal" THEN
        IF xB > xA THEN
            IF xAttA >= xFB AND yAttA = yFB THEN
                IF joueurB$ = "protegeH" THEN joueurB$ = "clingH": GOTO gestionB
                joueurB$ = "tombe": infoBdegatF = infoBdegatF + 1: GOTO gestionB
            END IF

            IF xAttA >= xTB AND yAttA = yTB THEN
                IF joueurA$ = "coupdetete" THEN joueurB$ = "tombe": GOTO gestionB
                joueurB$ = "touche": scoreA = scoreA + 250: infoBdegatT = infoBdegatT + 1: GOTO gestionB
            END IF

            IF xAttA >= xMB AND yAttA = yMB THEN
                IF joueurB$ = "protegeD" THEN joueurB$ = "clingD": GOTO gestionB
                joueurB$ = "touche": scoreA = scoreA + 250: GOTO gestionB
            END IF

            IF xAttA >= xGB AND yAttA = yGB THEN
                IF joueurA$ = "araignee" THEN joueurB$ = "tombe": GOTO gestionB
                IF joueurA$ = "rouladeAV" THEN joueurB$ = "tombe": GOTO gestionB
                IF joueurB$ = "protegeD" THEN joueurB$ = "clingD": GOTO gestionB
                IF joueurA$ = "coupdepied" THEN joueurB$ = "tombe": infoBdegatG = infoBdegatG + 1: GOTO gestionB
                joueurB$ = "touche": scoreA = scoreA + 100: infoBdegatG = infoBdegatG + 1: GOTO gestionB
            END IF
        END IF
    END IF

    IF sens$ = "inverse" THEN
        IF xB < xA THEN
            IF xAttA <= xFB AND yAttA = yFB THEN
                IF joueurB$ = "protegeHR" THEN joueurB$ = "clingH": GOTO gestionB
                joueurB$ = "tombeR": infoBdegatF = infoBdegatF + 1: GOTO gestionB
            END IF

            IF xAttA <= xTB AND yAttA = yTB THEN
                IF joueurA$ = "coupdeteteR" THEN joueurB$ = "tombeR": GOTO gestionB
                joueurB$ = "toucheR": scoreA = scoreA + 250: infoBdegatT = infoBdegatT + 1: GOTO gestionB
            END IF

            IF xAttA <= xMB AND yAttA = yMB THEN
                IF joueurB$ = "protegeDR" THEN joueurB$ = "clingD": GOTO gestionB
                joueurB$ = "toucheR": scoreA = scoreA + 250: GOTO gestionB
            END IF

            IF xAttA <= xGB AND yAttA = yGB THEN
                IF joueurA$ = "araigneeR" THEN joueurB$ = "tombeR": GOTO gestionB
                IF joueurA$ = "rouladeAVR" THEN joueurB$ = "tombeR": GOTO gestionB
                IF joueurB$ = "protegeDR" THEN joueurB$ = "clingD": GOTO gestionB
                IF joueurA$ = "coupdepiedR" THEN joueurB$ = "tombeR": infoBdegatG = infoBdegatG + 1: GOTO gestionB
                joueurB$ = "toucheR": scoreA = scoreA + 100: infoBdegatG = infoBdegatG + 1: GOTO gestionB
            END IF
        END IF
    END IF

    IF Boccupe$ = "oui" THEN GOTO gestionB
    sangB$ = "non"

    '                       ********************************************
    '                       ******* evenements clavier joueurB *********
    '                       ********************************************

    clavierB:

    x2 = 7: y2 = 7
    levier2$ = "neutre":

    IF partie$ = "vs" THEN

        '                                   entre des touches

        IF _KEYDOWN(105) OR STICK(3) < 65 THEN y2 = y2 - 1
        IF _KEYDOWN(107) OR STICK(3) > 190 THEN y2 = y2 + 1
        IF _KEYDOWN(108) OR STICK(2) > 190 THEN x2 = x2 + 1
        IF _KEYDOWN(106) OR STICK(2) < 65 THEN x2 = x2 - 1


        IF _KEYDOWN(32) OR STRIG(3) = -1 THEN attaqueB$ = "oui" ELSE attaqueB$ = "non"




        '                       amplitude du pave virtuel
        IF y2 > 9 THEN y2 = 9
        IF y2 < 5 THEN y2 = 5
        IF x2 > 9 THEN x2 = 9
        IF x2 < 5 THEN x2 = 5

        '                        position du "levier"  virtuel

        IF sens$ = "normal" THEN
            IF (x2 <= 6 AND y2 <= 6) THEN levier2$ = "hautG"
            IF (x2 >= 8 AND y2 <= 6) THEN levier2$ = "hautD"
            IF (x2 <= 6 AND y2 >= 8) THEN levier2$ = "basG"
            IF (x2 >= 8 AND y2 >= 8) THEN levier2$ = "basD"
            IF (x2 <= 6 AND y2 = 7) THEN levier2$ = "gauche"
            IF (x2 >= 8 AND y2 = 7) THEN levier2$ = "droite"
            IF (x2 = 7 AND y2 >= 8) THEN levier2$ = "bas"
            IF (x2 = 7 AND y2 <= 6) THEN levier2$ = "haut"
        END IF
        IF sens$ = "inverse" THEN
            IF (x2 <= 6 AND y2 <= 6) THEN levier2$ = "hautG"
            IF (x2 >= 8 AND y2 <= 6) THEN levier2$ = "hautD"
            IF (x2 <= 6 AND y2 >= 8) THEN levier2$ = "basG"
            IF (x2 >= 8 AND y2 >= 8) THEN levier2$ = "basD"
            IF (x2 <= 6 AND y2 = 7) THEN levier2$ = "gauche"
            IF (x2 >= 8 AND y2 = 7) THEN levier2$ = "droite"
            IF (x2 = 7 AND y2 >= 8) THEN levier2$ = "bas"
            IF (x2 = 7 AND y2 <= 6) THEN levier2$ = "haut"
        END IF
    END IF

    '                       **********************************
    '                       ******* animations  auto *********
    '                       **********************************

    IF entree$ = "oui" THEN levier2$ = "gauche": GOTO actionB

    IF sortieB$ = "oui" THEN
        IF tempsfini$ = "oui" THEN
            IF sens$ = "inverse" THEN levier2$ = "gauche": GOTO actionB
        END IF

        sens$ = "normal": levier2$ = "droite": GOTO actionB
    END IF

    '                       *****************************************
    '                       ******* Intelligence Artificielle *******
    '                       *****************************************

    IF joueurA$ = "finderoulade" OR joueurA$ = "finderouladeR" OR joueurB$ = "finderoulade" OR joueurB$ = "finderouladeR" THEN GOTO gestionB

    IF partie$ = "solo" THEN

        ' ***************************IA de 1,2,3,6

        IF IA = 0 OR IA = 1 OR IA = 2 OR IA = 3 OR IA = 6 THEN
            IF sens$ = "normal" THEN
                distance = xB - xA

                IF distance >= 15 THEN '  quand trop loin
                    joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                END IF

                IF IA = 6 THEN
                    IF distance < 15 THEN
                        IF joueurA$ = "decapite" THEN joueurB$ = "genou": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF
                END IF

                IF IA = 3 THEN
                    IF distance < 15 THEN
                        IF infoBdegatT > 2 THEN
                            IF joueurA$ = "decapite" THEN joueurB$ = "assis2": GOTO gestionB
                        END IF

                        IF joueurA$ = "decapite" THEN joueurB$ = "protegeD": reftempsB = temps: GOTO gestionB
                    END IF
                END IF


                IF distance = 12 AND joueurA$ = "debout" THEN joueurB$ = "decapite": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                IF distance > 9 AND distance < 15 THEN ' pour se rapprocher
                    IF levier1$ = "gauche" THEN joueurB$ = "debout": GOTO gestionB
                    levier2$ = "gauche": GOTO actionB
                END IF

                IF distance = 9 THEN
                    IF attenteA > 100 THEN levier2$ = "gauche": GOTO actionB
                    IF joueurA$ = "rouladeAR" THEN joueurB$ = "devant": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF Aoccupe$ = "oui" THEN levier2$ = "gauche": GOTO actionB

                END IF

                IF distance < 9 AND distance > 6 THEN ' distance de combat 1
                    ' pour autoriser les croisements
                    IF demo$ = "non" AND joueurA$ = "rouladeAV" THEN joueurB$ = "saute": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                    ' pour se rapprocher
                    IF joueurA$ = "rouladeAR" THEN joueurB$ = "genou": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF levier1$ = "gauche" THEN joueurB$ = "araignee": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB


                    'pour eviter les degats repetitifs

                    IF IA > 1 THEN
                        IF infoBdegatG > 4 THEN
                            IF joueurA$ = "assis2" OR joueurA$ = "genou" THEN joueurB$ = "genou": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF
                        IF infoBdegatG > 2 THEN
                            IF joueurA$ = "assis2" OR joueurA$ = "rouladeAV" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF

                        IF infoBdegatT > 2 THEN
                            IF joueurA$ = "cou" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF

                        IF infoBdegatF > 2 THEN
                            IF joueurA$ = "front" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF

                    END IF


                    'pour alterner les attaques
                    IF infocoupB = 0 THEN joueurB$ = "coupdepied": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 1 THEN joueurB$ = "debout": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 2 THEN joueurB$ = "araignee": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 3 THEN joueurB$ = "debout": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 4 THEN joueurB$ = "assis2": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 5 THEN joueurB$ = "genou": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 6 THEN levier2$ = "gauche": infocoupB = 0: GOTO actionB


                END IF
                IF distance <= 6 THEN

                    ' pour autoriser les croisements
                    IF demo$ = "non" AND joueurA$ = "saute" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                    IF IA = 3 THEN
                        IF joueurA$ = "devant" THEN joueurB$ = "protegeD": reftempsB = temps: GOTO gestionB
                    END IF

                    IF IA = 2 THEN
                        IF joueurA$ = "genou" THEN joueurB$ = "saute": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF

                    IF IA > 1 THEN
                        IF infoBdegatG > 4 THEN
                            IF joueurA$ = "assis2" OR joueurA$ = "genou" THEN joueurB$ = "coupdepied": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                            IF IA > 2 THEN IF joueurA$ = "araignee" THEN joueurB$ = "araignee": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF
                        IF infoBdegatG > 2 THEN
                            IF joueurA$ = "coupdepied" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                            IF joueurA$ = "assis2" OR joueurA$ = "genou" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF
                    END IF

                    IF infocoupB = 0 THEN joueurB$ = "coupdepied": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 1 THEN joueurB$ = "coupdetete": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 2 THEN joueurB$ = "araignee": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 3 THEN joueurB$ = "debout": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 4 THEN joueurB$ = "assis2": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 5 THEN joueurB$ = "genou": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 6 THEN joueurB$ = "debout": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 7 THEN levier2$ = "gauche": infocoupB = 0: GOTO actionB

                END IF
            END IF


            IF sens$ = "inverse" THEN

                distance = xA - xB

                IF distance >= 15 THEN '  quand trop loin
                    joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                END IF

                IF IA = 6 THEN
                    IF distance < 15 THEN
                        IF joueurA$ = "decapiteR" THEN joueurB$ = "genouR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF
                END IF

                IF IA = 3 THEN
                    IF distance < 15 THEN
                        IF infoBdegatT > 2 THEN
                            IF joueurA$ = "decapiteR" THEN joueurB$ = "assis2R": GOTO gestionB
                        END IF

                        IF joueurA$ = "decapiteR" THEN joueurB$ = "protegeDR": reftempsB = temps: GOTO gestionB
                    END IF
                END IF

                IF distance = 12 AND joueurA$ = "deboutR" THEN joueurB$ = "decapiteR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                IF distance > 9 AND distance < 15 THEN ' pour se rapprocher
                    IF levier1$ = "droite" THEN joueurB$ = "deboutR": GOTO gestionB
                    levier2$ = "droite": GOTO actionB
                END IF

                IF distance = 9 THEN
                    IF attenteA > 100 THEN levier2$ = "droite": GOTO actionB
                    IF joueurA$ = "rouladeARR" THEN joueurB$ = "devantR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF Aoccupe$ = "oui" THEN levier2$ = "droite": GOTO actionB

                END IF

                IF distance < 9 AND distance > 6 THEN ' distance de combat 1
                    ' pour autoriser les croisements
                    IF demo$ = "non" AND joueurA$ = "rouladeAVR" THEN joueurB$ = "sauteR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                    ' pour se rapprocher
                    IF joueurA$ = "rouladeARR" THEN joueurB$ = "genouR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF levier1$ = "droite" THEN joueurB$ = "araigneeR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB


                    'pour eviter les degats repetitifs

                    IF IA > 1 THEN
                        IF infoBdegatG > 4 THEN
                            IF joueurA$ = "assis2R" OR joueurA$ = "genouR" THEN joueurB$ = "genouR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF
                        IF infoBdegatG > 2 THEN
                            IF joueurA$ = "assis2R" OR joueurA$ = "rouladeAVR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF

                        IF infoBdegatT > 2 THEN
                            IF joueurA$ = "couR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF

                        IF infoBdegatF > 2 THEN
                            IF joueurA$ = "frontR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF

                    END IF


                    'pour alterner les attaques
                    IF infocoupB = 0 THEN joueurB$ = "coupdepiedR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 1 THEN joueurB$ = "deboutR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 2 THEN joueurB$ = "araigneeR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 3 THEN joueurB$ = "deboutR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 4 THEN joueurB$ = "assis2R": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 5 THEN joueurB$ = "genouR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 6 THEN levier2$ = "droite": infocoupB = 0: GOTO actionB


                END IF
                IF distance <= 6 THEN

                    ' pour autoriser les croisements
                    IF demo$ = "non" AND joueurA$ = "sauteR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                    IF IA = 3 THEN
                        IF joueurA$ = "devantR" THEN joueurB$ = "protegeDR": reftempsB = temps: GOTO gestionB
                    END IF

                    IF IA = 2 THEN
                        IF joueurA$ = "genouR" THEN joueurB$ = "sauteR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF


                    IF IA > 1 THEN
                        IF infoBdegatG > 4 THEN
                            IF joueurA$ = "assis2R" OR joueurA$ = "genouR" THEN joueurB$ = "genouR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                            IF IA > 2 THEN IF joueurA$ = "araigneeR" THEN joueurB$ = "araigneeR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF
                        IF infoBdegatG > 2 THEN
                            IF joueurA$ = "coupdepiedR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                            IF joueurA$ = "assis2R" OR joueurA$ = "coupdepiedR" THEN joueurB$ = "genouR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        END IF
                    END IF

                    IF infocoupB = 0 THEN joueurB$ = "coupdepiedR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 1 THEN joueurB$ = "coupdeteteR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 2 THEN joueurB$ = "araigneeR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 3 THEN joueurB$ = "deboutR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 4 THEN joueurB$ = "assis2R": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 5 THEN joueurB$ = "genouR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 6 THEN joueurB$ = "deboutR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 7 THEN levier2$ = "droite": infocoupB = 0: GOTO actionB

                END IF
            END IF

        END IF


        ' ************************* IA de 4 , 5, 7

        IF IA = 4 OR IA = 5 OR IA = 7 THEN
            IF sens$ = "normal" THEN
                distance = xB - xA

                IF distance >= 15 THEN '  quand trop loin
                    joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                END IF

                IF distance < 15 THEN
                    IF IA = 7 THEN IF joueurA$ = "decapite" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                END IF

                IF distance = 12 AND joueurA$ = "debout" THEN joueurB$ = "decapite": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                IF distance > 9 AND distance < 15 THEN ' pour se rapprocher
                    IF levier1$ = "gauche" THEN joueurB$ = "debout": GOTO gestionB
                    levier2$ = "gauche": GOTO actionB
                END IF

                IF distance = 9 THEN
                    IF attenteA > 100 THEN joueurB$ = "decapite": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF demo$ = "oui" THEN IF attenteA > 25 THEN joueurB$ = "decapite": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF joueurA$ = "rouladeAR" THEN joueurB$ = "genou": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF IA < 7 THEN IF Aoccupe$ = "oui" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF IA = 7 THEN IF Aoccupe$ = "oui" THEN levier2$ = "gauche": GOTO actionB
                END IF

                IF distance < 9 AND distance > 6 THEN ' distance de combat 1
                    ' pour autoriser les croisements
                    IF demo$ = "non" AND joueurA$ = "rouladeAV" THEN joueurB$ = "saute": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                    ' pour se rapprocher
                    IF joueurA$ = "rouladeAR" THEN joueurB$ = "genou": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF levier1$ = "gauche" THEN joueurB$ = "araignee": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB


                    'plus l'IA est forte, plus il y des des coups imposs avant infocoupB ou infodegat

                    IF IA = 5 THEN
                        IF joueurA$ = "front" THEN joueurB$ = "protegeH": reftempsB = temps: GOTO gestionB
                    END IF

                    'pour eviter les degats repetitifs
                    IF infoBdegatG > 4 THEN
                        IF joueurA$ = "assis2" OR joueurA$ = "genou" OR joueurA$ = "araignee" THEN joueurB$ = "araignee": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF
                    IF infoBdegatG > 2 THEN
                        IF joueurA$ = "assis2" OR joueurA$ = "genou" OR joueurA$ = "araignee" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF

                    IF infoBdegatT > 2 THEN
                        IF joueurA$ = "cou" THEN joueurB$ = "genou": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF

                    IF infoBdegatF > 2 THEN
                        IF IA < 7 THEN IF joueurA$ = "front" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF



                    'pour alterner les attaques

                    IF infocoupB = 0 THEN joueurB$ = "devant": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 1 THEN joueurB$ = "front": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 2 THEN joueurB$ = "araignee": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 3 THEN joueurB$ = "araignee": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 4 THEN joueurB$ = "cou": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 5 THEN levier2$ = "gauche": infocoupB = 0: GOTO actionB


                END IF
                IF distance <= 6 THEN

                    ' pour autoriser les croisements
                    IF demo$ = "non" AND joueurA$ = "saute" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB


                    IF IA > 4 THEN IF joueurA$ = "devant" THEN joueurB$ = "protegeD": reftempsB = temps: GOTO gestionB

                    IF IA > 4 AND IA < 7 THEN IF joueurA$ = "genou" THEN joueurB$ = "saute": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                    IF infoBdegatG > 4 THEN
                        IF joueurA$ = "assis2" OR joueurA$ = "genou" OR joueurA$ = "araignee" THEN joueurB$ = "araignee": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF
                    IF infoBdegatG > 2 THEN
                        IF joueurA$ = "coupdepied" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        IF joueurA$ = "assis2" OR joueurA$ = "genou" OR joueurA$ = "araignee" THEN joueurB$ = "rouladeAV": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF

                    IF infocoupB = 0 THEN joueurB$ = "coupdepied": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 1 THEN joueurB$ = "coupdetete": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 2 THEN joueurB$ = "araignee": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 3 THEN joueurB$ = "genou": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 4 THEN joueurB$ = "genou": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 5 THEN levier2$ = "gauche": infocoupB = 0: GOTO actionB


                END IF
            END IF


            IF sens$ = "inverse" THEN

                distance = xA - xB

                IF distance >= 15 THEN '  quand trop loin
                    joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                END IF

                IF distance < 15 THEN
                    IF IA = 7 THEN IF joueurA$ = "decapiteR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                END IF

                IF distance = 12 AND joueurA$ = "deboutR" THEN joueurB$ = "decapiteR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                IF distance > 9 AND distance < 15 THEN ' pour se rapprocher
                    IF levier1$ = "droite" THEN joueurB$ = "deboutR": GOTO gestionB
                    levier2$ = "droite": GOTO actionB
                END IF

                IF distance = 9 THEN
                    IF attenteA > 100 THEN joueurB$ = "decapiteR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF demo$ = "oui" THEN IF attenteA > 100 THEN joueurB$ = "decapiteR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF joueurA$ = "rouladeARR" THEN joueurB$ = "genouR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF IA < 7 THEN IF Aoccupe$ = "oui" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF IA = 7 THEN IF Aoccupe$ = "oui" THEN levier2$ = "droite": GOTO actionB
                END IF

                IF distance < 9 AND distance > 6 THEN ' distance de combat 1
                    ' pour autoriser les croisements
                    IF demo$ = "non" AND joueurA$ = "rouladeAV" THEN joueurB$ = "sauteR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                    ' pour se rapprocher
                    IF joueurA$ = "rouladeARR" THEN joueurB$ = "genouR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF levier1$ = "droite" THEN joueurB$ = "araigneeR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB


                    'plus l'IA est forte, plus il y des des coups imposs avant infocoupB ou infodegat

                    IF IA = 5 THEN
                        IF joueurA$ = "frontR" THEN joueurB$ = "protegeHR": reftempsB = temps: GOTO gestionB
                    END IF

                    'pour eviter les degats repetitifs
                    IF infoBdegatG > 4 THEN
                        IF joueurA$ = "assis2R" OR joueurA$ = "genouR" OR joueurA$ = "araigneeR" THEN joueurB$ = "araigneeR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF
                    IF infoBdegatG > 2 THEN
                        IF joueurA$ = "assis2R" OR joueurA$ = "genouR" OR joueurA$ = "araigneeR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF

                    IF infoBdegatT > 2 THEN
                        IF joueurA$ = "couR" THEN joueurB$ = "genouR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF

                    IF infoBdegatF > 2 THEN
                        IF IA < 7 THEN IF joueurA$ = "frontR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF



                    'pour alterner les attaques

                    IF infocoupB = 0 THEN joueurB$ = "devantR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 1 THEN joueurB$ = "frontR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 2 THEN joueurB$ = "araigneeR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 3 THEN joueurB$ = "araigneeR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 4 THEN joueurB$ = "couR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 5 THEN levier2$ = "droite": infocoupB = 0: GOTO actionB


                END IF
                IF distance <= 6 THEN

                    ' pour autoriser les croisements
                    IF demo$ = "non" AND joueurA$ = "sauteR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB


                    IF IA > 4 THEN IF joueurA$ = "devantR" THEN joueurB$ = "protegeDR": reftempsB = temps: GOTO gestionB

                    IF IA > 4 AND IA < 7 THEN IF joueurA$ = "genouR" THEN joueurB$ = "sauteR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB

                    IF infoBdegatG > 4 THEN
                        IF joueurA$ = "assis2R" OR joueurA$ = "genouR" OR joueurA$ = "araigneeR" THEN joueurB$ = "araigneeR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF
                    IF infoBdegatG > 2 THEN
                        IF joueurA$ = "coupdepiedR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                        IF joueurA$ = "assis2R" OR joueurA$ = "genouR" OR joueurA$ = "araigneeR" THEN joueurB$ = "rouladeAVR": reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    END IF

                    IF infocoupB = 0 THEN joueurB$ = "coupdepiedR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 1 THEN joueurB$ = "coupdeteteR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 2 THEN joueurB$ = "araigneeR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 3 THEN joueurB$ = "genouR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 4 THEN joueurB$ = "genouR": infocoupB = infocoupB + 1: reftempsB = temps: Boccupe$ = "oui": GOTO gestionB
                    IF infocoupB = 5 THEN levier2$ = "droite": infocoupB = 0: GOTO actionB


                END IF

            END IF

        END IF


    END IF

    '                       redirection suivant les touches

    IF levier2$ = "hautG" GOTO actionB
    IF levier2$ = "hautD" GOTO actionB
    IF levier2$ = "basG" GOTO actionB
    IF levier2$ = "basD" GOTO actionB
    IF levier2$ = "bas" GOTO actionB
    IF levier2$ = "haut" GOTO actionB
    IF levier2$ = "gauche" GOTO actionB
    IF levier2$ = "droite" GOTO actionB


    '                       actions si aucune touche n'a ete touchee


    spriteavanceB = 0
    spritereculeB = 0

    protegeDB$ = "non": protegeHB$ = "non"

    attenteB = attenteB + 1
    levier2$ = "neutre"

    ' pour se relever
    assisB$ = "non"
    IF joueurB$ = "assis2" THEN joueurB$ = "releve": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
    IF joueurB$ = "assis2R" THEN joueurB$ = "releveR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB


    'attente des 5 secondes
    IF sens$ = "normal" THEN
        IF attenteB > 250 THEN joueurB$ = "attente": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
    END IF
    IF sens$ = "inverse" THEN
        IF attenteB > 250 THEN joueurB$ = "attenteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
    END IF

    IF sens$ = "normal" THEN joueurB$ = "debout"
    IF sens$ = "inverse" THEN joueurB$ = "deboutR"

    GOTO gestionB



    '                       *****************************************
    '                       *************actions joueur 2************
    '                       *****************************************
    actionB:

    attenteB = 1

    IF partie$ = "solo" THEN '  ****** IA mode ******

        '                       droite,gauche, decapite, devant (normal)  IA
        IF sens$ = "normal" THEN
            IF levier2$ = "gauche" THEN
                protegeDB$ = "non"
                IF spriteavanceB = 1 THEN joueurB$ = "avance1": GOTO gestionB
                IF spriteavanceB = 2 THEN joueurB$ = "avance2": GOTO gestionB
                IF spriteavanceB = 3 THEN joueurB$ = "avance3": GOTO gestionB
                IF spriteavanceB = 4 THEN joueurB$ = "avance4": GOTO gestionB
                joueurB$ = "avance": reftempsB = temps
            END IF

            IF levier2$ = "droite" THEN
                protegeHB$ = "non"
                IF spritereculeB = 1 THEN joueurB$ = "recule1": GOTO gestionB
                IF spritereculeB = 2 THEN joueurB$ = "recule2": GOTO gestionB
                IF spritereculeB = 3 THEN joueurB$ = "recule3": GOTO gestionB
                IF spritereculeB = 4 THEN joueurB$ = "recule4": GOTO gestionB
                joueurB$ = "recule": reftempsB = temps
            END IF
        END IF
        '                       droite, gauche, decapite, devant (inverse)  ******* IA mode ********

        IF sens$ = "inverse" THEN
            IF levier2$ = "droite" THEN
                protegeDB$ = "non"
                IF spriteavanceB = 1 THEN joueurB$ = "avance1R": GOTO gestionB
                IF spriteavanceB = 2 THEN joueurB$ = "avance2R": GOTO gestionB
                IF spriteavanceB = 3 THEN joueurB$ = "avance3R": GOTO gestionB
                IF spriteavanceB = 4 THEN joueurB$ = "avance4R": GOTO gestionB
                joueurB$ = "avanceR": reftempsB = temps
            END IF

            IF levier2$ = "gauche" THEN
                protegeHB$ = "non"
                IF spritereculeB = 1 THEN joueurB$ = "recule1R": GOTO gestionB
                IF spritereculeB = 2 THEN joueurB$ = "recule2R": GOTO gestionB
                IF spritereculeB = 3 THEN joueurB$ = "recule3R": GOTO gestionB
                IF spritereculeB = 4 THEN joueurB$ = "recule4R": GOTO gestionB
                joueurB$ = "reculeR": reftempsB = temps
            END IF
        END IF

        GOTO gestionB
    END IF



    '                       droite,gauche, decapite, devant (normal)


    IF sens$ = "normal" THEN
        IF levier2$ = "gauche" THEN
            protegeDB$ = "non"
            IF spriteavanceB = 1 THEN joueurB$ = "avance1": GOTO gestionB
            IF spriteavanceB = 2 THEN joueurB$ = "avance2": GOTO gestionB
            IF spriteavanceB = 3 THEN joueurB$ = "avance3": GOTO gestionB
            IF spriteavanceB = 4 THEN joueurB$ = "avance4": GOTO gestionB
            joueurB$ = "avance": reftempsB = temps
            IF attaqueB$ = "oui" AND entree$ = "non" THEN joueurB$ = "devant": Boccupe$ = "oui": reftempsB = temps
        END IF

        IF levier2$ = "droite" THEN
            protegeHB$ = "non"
            IF spritereculeB = 1 THEN joueurB$ = "recule1": GOTO gestionB
            IF spritereculeB = 2 THEN joueurB$ = "recule2": GOTO gestionB
            IF spritereculeB = 3 THEN joueurB$ = "recule3": GOTO gestionB
            IF spritereculeB = 4 THEN joueurB$ = "recule4": GOTO gestionB
            joueurB$ = "recule": reftempsB = temps
            IF attaqueB$ = "oui" AND sortieB$ = "non" THEN joueurB$ = "decapite": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF


    '                       droite, gauche, decapite, devant (inverse)

    IF sens$ = "inverse" THEN
        IF levier2$ = "droite" THEN
            protegeDB$ = "non"
            IF spriteavanceB = 1 THEN joueurB$ = "avance1R": GOTO gestionB
            IF spriteavanceB = 2 THEN joueurB$ = "avance2R": GOTO gestionB
            IF spriteavanceB = 3 THEN joueurB$ = "avance3R": GOTO gestionB
            IF spriteavanceB = 4 THEN joueurB$ = "avance4R": GOTO gestionB
            joueurB$ = "avanceR": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "devantR": Boccupe$ = "oui": reftempsB = temps:
        END IF

        IF levier2$ = "gauche" THEN
            protegeHB$ = "non"
            IF spritereculeB = 1 THEN joueurB$ = "recule1R": GOTO gestionB
            IF spritereculeB = 2 THEN joueurB$ = "recule2R": GOTO gestionB
            IF spritereculeB = 3 THEN joueurB$ = "recule3R": GOTO gestionB
            IF spritereculeB = 4 THEN joueurB$ = "recule4R": GOTO gestionB
            joueurB$ = "reculeR": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "decapiteR": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF

    '                           saute, attaque cou

    IF sens$ = "normal" THEN

        IF levier2$ = "haut" THEN
            protegeDB$ = "non": protegeHB$ = "non"
            joueurB$ = "saute": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        END IF
    END IF

    IF sens$ = "inverse" THEN
        IF levier2$ = "haut" THEN
            protegeDB$ = "non": protegeHB$ = "non"
            joueurB$ = "sauteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        END IF
    END IF


    '                               assis, attaque genou
    IF sens$ = "normal" THEN
        IF levier2$ = "bas" THEN
            IF attaqueB$ = "oui" THEN joueurB$ = "genou": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
            IF assisB$ = "oui" THEN joueurB$ = "assis2": GOTO gestionB
            joueurB$ = "assis": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        END IF
    END IF
    IF sens$ = "inverse" THEN
        IF levier2$ = "bas" THEN
            IF attaqueB$ = "oui" THEN joueurB$ = "genouR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
            IF assisB$ = "oui" THEN joueurB$ = "assis2R": GOTO gestionB
            joueurB$ = "assisR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        END IF
    END IF


    '                               roulade AV, coup de pied
    IF sens$ = "normal" THEN
        IF levier2$ = "basG" THEN
            joueurB$ = "rouladeAV": Boccupe$ = "oui": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "coupdepied": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF
    IF sens$ = "inverse" THEN
        IF levier2$ = "basD" THEN
            joueurB$ = "rouladeAVR": Boccupe$ = "oui": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "coupdepiedR": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF



    '                               roulade AR, coup sur front
    IF sens$ = "normal" THEN
        IF levier2$ = "basD" THEN
            joueurB$ = "rouladeAR": Boccupe$ = "oui": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "front": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF
    IF sens$ = "inverse" THEN
        IF levier2$ = "basG" THEN
            joueurB$ = "rouladeARR": Boccupe$ = "oui": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "frontR": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF

    '                                   protection Haute, araignee
    IF sens$ = "normal" THEN
        IF levier2$ = "hautD" THEN
            IF protegeHB$ = "oui" THEN joueurB$ = "protegeH": GOTO gestionB
            joueurB$ = "protegeH1": Boccupe$ = "oui": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "araignee": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF

    IF sens$ = "inverse" THEN
        IF levier2$ = "hautG" THEN
            IF protegeHB$ = "oui" THEN joueurB$ = "protegeHR": GOTO gestionB
            joueurB$ = "protegeHR1": Boccupe$ = "oui": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "araigneeR": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF


    '                                   protection devant, coup de tete
    IF sens$ = "normal" THEN
        IF levier2$ = "hautG" THEN
            IF protegeDB$ = "oui" THEN joueurB$ = "protegeD": GOTO gestionB
            joueurB$ = "protegeD1": Boccupe$ = "oui": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "coupdetete": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF
    IF sens$ = "inverse" THEN
        IF levier2$ = "hautD" THEN
            IF protegeDB$ = "oui" THEN joueurB$ = "protegeDR": GOTO gestionB
            joueurB$ = "protegeDR1": Boccupe$ = "oui": reftempsB = temps
            IF attaqueB$ = "oui" THEN joueurB$ = "coupdeteteR": Boccupe$ = "oui": reftempsB = temps
        END IF
    END IF


    '                       ***********************************
    '                       *********gestion joueur 2**********
    '                       ***********************************
    gestionB:

    IF joueurB$ = "debout" THEN
        spriteB$ = "debout": decapiteB$ = "oui"
        sangB$ = "non"
        xAttB = xB + 4: yAttB = 14
        yFB = 15: yTB = 16: yMB = 18: yGB = 20
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        IF partie$ = "solo" THEN
            IF temps > reftempsB + 20 THEN Boccupe$ = "non"
        END IF
    END IF

    IF joueurB$ = "deboutR" THEN
        spriteB$ = "deboutR"
        decapiteB$ = "oui"
        sangB$ = "non"
        xAttB = xB: yAttB = 14:
        yFB = 15: yTB = 16: yMB = 18: yGB = 20
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        IF partie$ = "solo" THEN
            IF temps > reftempsB + 20 THEN Boccupe$ = "non"
        END IF
    END IF

    IF joueurB$ = "attente" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        IF temps > reftempsB + 50 THEN Boccupe$ = "non": attenteB = 1: joueurB$ = "debout": GOTO colision
        IF temps > reftempsB + 37 THEN spriteB$ = "attente1": GOTO colision
        IF temps > reftempsB + 30 THEN spriteB$ = "attente2": GOTO colision
        IF temps > reftempsB + 23 THEN spriteB$ = "attente3": GOTO colision
        IF temps > reftempsB + 15 THEN spriteB$ = "attente2": GOTO colision
        IF temps > reftempsB + 8 THEN GOTO colision
        IF temps > reftempsB + 7 THEN _SNDPLAY attente: spriteB$ = "attente1": GOTO colision
    END IF

    IF joueurB$ = "attenteR" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        IF temps > reftempsB + 50 THEN Boccupe$ = "non": attenteB = 1: joueurB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 37 THEN spriteB$ = "attente1R": GOTO colision
        IF temps > reftempsB + 30 THEN spriteB$ = "attente2R": GOTO colision
        IF temps > reftempsB + 23 THEN spriteB$ = "attente3R": GOTO colision
        IF temps > reftempsB + 15 THEN spriteB$ = "attente2R": GOTO colision
        IF temps > reftempsB + 8 THEN GOTO colision
        IF temps > reftempsB + 7 THEN _SNDPLAY attente: spriteB$ = "attente1R": GOTO colision
    END IF

    IF joueurB$ = "saute" THEN
        xAttB = xB + 4: xFB = xB: xTB = xB: xMB = xB: xGB = xB
        yGB = yMB: yAttB = 14
        decapiteB$ = "non"
        IF attaqueB$ = "oui" THEN joueurB$ = "cou": Boccupe$ = "oui": reftempsB = temps: GOTO colision
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": spriteB$ = "debout": joueurB$ = "debout": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "debout": xMB = xB: xGB = xB: GOTO colision
        IF temps > reftempsB + 30 THEN spriteB$ = "saut1": xMB = xB: xGB = xB + 1: decapiteB$ = "oui": GOTO colision
        IF temps > reftempsB + 13 THEN spriteB$ = "saut2": xMB = xB + 3: xGB = xB + 3: GOTO colision
        IF temps > reftempsB + 2 THEN spriteB$ = "saut1": xMB = xB: xGB = xB + 3
        spriteB$ = "saut1"
    END IF

    IF joueurB$ = "sauteR" THEN
        xAttB = xB: xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        yGB = yMB: yAttB = 14
        decapiteB$ = "non"
        IF attaqueB$ = "oui" THEN joueurB$ = "couR": Boccupe$ = "oui": reftempsB = temps: GOTO colision
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": spriteB$ = "deboutR": joueurB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "deboutR": xMB = xB + 4: xGB = xB + 4: GOTO colision
        IF temps > reftempsB + 30 THEN spriteB$ = "saut1R": xMB = xB + 4: xGB = xB + 1: decapiteB$ = "oui": GOTO colision
        IF temps > reftempsB + 13 THEN spriteB$ = "saut2R": xMB = xB + 1: xGB = xB + 1: GOTO colision
        IF temps > reftempsB + 2 THEN spriteB$ = "saut1R": xMB = xB + 4: xGB = xB + 1
        spriteB$ = "saut1R"
    END IF

    '                                   avance
    IF joueurB$ = "avance" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        IF attaqueB$ = "oui" AND entree$ = "non" THEN joueurB$ = "devant": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        spriteB$ = "marche1": spriteavanceB = 1: xB = xB - 1
    END IF

    IF joueurB$ = "avance1" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        IF attaqueB$ = "oui" AND entree$ = "non" THEN joueurB$ = "devant": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 9 THEN xB = xB - 1: spriteB$ = "marche2": spriteavanceB = 2
    END IF

    IF joueurB$ = "avance2" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        spriteB$ = "marche2"
        IF attaqueB$ = "oui" AND entree$ = "non" THEN joueurB$ = "devant": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 18 THEN xB = xB - 1: spriteB$ = "marche3": spriteavanceB = 3
    END IF

    IF joueurB$ = "avance3" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        spriteB$ = "marche3"
        IF attaqueB$ = "oui" AND entree$ = "non" THEN joueurB$ = "devant": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 27 THEN xB = xB - 1: spriteB$ = "debout": spriteavanceB = 4
    END IF

    IF joueurB$ = "avance4" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        spriteB$ = "debout"
        IF attaqueB$ = "oui" AND entree$ = "non" THEN joueurB$ = "devant": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 36 THEN joueurB$ = "debout": reftempsB = temps: spriteavanceB = 0
    END IF


    IF joueurB$ = "avanceR" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        xAttB = xB
        IF attaqueB$ = "oui" THEN joueurB$ = "devantR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        spriteB$ = "marche1R": spriteavanceB = 1: xB = xB + 1
    END IF

    IF joueurB$ = "avance1R" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        xAttB = xB
        IF attaqueB$ = "oui" THEN joueurB$ = "devantR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 9 THEN xB = xB + 1: spriteB$ = "marche2R": spriteavanceB = 2
    END IF

    IF joueurB$ = "avance2R" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        xAttB = xB
        spriteB$ = "marche2R"
        IF attaqueB$ = "oui" THEN joueurB$ = "devantR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 17 THEN xB = xB + 1: spriteB$ = "marche3R": spriteavanceB = 3
    END IF

    IF joueurB$ = "avance3R" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        xAttB = xB
        spriteB$ = "marche3R"
        IF attaqueB$ = "oui" THEN joueurB$ = "devantR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 27 THEN xB = xB + 1: spriteB$ = "deboutR": spriteavanceB = 4
    END IF

    IF joueurB$ = "avance4R" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        xAttB = xB
        spriteB$ = "deboutR"
        IF attaqueB$ = "oui" THEN joueurB$ = "devantR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 36 THEN joueurB$ = "deboutR": reftempsB = temps: spriteavanceB = 0
    END IF

    '                                        recule
    IF joueurB$ = "recule" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        IF attaqueB$ = "oui" AND sortieB$ = "non" THEN joueurB$ = "decapite": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        spriteB$ = "marche3": spritereculeB = 1: xB = xB + 1
    END IF

    IF joueurB$ = "recule1" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        IF attaqueB$ = "oui" AND sortieB$ = "non" THEN joueurB$ = "decapite": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 9 THEN xB = xB + 1: spriteB$ = "marche2": spritereculeB = 2
    END IF
    IF joueurB$ = "recule2" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        spriteB$ = "marche2"
        IF attaqueB$ = "oui" AND sortieB$ = "non" THEN joueurB$ = "decapite": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 18 THEN xB = xB + 1: spriteB$ = "marche1": spritereculeB = 3
    END IF
    IF joueurB$ = "recule3" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        spriteB$ = "marche1"
        IF attaqueB$ = "oui" AND sortieB$ = "non" THEN joueurB$ = "decapite": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 26 THEN xB = xB + 1: spriteB$ = "debout": spritereculeB = 4
    END IF
    IF joueurB$ = "recule4" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        spriteB$ = "debout"
        IF attaqueB$ = "oui" AND sortieB$ = "non" THEN joueurB$ = "decapite": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 36 THEN joueurB$ = "debout": reftempsB = temps: spritereculeB = 0
    END IF

    '                               recule inverse
    IF joueurB$ = "reculeR" THEN
        xAttB = xB
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        IF attaqueB$ = "oui" THEN joueurB$ = "decapiteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        spriteB$ = "marche3R": spritereculeB = 1: xB = xB - 1
    END IF

    IF joueurB$ = "recule1R" THEN
        xAttB = xB
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        IF attaqueB$ = "oui" THEN joueurB$ = "decapiteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 9 THEN xB = xB - 1: spriteB$ = "marche2R": spritereculeB = 2
    END IF
    IF joueurB$ = "recule2R" THEN
        xAttB = xB
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        spriteB$ = "marche2R"
        IF attaqueB$ = "oui" THEN joueurB$ = "decapiteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 18 THEN xB = xB - 1: spriteB$ = "marche1R": spritereculeB = 3
    END IF
    IF joueurB$ = "recule3R" THEN
        xAttB = xB
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        spriteB$ = "marche1R"
        IF attaqueB$ = "oui" THEN joueurB$ = "decapiteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 26 THEN xB = xB - 1: spriteB$ = "deboutR": spritereculeB = 4
    END IF
    IF joueurB$ = "recule4R" THEN
        xAttB = xB
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        spriteB$ = "deboutR"
        IF attaqueB$ = "oui" THEN joueurB$ = "decapiteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 36 THEN joueurB$ = "deboutR": reftempsB = temps: spritereculeB = 0
    END IF

    IF joueurB$ = "assis" THEN
        xAttB = xB + 4
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB
        spriteB$ = "assis1"
        IF temps > reftempsB + 10 THEN joueurB$ = "assis2": GOTO colision
        IF attaqueB$ = "oui" THEN joueurB$ = "genou": Boccupe$ = "oui": reftempsB = temps
    END IF

    IF joueurB$ = "assis2" THEN
        assisB$ = "oui"
        xAttB = xB + 4
        xFB = xB + 4: xTB = xB + 4: xMB = xB: xGB = xB
        spriteB$ = "assis2"
        IF attaqueB$ = "oui" THEN joueurB$ = "genou": Boccupe$ = "oui": reftempsB = temps
        IF partie$ = "solo" THEN
            IF temps > reftempsB + 20 THEN Boccupe$ = "non"
            GOTO colision
        END IF
        Boccupe$ = "non"
    END IF

    IF joueurB$ = "releve" THEN
        xAttB = xB + 4: yAttA = 14
        xFB = xB + 4: xTB = xB + 4: xMB = xB: xGB = xB
        spriteB$ = "assis1"
        IF temps > reftempsB + 10 THEN joueurB$ = "debout": Boccupe$ = "non": GOTO colision
        IF attaqueB$ = "oui" THEN joueurB$ = "genou": Boccupe$ = "oui": reftempsB = temps
    END IF


    IF joueurB$ = "assisR" THEN
        xAttB = xB
        xFB = xB: xTB = xB: xMB = xB: xGB = xB + 4
        spriteB$ = "assis1R"
        IF temps > reftemps + 10 THEN joueurB$ = "assis2R": GOTO colision
        IF attaqueB$ = "oui" THEN joueurB$ = "genouR": Boccupe$ = "oui": reftempsB = temps
    END IF

    IF joueurB$ = "assis2R" THEN
        assisB$ = "oui"
        xAttB = xB
        xFB = xB: xTB = xB: xMB = xB + 4: xGB = xB + 4
        spriteB$ = "assis2R"
        IF attaqueB$ = "oui" THEN joueurB$ = "genouR": Boccupe$ = "oui": reftempsB = temps
        IF partie$ = "solo" THEN
            IF temps > reftempsB + 20 THEN Boccupe$ = "non"
            GOTO colision
        END IF
        Boccupe$ = "non"
    END IF

    IF joueurB$ = "releveR" THEN
        xAttB = xB: yAttA = 14
        xFB = xB: xTB = xB: xMB = xB + 4: xGB = xB + 4
        spriteB$ = "assis1R"
        IF temps > reftempsB + 10 THEN joueurB$ = "deboutR": Boccupe$ = "non": GOTO colision
        IF attaqueB$ = "oui" THEN joueurB$ = "genouR": Boccupe$ = "oui": reftempsB = temps
    END IF

    IF joueurB$ = "rouladeAV" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB
        yGB = 20: yAttB = yGB: xAttB = xB + 4
        IF attaqueB$ = "oui" THEN joueurB$ = "coupdepied": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 38 THEN
            spriteB$ = "debout": xTB = xB: xMB = xB:
            Boccupe$ = "non": xB = xB - 1: joueurB$ = "finderoulade": GOTO finderouladeB
        END IF
        IF temps > reftempsB + 33 THEN spriteB$ = "debout": GOTO colision
        IF temps > reftempsB + 31 THEN GOTO colision
        IF temps > reftempsB + 30 THEN xB = xB - 1: spriteB$ = "roulade6": GOTO colision
        IF temps > reftempsB + 29 THEN GOTO colision
        IF temps > reftempsB + 28 THEN xB = xB - 1: spriteB$ = "roulade5": GOTO colision
        IF temps > reftempsB + 26 THEN GOTO colision
        IF temps > reftempsB + 25 THEN xB = xB - 1: spriteB$ = "roulade5": GOTO colision
        IF temps > reftempsB + 23 THEN GOTO colision
        IF temps > reftempsB + 22 THEN xB = xB - 1: spriteB$ = "roulade4": GOTO colision
        IF temps > reftempsB + 20 THEN GOTO colision
        IF temps > reftempsB + 19 THEN xB = xB - 1: spriteB$ = "roulade4": GOTO colision
        IF temps > reftempsB + 17 THEN GOTO colision
        IF temps > reftempsB + 16 THEN xB = xB - 1: xAttB = xB - 1: spriteB$ = "roulade3": GOTO colision
        IF temps > reftempsB + 14 THEN GOTO colision
        IF temps > reftempsB + 13 THEN xB = xB - 1: xAttB = xB - 1: spriteB$ = "roulade3": GOTO colision
        IF temps > reftempsB + 11 THEN GOTO colision
        IF temps > reftempsB + 10 THEN xB = xB - 1: spriteB$ = "roulade2": GOTO colision
        IF temps > reftempsB + 8 THEN GOTO colision
        IF temps > reftempsB + 7 THEN xB = xB - 1: spriteB$ = "roulade2": GOTO colision
        IF temps > reftempsB + 5 THEN GOTO colision
        IF temps > reftempsB + 4 THEN xB = xB - 1: spriteB$ = "roulade1": GOTO colision
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN _SNDPLAY roule: xB = xB - 1: spriteB$ = "roulade1": GOTO colision
    END IF

    finderouladeB:

    IF joueurB$ = "finderoulade" THEN
        IF xB > xA THEN
            joueurB$ = "debout"
            spriteB$ = "debout"
            xAttB = xB + 4: yAttB = 17
            xFB = xB: xTB = xB: xMB = xB: xGB = xB
            yFB = 15: yTB = 16: yMB = 18: yGB = 20
            GOTO colision
        END IF
        IF xB < xA + 1 THEN
            joueurA$ = "retourne": yAttA = 14: Aoccupe$ = "oui": reftemps = temps
            joueurB$ = "retourne": yAttB = 14: Boccupe$ = "oui": reftempsB = temps
            GOTO affichage
        END IF
    END IF

    IF joueurB$ = "rouladeAVR" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB + 4
        yGB = 20: yAttB = yGB: xAttB = xB
        IF attaqueB$ = "oui" THEN joueurB$ = "coupdepiedR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 38 THEN
            spriteB$ = "deboutR": xTB = xB + 4: xMB = xB + 4:
            Boccupe$ = "non": xB = xB + 1: joueurB$ = "finderouladeR": GOTO finderouladeBR
        END IF
        IF temps > reftempsB + 33 THEN spriteB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 31 THEN GOTO colision
        IF temps > reftempsB + 30 THEN xB = xB + 1: spriteB$ = "roulade6R": GOTO colision
        IF temps > reftempsB + 29 THEN GOTO colision
        IF temps > reftempsB + 28 THEN xB = xB + 1: spriteB$ = "roulade5R": GOTO colision
        IF temps > reftempsB + 26 THEN GOTO colision
        IF temps > reftempsB + 25 THEN xB = xB + 1: spriteB$ = "roulade5R": GOTO colision
        IF temps > reftempsB + 23 THEN GOTO colision
        IF temps > reftempsB + 22 THEN xB = xB + 1: spriteB$ = "roulade4R": GOTO colision
        IF temps > reftempsB + 20 THEN GOTO colision
        IF temps > reftempsB + 19 THEN xB = xB + 1: spriteB$ = "roulade4R": GOTO colision
        IF temps > reftempsB + 17 THEN GOTO colision
        IF temps > reftempsB + 16 THEN xB = xB + 1: xAttB = xB + 5: spriteB$ = "roulade3R": GOTO colision
        IF temps > reftempsB + 14 THEN GOTO colision
        IF temps > reftempsB + 13 THEN xB = xB + 1: xAttB = xB + 5: spriteB$ = "roulade3R": GOTO colision
        IF temps > reftempsB + 11 THEN GOTO colision
        IF temps > reftempsB + 10 THEN xB = xB + 1: spriteB$ = "roulade2R": GOTO colision
        IF temps > reftempsB + 8 THEN GOTO colision
        IF temps > reftempsB + 7 THEN xB = xB + 1: spriteB$ = "roulade2R": GOTO colision
        IF temps > reftempsB + 5 THEN GOTO colision
        IF temps > reftempsB + 4 THEN xB = xB + 1: spriteB$ = "roulade1R": GOTO colision
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN _SNDPLAY roule: xB = xB + 1: spriteB$ = "roulade1R": GOTO colision
    END IF

    finderouladeBR:

    IF joueurB$ = "finderouladeR" THEN
        IF xB < xA THEN
            joueurB$ = "deboutR"
            spriteB$ = "deboutR"
            xAttB = xB: yAttB = 17
            xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
            yFB = 15: yTB = 16: yMB = 18: yGB = 20
            GOTO colision
        END IF
        IF xB > xA - 1 THEN
            joueurA$ = "retourneR": Aoccupe$ = "oui": reftemps = temps
            joueurB$ = "retourneR": Boccupe$ = "oui": reftempsB = temps
            GOTO affichage
        END IF
    END IF

    IF joueurB$ = "rouladeAR" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB
        yGB = 20: yAttB = yGB: xAttB = xB + 4
        IF attaqueB$ = "oui" THEN joueurB$ = "front": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 38 THEN
            spriteB$ = "debout": xTB = xB: xMB = xB:
            Boccupe$ = "non": joueurB$ = "debout": GOTO colision
        END IF
        IF temps > reftempsB + 33 THEN spriteB$ = "debout": GOTO colision
        IF temps > reftempsB + 30 THEN GOTO colision
        IF temps > reftempsB + 29 THEN xB = xB + 1: spriteB$ = "roulade1": GOTO colision
        IF temps > reftempsB + 27 THEN GOTO colision
        IF temps > reftempsB + 26 THEN xB = xB + 1: spriteB$ = "roulade1": GOTO colision
        IF temps > reftempsB + 24 THEN GOTO colision
        IF temps > reftempsB + 23 THEN xB = xB + 1: spriteB$ = "roulade2": GOTO colision
        IF temps > reftempsB + 21 THEN GOTO colision
        IF temps > reftempsB + 20 THEN xB = xB + 1: spriteB$ = "roulade2": GOTO colision
        IF temps > reftempsB + 18 THEN GOTO colision
        IF temps > reftempsB + 17 THEN xB = xB + 1: spriteB$ = "roulade3": GOTO colision
        IF temps > reftempsB + 15 THEN GOTO colision
        IF temps > reftempsB + 14 THEN xB = xB + 1: spriteB$ = "roulade3": GOTO colision
        IF temps > reftempsB + 12 THEN GOTO colision
        IF temps > reftempsB + 11 THEN xB = xB + 1: spriteB$ = "roulade4": GOTO colision
        IF temps > reftempsB + 9 THEN GOTO colision
        IF temps > reftempsB + 8 THEN xB = xB + 1: spriteB$ = "roulade4": GOTO colision
        IF temps > reftempsB + 6 THEN GOTO colision
        IF temps > reftempsB + 5 THEN xB = xB + 1: spriteB$ = "roulade5": GOTO colision
        IF temps > reftempsB + 3 THEN GOTO colision
        IF temps > reftempsB + 2 THEN xB = xB + 1: spriteB$ = "roulade6": GOTO colision
        IF temps > reftempsB + 1 THEN _SNDPLAY roule: spriteB$ = "roulade6": GOTO colision
    END IF

    IF joueurB$ = "rouladeARR" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB + 4
        yGB = 20: yAttB = yGB: xAttB = xB
        IF attaqueB$ = "oui" THEN joueurB$ = "frontR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 38 THEN
            spriteB$ = "deboutR": xTB = xB + 4: xMB = xB + 4:
            Boccupe$ = "non": joueurB$ = "deboutR": GOTO colision
        END IF
        IF temps > reftempsB + 33 THEN spriteB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 30 THEN GOTO colision
        IF temps > reftempsB + 29 THEN xB = xB - 1: spriteB$ = "roulade1R": GOTO colision
        IF temps > reftempsB + 27 THEN GOTO colision
        IF temps > reftempsB + 26 THEN xB = xB - 1: spriteB$ = "roulade1R": GOTO colision
        IF temps > reftempsB + 24 THEN GOTO colision
        IF temps > reftempsB + 23 THEN xB = xB - 1: spriteB$ = "roulade2R": GOTO colision
        IF temps > reftempsB + 21 THEN GOTO colision
        IF temps > reftempsB + 20 THEN xB = xB - 1: spriteB$ = "roulade2R": GOTO colision
        IF temps > reftempsB + 18 THEN GOTO colision
        IF temps > reftempsB + 17 THEN xB = xB - 1: spriteB$ = "roulade3R": GOTO colision
        IF temps > reftempsB + 15 THEN GOTO colision
        IF temps > reftempsB + 14 THEN xB = xB - 1: spriteB$ = "roulade3R": GOTO colision
        IF temps > reftempsB + 12 THEN GOTO colision
        IF temps > reftempsB + 11 THEN xB = xB - 1: spriteB$ = "roulade4R": GOTO colision
        IF temps > reftempsB + 9 THEN GOTO colision
        IF temps > reftempsB + 8 THEN xB = xB - 1: spriteB$ = "roulade4R": GOTO colision
        IF temps > reftempsB + 6 THEN GOTO colision
        IF temps > reftempsB + 5 THEN xB = xB - 1: spriteB$ = "roulade5R": GOTO colision
        IF temps > reftempsB + 3 THEN GOTO colision
        IF temps > reftempsB + 2 THEN xB = xB - 1: spriteB$ = "roulade6R": GOTO colision
        IF temps > reftempsB + 1 THEN _SNDPLAY roule: spriteB$ = "roulade6R": GOTO colision
    END IF

    IF joueurB$ = "protegeH1" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        yGB = 20
        IF attaqueB$ = "oui" THEN joueurB$ = "araignee": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 5 THEN protegeHB$ = "oui": joueurB$ = "protegeH": Boccupe$ = "non": GOTO colision
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN _SNDPLAY protege: xB = xB + 1: spriteB$ = "marche1": GOTO colision
    END IF

    IF joueurB$ = "protegeH" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        xAttB = xB + 4
        yGB = 20
        spriteB$ = "protegeH"
        IF attaqueB$ = "oui" THEN joueurB$ = "araignee": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
    END IF

    IF joueurB$ = "protegeHR1" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        xAttB = xB
        yGB = 20
        IF attaqueB$ = "oui" THEN joueurB$ = "araigneeR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 5 THEN protegeHB$ = "oui": joueurB$ = "protegeHR": Boccupe$ = "non": GOTO colision
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN _SNDPLAY protege: xB = xB - 1: spriteB$ = "marche1R": GOTO colision
    END IF

    IF joueurB$ = "protegeHR" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        xAttB = xB
        yGB = 20
        spriteB$ = "protegeHR"
        IF attaqueB$ = "oui" THEN joueurB$ = "araigneeR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
    END IF

    IF joueurB$ = "protegeD1" THEN
        xAttB = xB + 4
        yGB = 20
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        decapiteB$ = "non"
        spriteB$ = "protegeH"
        IF attaqueB$ = "oui" THEN joueurB$ = "coupdetete": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 5 THEN joueurB$ = "protegeD": protegeDB$ = "oui": Boccupe$ = "non"
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN _SNDPLAY protege
    END IF

    IF joueurB$ = "protegeD" THEN
        xAttB = xB + 4
        yGB = 20
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        decapiteB$ = "non"
        spriteB$ = "protegeD"
        IF attaqueB$ = "oui" THEN joueurB$ = "coupdetete": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
    END IF

    IF joueurB$ = "protegeDR1" THEN
        xAttB = xB
        yGB = 20
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        decapiteB$ = "non"
        spriteB$ = "protegeHR"
        IF attaqueB$ = "oui" THEN joueurB$ = "coupdeteteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
        IF temps > reftempsB + 5 THEN joueurB$ = "protegeDR": protegeDB$ = "oui": Boccupe$ = "non"
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN _SNDPLAY protege
    END IF

    IF joueurB$ = "protegeDR" THEN
        xAttB = xB
        yGB = 20
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        decapiteB$ = "non"
        spriteB$ = "protegeDR"
        IF attaqueB$ = "oui" THEN joueurB$ = "coupdeteteR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
    END IF

    IF joueurB$ = "cou" THEN '****attention au temps sinon il saute
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        yGB = 20
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": joueurB$ = "debout": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "cou2": xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 31 THEN xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 30 THEN
            spriteB$ = "cou3"
            IF joueurA$ = "cou" THEN GOTO colision
            xTB = xB + 4: xAttB = xB - 3: GOTO colision
        END IF
        IF temps > reftempsB + 16 THEN GOTO colision
        IF temps > reftempsB + 15 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "cou2": yAttB = yTB: GOTO colision
        END IF
        IF temps > reftempsB + 3 THEN spriteB$ = "cou1": GOTO colision
    END IF

    IF joueurB$ = "couR" THEN '****attention au temps sinon il saute
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        yGB = 20
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": joueurB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "cou2R": xAttB = xB: GOTO colision
        IF temps > reftempsB + 31 THEN xAttB = xB: GOTO colision
        IF temps > reftempsB + 30 THEN
            spriteB$ = "cou3R"
            IF joueurA$ = "couR" THEN GOTO colision
            xTB = xB: xAttB = xB + 7: GOTO colision
        END IF
        IF temps > reftempsB + 16 THEN GOTO colision
        IF temps > reftempsB + 15 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "cou2R": yAttB = yTB: GOTO colision
        END IF
        IF temps > reftempsB + 3 THEN spriteB$ = "cou1R": GOTO colision
    END IF

    IF joueurB$ = "devant" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        yGB = 20
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": joueurB$ = "debout": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "devant2": GOTO colision
        IF temps > reftempsB + 21 THEN spriteB$ = "devant3": xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 20 THEN
            spriteB$ = "devant3"
            IF joueurA$ = "devant" THEN GOTO colision
            xMB = xB + 4: xAttB = xB - 2: GOTO colision
        END IF
        IF temps > reftempsB + 11 THEN GOTO colision
        IF temps > reftempsB + 10 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "devant2": yAttB = yMB
        END IF
        spriteB$ = "devant1"
    END IF

    IF joueurB$ = "devantR" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        yGB = 20
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": joueurB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "devant2R": GOTO colision
        IF temps > reftempsB + 21 THEN spriteB$ = "devant3R": xAttB = xB: GOTO colision
        IF temps > reftempsB + 20 THEN
            spriteB$ = "devant3R"
            IF joueurA$ = "devantR" THEN GOTO colision
            xMB = xB: xAttB = xB + 6: GOTO colision
        END IF
        IF temps > reftempsB + 11 THEN GOTO colision
        IF temps > reftempsB + 10 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "devant2R": yAttB = yMB: GOTO colision
        END IF
        spriteB$ = "devant1R"
    END IF

    IF joueurB$ = "genou" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB
        yGB = 20
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": joueurB$ = "assis2": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "genou2": GOTO colision
        IF temps > reftempsB + 21 THEN spriteB$ = "genou3": xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 20 THEN
            spriteB$ = "genou3"
            IF joueurA$ = "genou" THEN GOTO colision
            xGB = xB + 4: xAttB = xB - 3: GOTO colision
        END IF
        IF temps > reftempsB + 11 THEN GOTO colision
        IF temps > reftempsB + 10 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "genou2": yAttB = yGB: GOTO colision
        END IF
        spriteB$ = "genou1"
    END IF

    IF joueurB$ = "genouR" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB + 4
        yGB = 20
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": joueurB$ = "assis2R": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "genou2R": GOTO colision
        IF temps > reftempsB + 21 THEN spriteB$ = "genou3R": xAttB = xB: GOTO colision
        IF temps > reftempsB + 20 THEN
            spriteB$ = "genou3R"
            IF joueurA$ = "genouR" THEN GOTO colision
            xGB = xB: xAttB = xB + 7: GOTO colision
        END IF
        IF temps > reftempsB + 11 THEN GOTO colision
        IF temps > reftempsB + 10 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "genou2R": yAttB = yGB: GOTO colision
        END IF
        spriteB$ = "genou1R"
    END IF

    IF joueurB$ = "araignee" THEN
        xFB = xB: xTB = xB: xMB = xB + 4: xGB = xB
        yAttB = yGB: xAttB = xB + 4: yGB = 20
        IF temps > reftempsB + 24 THEN Boccupe$ = "non": joueurB$ = "debout": GOTO colision
        IF temps > reftempsB + 19 THEN xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 18 THEN
            _SNDPLAY epee
            spriteB$ = "toile4"
            IF joueurA$ = "araignee" THEN GOTO colision
            xAttB = xB - 1: GOTO colision
        END IF
        IF temps > reftempsB + 13 THEN GOTO colision
        IF temps > reftempsB + 12 THEN spriteB$ = "toile3": xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 7 THEN GOTO colision
        IF temps > reftempsB + 6 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "toile2": xAttB = xB + 4: GOTO colision
        END IF
        spriteB$ = "toile1"
    END IF

    IF joueurB$ = "araigneeR" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB: xGB = xB + 4
        yAttB = yGB: xAttB = xB: yGB = 20
        IF temps > reftempsB + 24 THEN Boccupe$ = "non": joueurB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 19 THEN xAttB = xB: GOTO colision
        IF temps > reftempsB + 18 THEN
            _SNDPLAY epee
            spriteB$ = "toile4R"
            IF joueurA$ = "araigneeR" THEN GOTO colision
            xAttB = xB + 5: GOTO colision
        END IF
        IF temps > reftempsB + 13 THEN GOTO colision
        IF temps > reftempsB + 12 THEN spriteB$ = "toile3R": xAttB = xB: GOTO colision
        IF temps > reftempsB + 7 THEN GOTO colision
        IF temps > reftempsB + 6 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "toile2R": xAttB = xB: GOTO colision
        END IF
        spriteB$ = "toile1R"
    END IF

    IF joueurB$ = "coupdepied" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        spriteB$ = "pied1": yAttB = yGB: yGB = 20
        IF temps > reftempsB + 15 THEN spriteB$ = "pied2": xAttB = xB - 1
        IF temps > reftempsB + 16 THEN spriteB$ = "pied2": xAttB = xB + 4
        IF temps > reftempsB + 30 THEN spriteB$ = "pied1"
        IF temps > reftempsB + 45 THEN spriteB$ = "debout"
        IF temps > reftempsB + 50 THEN Boccupe$ = "non": joueurB$ = "debout"
    END IF

    IF joueurB$ = "coupdepiedR" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        spriteB$ = "pied1R": yAttB = yGB: yGB = 20
        IF temps > reftempsB + 15 THEN spriteB$ = "pied2R": xAttB = xB + 5
        IF temps > reftempsB + 16 THEN spriteB$ = "pied2R": xAttB = xB
        IF temps > reftempsB + 30 THEN spriteB$ = "pied1R"
        IF temps > reftempsB + 45 THEN spriteB$ = "deboutR"
        IF temps > reftempsB + 50 THEN Boccupe$ = "non": joueurB$ = "deboutR"
    END IF

    IF joueurB$ = "coupdetete" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        yGB = 20
        IF temps > reftempsB + 37 THEN Boccupe$ = "non": spriteB$ = "debout": joueurB$ = "debout": GOTO colision
        IF temps > reftempsB + 29 THEN GOTO colision
        IF temps > reftempsB + 28 THEN xB = xB + 1: spriteB$ = "tete1": GOTO colision
        IF temps > reftempsB + 20 THEN xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 19 THEN spriteB$ = "tete2": xAttB = xB: GOTO colision
        IF temps > reftempsB + 18 THEN xB = xB - 1: spriteB$ = "tete2": xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 9 THEN spriteB$ = "tete1": yAttB = yTB: GOTO colision
        IF temps > reftempsB + 1 THEN spriteB$ = "tete1"
    END IF

    IF joueurB$ = "coupdeteteR" THEN
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        yGB = 20
        IF temps > reftempsB + 37 THEN Boccupe$ = "non": spriteB$ = "deboutR": joueurB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 29 THEN GOTO colision
        IF temps > reftempsB + 28 THEN xB = xB - 1: spriteB$ = "tete1R": xAttB = xB: GOTO colision
        IF temps > reftempsB + 20 THEN xAttB = xB: GOTO colision
        IF temps > reftempsB + 19 THEN spriteB$ = "tete2R": xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 18 THEN xB = xB + 1: spriteB$ = "tete2R": xAttB = xB: GOTO colision
        IF temps > reftempsB + 9 THEN spriteB$ = "tete1R": yAttB = yTB: GOTO colision
        IF temps > reftempsB + 1 THEN spriteB$ = "tete1R"
    END IF

    IF joueurB$ = "decapite" THEN
        decapiteB$ = "non"
        xFB = xB + 1: xTB = xB + 2: xMB = xB + 2: xGB = xB
        IF temps > reftempsB + 58 THEN Boccupe$ = "non": spriteB$ = "debout": joueurB$ = "debout": GOTO colision
        IF temps > reftempsB + 51 THEN spriteB$ = "cou2": xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 50 THEN spriteB$ = "cou3": xTB = xB + 4: xAttB = xB - 2: GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "cou3": yAttB = yTB: GOTO colision
        IF temps > reftempsB + 35 THEN spriteB$ = "cou2": yAttB = yTB: GOTO colision
        IF temps > reftempsB + 30 THEN spriteB$ = "cou1": yAttB = yTB: GOTO colision
        IF temps > reftempsB + 25 THEN GOTO colision
        IF temps > reftempsB + 24 THEN xB = xB - 1: GOTO colision
        IF temps > reftempsB + 20 THEN spriteB$ = "retourne3": GOTO colision
        IF temps > reftempsB + 19 THEN xB = xB - 1: GOTO colision
        IF temps > reftempsB + 15 THEN spriteB$ = "retourne3": GOTO colision
        IF temps > reftempsB + 14 THEN _SNDPLAY decapite: xB = xB - 1: GOTO colision
        IF temps > reftempsB + 10 THEN spriteB$ = "retourne2": GOTO colision
        IF temps > reftempsB + 9 THEN xB = xB - 1: GOTO colision
        IF temps > reftempsB + 5 THEN spriteB$ = "retourne2": GOTO colision
        IF temps > reftempsB + 4 THEN xB = xB - 1: GOTO colision
        IF temps > reftempsB + 2 THEN spriteB$ = "retourne1": GOTO colision
        IF temps > reftempsB + 1 THEN xB = xB - 1: spriteB$ = "retourne1": GOTO colision
    END IF

    IF joueurB$ = "decapiteR" THEN
        decapiteB$ = "non"
        xFB = xB + 3: xTB = xB + 2: xMB = xB + 2: xGB = xB + 4
        IF temps > reftempsB + 58 THEN Boccupe$ = "non": spriteB$ = "deboutR": joueurB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 51 THEN spriteB$ = "cou2R": xAttB = xB: GOTO colision
        IF temps > reftempsB + 50 THEN spriteB$ = "cou3R": xTB = xB: xAttB = xB + 6: GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "cou3R": yAttB = yTB: GOTO colision
        IF temps > reftempsB + 35 THEN spriteB$ = "cou2R": yAttB = yTB: GOTO colision
        IF temps > reftempsB + 30 THEN spriteB$ = "cou1R": yAttB = yTB: GOTO colision
        IF temps > reftempsB + 25 THEN GOTO colision
        IF temps > reftempsB + 24 THEN xB = xB + 1: GOTO colision
        IF temps > reftempsB + 20 THEN spriteB$ = "retourne3R": GOTO colision
        IF temps > reftempsB + 19 THEN xB = xB + 1: GOTO colision
        IF temps > reftempsB + 15 THEN spriteB$ = "retourne3R": GOTO colision
        IF temps > reftempsB + 14 THEN _SNDPLAY decapite: xB = xB + 1: GOTO colision
        IF temps > reftempsB + 10 THEN spriteB$ = "retourne2R": GOTO colision
        IF temps > reftempsB + 9 THEN xB = xB + 1: GOTO colision
        IF temps > reftempsB + 5 THEN spriteB$ = "retourne2R": GOTO colision
        IF temps > reftempsB + 4 THEN xB = xB + 1: GOTO colision
        IF temps > reftempsB + 2 THEN spriteB$ = "retourne1R": GOTO colision
        IF temps > reftempsB + 1 THEN xB = xB + 1: spriteB$ = "retourne1R": GOTO colision
    END IF

    IF joueurB$ = "front" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        yGB = 20
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": joueurB$ = "debout": GOTO colision
        IF temps > reftempsB + 35 THEN spriteB$ = "front2": GOTO colision
        IF temps > reftempsB + 24 THEN spriteB$ = "front3": xAttB = xB + 4: GOTO colision
        IF temps > reftempsB + 23 THEN
            spriteB$ = "front3"
            IF joueurA$ = "front" THEN GOTO colision
            xFB = xB + 4: xAttB = xB - 3: GOTO colision
        END IF
        IF temps > reftempsB + 6 THEN GOTO colision
        IF temps > reftempsB + 5 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "front2": yAttB = yFB: GOTO colision
        END IF
        IF temps > reftempsB + 3 THEN spriteB$ = "front1": GOTO colision
    END IF

    IF joueurB$ = "frontR" THEN
        yGB = 20
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        IF temps > reftempsB + 45 THEN Boccupe$ = "non": joueurB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 35 THEN spriteB$ = "front2R": GOTO colision
        IF temps > reftempsB + 24 THEN spriteB$ = "front3R": xAttB = xB: GOTO colision
        IF temps > reftempsB + 23 THEN
            spriteB$ = "front3R"
            IF joueurA$ = "frontR" THEN GOTO colision
            xFB = xB: xAttB = xB + 7: GOTO colision
        END IF
        IF temps > reftempsB + 6 THEN GOTO colision
        IF temps > reftempsB + 5 THEN
            songrogne = songrogne + 1
            IF songrogne > 6 THEN songrogne = 0
            IF songrogne = 3 THEN _SNDPLAY grogne1
            IF songrogne = 6 THEN _SNDPLAY grogne2
            _SNDPLAY epee: spriteB$ = "front2R": yAttB = yFB: GOTO colision
        END IF
        IF temps > reftempsB + 3 THEN spriteB$ = "front1R": GOTO colision
    END IF

    IF joueurB$ = "retourne" THEN
        xAttB = xB + 4: xFB = xB: xTB = xB: xMB = xB: xGB = xB
        yAttB = 14:
        spriteB$ = "retourne1"
        IF temps > reftempsB + 5 THEN spriteB$ = "retourne2"
        IF temps > reftempsB + 10 THEN spriteB$ = "retourne3"
        IF temps > reftempsB + 15 THEN joueurB$ = "deboutR": Boccupe$ = "non": sens$ = "inverse"
    END IF

    IF joueurB$ = "retourneR" THEN
        xAttB = xB: xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        yAttB = 14:
        spriteB$ = "retourne1R"
        IF temps > reftempsB + 5 THEN spriteB$ = "retourne2R"
        IF temps > reftempsB + 10 THEN spriteB$ = "retourne3R"
        IF temps > reftempsB + 15 THEN joueurB$ = "debout": Boccupe$ = "non": sens$ = "normal"
    END IF

    IF joueurB$ = "vainqueur" THEN
        spriteB$ = "vainqueur1"
        decapiteB$ = "oui"
        sangB$ = "non"
        xAttB = xB + 4: yAttB = 14: yGB = 20
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        IF temps > reftempsB + 18 THEN spriteB$ = "vainqueur2"
        IF temps > reftempsB + 35 THEN spriteB$ = "vainqueur3"
        IF temps > reftempsB + 85 THEN spriteB$ = "vainqueur2"
        IF temps > reftempsB + 100 THEN spriteB$ = "vainqueur1"
    END IF

    IF joueurB$ = "vainqueurR" THEN
        spriteB$ = "vainqueur1R"
        decapiteB$ = "oui"
        sangB$ = "non"
        xAttB = xB: yAttB = 14: yGB = 20
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        IF temps > reftempsB + 18 THEN spriteB$ = "vainqueur2R"
        IF temps > reftempsB + 35 THEN spriteB$ = "vainqueur3R"
        IF temps > reftempsB + 85 THEN spriteB$ = "vainqueur2R"
        IF temps > reftempsB + 100 THEN spriteB$ = "vainqueur1R"
    END IF

    IF joueurB$ = "vainqueurKO" THEN
        decapiteB$ = "oui"
        sangB$ = "non"
        xAttB = xB + 4: yGB = 20: 'yAttB = 14:
        xFB = xB: xTB = xB: xMB = xB: xGB = xB

        IF temps > reftemps + 230 THEN
            gnome$ = "oui": reftemps = temps
            xGNOME = 1
            xSPRt = 270
            GOTO affichage
        END IF

        IF temps > reftempsB + 205 THEN spriteB$ = "vainqueur1": GOTO colision
        IF temps > reftempsB + 195 THEN spriteB$ = "vainqueur2": GOTO colision
        IF temps > reftempsB + 140 THEN spriteB$ = "vainqueur3": GOTO colision
        IF temps > reftempsB + 123 THEN spriteB$ = "vainqueur2": GOTO colision
        IF temps > reftempsB + 105 THEN spriteB$ = "vainqueur1": GOTO colision
        IF temps > reftempsB + 100 THEN spriteB$ = "debout": GOTO colision
        IF temps > reftempsB + 75 THEN spriteB$ = "pied1": spriteA$ = "mort4": GOTO colision
        IF temps > reftempsB + 71 THEN GOTO colision
        IF temps > reftempsB + 70 THEN
            spriteB$ = "pied2": spriteA$ = "mort3": xA = xA - 2: GOTO colision
        END IF
        IF temps > reftempsB + 55 THEN spriteB$ = "pied1": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "debout": GOTO colision
        IF temps > reftempsB + 36 THEN GOTO colision
        IF temps > reftempsB + 35 THEN
            distance = xB - xA
            IF distance < 5 THEN spriteB$ = "marche3": xB = xB + 1
            IF distance > 5 THEN spriteB$ = "marche3": xB = xB - 1
            GOTO colision
        END IF
        IF temps > reftempsB + 30 THEN spriteB$ = "debout": GOTO colision
        IF temps > reftempsB + 23 THEN spriteB$ = "retourne3": GOTO colision
        IF temps > reftempsB + 15 THEN spriteB$ = "retourne2": GOTO colision
        IF temps > reftempsB + 8 THEN spriteB$ = "retourne1"
    END IF

    IF joueurB$ = "vainqueurKOR" THEN
        decapiteB$ = "oui"
        sangB$ = "non"
        xAttB = xB: yGB = 20: ' yAttB = 14
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4

        IF temps > reftemps + 230 THEN
            gnome$ = "oui": reftemps = temps
            xGNOME = 1
            xSPRt = 270
            GOTO affichage
        END IF

        IF temps > reftempsB + 205 THEN spriteB$ = "vainqueur1R": GOTO colision
        IF temps > reftempsB + 190 THEN spriteB$ = "vainqueur2R": GOTO colision
        IF temps > reftempsB + 140 THEN spriteB$ = "vainqueur3R": GOTO colision
        IF temps > reftempsB + 123 THEN spriteB$ = "vainqueur2R": GOTO colision
        IF temps > reftempsB + 105 THEN spriteB$ = "vainqueur1R": GOTO colision
        IF temps > reftempsB + 100 THEN spriteB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 75 THEN spriteB$ = "pied1R": spriteA$ = "mort4R": GOTO colision
        IF temps > reftempsB + 71 THEN GOTO colision
        IF temps > reftempsB + 70 THEN
            spriteB$ = "pied2R": spriteA$ = "mort3R": xA = xA + 2: GOTO colision
        END IF
        IF temps > reftempsB + 55 THEN spriteB$ = "pied1R": GOTO colision
        IF temps > reftempsB + 40 THEN spriteB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 36 THEN GOTO colision
        IF temps > reftempsB + 35 THEN
            distance = xA - xB
            IF distance < 5 THEN spriteB$ = "marche3R": xB = xB - 1
            IF distance > 5 THEN spriteB$ = "marche3R": xB = xB + 1
            GOTO colision
        END IF
        IF temps > reftempsB + 30 THEN spriteB$ = "deboutR": GOTO colision
        IF temps > reftempsB + 23 THEN spriteB$ = "retourne3R": GOTO colision
        IF temps > reftempsB + 15 THEN spriteB$ = "retourne2R": GOTO colision
        IF temps > reftempsB + 8 THEN spriteB$ = "retourne1R"
    END IF


    '                               ******degats B ******
    IF joueurB$ = "touche" THEN
        attenteB = 0
        xAttB = xB + 4
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        yFB = 15: yTB = 16: yMB = 18: yGB = 20
        IF joueurA$ = "coupdepied" THEN joueurB$ = "tombe": GOTO gestionB


        sangB$ = "oui"
        serpentB$ = "oui"

        IF joueurA$ = "decapite" AND decapiteB$ = "oui" THEN
            joueurB$ = "mortdecap": Boccupe$ = "oui": reftempsB = temps
            xSPRt = xB + 3: scoreA = scoreA + 250
            sangB$ = "non": GOTO mortB
        END IF

        vieB = vieB - 1
        IF vieB <= 0 THEN
            joueurB$ = "mort": Boccupe$ = "oui": reftempsB = temps: sangB$ = "oui": GOTO mortB
        END IF

        sontouche = sontouche + 1
        IF sontouche > 3 THEN sontouche = 1
        IF sontouche = 1 THEN _SNDPLAY touche
        IF sontouche = 2 THEN _SNDPLAY touche2
        IF sontouche = 3 THEN _SNDPLAY touche3


        joueurB$ = "touche1": Boccupe$ = "oui": reftempsB = temps: decapiteB$ = "oui"
        GOTO colision

    END IF

    IF joueurB$ = "touche1" THEN
        IF temps > reftempsB + 20 THEN
            spriteB$ = "debout": Boccupe$ = "non"
            joueurB$ = "debout": GOTO colision
        END IF
        IF temps > reftempsB + 15 THEN spriteB$ = "touche4": GOTO colision ' pour serpent
        IF temps > reftempsB + 11 THEN GOTO colision
        IF temps > reftempsB + 10 THEN xB = xB + 1: sangB$ = "non": spriteB$ = "touche3": GOTO colision
        IF temps > reftempsB + 6 THEN GOTO colision
        IF temps > reftempsB + 5 THEN xB = xB + 2: spriteB$ = "touche2": GOTO colision
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN xB = xB + 1: spriteB$ = "touche1": GOTO colision
        spriteB$ = "touche1"
    END IF

    IF joueurB$ = "toucheR" THEN
        attenteB = 0
        xAttB = xB
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        yFB = 15: yTB = 16: yMB = 18: yGB = 20
        IF joueurA$ = "coupdepiedR" THEN joueurB$ = "tombeR": GOTO gestionB

        sangB$ = "oui"
        serpentB$ = "oui"

        IF joueurA$ = "decapiteR" AND decapiteB$ = "oui" THEN
            joueurB$ = "mortdecapR": Boccupe$ = "oui": reftempsB = temps
            xSPRt = xB + 3: scoreA = scoreA + 250
            sangB$ = "non": GOTO mortB
        END IF

        vieB = vieB - 1
        IF vieB <= 0 THEN
            joueurB$ = "mortR": Boccupe$ = "oui": reftempsB = temps: sangB$ = "oui": GOTO mortB
        END IF

        sontouche = sontouche + 1
        IF sontouche > 3 THEN sontouche = 1
        IF sontouche = 1 THEN _SNDPLAY touche
        IF sontouche = 2 THEN _SNDPLAY touche2
        IF sontouche = 3 THEN _SNDPLAY touche3


        joueurB$ = "touche1R": Boccupe$ = "oui": reftempsB = temps: decapiteB$ = "oui"
        GOTO colision
    END IF

    IF joueurB$ = "touche1R" THEN
        IF temps > reftempsB + 20 THEN
            spriteB$ = "deboutR": Boccupe$ = "non"
            joueurB$ = "deboutR": GOTO colision
        END IF
        IF temps > reftempsB + 15 THEN spriteB$ = "touche4R": GOTO colision ' pour serpent
        IF temps > reftempsB + 11 THEN GOTO colision
        IF temps > reftempsB + 10 THEN xB = xB - 1: sangB$ = "non": spriteB$ = "touche3R": GOTO colision
        IF temps > reftempsB + 6 THEN GOTO colision
        IF temps > reftempsB + 5 THEN xB = xB - 2: spriteB$ = "touche2R": GOTO colision
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN xB = xB - 1: spriteB$ = "touche1R": GOTO colision
        spriteB$ = "touche1R"
    END IF

    IF joueurB$ = "tombe" THEN
        attenteB = 0
        xAttB = xB + 4
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        yFB = 15: yTB = 16: yMB = 18: yGB = 20
        sangB$ = "oui"
        serpentB$ = "oui"

        vieB = vieB - 1: scoreA = scoreA + 100
        IF joueurA$ = "rouladeAV" THEN vieB = vieB + 1: sangB$ = "non": serpentB$ = "non": scoreA = scoreA - 100
        IF vieB <= 0 THEN
            joueurB$ = "mort": Boccupe$ = "oui": reftempsB = temps: sangB$ = "oui"
            IF joueurA$ = "coupdetete" OR joueurA$ = "coupdepied" THEN sangB$ = "non"
            GOTO mortB
        END IF

        IF joueurA$ = "coupdetete" THEN scoreA = scoreA + 150: sangB$ = "non": _SNDPLAY coupdetete

        IF joueurA$ = "coupdepied" THEN scoreA = scoreA + 150: sangB$ = "non": _SNDPLAY coupdepied

        joueurB$ = "tombe1": Boccupe$ = "oui": reftempsB = temps
        GOTO colision
    END IF

    IF joueurB$ = "tombe1" THEN
        attenteB = 0
        xAttB = xB + 4
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4
        IF temps > reftempsB + 25 THEN
            spriteB$ = "debout": xB = xB + 1: joueurB$ = "debout": Boccupe$ = "non":
            GOTO colision
        END IF
        IF temps > reftempsB + 20 THEN spriteB$ = "tombe4": GOTO colision
        IF temps > reftempsB + 15 THEN spriteB$ = "tombe3": GOTO colision
        IF temps > reftempsB + 10 THEN GOTO colision
        IF temps > reftempsB + 9 THEN sangB$ = "non": xB = xB + 2: spriteB$ = "tombe2": GOTO colision
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN
            _SNDPLAY tombe
            IF joueurA$ = "coupdetete" THEN _SNDSTOP tombe
            xB = xB + 2: GOTO colision
        END IF
        spriteB$ = "tombe1"
    END IF

    IF joueurB$ = "tombeR" THEN
        xAttB = xB
        attenteB = 0
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        yFB = 15: yTB = 16: yMB = 18: yGB = 20
        sangB$ = "oui"
        serpentB$ = "oui"

        vieB = vieB - 1: scoreA = scoreA + 100
        IF joueurA$ = "rouladeAVR" THEN vieB = vieB + 1: sangB$ = "non": serpentB$ = "non": scoreA = scoreA - 100
        IF vieB <= 0 THEN
            joueurB$ = "mortR": Boccupe$ = "oui": reftempsB = temps: sangB$ = "oui"
            IF joueurA$ = "coupdeteteR" OR joueurA$ = "coupdepiedR" THEN sangB$ = "non"
            GOTO mortB
        END IF

        IF joueurA$ = "coupdeteteR" THEN scoreA = scoreA + 150: sangB$ = "non": _SNDPLAY coupdetete

        IF joueurA$ = "coupdepiedR" THEN scoreA = scoreA + 150: sangB$ = "non": _SNDPLAY coupdepied

        joueurB$ = "tombe1R": Boccupe$ = "oui": reftempsB = temps
        GOTO colision
    END IF

    IF joueurB$ = "tombe1R" THEN
        xAttB = xB
        attenteB = 0
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        IF temps > reftempsB + 25 THEN
            spriteB$ = "deboutR": xB = xB - 1: joueurB$ = "deboutR": Boccupe$ = "non": GOTO colision
        END IF
        IF temps > reftempsB + 20 THEN spriteB$ = "tombe4R": GOTO colision
        IF temps > reftempsB + 25 THEN spriteB$ = "tombe3R": GOTO colision
        IF temps > reftempsB + 10 THEN GOTO colision
        IF temps > reftempsB + 9 THEN sangB$ = "non": xB = xB - 2: spriteB$ = "tombe2R": GOTO colision
        IF temps > reftempsB + 2 THEN GOTO colision
        IF temps > reftempsB + 1 THEN
            _SNDPLAY tombe
            IF joueurA$ = "coupdeteteR" THEN _SNDSTOP tombe
            xB = xB - 2: GOTO colision
        END IF
        spriteB$ = "tombe1R"
    END IF


    '                               bruit des epees  et decapitations loupees
    IF sens$ = "normal" THEN

        IF joueurB$ = "clingD" THEN
            IF joueurA$ = "decapite" AND decapiteB$ = "non" THEN joueurB$ = "touche": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
            IF joueurA$ = "genou" THEN joueurB$ = "touche": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
            IF distance < 12 THEN
                soncling = soncling + 1
                IF soncling > 3 THEN soncling = 1
                IF soncling = 1 THEN _SNDPLAY cling
                IF soncling = 2 THEN _SNDPLAY cling2
                IF soncling = 3 THEN _SNDPLAY cling3
            END IF
            joueurB$ = "protegeD": GOTO colision
        END IF

        IF joueurB$ = "clingH" THEN
            IF distance < 12 THEN
                soncling = soncling + 1
                IF soncling > 3 THEN soncling = 1
                IF soncling = 1 THEN _SNDPLAY cling
                IF soncling = 2 THEN _SNDPLAY cling2
                IF soncling = 3 THEN _SNDPLAY cling3
            END IF
            joueurB$ = "protegeH": GOTO colision
        END IF

    END IF

    IF sens$ = "inverse" THEN

        IF joueurB$ = "clingD" THEN

            IF joueurA$ = "decapiteR" AND decapiteB$ = "non" THEN joueurB$ = "toucheR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
            IF joueurA$ = "genouR" THEN joueurB$ = "toucheR": Boccupe$ = "oui": reftempsB = temps: GOTO gestionB
            IF distance < 12 THEN
                soncling = soncling + 1
                IF soncling > 3 THEN soncling = 1
                IF soncling = 1 THEN _SNDPLAY cling
                IF soncling = 2 THEN _SNDPLAY cling2
                IF soncling = 3 THEN _SNDPLAY cling3
            END IF
            joueurB$ = "protegeDR": GOTO colision
        END IF

        IF joueurB$ = "clingH" THEN
            IF distance < 12 THEN
                soncling = soncling + 1
                IF soncling > 3 THEN soncling = 1
                IF soncling = 1 THEN _SNDPLAY cling
                IF soncling = 2 THEN _SNDPLAY cling2
                IF soncling = 3 THEN _SNDPLAY cling3
            END IF
            joueurB$ = "protegeHR": GOTO colision
        END IF

    END IF

    '                                   *************************************
    '                                   **********gestion de la mort*********
    '                                   *************************************
    mortB:

    IF joueurB$ = "mort" THEN
        xFB = xB: xTB = xB: xMB = xB: xGB = xB
        IF temps > reftempsB + 16 THEN GOTO colision
        IF temps > reftempsB + 15 THEN sangB$ = "non": spriteB$ = "mort2": GOTO colision
        IF temps > reftempsB + 1 THEN spriteB$ = "mort1": GOTO colision
        spriteB$ = "mort1": joueurA$ = "vainqueurKO": Aoccupe$ = "oui": reftemps = temps
        IF lancerfin$ = "oui" THEN _SNDPLAY mortKO: lancerfin$ = "non"
    END IF

    IF joueurB$ = "mortR" THEN
        IF temps > reftempsB + 16 THEN GOTO colision
        IF temps > reftempsB + 15 THEN sangB$ = "non": spriteB$ = "mort2R": GOTO colision
        IF temps > reftempsB + 1 THEN spriteB$ = "mort1R": GOTO colision
        spriteB$ = "mort1R": joueurA$ = "vainqueurKOR": Aoccupe$ = "oui": reftemps = temps
        IF lancerfin$ = "oui" THEN _SNDPLAY mortKO: lancerfin$ = "non"
    END IF

    IF joueurB$ = "mortdecap" THEN
        IF temps > reftempsB + 80 THEN spriteB$ = "decap4": GOTO colision
        IF temps > reftempsB + 70 THEN spriteB$ = "decap3": GOTO colision
        IF temps > reftempsB + 55 THEN sangdecapB = 0: GOTO colision
        IF temps > reftempsB + 50 THEN sangdecapB = 6: GOTO colision
        IF temps > reftempsB + 45 THEN sangdecapB = 5: GOTO colision
        IF temps > reftempsB + 40 THEN sangdecapB = 4: GOTO colision
        IF temps > reftempsB + 35 THEN spriteB$ = "decap2": GOTO colision
        IF temps > reftempsB + 20 THEN sangdecapB = 0: GOTO colision
        IF temps > reftempsB + 15 THEN sangdecapB = 3: GOTO colision
        IF temps > reftempsB + 10 THEN sangdecapB = 2: GOTO colision
        IF temps > reftempsB + 5 THEN sangdecapB = 1: GOTO colision
        spriteB$ = "decap1": joueurA$ = "vainqueur": Aoccupe$ = "oui": reftemps = temps
        IF lancerfin$ = "oui" THEN _SNDPLAY mortdecap: lancerfin$ = "non"
    END IF
    IF joueurB$ = "mortdecapR" THEN
        IF temps > reftempsB + 80 THEN spriteB$ = "decap4R": GOTO colision
        IF temps > reftempsB + 70 THEN spriteB$ = "decap3R": GOTO colision
        IF temps > reftempsB + 55 THEN sangdecapB = 0: GOTO colision
        IF temps > reftempsB + 50 THEN sangdecapB = 6: GOTO colision
        IF temps > reftempsB + 45 THEN sangdecapB = 5: GOTO colision
        IF temps > reftempsB + 40 THEN sangdecapB = 4: GOTO colision
        IF temps > reftempsB + 35 THEN spriteB$ = "decap2R": GOTO colision
        IF temps > reftempsB + 20 THEN sangdecapB = 0: GOTO colision
        IF temps > reftempsB + 15 THEN sangdecapB = 3: GOTO colision
        IF temps > reftempsB + 10 THEN sangdecapB = 2: GOTO colision
        IF temps > reftempsB + 5 THEN sangdecapB = 1: GOTO colision
        spriteB$ = "decap1R": joueurA$ = "vainqueurR": Aoccupe$ = "oui": reftemps = temps
        IF lancerfin$ = "oui" THEN _SNDPLAY mortdecap: lancerfin$ = "non"
    END IF

    '                   ***************************************
    '                   ***********   SORCIER    **************
    '                   ***************************************

    IF joueurB$ = "sorcier" THEN

        gnome$ = "non"
        xFB = xB + 4: xTB = xB + 4: xMB = xB + 4: xGB = xB + 4

        IF temps > reftempsB + 171 THEN spriteB$ = "sorcier1": reftempsB = temps: GOTO colision


        IF temps > reftempsB + 170 THEN xAttB = 6: GOTO colision
        IF temps > reftempsB + 165 THEN xAttB = 32: GOTO colision
        IF temps > reftempsB + 160 THEN xAttB = 29: GOTO colision
        IF temps > reftempsB + 155 THEN xAttB = 26: GOTO colision
        IF temps > reftempsB + 150 THEN xAttB = 23: GOTO colision
        IF temps > reftempsB + 145 THEN xAttB = 20: GOTO colision
        IF temps > reftempsB + 140 THEN xAttB = 17: spriteB$ = "sorcier1": GOTO colision
        IF temps > reftempsB + 135 THEN xAttB = 14: GOTO colision
        IF temps > reftempsB + 131 THEN GOTO colision
        IF temps > reftempsB + 130 THEN spriteB$ = "sorcier2": yAttB = 16: _SNDPLAY feu: GOTO colision
        IF temps > reftempsB + 90 THEN xAttB = 6: GOTO colision
        IF temps > reftempsB + 85 THEN xAttB = 32: GOTO colision
        IF temps > reftempsB + 80 THEN xAttB = 29: GOTO colision
        IF temps > reftempsB + 75 THEN xAttB = 26: GOTO colision
        IF temps > reftempsB + 70 THEN xAttB = 23: GOTO colision
        IF temps > reftempsB + 65 THEN xAttB = 20: yAttB = 20: GOTO colision
        IF temps > reftempsB + 60 THEN xAttB = 17: spriteB$ = "sorcier1": yAttB = 18: GOTO colision
        IF temps > reftempsB + 55 THEN xAttB = 14: GOTO colision
        IF temps > reftempsB + 51 THEN GOTO colision
        IF temps > reftempsB + 50 THEN spriteB$ = "sorcier2": _SNDPLAY feu: GOTO colision
        spriteB$ = "sorcier1"
        xAttB = xB: yAttB = 16: yGB = 20
        sangB$ = "non"
    END IF


    '                   ***************************************
    '                   ***********   COLISION   **************
    '                   ***************************************
    colision:

    IF sens$ = "inverse" GOTO colisionR

    IF joueurA$ = "saute" AND joueurB$ = "rouladeAV" THEN GOTO sortiecadre
    IF joueurB$ = "saute" AND joueurA$ = "rouladeAV" THEN GOTO sortiecadre

    '                               pour empecher que A entre dans B


    IF levier1$ = "droite" OR joueurA$ = "rouladeAV" OR joueurA$ = "decapite" THEN
        distance = xB - xA
        IF distance < 4 THEN xA = xA - 1:
    END IF


    '                                pour empecher que B entre dans A

    IF levier2$ = "gauche" OR joueurB$ = "rouladeAV" OR joueurB$ = "decapite" THEN
        distance = xB - xA
        IF distance < 4 THEN xB = xB + 1
    END IF

    '                               garder la distance debout
    IF joueurB$ = "debout" AND joueurA$ = "debout" THEN
        distance = xB - xA
        IF distance < 4 THEN xA = xA - 1: xB = xB + 1
    END IF


    '                               sortie du cadre
    sortiecadre:

    IF entree$ = "oui" OR sortieA$ = "oui" OR sortieB$ = "oui" THEN
        IF xA < 0 THEN xA = 0
        IF xB < 0 THEN xB = 0
        IF xA > 40 THEN xA = 40
        IF xB > 40 THEN xB = 40
        GOTO tetesvolantes
    END IF

    IF entree$ = "non" THEN
        IF xA < 5 THEN xA = 5
        IF xA > 32 THEN xA = 32
        IF xB < 5 THEN xB = 5
        IF xB > 32 THEN xB = 32
    END IF


    GOTO tetesvolantes

    '                   ***************************************
    '                   ***********   COLISION INVERSE ********
    '                   ***************************************

    IF sens$ = "normal" THEN GOTO affichage

    colisionR:

    IF joueurA$ = "sauteR" AND joueurB$ = "rouladeAVR" THEN GOTO sortiecadreR
    IF joueurB$ = "sauteR" AND joueurA$ = "rouladeAVR" THEN GOTO sortiecadreR

    '                               pour empecher que A entre dans B (inverse)

    IF levier1$ = "gauche" OR joueurA$ = "rouladeAVR" OR joueurA$ = "decapiteR" THEN
        distance = xA - xB
        IF distance < 4 THEN xA = xA + 1
    END IF


    '                                pour empecher que B entre dans A (inverse)

    IF levier2$ = "droite" OR joueurB$ = "rouladeAVR" OR joueurB$ = "decapiteR" THEN
        distance = xA - xB
        IF distance < 4 THEN xB = xB - 1
    END IF

    '                               garder la distance debout
    IF joueurB$ = "deboutR" AND joueurA$ = "deboutR" THEN
        distance = xA - xB
        IF distance < 4 THEN xA = xA + 1: xB = xB - 1
    END IF


    sortiecadreR:

    IF sortieA$ = "oui" OR sortieB$ = "oui" OR entreesorcier$ = "oui" THEN
        IF xA < 0 THEN xA = 0
        IF xB < 0 THEN xB = 0
        IF xA > 40 THEN xA = 40
        IF xB > 40 THEN xB = 40
        GOTO tetesvolantes
    END IF

    IF xA < 5 THEN xA = 5
    IF xA > 32 THEN xA = 32
    IF xB < 5 THEN xB = 5
    IF xB > 32 THEN xB = 32



    '                       ****************************************
    '                       ********* les tetes volantes ! *********
    '                       ****************************************
    tetesvolantes:

    IF sortieA$ = "oui" OR sortieB$ = "oui" THEN GOTO affichage

    IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" OR joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN

        IF xA > 19 AND xB > 20 THEN GOTO teteagauche

        IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" THEN


            IF temps > reftemps + 125 THEN
                gnome$ = "oui": reftemps = temps
                xGNOME = 1
                GOTO affichage
            END IF

            IF temps > reftemps + 56 THEN ySPRt = 164: xSPRt = xA + 16: numerotete = 3: GOTO affichage
            IF temps > reftemps + 52 THEN ySPRt = 157: xSPRt = xA + 15: numerotete = 2: GOTO affichage
            IF temps > reftemps + 48 THEN ySPRt = 159: xSPRt = xA + 14: numerotete = 1: GOTO affichage

            IF temps > reftemps + 45 THEN ySPRt = 157: xSPRt = xA + 13: numerotete = 6: GOTO affichage
            IF temps > reftemps + 44 THEN
                _SNDPLAY tete
                ySPRt = 157: xSPRt = xA + 13: numerotete = 6: GOTO affichage
            END IF

            IF temps > reftemps + 40 THEN ySPRt = 159: xSPRt = xA + 12: numerotete = 5: GOTO affichage
            IF temps > reftemps + 36 THEN ySPRt = 159: xSPRt = xA + 11: numerotete = 4: GOTO affichage
            IF temps > reftemps + 32 THEN ySPRt = 159: xSPRt = xA + 10: numerotete = 3: GOTO affichage

            IF temps > reftemps + 29 THEN ySPRt = 159: xSPRt = xA + 9: numerotete = 2: GOTO affichage
            IF temps > reftemps + 28 THEN
                _SNDPLAY tete
                ySPRt = 159: xSPRt = xA + 9: numerotete = 2: GOTO affichage
            END IF

            IF temps > reftemps + 24 THEN ySPRt = 139: xSPRt = xA + 8: numerotete = 1: GOTO affichage
            IF temps > reftemps + 20 THEN ySPRt = 125: xSPRt = xA + 7: numerotete = 6: GOTO affichage
            IF temps > reftemps + 16 THEN ySPRt = 125: xSPRt = xA + 6: numerotete = 5: GOTO affichage
            IF temps > reftemps + 12 THEN ySPRt = 118: xSPRt = xA + 5: numerotete = 4: GOTO affichage
            IF temps > reftemps + 8 THEN ySPRt = 111: xSPRt = xA + 4: numerotete = 3: GOTO affichage
            IF temps > reftemps + 4 THEN ySPRt = 111: xSPRt = xA + 3: numerotete = 2: GOTO affichage
            IF temps >= reftemps THEN ySPRt = 111: xSPRt = xA + 2: numerotete = 1: GOTO affichage

        END IF


        IF joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN

            IF temps > reftemps + 125 THEN
                gnome$ = "oui": reftemps = temps
                xGNOME = 1
                GOTO affichage
            END IF

            IF temps > reftemps + 56 THEN ySPRt = 164: xSPRt = xB + 16: numerotete = 3: GOTO affichage
            IF temps > reftemps + 52 THEN ySPRt = 157: xSPRt = xB + 15: numerotete = 2: GOTO affichage
            IF temps > reftemps + 48 THEN ySPRt = 159: xSPRt = xB + 14: numerotete = 1: GOTO affichage

            IF temps > reftemps + 45 THEN ySPRt = 157: xSPRt = xB + 13: numerotete = 6: GOTO affichage
            IF temps > reftemps + 44 THEN
                _SNDPLAY tete
                ySPRt = 157: xSPRt = xB + 13: numerotete = 6: GOTO affichage
            END IF

            IF temps > reftemps + 40 THEN ySPRt = 159: xSPRt = xB + 12: numerotete = 5: GOTO affichage
            IF temps > reftemps + 36 THEN ySPRt = 159: xSPRt = xB + 11: numerotete = 4: GOTO affichage
            IF temps > reftemps + 32 THEN ySPRt = 159: xSPRt = xB + 10: numerotete = 3: GOTO affichage

            IF temps > reftemps + 29 THEN ySPRt = 159: xSPRt = xB + 9: numerotete = 2: GOTO affichage
            IF temps > reftemps + 28 THEN
                _SNDPLAY tete
                ySPRt = 159: xSPRt = xB + 9: numerotete = 2: GOTO affichage
            END IF

            IF temps > reftemps + 24 THEN ySPRt = 139: xSPRt = xB + 8: numerotete = 1: GOTO affichage
            IF temps > reftemps + 20 THEN ySPRt = 125: xSPRt = xB + 7: numerotete = 6: GOTO affichage
            IF temps > reftemps + 16 THEN ySPRt = 125: xSPRt = xB + 6: numerotete = 5: GOTO affichage
            IF temps > reftemps + 12 THEN ySPRt = 118: xSPRt = xB + 5: numerotete = 4: GOTO affichage
            IF temps > reftemps + 8 THEN ySPRt = 111: xSPRt = xB + 4: numerotete = 3: GOTO affichage
            IF temps > reftemps + 4 THEN ySPRt = 111: xSPRt = xB + 3: numerotete = 2: GOTO affichage
            IF temps >= reftemps THEN ySPRt = 111: xSPRt = xB + 2: numerotete = 1: GOTO affichage
            GOTO affichage
        END IF

        teteagauche:

        IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" THEN

            IF temps > reftemps + 125 THEN
                gnome$ = "oui": reftemps = temps
                xGNOME = 1
                GOTO affichage
            END IF

            IF temps > reftemps + 56 THEN ySPRt = 164: xSPRt = xA - 12: numerotete = 3: GOTO affichage
            IF temps > reftemps + 52 THEN ySPRt = 157: xSPRt = xA - 11: numerotete = 2: GOTO affichage
            IF temps > reftemps + 48 THEN ySPRt = 159: xSPRt = xA - 10: numerotete = 1: GOTO affichage

            IF temps > reftemps + 45 THEN ySPRt = 157: xSPRt = xA - 9: numerotete = 6: GOTO affichage
            IF temps > reftemps + 44 THEN
                _SNDPLAY tete
                ySPRt = 157: xSPRt = xA - 9: numerotete = 6: GOTO affichage
            END IF

            IF temps > reftemps + 40 THEN ySPRt = 159: xSPRt = xA - 8: numerotete = 5: GOTO affichage
            IF temps > reftemps + 36 THEN ySPRt = 159: xSPRt = xA - 7: numerotete = 4: GOTO affichage
            IF temps > reftemps + 32 THEN ySPRt = 159: xSPRt = xA - 6: numerotete = 3: GOTO affichage

            IF temps > reftemps + 29 THEN ySPRt = 159: xSPRt = xA - 5: numerotete = 2: GOTO affichage
            IF temps > reftemps + 28 THEN
                _SNDPLAY tete
                ySPRt = 159: xSPRt = xA - 5: numerotete = 2: GOTO affichage
            END IF

            IF temps > reftemps + 24 THEN ySPRt = 139: xSPRt = xA - 4: numerotete = 1: GOTO affichage
            IF temps > reftemps + 20 THEN ySPRt = 125: xSPRt = xA - 3: numerotete = 6: GOTO affichage
            IF temps > reftemps + 16 THEN ySPRt = 125: xSPRt = xA - 2: numerotete = 5: GOTO affichage
            IF temps > reftemps + 12 THEN ySPRt = 118: xSPRt = xA - 1: numerotete = 4: GOTO affichage
            IF temps > reftemps + 8 THEN ySPRt = 111: xSPRt = xA: numerotete = 3: GOTO affichage
            IF temps > reftemps + 4 THEN ySPRt = 111: xSPRt = xA + 1: numerotete = 2: GOTO affichage
            IF temps >= reftemps THEN ySPRt = 111: xSPRt = xA + 2: numerotete = 1: GOTO affichage

        END IF

        IF joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN

            IF temps > reftemps + 125 THEN
                gnome$ = "oui": reftemps = temps
                xGNOME = 1
                GOTO affichage
            END IF

            IF temps > reftemps + 56 THEN ySPRt = 164: xSPRt = xB - 16: numerotete = 3: GOTO affichage
            IF temps > reftemps + 52 THEN ySPRt = 157: xSPRt = xB - 15: numerotete = 2: GOTO affichage
            IF temps > reftemps + 48 THEN ySPRt = 159: xSPRt = xB - 14: numerotete = 1: GOTO affichage

            IF temps > reftemps + 45 THEN ySPRt = 157: xSPRt = xB - 13: numerotete = 6: GOTO affichage
            IF temps > reftemps + 44 THEN
                _SNDPLAY tete
                ySPRt = 157: xSPRt = xB - 13: numerotete = 6: GOTO affichage
            END IF

            IF temps > reftemps + 40 THEN ySPRt = 159: xSPRt = xB - 12: numerotete = 5: GOTO affichage
            IF temps > reftemps + 36 THEN ySPRt = 159: xSPRt = xB - 11: numerotete = 4: GOTO affichage
            IF temps > reftemps + 32 THEN ySPRt = 159: xSPRt = xB - 10: numerotete = 3: GOTO affichage

            IF temps > reftemps + 29 THEN ySPRt = 159: xSPRt = xB - 9: numerotete = 2: GOTO affichage
            IF temps > reftemps + 28 THEN
                _SNDPLAY tete
                ySPRt = 159: xSPRt = xB - 9: numerotete = 2: GOTO affichage
            END IF

            IF temps > reftemps + 24 THEN ySPRt = 139: xSPRt = xB - 8: numerotete = 1: GOTO affichage
            IF temps > reftemps + 20 THEN ySPRt = 125: xSPRt = xB - 7: numerotete = 6: GOTO affichage
            IF temps > reftemps + 16 THEN ySPRt = 125: xSPRt = xB - 6: numerotete = 5: GOTO affichage
            IF temps > reftemps + 12 THEN ySPRt = 118: xSPRt = xB - 5: numerotete = 4: GOTO affichage
            IF temps > reftemps + 8 THEN ySPRt = 111: xSPRt = xB - 4: numerotete = 3: GOTO affichage
            IF temps > reftemps + 4 THEN ySPRt = 111: xSPRt = xB - 3: numerotete = 2: GOTO affichage
            IF temps >= reftemps THEN ySPRt = 111: xSPRt = xB - 2: numerotete = 1: GOTO affichage

        END IF

    END IF

    '                   *********************************
    '                   *******  PASSAGE DU GNOME *******
    '                   *********************************

    gnome:
    IF gnome$ = "oui" THEN

        numerognome = 4
        IF temps > reftemps + 6 THEN numerognome = 1
        IF temps > reftemps + 12 THEN numerognome = 2
        IF temps > reftemps + 18 THEN numerognome = 3


        IF temps > reftemps + 24 THEN reftemps = temps: GOTO affichage
        IF temps > reftemps + 19 THEN GOTO affichage
        IF temps > reftemps + 18 THEN xGNOME = xGNOME + 1: GOTO affichage
        IF temps > reftemps + 7 THEN GOTO affichage
        IF temps > reftemps + 6 THEN xGNOME = xGNOME + 1: GOTO affichage



    END IF



    affichage:
    '                   **********************************************
    '                   ************      AFFICHAGE        ***********
    '                   **********************************************

    '                           fond decor


    _PUTIMAGE (38, 104), fond


    IF transition$ = "oui" THEN

        IF temps > reftemps + 55 THEN
            IF joueurB$ = "mort" OR joueurB$ = "mortR" OR joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN xA = 1
            IF joueurA$ = "mort" OR joueurA$ = "mortR" OR joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" THEN xB = 39
        END IF
        IF temps > reftemps + 56 THEN transition$ = "non": transitionfinie$ = "oui"

    END IF


    '                           caches bleus

    LINE (90, 56)-(233, 64), _RGB(34, 34, 153), BF


    IF sorcier$ = "oui" OR sorcier$ = "mort" OR jeu$ = "perdu" THEN

        LINE (114, 95)-(129, 100), _RGB(0, 0, 0), BF
        LINE (109, 100)-(134, 114), _RGB(0, 0, 0), BF


        'points de vie cachs
        LINE (276, 0)-(319, 22), _RGB(0, 0, 0), BF
        LINE (0, 0)-(45, 22), _RGB(0, 0, 0), BF
    END IF



    '                               affichage du temps

    IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" OR joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN GOTO affichetemps
    IF joueurA$ = "mort" OR joueurA$ = "mortR" OR joueurB$ = "mort" OR joueurB$ = "mortR" THEN GOTO affichetemps

    IF temps > chrono + 50 THEN
        chronometre = chronometre - 1
        chrono = temps
    END IF

    IF chronometre < 0 THEN
        chronometre = 0
        IF partie$ = "vs" THEN
            sortieA$ = "oui": sortieB$ = "oui": tempsfini$ = "oui": Aoccupe$ = "non": Boccupe$ = "non"
        END IF
    END IF


    affichetemps:

    COLOR _RGB(0, 0, 0)
    _FONT 8

    _PRINTMODE _KEEPBACKGROUND
    IF partie$ = "solo" THEN LOCATE 8, 20: PRINT "0": LOCATE 8, 20: PRINT IA

    IF partie$ = "vs" THEN
        IF chronometre > 10 THEN LOCATE 8, 19: PRINT chronometre
        IF chronometre = 10 THEN LOCATE 8, 19: PRINT chronometre
        IF chronometre < 10 THEN LOCATE 8, 20: PRINT "0": LOCATE 8, 20: PRINT chronometre
    END IF


    '                                  affichage du score

    IF scoreA = 0 THEN LOCATE 8, 13: PRINT "00000"
    IF scoreB = 0 THEN LOCATE 8, 24: PRINT "00000"

    IF scoreA > 99999 THEN scoreA = 0: IF scoreB > 99999 THEN scoreB = 0

    IF scoreA > 99 AND scoreA < 999 THEN
        LOCATE 8, 13: PRINT "00": LOCATE 8, 14: PRINT scoreA
    END IF
    IF scoreA > 999 AND scoreA < 9999 THEN
        LOCATE 8, 13: PRINT "0": LOCATE 8, 13: PRINT scoreA
    END IF
    IF scoreA > 9999 AND scoreA < 99999 THEN
        LOCATE 8, 12: PRINT scoreA
    END IF

    IF scoreB > 99 AND scoreB < 999 THEN
        LOCATE 8, 24: PRINT "00": LOCATE 8, 25: PRINT scoreB
    END IF
    IF scoreB > 999 AND scoreB < 9999 THEN
        LOCATE 8, 24: PRINT "0": LOCATE 8, 24: PRINT scoreB
    END IF
    IF scoreB > 9999 AND scoreB < 99999 THEN
        LOCATE 8, 23: PRINT scoreB
    END IF



    '                                 points de vie

    IF vieA = 11 THEN LINE (38, 10)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 10 THEN LINE (29, 10)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 9 THEN LINE (22, 10)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 8 THEN LINE (13, 10)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 7 THEN LINE (6, 10)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 6 THEN LINE (0, 10)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 5 THEN LINE (38, 0)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 4 THEN LINE (29, 0)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 3 THEN LINE (22, 0)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 2 THEN LINE (13, 0)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 1 THEN LINE (6, 0)-(45, 22), _RGB(0, 0, 0), BF
    IF vieA = 0 THEN LINE (0, 0)-(45, 22), _RGB(0, 0, 0), BF

    IF vieB = 11 THEN LINE (315, 10)-(639, 22), _RGB(0, 0, 0), BF
    IF vieB = 10 THEN LINE (306, 10)-(639, 22), _RGB(0, 0, 0), BF
    IF vieB = 9 THEN LINE (299, 10)-(639, 22), _RGB(0, 0, 0), BF
    IF vieB = 8 THEN LINE (290, 10)-(639, 22), _RGB(0, 0, 0), BF
    IF vieB = 7 THEN LINE (283, 10)-(639, 22), _RGB(0, 0, 0), BF
    IF vieB = 6 THEN LINE (276, 10)-(639, 22), _RGB(0, 0, 0), BF
    IF vieB = 5 THEN LINE (315, 0)-(639, 10), _RGB(0, 0, 0), BF
    IF vieB = 4 THEN LINE (306, 0)-(639, 10), _RGB(0, 0, 0), BF
    IF vieB = 3 THEN LINE (299, 0)-(639, 10), _RGB(0, 0, 0), BF
    IF vieB = 2 THEN LINE (290, 0)-(639, 10), _RGB(0, 0, 0), BF
    IF vieB = 1 THEN LINE (283, 0)-(639, 10), _RGB(0, 0, 0), BF
    IF vieB = 0 THEN LINE (276, 0)-(319, 22), _RGB(0, 0, 0), BF


    IF version$ = "oui" THEN
        COLOR _RGB(255, 255, 255)
        _FONT 8
        LOCATE 18, 36: PRINT "FL VERSION": LOCATE 19, 15: PRINT "2012"
    END IF

    '                       ****************************************
    '                       *********** affichage sprite A**********
    '                       ****************************************


    ' choix du sprite

    IF spriteA$ = "debout" THEN imageA = deboutA: sensimageA$ = "normal"
    IF spriteA$ = "assis1" THEN imageA = assis1A: sensimageA$ = "normal"
    IF spriteA$ = "assis2" THEN imageA = assis2A: sensimageA$ = "normal"
    IF spriteA$ = "attente1" THEN imageA = attente1A: sensimageA$ = "normal"
    IF spriteA$ = "attente2" THEN imageA = attente2A: sensimagesA$ = "normal"
    IF spriteA$ = "attente3" THEN imageA = attente3A: sensimagesA$ = "normal"
    IF spriteA$ = "cou1" THEN imageA = protegeHA: sensimagesA$ = "normal"
    IF spriteA$ = "cou2" THEN imageA = cou2A: sensimagesA$ = "normal"
    IF spriteA$ = "cou3" THEN imageA = cou3A: sensimagesA$ = "normal"
    IF spriteA$ = "devant1" THEN imageA = devant1A: sensimageA$ = "normal"
    IF spriteA$ = "devant2" THEN imageA = devant2A: sensimageA$ = "normal"
    IF spriteA$ = "devant3" THEN imageA = devant3A: sensimagesA$ = "normal"
    IF spriteA$ = "genou1" THEN imageA = genou1A: sensimageA$ = "normal"
    IF spriteA$ = "genou2" THEN imageA = assis2A: sensimageA$ = "normal"
    IF spriteA$ = "genou3" THEN imageA = genou3A: sensimagesA$ = "normal"
    IF spriteA$ = "marche1" THEN imageA = marche1A: sensimageA$ = "normal"
    IF spriteA$ = "marche2" THEN imageA = marche2A: sensimageA$ = "normal"
    IF spriteA$ = "marche3" THEN imageA = marche3A: sensimageA$ = "normal"
    IF spriteA$ = "saut1" THEN imageA = saut1A: sensimagesA$ = "normal"
    IF spriteA$ = "saut2" THEN imageA = saut2A: sensimagesA$ = "normal"
    IF spriteA$ = "vainqueur1" THEN imageA = vainqueur1A: sensimageA$ = "normal"
    IF spriteA$ = "vainqueur2" THEN imageA = vainqueur2A: sensimageA$ = "normal"
    IF spriteA$ = "vainqueur3" THEN imageA = vainqueur3A: sensimageA$ = "normal"
    IF spriteA$ = "retourne1" THEN imageA = retourne1A: sensimageA$ = "normal"
    IF spriteA$ = "retourne2" THEN imageA = retourne2A: sensimageA$ = "normal"
    IF spriteA$ = "retourne3" THEN imageA = retourne3A: sensimageA$ = "normal"
    IF spriteA$ = "front1" THEN imageA = front1A: sensimagesA$ = "normal"
    IF spriteA$ = "front2" THEN imageA = front2A: sensimagesA$ = "normal"
    IF spriteA$ = "front3" THEN imageA = front3A: sensimagesA$ = "normal"
    IF spriteA$ = "toile1" THEN imageA = toile1A: sensimagesA$ = "normal"
    IF spriteA$ = "toile2" THEN imageA = toile2A: sensimagesA$ = "normal"
    IF spriteA$ = "toile3" THEN imageA = toile3A: sensimagesA$ = "normal"
    IF spriteA$ = "toile4" THEN imageA = toile4A: sensimagesA$ = "normal"
    IF spriteA$ = "tombe1" THEN imageA = tombe1A: sensimagesA$ = "normal"
    IF spriteA$ = "tombe2" THEN imageA = tombe2A: sensimagesA$ = "normal"
    IF spriteA$ = "tombe3" THEN imageA = tombe3A: sensimagesA$ = "normal"
    IF spriteA$ = "protegeD" THEN imageA = protegeDA: sensimagesA$ = "normal"
    IF spriteA$ = "protegeH" THEN imageA = protegeHA: sensimagesA$ = "normal"
    IF spriteA$ = "tete1" THEN imageA = couptete1A: sensimagesA$ = "normal"
    IF spriteA$ = "tete2" THEN imageA = couptete2A: sensimageA$ = "normal"
    IF spriteA$ = "touche1" THEN imageA = touche2A: sensimageA$ = "normal"
    IF spriteA$ = "touche2" THEN imageA = touche1A: sensimageA$ = "normal"
    IF spriteA$ = "touche3" THEN imageA = touche2A: sensimageA$ = "normal"

    IF spriteA$ = "pied1" THEN imageA = pied1A: sensimagesA$ = "normal"
    IF spriteA$ = "pied2" THEN imageA = pied2A: sensimagesA$ = "normal"
    IF spriteA$ = "decap1" THEN imageA = decap1A: sensimageA$ = "normal"
    IF spriteA$ = "decap2" THEN imageA = decap2A: sensimageA$ = "normal"
    IF spriteA$ = "decap3" THEN imageA = decap3A: sensimagesA$ = "normal"
    IF spriteA$ = "decap4" THEN imageA = decap4A: sensimagesA$ = "normal"
    IF spriteA$ = "mort1" THEN imageA = assis1A: sensimageA$ = "normal"
    IF spriteA$ = "mort2" THEN imageA = mort2A: sensimagesA$ = "normal"
    IF spriteA$ = "mort3" THEN imageA = mort3A: sensimagesA$ = "normal"
    IF spriteA$ = "mort4" THEN imageA = mort4A: sensimagesA$ = "normal"


    IF spriteA$ = "roulade1" THEN imageA = roulade1A: sensimageA$ = "normal"
    IF spriteA$ = "roulade2" THEN imageA = roulade2A: sensimageA$ = "normal"
    IF spriteA$ = "roulade3" THEN imageA = roulade3A: sensimageA$ = "normal"
    IF spriteA$ = "roulade4" THEN imageA = roulade2A: sensimageA$ = "inverse"
    IF spriteA$ = "roulade5" THEN imageA = roulade5A: sensimageA$ = "normal"
    IF spriteA$ = "roulade6" THEN imageA = roulade1A: sensimageA$ = "inverse"


    IF spriteA$ = "deboutR" THEN imageA = deboutA: sensimageA$ = "inverse"
    IF spriteA$ = "assis1R" THEN imageA = assis1A: sensimageA$ = "inverse"
    IF spriteA$ = "assis2R" THEN imageA = assis2A: sensimageA$ = "inverse"
    IF spriteA$ = "attente1R" THEN imageA = attente1A: sensimageA$ = "inverse"
    IF spriteA$ = "attente2R" THEN imageA = attente2A: sensimageA$ = "large1R"
    IF spriteA$ = "attente3R" THEN imageA = attente3A: sensimageA$ = "large1R"
    IF spriteA$ = "cou1R" THEN imageA = protegeHA: sensimageA$ = "large1R"
    IF spriteA$ = "cou2R" THEN imageA = cou2A: sensimageA$ = "large1R"
    IF spriteA$ = "cou3R" THEN imageA = cou3A: sensimageA$ = "large4R"
    IF spriteA$ = "devant1R" THEN imageA = devant1A: sensimageA$ = "inverse"
    IF spriteA$ = "devant2R" THEN imageA = devant2A: sensimageA$ = "inverse"
    IF spriteA$ = "devant3R" THEN imageA = devant3A: sensimageA$ = "large3R"
    IF spriteA$ = "genou1R" THEN imageA = genou1A: sensimageA$ = "inverse"
    IF spriteA$ = "genou2R" THEN imageA = assis2A: sensimageA$ = "inverse"
    IF spriteA$ = "genou3R" THEN imageA = genou3A: sensimageA$ = "large3R"
    IF spriteA$ = "marche1R" THEN imageA = marche1A: sensimageA$ = "inverse"
    IF spriteA$ = "marche2R" THEN imageA = marche2A: sensimageA$ = "inverse"
    IF spriteA$ = "marche3R" THEN imageA = marche3A: sensimageA$ = "inverse"
    IF spriteA$ = "saut1R" THEN imageA = saut1A: sensimageA$ = "large1R"
    IF spriteA$ = "saut2R" THEN imageA = saut2A: sensimageA$ = "large1R"
    IF spriteA$ = "vainqueur1R" THEN imageA = vainqueur1A: sensimageA$ = "inverse"
    IF spriteA$ = "vainqueur2R" THEN imageA = vainqueur2A: sensimageA$ = "inverse"
    IF spriteA$ = "vainqueur3R" THEN imageA = vainqueur3A: sensimageA$ = "inverse"
    IF spriteA$ = "retourne1R" THEN imageA = retourne1A: sensimageA$ = "inverse"
    IF spriteA$ = "retourne2R" THEN imageA = retourne2A: sensimageA$ = "inverse"
    IF spriteA$ = "retourne3R" THEN imageA = retourne3A: sensimageA$ = "inverse"
    IF spriteA$ = "front1R" THEN imageA = front1A: sensimageA$ = "large1R"
    IF spriteA$ = "front2R" THEN imageA = front2A: sensimageA$ = "large1R"
    IF spriteA$ = "front3R" THEN imageA = front3A: sensimageA$ = "large3R"
    IF spriteA$ = "toile1R" THEN imageA = toile1A: sensimageA$ = "large1R"
    IF spriteA$ = "toile2R" THEN imageA = toile2A: sensimageA$ = "large1R"
    IF spriteA$ = "toile3R" THEN imageA = toile3A: sensimageA$ = "large1R"
    IF spriteA$ = "toile4R" THEN imageA = toile4A: sensimageA$ = "large3R"
    IF spriteA$ = "tombe1R" THEN imageA = tombe1A: sensimageA$ = "large1R"
    IF spriteA$ = "tombe2R" THEN imageA = tombe2A: sensimageA$ = "large3R"
    IF spriteA$ = "tombe3R" THEN imageA = tombe3A: sensimageA$ = "large3R"
    IF spriteA$ = "protegeDR" THEN imageA = protegeDA: sensimageA$ = "large1R"
    IF spriteA$ = "protegeHR" THEN imageA = protegeHA: sensimageA$ = "large1R"
    IF spriteA$ = "tete1R" THEN imageA = couptete1A: sensimageA$ = "large1R"
    IF spriteA$ = "tete2R" THEN imageA = couptete2A: sensimageA$ = "inverse"
    IF spriteA$ = "touche1R" THEN imageA = touche2A: sensimageA$ = "inverse"
    IF spriteA$ = "touche2R" THEN imageA = touche1A: sensimageA$ = "inverse"
    IF spriteA$ = "touche3R" THEN imageA = touche2A: sensimageA$ = "inverse"
    IF spriteA$ = "pied1R" THEN imageA = pied1A: sensimageA$ = "large1R"
    IF spriteA$ = "pied2R" THEN imageA = pied2A: sensimageA$ = "large1R"
    IF spriteA$ = "decap1R" THEN imageA = decap1A: sensimageA$ = "inverse"
    IF spriteA$ = "decap2R" THEN imageA = decap2A: sensimageA$ = "inverse"
    IF spriteA$ = "decap3R" THEN imageA = decap3A: sensimageA$ = "large1R"
    IF spriteA$ = "decap4R" THEN imageA = decap4A: sensimageA$ = "large3R"
    IF spriteA$ = "mort1R" THEN imageA = assis1A: sensimageA$ = "inverse"
    IF spriteA$ = "mort2R" THEN imageA = mort2A: sensimageA$ = "large1R"
    IF spriteA$ = "mort3R" THEN imageA = mort3A: sensimageA$ = "large1R"
    IF spriteA$ = "mort4R" THEN imageA = mort4A: sensimageA$ = "large3R"


    IF spriteA$ = "roulade1R" THEN imageA = roulade1A: sensimageA$ = "inverse"
    IF spriteA$ = "roulade2R" THEN imageA = roulade2A: sensimageA$ = "inverse"
    IF spriteA$ = "roulade3R" THEN imageA = roulade3A: sensimageA$ = "normal"
    IF spriteA$ = "roulade4R" THEN imageA = roulade2A: sensimageA$ = "normal"
    IF spriteA$ = "roulade5R" THEN imageA = roulade5A: sensimageA$ = "normal"
    IF spriteA$ = "roulade6R" THEN imageA = roulade1A: sensimageA$ = "normal"



    a2 = (xA - 1) * 8: b2 = ((yFA - 2) * 8)

    IF a2 > 0 THEN
        IF sensimageA$ = "normal" THEN
            _PUTIMAGE (a2, b2), imageA
        END IF

        IF sensimageA$ = "inverse" THEN
            _PUTIMAGE (a2 + 39, b2)-(a2, b2 + 79), imageA
        END IF

        IF sensimageA$ = "large3R" THEN
            _PUTIMAGE (a2 + 40, b2)-(a2 - 23, b2 + 79), imageA ' retirer 23 (3*8)-1  a2
        END IF '                                              attention a gauche a2 serait de 63 (39+24)

        IF sensimageA$ = "large4R" THEN
            _PUTIMAGE (a2 + 41, b2)-(a2 - 31, b2 + 79), imageA ' retirer 31 (4*8)-1  a4
        END IF

        IF sensimageA$ = "large1R" THEN
            _PUTIMAGE (a2 + 39, b2)-(a2 - 8, b2 + 79), imageA
        END IF
    END IF


    '                       ****************************************
    '                       *********** affichage sprite B**********
    '                       ****************************************


    'choix du sprite

    IF spriteB$ = "debout" THEN imageB = deboutB: sensimageB$ = "normal"
    IF spriteB$ = "assis1" THEN imageB = assis1B: sensimageB$ = "normal"
    IF spriteB$ = "assis2" THEN imageB = assis2B: sensimageB$ = "normal"
    IF spriteB$ = "attente1" THEN imageB = attente1B: sensimageB$ = "normal"
    IF spriteB$ = "attente2" THEN imageB = attente2B: sensimageB$ = "large1"
    IF spriteB$ = "attente3" THEN imageB = attente3B: sensimageB$ = "large1"
    IF spriteB$ = "cou1" THEN imageB = protegeHB: sensimageB$ = "large1"
    IF spriteB$ = "cou2" THEN imageB = cou2B: sensimageB$ = "large1"
    IF spriteB$ = "cou3" THEN imageB = cou3B: sensimageB$ = "large4"
    IF spriteB$ = "devant1" THEN imageB = devant1B: sensimageB$ = "normal"
    IF spriteB$ = "devant2" THEN imageB = devant2B: sensimageB$ = "normal"
    IF spriteB$ = "devant3" THEN imageB = devant3B: sensimageB$ = "large3"
    IF spriteB$ = "genou1" THEN imageB = genou1B: sensimageB$ = "normal"
    IF spriteB$ = "genou2" THEN imageB = assis2B: sensimageB$ = "normal"
    IF spriteB$ = "genou3" THEN imageB = genou3B: sensimageB$ = "large3"
    IF spriteB$ = "marche1" THEN imageB = marche1B: sensimageB$ = "normal"
    IF spriteB$ = "marche2" THEN imageB = marche2B: sensimageB$ = "normal"
    IF spriteB$ = "marche3" THEN imageB = marche3B: sensimageB$ = "normal"
    IF spriteB$ = "saut1" THEN imageB = saut1B: sensimageB$ = "large1"
    IF spriteB$ = "saut2" THEN imageB = saut2B: sensimageB$ = "large1"
    IF spriteB$ = "vainqueur1" THEN imageB = vainqueur1B: sensimageB$ = "normal"
    IF spriteB$ = "vainqueur2" THEN imageB = vainqueur2B: sensimageB$ = "normal"
    IF spriteB$ = "vainqueur3" THEN imageB = vainqueur3B: sensimageB$ = "normal"
    IF spriteB$ = "retourne1" THEN imageB = retourne1B: sensimageB$ = "normal"
    IF spriteB$ = "retourne2" THEN imageB = retourne2B: sensimageB$ = "normal"
    IF spriteB$ = "retourne3" THEN imageB = retourne3B: sensimageB$ = "normal"
    IF spriteB$ = "front1" THEN imageB = front1B: sensimageB$ = "large1"
    IF spriteB$ = "front2" THEN imageB = front2B: sensimageB$ = "large1"
    IF spriteB$ = "front3" THEN imageB = front3B: sensimageB$ = "large3"
    IF spriteB$ = "toile1" THEN imageB = toile1B: sensimageB$ = "large1"
    IF spriteB$ = "toile2" THEN imageB = toile2B: sensimageB$ = "large1"
    IF spriteB$ = "toile3" THEN imageB = toile3B: sensimageB$ = "large1"
    IF spriteB$ = "toile4" THEN imageB = toile4B: sensimageB$ = "large3"
    IF spriteB$ = "tombe1" THEN imageB = tombe1B: sensimageB$ = "large1"
    IF spriteB$ = "tombe2" THEN imageB = tombe2B: sensimageB$ = "large3"
    IF spriteB$ = "tombe3" THEN imageB = tombe3B: sensimageB$ = "large3"
    IF spriteB$ = "protegeD" THEN imageB = protegeDB: sensimageB$ = "large1"
    IF spriteB$ = "protegeH" THEN imageB = protegeHB: sensimageB$ = "large1"
    IF spriteB$ = "tete1" THEN imageB = couptete1B: sensimageB$ = "large1"
    IF spriteB$ = "tete2" THEN imageB = couptete2B: sensimageB$ = "normal"
    IF spriteB$ = "touche1" THEN imageB = touche2B: sensimageB$ = "normal"
    IF spriteB$ = "touche2" THEN imageB = touche1B: sensimageB$ = "normal"
    IF spriteB$ = "touche3" THEN imageB = touche2B: sensimageB$ = "normal"
    IF spriteB$ = "pied1" THEN imageB = pied1B: sensimageB$ = "large1"
    IF spriteB$ = "pied2" THEN imageB = pied2B: sensimageB$ = "large1"
    IF spriteB$ = "decap1" THEN imageB = decap1B: sensimageB$ = "normal"
    IF spriteB$ = "decap2" THEN imageB = decap2B: sensimageB$ = "normal"
    IF spriteB$ = "decap3" THEN imageB = decap3B: sensimageB$ = "large1"
    IF spriteB$ = "decap4" THEN imageB = decap4B: sensimageB$ = "large3"
    IF spriteB$ = "mort1" THEN imageB = assis1B: sensimageB$ = "normal"
    IF spriteB$ = "mort2" THEN imageB = mort2B: sensimageB$ = "large1"
    IF spriteB$ = "mort3" THEN imageB = mort3B: sensimageB$ = "large1"
    IF spriteB$ = "mort4" THEN imageB = mort4B: sensimageB$ = "large3"


    IF spriteB$ = "roulade1" THEN imageB = roulade1B: sensimageB$ = "normal"
    IF spriteB$ = "roulade2" THEN imageB = roulade2B: sensimageB$ = "normal"
    IF spriteB$ = "roulade3" THEN imageB = roulade3B: sensimageB$ = "inverse"
    IF spriteB$ = "roulade4" THEN imageB = roulade2B: sensimageB$ = "inverse"
    IF spriteB$ = "roulade5" THEN imageB = roulade5B: sensimageB$ = "inverse"
    IF spriteB$ = "roulade6" THEN imageB = roulade1B: sensimageB$ = "inverse"


    IF spriteB$ = "deboutR" THEN imageB = deboutB: sensimageB$ = "inverse"
    IF spriteB$ = "assis1R" THEN imageB = assis1B: sensimageB$ = "inverse"
    IF spriteB$ = "assis2R" THEN imageB = assis2B: sensimageB$ = "inverse"
    IF spriteB$ = "attente1R" THEN imageB = attente1B: sensimageB$ = "inverse"
    IF spriteB$ = "attente2R" THEN imageB = attente2B: sensimagesB$ = "inverse"
    IF spriteB$ = "attente3R" THEN imageB = attente3B: sensimagesB$ = "inverse"
    IF spriteB$ = "cou1R" THEN imageB = protegeHB: sensimagesB$ = "inverse"
    IF spriteB$ = "cou2R" THEN imageB = cou2B: sensimagesB$ = "inverse"
    IF spriteB$ = "cou3R" THEN imageB = cou3B: sensimageB$ = "inverse"
    IF spriteB$ = "devant1R" THEN imageB = devant1B: sensimageB$ = "inverse"
    IF spriteB$ = "devant2R" THEN imageB = devant2B: sensimageB$ = "inverse"
    IF spriteB$ = "devant3R" THEN imageB = devant3B: sensimagesB$ = "inverse"
    IF spriteB$ = "genou1R" THEN imageB = genou1B: sensimageB$ = "inverse"
    IF spriteB$ = "genou2R" THEN imageB = assis2B: sensimageB$ = "inverse"
    IF spriteB$ = "genou3R" THEN imageB = genou3B: sensimagesB$ = "inverse"
    IF spriteB$ = "marche1R" THEN imageB = marche1B: sensimageB$ = "inverse"
    IF spriteB$ = "marche2R" THEN imageB = marche2B: sensimageB$ = "inverse"
    IF spriteB$ = "marche3R" THEN imageB = marche3B: sensimageB$ = "inverse"
    IF spriteB$ = "saut1R" THEN imageB = saut1B: sensimagesB$ = "inverse"
    IF spriteB$ = "saut2R" THEN imageB = saut2B: sensimagesB$ = "inverse"
    IF spriteB$ = "vainqueur1R" THEN imageB = vainqueur1B: sensimageB$ = "inverse"
    IF spriteB$ = "vainqueur2R" THEN imageB = vainqueur2B: sensimageB$ = "inverse"
    IF spriteB$ = "vainqueur3R" THEN imageB = vainqueur3B: sensimageB$ = "inverse"
    IF spriteB$ = "retourne1R" THEN imageB = retourne1B: sensimageB$ = "inverse"
    IF spriteB$ = "retourne2R" THEN imageB = retourne2B: sensimageB$ = "inverse"
    IF spriteB$ = "retourne3R" THEN imageB = retourne3B: sensimageB$ = "inverse"
    IF spriteB$ = "front1R" THEN imageB = front1B: sensimagesB$ = "inverse"
    IF spriteB$ = "front2R" THEN imageB = front2B: sensimagesB$ = "inverse"
    IF spriteB$ = "front3R" THEN imageB = front3B: sensimagesB$ = "inverse"
    IF spriteB$ = "toile1R" THEN imageB = toile1B: sensimagesB$ = "inverse"
    IF spriteB$ = "toile2R" THEN imageB = toile2B: sensimagesB$ = "inverse"
    IF spriteB$ = "toile3R" THEN imageB = toile3B: sensimagesB$ = "inverse"
    IF spriteB$ = "toile4R" THEN imageB = toile4B: sensimagesB$ = "inverse"
    IF spriteB$ = "tombe1R" THEN imageB = tombe1B: sensimagesB$ = "inverse"
    IF spriteB$ = "tombe2R" THEN imageB = tombe2B: sensimagesB$ = "inverse"
    IF spriteB$ = "tombe3R" THEN imageB = tombe3B: sensimagesB$ = "inverse"
    IF spriteB$ = "protegeDR" THEN imageB = protegeDB: sensimagesB$ = "inverse"
    IF spriteB$ = "protegeHR" THEN imageB = protegeHB: sensimagesB$ = "inverse"
    IF spriteB$ = "tete1R" THEN imageB = couptete1B: sensimagesB$ = "inverse"
    IF spriteB$ = "tete2R" THEN imageB = couptete2B: sensimageB$ = "inverse"
    IF spriteB$ = "touche1R" THEN imageB = touche2B: sensimageB$ = "inverse"
    IF spriteB$ = "touche2R" THEN imageB = touche1B: sensimageB$ = "inverse"
    IF spriteB$ = "touche3R" THEN imageB = touche2B: sensimageB$ = "inverse"

    IF spriteB$ = "pied1R" THEN imageB = pied1B: sensimagesB$ = "inverse"
    IF spriteB$ = "pied2R" THEN imageB = pied2B: sensimagesB$ = "inverse"
    IF spriteB$ = "decap1R" THEN imageB = decap1B: sensimageB$ = "inverse"
    IF spriteB$ = "decap2R" THEN imageB = decap2B: sensimageB$ = "inverse"
    IF spriteB$ = "decap3R" THEN imageB = decap3B: sensimagesB$ = "inverse"
    IF spriteB$ = "decap4R" THEN imageB = decap4B: sensimagesB$ = "inverse"
    IF spriteB$ = "mort1R" THEN imageB = assis1B: sensimageB$ = "inverse"
    IF spriteB$ = "mort2R" THEN imageB = mort2B: sensimagesB$ = "inverse"
    IF spriteB$ = "mort3R" THEN imageB = mort3B: sensimagesB$ = "inverse"
    IF spriteB$ = "mort4R" THEN imageB = mort4B: sensimagesB$ = "inverse"


    IF spriteB$ = "roulade1R" THEN imageB = roulade1B: sensimageB$ = "inverse"
    IF spriteB$ = "roulade2R" THEN imageB = roulade2B: sensimageB$ = "inverse"
    IF spriteB$ = "roulade3R" THEN imageB = roulade3B: sensimageB$ = "inverse"
    IF spriteB$ = "roulade4R" THEN imageB = roulade2B: sensimageB$ = "normal"
    IF spriteB$ = "roulade5R" THEN imageB = roulade5B: sensimageB$ = "inverse"
    IF spriteB$ = "roulade6R" THEN imageB = roulade1B: sensimageB$ = "normal"

    IF spriteB$ = "sorcier1" THEN imageB = drax1B: sensimageB$ = "inverse"
    IF spriteB$ = "sorcier2" THEN imageB = drax2B: sensimageB$ = "inverse"

    IF spriteB$ = "marianna" THEN imageB = mariannaB: sensimagesB$ = "inverse"


    a4 = (xB - 1) * 8: b4 = ((yFB - 2) * 8)

    IF a4 < 304 THEN
        IF sensimageB$ = "large4" THEN
            _PUTIMAGE (a4 + 41, b4)-(a4 - 31, b4 + 79), imageB ' retirer 31 (4*8)-1  a4
        END IF '

        IF sensimageB$ = "large3" THEN
            _PUTIMAGE (a4 + 40, b4)-(a4 - 23, b4 + 79), imageB ' retirer 23 (3*8)-1  a4
        END IF '                                             attention a gauche a4 serait de 63 (39+24)

        IF sensimageB$ = "large1" THEN
            _PUTIMAGE (a4 + 39, b4)-(a4 - 8, b4 + 79), imageB
        END IF '

        IF sensimageB$ = "normal" THEN
            _PUTIMAGE (a4 + 39, b4)-(a4, b4 + 79), imageB
        END IF
        IF sensimageB$ = "inverse" THEN
            _PUTIMAGE (a4, b4), imageB
        END IF
    END IF

    '                           ***********************************************
    '                           re-affichage du spriteA en cas de chevauchement

    IF joueurA$ = "mort" OR joueurA$ = "mortR" OR joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" OR joueurA$ = "genou" OR joueurA$ = "genouR" THEN


        a2 = (xA - 1) * 8: b2 = ((yFA - 2) * 8)

        IF a2 > 1 AND a2 < 304 THEN

            IF sensimageA$ = "normal" THEN
                _PUTIMAGE (a2, b2), imageA
            END IF

            IF sensimageA$ = "inverse" THEN
                _PUTIMAGE (a2 + 39, b2)-(a2, b2 + 79), imageA
            END IF

            IF sensimageA$ = "large3R" THEN
                _PUTIMAGE (a2 + 40, b2)-(a2 - 23, b2 + 79), imageA ' retirer 23 (3*8)-1  a2
            END IF '                                              attention a gauche a2 serait de 63 (39+24)

            IF sensimageA$ = "large4R" THEN
                _PUTIMAGE (a2 + 41, b2)-(a2 - 31, b2 + 79), imageA ' retirer 31 (4*8)-1  a4
            END IF

            IF sensimageA$ = "large1R" THEN
                _PUTIMAGE (a2 + 39, b2)-(a2 - 8, b2 + 79), imageA
            END IF
        END IF
    END IF


    '                       ****************************************
    '                       ********* affichage du sang ************
    '                       ****************************************

    '                    gicles de sang de decapitation

    IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" THEN
        IF sangdecapA = 1 THEN
            Xgicle = (xA * 8) + 3: Ygicle = (yFA - 1) * 8
            objet = gicle1
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
        IF sangdecapA = 2 THEN
            Xgicle = (xA * 8) + 3: Ygicle = (yFA - 1) * 8
            objet = gicle2
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
        IF sangdecapA = 3 THEN
            Xgicle = (xA * 8) + 3: Ygicle = (yFA - 1) * 8
            objet = gicle3
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF

        IF sangdecapA = 4 THEN
            Xgicle = (xA * 8) + 2: Ygicle = ((yMA - 2) * 8) - 2
            objet = gicle1
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
        IF sangdecapA = 5 THEN
            Xgicle = (xA * 8) + 2: Ygicle = ((yMA - 2) * 8) - 2
            objet = gicle2
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
        IF sangdecapA = 6 THEN
            Xgicle = (xA * 8) + 2: Ygicle = ((yMA - 2) * 8) - 2
            objet = gicle3
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
    END IF

    IF joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN
        IF sangdecapB = 1 THEN
            Xgicle = (xB * 8) + 3: Ygicle = (yFB - 1) * 8
            objet = gicle1
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
        IF sangdecapB = 2 THEN
            Xgicle = (xB * 8) + 3: Ygicle = (yFB - 1) * 8
            objet = gicle2
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
        IF sangdecapB = 3 THEN
            Xgicle = (xB * 8) + 3: Ygicle = (yFB - 1) * 8
            objet = gicle3
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF

        IF sangdecapB = 4 THEN
            Xgicle = (xB * 8) + 1: Ygicle = ((yMB - 2) * 8) - 2
            objet = gicle1
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
        IF sangdecapB = 5 THEN
            Xgicle = (xB * 8) + 1: Ygicle = ((yMB - 2) * 8) - 2
            objet = gicle2
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
        IF sangdecapB = 6 THEN
            Xgicle = (xB * 8) + 1: Ygicle = ((yMB - 2) * 8) - 2
            objet = gicle3
            _PUTIMAGE (Xgicle, Ygicle), objet
        END IF
    END IF

    '                           taches de sang au combat

    IF sangA$ = "non" THEN GOTO sang2


    IF joueurA$ = "touche1" OR joueurA$ = "touche1R" OR joueurA$ = "mort" THEN
        xS1 = xA: yS1 = yAttB
    END IF

    IF joueurA$ = "tombe1" OR joueurA$ = "tombe1R" OR joueurA$ = "mortR" THEN
        xS1 = xA: yS1 = yAttB
    END IF

    xS2 = xS1 * 8: yS2 = yS1 * 8
    objet = tachesang
    _PUTIMAGE (xS2, yS2), objet


    sang2:

    IF sangB$ = "non" THEN GOTO serpent


    IF joueurB$ = "touche1" OR joueurB$ = "touche1R" OR joueurB$ = "mort" THEN
        xS1 = xB + 1: yS1 = yAttA
    END IF

    IF joueurB$ = "tombe1" OR joueurB$ = "tombe1R" OR joueurB$ = "mortR" THEN
        xS1 = xB + 1: yS1 = yAttA
    END IF

    xS2 = xS1 * 8: yS2 = yS1 * 8
    objet = tachesang
    _PUTIMAGE (xS2, yS2), objet


    '                       ****************************************
    '                       ********* affichage du serpent *********
    '                       ****************************************
    serpent:


    IF entree$ = "oui" THEN
        objet2 = serpent1
        IF xA = 3 THEN objet2 = serpent2
        IF xA = 4 THEN objet2 = serpent3
        IF xA = 5 THEN objet2 = serpent2
        IF xA = 6 THEN objet2 = serpent1
        _PUTIMAGE (11, 22), objet2
        objet2 = serpent1
        IF xB = 34 THEN objet2 = serpent2
        IF xB = 33 THEN objet2 = serpent3
        IF xB = 32 THEN objet2 = serpent2
        IF xB = 31 THEN objet2 = serpent1
        _PUTIMAGE (306, 22)-(275, 54), objet2
        GOTO arbres
    END IF

    IF entreesorcier$ = "oui" THEN
        IF xA = 35 THEN objet2 = serpent3
        IF xA = 34 THEN objet2 = serpent2
        IF xA = 33 THEN objet2 = serpent1
        _PUTIMAGE (11, 22), objet2
        IF xA = 35 THEN objet2 = serpent3
        IF xA = 34 THEN objet2 = serpent2
        IF xA = 33 THEN objet2 = serpent1
        _PUTIMAGE (306, 22)-(275, 54), objet2
        GOTO arbres
    END IF

    '                                   affichage serpentA

    IF serpentA$ = "non" THEN GOTO serpent2

    IF spriteA$ = "touche1" OR spriteA$ = "touche1R" THEN
        objet2 = serpent2
        _PUTIMAGE (11, 22), objet2
    END IF
    IF spriteA$ = "touche2" OR spriteA$ = "touche2R" THEN
        objet2 = serpent3
        _PUTIMAGE (11, 22), objet2
    END IF
    IF spriteA$ = "touche3" OR spriteA$ = "touche3R" THEN
        objet2 = serpent2
        _PUTIMAGE (11, 22), objet2
    END IF
    IF spriteA$ = "touche4" OR spriteA$ = "touche4R" THEN
        objet2 = serpent1
        _PUTIMAGE (11, 22), objet2
    END IF


    IF spriteA$ = "tombe1" OR spriteA$ = "tombe1R" THEN
        objet2 = serpent2
        _PUTIMAGE (11, 22), objet2
    END IF
    IF spriteA$ = "tombe2" OR spriteA$ = "tombe2R" THEN
        objet2 = serpent3
        _PUTIMAGE (11, 22), objet2
    END IF
    IF spriteA$ = "tombe3" OR spriteA$ = "tombe3R" THEN
        objet2 = serpent2
        _PUTIMAGE (11, 22), objet2
    END IF
    IF spriteA$ = "tombe4" OR spriteA$ = "tombe4R" THEN
        objet2 = serpent1
        _PUTIMAGE (11, 22), objet2
    END IF


    serpent2:

    '                                   affichage serpentB

    IF serpentB$ = "non" THEN GOTO tete2

    IF spriteB$ = "touche1" OR spriteB$ = "touche1R" THEN
        objet2 = serpent2
        _PUTIMAGE (306, 22)-(275, 54), objet2
    END IF
    IF spriteB$ = "touche2" OR spriteB$ = "touche2R" THEN
        objet2 = serpent3
        _PUTIMAGE (306, 22)-(275, 54), objet2
    END IF
    IF spriteB$ = "touche3" OR spriteB$ = "touche3R" THEN
        objet2 = serpent2
        _PUTIMAGE (306, 22)-(275, 54), objet2
    END IF
    IF spriteB$ = "touche4" OR spriteB$ = "touche4R" THEN
        objet2 = serpent1
        _PUTIMAGE (306, 22)-(275, 54), objet2
    END IF

    IF spriteB$ = "tombe1" OR spriteB$ = "tombe1R" THEN
        objet2 = serpent2
        _PUTIMAGE (306, 22)-(275, 54), objet2
    END IF
    IF spriteB$ = "tombe2" OR spriteB$ = "tombe2R" THEN
        objet2 = serpent3
        _PUTIMAGE (306, 22)-(275, 54), objet2
    END IF
    IF spriteB$ = "tombe3" OR spriteB$ = "tombe3R" THEN
        objet2 = serpent2
        _PUTIMAGE (306, 22)-(275, 54), objet2
    END IF
    IF spriteB$ = "tombe4" OR spriteB$ = "tombe4R" THEN
        objet2 = serpent1
        _PUTIMAGE (306, 22)-(275, 54), objet2
    END IF



    '                       ****************************************
    '                       ********* affichage des tetes **********
    '                       ****************************************
    tete2:

    IF gnome$ = "oui" THEN

        IF joueurA$ = "mort" OR joueurB$ = "mort" OR joueurA$ = "mortR" OR joueurB$ = "mortR" THEN GOTO gnome2

        IF football$ = "oui" THEN GOTO gnometapetete

        IF xGNOME < 33 AND (xGNOME * 8) > xSPRt - 24 THEN football$ = "oui": reftempsB = temps
        GOTO afficheteombre

        gnometapetete:
        IF football$ = "oui" THEN

            IF temps > reftempsB + 113 THEN GOTO afficheteombre
            IF temps > reftempsB + 112 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 5: GOTO afficheteombre
            IF temps > reftempsB + 106 THEN GOTO afficheteombre
            IF temps > reftempsB + 105 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 6: GOTO afficheteombre
            IF temps > reftempsB + 98 THEN GOTO afficheteombre
            IF temps > reftempsB + 97 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 1: GOTO afficheteombre
            IF temps > reftempsB + 91 THEN GOTO afficheteombre
            IF temps > reftempsB + 90 THEN ySPRt = 159: xSPRt = xSPRt + 16: numerotete = 2: GOTO afficheteombre
            IF temps > reftempsB + 83 THEN GOTO afficheteombre
            IF temps > reftempsB + 82 THEN
                IF xGNOME < 273 AND xSPRt < 273 THEN _SNDPLAY tete
                ySPRt = 159: xSPRt = xSPRt + 16: numerotete = 3: GOTO afficheteombre
            END IF
            IF temps > reftempsB + 76 THEN GOTO afficheteombre
            IF temps > reftempsB + 75 THEN ySPRt = 157: xSPRt = xSPRt + 16: numerotete = 4: GOTO afficheteombre
            IF temps > reftempsB + 68 THEN GOTO afficheteombre
            IF temps > reftempsB + 67 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 5: GOTO afficheteombre
            IF temps > reftempsB + 61 THEN GOTO afficheteombre
            IF temps > reftempsB + 60 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 6: GOTO afficheteombre
            IF temps > reftempsB + 53 THEN GOTO afficheteombre
            IF temps > reftempsB + 52 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 1: GOTO afficheteombre
            IF temps > reftempsB + 46 THEN GOTO afficheteombre
            IF temps > reftempsB + 45 THEN ySPRt = 159: xSPRt = xSPRt + 16: numerotete = 2: GOTO afficheteombre
            IF temps > reftempsB + 38 THEN GOTO afficheteombre
            IF temps > reftempsB + 37 THEN
                IF xGNOME < 273 AND xSPRt < 273 THEN _SNDPLAY tete
                ySPRt = 159: xSPRt = xSPRt + 16: numerotete = 3: GOTO afficheteombre
            END IF
            IF temps > reftempsB + 31 THEN GOTO afficheteombre
            IF temps > reftempsB + 30 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 4: GOTO afficheteombre
            IF temps > reftempsB + 23 THEN GOTO afficheteombre
            IF temps > reftempsB + 22 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 5: GOTO afficheteombre
            IF temps > reftempsB + 16 THEN GOTO afficheteombre
            IF temps > reftempsB + 15 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 6: GOTO afficheteombre
            IF temps > reftempsB + 8 THEN GOTO afficheteombre
            IF temps > reftempsB + 7 THEN ySPRt = 151: xSPRt = xSPRt + 16: numerotete = 1: GOTO afficheteombre
            IF temps > reftempsB + 5 THEN GOTO afficheteombre
            IF temps > reftempsB + 4 THEN ySPRt = 153: xSPRt = xSPRt + 16: numerotete = 2: GOTO afficheteombre
            IF temps > reftempsB + 2 THEN GOTO afficheteombre
            IF temps > reftempsB + 1 THEN
                IF xGNOME < 273 AND xSPRt < 273 THEN _SNDPLAY teteX
                GOTO afficheteombre
            END IF

        END IF

        afficheteombre:
        IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" THEN
            IF numerotete = 1 THEN objet = tete1A
            IF numerotete = 2 THEN objet = tete2A
            IF numerotete = 3 THEN objet = tete3A
            IF numerotete = 4 THEN objet = tete4A
            IF numerotete = 5 THEN objet = tete5A
            IF numerotete = 6 THEN objet = tete6A
        END IF

        IF joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN
            IF numerotete = 1 THEN objet = tete1B
            IF numerotete = 2 THEN objet = tete2B
            IF numerotete = 3 THEN objet = tete3B
            IF numerotete = 4 THEN objet = tete4B
            IF numerotete = 5 THEN objet = tete5B
            IF numerotete = 6 THEN objet = tete6B
        END IF


        IF xSPRt < 320 THEN _PUTIMAGE (xSPRt, 175), spriteombre

        IF xSPRt < 320 THEN _PUTIMAGE (xSPRt, ySPRt), objet


        GOTO gnome2
    END IF

    IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" OR joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN

        IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" THEN
            IF numerotete = 1 THEN objet = tete1A
            IF numerotete = 2 THEN objet = tete2A
            IF numerotete = 3 THEN objet = tete3A
            IF numerotete = 4 THEN objet = tete4A
            IF numerotete = 5 THEN objet = tete5A
            IF numerotete = 6 THEN objet = tete6A
        END IF

        IF joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN
            IF numerotete = 1 THEN objet = tete1B
            IF numerotete = 2 THEN objet = tete2B
            IF numerotete = 3 THEN objet = tete3B
            IF numerotete = 4 THEN objet = tete4B
            IF numerotete = 5 THEN objet = tete5B
            IF numerotete = 6 THEN objet = tete6B
        END IF

        xSPRt = (xSPRt - 1) * 8 ' laisser en 8 pour le football :)

        ySPRt = ySPRt + 7

        IF xSPRt < 320 THEN _PUTIMAGE (xSPRt, 175), spriteombre

        IF xSPRt < 320 THEN _PUTIMAGE (xSPRt, ySPRt), objet

    END IF



    '                       ****************************************
    '                       ********* affichage du gnome  **********
    '                       ****************************************
    gnome2:

    IF gnome$ = "oui" THEN

        IF xGNOME > 39 THEN
            'xGNOME = 39
            IF joueurB$ = "mortdecap" OR joueurB$ = "mortdecapR" THEN
                IF partie$ = "vs" THEN bonusA$ = "oui"
                IF partie$ = "solo" THEN
                    IF xB >= 40 THEN sortieA$ = "oui": Aoccupe$ = "non"
                END IF
            END IF
            IF joueurB$ = "mort" OR joueurB$ = "mortR" THEN
                IF partie$ = "vs" THEN bonusA$ = "oui"
                IF partie$ = "solo" THEN
                    IF xB >= 40 THEN sortieA$ = "oui": Aoccupe$ = "non"
                END IF
            END IF

            IF joueurA$ = "mortdecap" OR joueurA$ = "mortdecapR" THEN
                IF partie$ = "vs" THEN bonusB$ = "oui"
                IF partie$ = "solo" THEN
                    IF xA >= 40 THEN sortieB$ = "oui": Boccupe$ = "non"
                END IF
            END IF
            IF joueurA$ = "mort" OR joueurA$ = "mortR" THEN
                IF partie$ = "vs" THEN bonusB$ = "oui"
                IF partie$ = "solo" THEN
                    IF xA >= 40 THEN sortieB$ = "oui": Boccupe$ = "non"
                END IF
            END IF


        END IF

        IF numerognome = 1 THEN objet = gnome1
        IF numerognome = 2 THEN objet = gnome2
        IF numerognome = 3 THEN objet = gnome3
        IF numerognome = 4 THEN objet = gnome4
        IF numerognome = 5 THEN objet = gnomerire1
        IF numerognome = 6 THEN objet = gnomerire2

        xGNOME2 = ((xGNOME - 1) * 8)

        IF xGNOME < 40 THEN _PUTIMAGE (xGNOME2, 152), objet

    END IF


    '  gnome rigole

    IF joueurA$ = "mortdecap" OR joueurA$ = "mort" THEN
        IF xGNOME > xA + 3 THEN
            sonrigole$ = "oui"
            gnomerigole$ = "oui"
        END IF
    END IF

    IF joueurA$ = "mortdecapR" OR joueurA$ = "mortR" THEN
        IF xGNOME > xA THEN
            sonrigole$ = "oui"
            gnomerigole$ = "oui"
        END IF
    END IF

    IF joueurB$ = "mortdecap" OR joueurB$ = "mort" THEN
        IF xGNOME > xB THEN
            sonrigole$ = "oui"
            gnomerigole$ = "oui"
        END IF
    END IF

    IF joueurB$ = "mortdecapR" OR joueurB$ = "mortR" THEN
        IF xGNOME > xB + 3 THEN
            sonrigole$ = "oui"
            gnomerigole$ = "oui"
        END IF
    END IF



    ' cadavre tir par le gnome

    IF joueurA$ = "mortdecap" OR joueurA$ = "mort" THEN
        IF xGNOME > xA + 5 THEN
            gnometire$ = "non"
            xA = xA + 1
        END IF
    END IF
    IF joueurA$ = "mortdecapR" OR joueurA$ = "mortR" THEN
        IF xGNOME > xA + 4 THEN
            gnometire$ = "non"
            xA = xA + 1
        END IF
    END IF

    IF joueurB$ = "mortdecap" OR joueurB$ = "mort" THEN
        IF xGNOME > xB + 4 THEN
            gnometire$ = "non"
            xB = xB + 1
        END IF
    END IF
    IF joueurB$ = "mortdecapR" OR joueurB$ = "mortR" THEN
        IF xGNOME > xB + 5 THEN
            gnometire$ = "non"
            xB = xB + 1
        END IF
    END IF



    '                       ****************************************
    '                       ********* affichage des arbres**********
    '                       ****************************************
    arbres:

    IF xA < 6 OR xB < 6 OR gnome$ = "oui" AND xGNOME < 12 THEN
        _PUTIMAGE (0, 104), arbreG
    END IF


    IF xB > 29 OR xA > 29 OR xGNOME > 32 OR xSPRt > 263 THEN
        _PUTIMAGE (272, 104), arbreD
    END IF


    '                       ****************************************
    '                       ************ affichage du feu **********
    '                       ****************************************


    IF jeu$ = "encours" AND sorcier$ = "oui" AND xAttB > xB + 5 THEN

        xfeu = (xAttB - 2) * 8: yfeu = yAttB * 8

        IF xAttB = 14 OR xAttB = 23 OR xAttB = 32 THEN
            objet = feu1
            _PUTIMAGE (xfeu, yfeu), objet
        END IF

        IF xAttB = 17 OR xAttB = 26 AND xAttB < xB + 20 THEN
            objet = feu2
            _PUTIMAGE (xfeu, yfeu), objet
        END IF

        IF xAttB = 20 OR xAttB = 29 THEN
            objet = feu3
            _PUTIMAGE (xfeu, yfeu), objet
        END IF

    END IF



    '                       ****************************************
    '                       ********* jeu gagn - jeu perdu ********
    '                       ****************************************


    IF jeu$ = "gagne" THEN
        ' cache marianna
        LINE (186, 95)-(200, 114), _RGB(0, 0, 0), BF
        LINE (185, 113)-(201, 114), _RGB(0, 0, 0), BF

        COLOR _RGB(0, 0, 0), _RGB(34, 34, 153)
        _FONT 8
        _PRINTMODE _FILLBACKGROUND
        LOCATE 10, 12: PRINT "Thanks big boy."


    END IF

    IF jeu$ = "perdu" AND joueurA$ = "sorcierFINI" THEN
        COLOR _RGB(0, 0, 0), _RGB(34, 34, 153)
        _FONT 8
        _PRINTMODE _FILLBACKGROUND
        LOCATE 10, 11: PRINT "Your end has come!"

    END IF

    _DISPLAY
    _LIMIT 50 ' nombre de boucles a la seconde



    '                        gestion du temps et retour



    IF arret$ = "oui" THEN

        IF jeu$ = "encours" THEN
            _SNDSTOP mortdecap: _SNDSTOP mortKO: _SNDSTOP prepare
            scoreA = 0: scoreB = 0
            GOTO menu
        END IF


        IF jeu$ = "gagne" OR jeu$ = "perdu" THEN
            IA = 0: scoreA = 0: scoreB = 0
            sorcier$ = "non": jeu$ = "encours"
            GOTO menu
        END IF

    END IF

LOOP
