DO
    debut:

    IF ... THEN GOTO degats
    IF ... THEN GOTO menu
    IF ... THEN GOTO debut
    IF ... THEN GOTO variable
    IF ... THEN GOTO clavier
    IF ... THEN GOTO clavierB
    IF ... THEN GOTO gnome

    degats:

    IF ... THEN GOTO gestion
    IF ... THEN GOTO clavier

    clavier:

    IF ... THEN GOTO action
    IF ... THEN GOTO gestion
    IF ... THEN GOTO menu

    action:

    IF ... GOTO gestion

    gestion:

    IF ... THEN GOTO joueur2
    IF ... THEN GOTO gestion
    IF ... THEN GOTO finderoulade

    finderoulade:

    IF ... THEN GOTO joueur2
    IF ... THEN GOTO affichage
    IF ... THEN GOTO gestion
    IF ... THEN GOTO finderouladeR

    finderouladeR:
    IF ... THEN GOTO joueur2
    IF ... THEN GOTO affichage
    IF ... THEN GOTO gestion
    IF ... THEN GOTO colision
    IF ... THEN GOTO mort

    mort:
    IF ... THEN GOTO joueur2

    joueur2:
    'debut joueur 2
    IF ... THEN GOTO debut
    IF ... THEN GOTO gestionB
    IF ... THEN GOTO clavierB

    clavierB:
    IF ... THEN GOTO actionB
    IF ... THEN GOTO gestionB

    GOTO gestionB

    actionB:
    IF ... THEN GOTO gestionB

    gestionB:
    IF ... THEN GOTO colision
    IF ... THEN GOTO gestionB
    IF ... THEN GOTO finderouladeB

    finderouladeB:
    IF ... THEN GOTO colision
    IF ... THEN GOTO affichage
    IF ... THEN GOTO finderouladeBR
    IF ... THEN GOTO gestionB

    finderouladeBR:
    IF ... THEN GOTO colision
    IF ... THEN GOTO affichage
    IF ... THEN GOTO gestionB
    IF ... THEN GOTO mortB

    mortB:
    IF ... THEN GOTO colision

    colision:
    IF ... GOTO colisionR
    IF ... THEN GOTO sortiecadre

    sortiecadre:

    IF ... THEN GOTO tetesvolantes

    GOTO tetesvolantes
    ' ???
    IF sens$ = "normal" THEN GOTO affichage

    colisionR:
    IF ... THEN GOTO sortiecadreR

    sortiecadreR:
    IF ... THEN GOTO tetesvolantes

    tetesvolantes:
    IF ... THEN GOTO affichage
    IF ... THEN
        IF ... THEN GOTO teteagauche
        teteagauche:
        IF ... THEN GOTO affichage
    END IF

    gnome:
    IF ... THEN GOTO affichage

    affichage:
    IF ... THEN GOTO affichetemps

    affichetemps:
    IF ... THEN GOTO sang2

    sang2:
    IF ... THEN GOTO serpent

    serpent:
    IF ... THEN GOTO arbres
    IF ... THEN GOTO serpent2

    serpent2:
    IF ... THEN GOTO tete2

    tete2:
    IF gnome$ = "oui" THEN
        IF ... THEN GOTO gnome2
        IF football$ = "oui" THEN GOTO gnometapetete
        GOTO afficheteombre

        gnometapetete:
        IF football$ = "oui" THEN
            IF ... THEN GOTO afficheteombre
        END IF

        afficheteombre:
        GOTO gnome2
    END IF

    gnome2:
    arbres:

    IF ... THEN GOTO menu
LOOP