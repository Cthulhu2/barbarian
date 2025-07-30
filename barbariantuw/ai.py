from barbariantuw import Levier, State
from barbariantuw.sprites import Barbarian


# *****************************************
# ******* Intelligence Artificielle *******
# *****************************************
def demo_joueurA(ja: Barbarian, jb: Barbarian, temps):
    distance = abs(ja.xLoc - jb.xLoc)
    if distance >= 15:  # quand trop loin
        ja.occupe_state(State.rouladeAV, temps)

    elif distance == 12 and jb.anims == 'debout':
        ja.occupe_state(State.decapite, temps)

    elif distance == 9:
        if jb.attente > 100:
            ja.occupe_state(State.decapite, temps)
        elif jb.state == State.rouladeAR:
            ja.occupe_state(State.genou, temps)
        elif jb.occupe:
            ja.occupe_state(State.rouladeAV, temps)
        else:
            return False

    elif 6 < distance < 9:  # distance de combat 1
        # pour se rapprocher
        if jb.state == State.rouladeAR:
            ja.occupe_state(State.genou, temps)
        elif jb.levier == Levier.gauche:
            ja.occupe_state(State.araignee, temps)
        elif jb.state == State.front:
            ja.state = State.protegeH
            ja.reftemps = temps
        # pour eviter les degats repetitifs
        elif ja.infoDegatG > 4 and jb.state in (State.assis2, State.genou):
            ja.occupe_state(State.genou, temps)
        elif ja.infoDegatG > 2 and jb.state in (State.assis2, State.genou):
            ja.occupe_state(State.rouladeAV, temps)
        elif ja.infoDegatT > 2 and jb.state == State.cou:
            ja.occupe_state(State.genou, temps)
        elif ja.infoDegatF > 2 and jb.state == State.front:
            ja.occupe_state(State.rouladeAV, temps)
        # pour alterner les attaques
        elif ja.infoCoup == 0:
            ja.infoCoup += 1
            ja.occupe_state(State.devant, temps)
        elif ja.infoCoup == 1:
            ja.infoCoup += 1
            ja.occupe_state(State.front, temps)
        elif ja.infoCoup == 2:
            ja.infoCoup += 1
            ja.occupe_state(State.araignee, temps)
        elif ja.infoCoup == 3:
            ja.infoCoup += 1
            ja.occupe_state(State.araignee, temps)
        elif ja.infoCoup == 4:
            ja.infoCoup += 1
            ja.occupe_state(State.cou, temps)
        elif ja.infoCoup == 5:
            ja.infoCoup = 0
            ja.levier = ja.avance_levier()
            ja.action(temps)
        else:
            return False

    elif distance <= 6:
        if jb.state == State.devant:
            ja.state = State.protegeD
            ja.reftemps = temps
        elif ja.infoDegatG > 4 and jb.state in (State.assis2, State.genou):
            ja.occupe_state(State.genou, temps)
        elif ja.infoDegatG > 2 and jb.state in (State.assis2, State.genou,
                                                State.coupdepied):
            ja.occupe_state(State.rouladeAV, temps)
        elif ja.infoCoup == 0:
            ja.infoCoup += 1
            ja.occupe_state(State.genou, temps)
        elif ja.infoCoup == 1:
            ja.infoCoup += 1
            ja.occupe_state(State.coupdetete, temps)
        elif ja.infoCoup == 2:
            ja.infoCoup += 1
            ja.occupe_state(State.araignee, temps)
        elif ja.infoCoup == 3:
            ja.infoCoup += 1
            ja.occupe_state(State.genou, temps)
        elif ja.infoCoup == 4:
            ja.infoCoup += 1
            ja.occupe_state(State.coupdepied, temps)
        elif ja.infoCoup == 5:
            ja.infoCoup = 0
            ja.levier = ja.avance_levier()
            ja.action(temps)
        else:
            return False
    return True


def joueurB(demo: bool, lvl: int, ja: Barbarian, jb: Barbarian, temps):
    distance = abs(jb.xLoc - ja.xLoc)
    # ***************************IA de 1,2,3,6
    if lvl in (0, 1, 2, 3, 6):
        if distance >= 15:
            # quand trop loin
            jb.occupe_state(State.rouladeAV, temps)
            return True
        if lvl == 6:
            if distance < 15:
                if ja.state == State.decapite:
                    jb.occupe_state(State.genou, temps)
                    return True
        if lvl == 3:
            if distance < 15:
                if jb.infoDegatT > 2:
                    if ja.state == State.decapite:
                        jb.state = State.assis2
                        return True
                if ja.state == State.decapite:
                    jb.state = State.protegeD
                    jb.reftemps = temps
                    return True
        if distance == 12 and ja.state == State.debout:
            jb.occupe_state(State.decapite, temps)
            return True
        if 9 < distance < 15:  # pour se rapprocher
            if ja.levier == ja.recule_levier():
                jb.state = State.debout
                return True
            jb.levier = jb.avance_levier()
        elif distance == 9:
            if ja.attente > 100:
                jb.levier = jb.avance_levier()
            elif ja.state == State.rouladeAR:
                jb.occupe_state(State.devant, temps)
                return True
            elif ja.occupe:
                jb.levier = jb.avance_levier()
        elif 6 < distance < 9:  # distance de combat 1
            # pour autoriser les croisements
            if not demo and ja.state == State.rouladeAV:
                jb.occupe_state(State.saute, temps)
                return True
            # pour se rapprocher
            if ja.state == State.rouladeAR:
                jb.occupe_state(State.genou, temps)
                return True
            if ja.levier == ja.recule_levier():
                jb.occupe_state(State.araignee, temps)
                return True
            # pour eviter les degats repetitifs
            if lvl > 1:
                if jb.infoDegatG > 4:
                    if ja.state in (State.assis2, State.genou):
                        jb.occupe_state(State.genou, temps)
                        return True
                if jb.infoDegatG > 2:
                    if ja.state in (State.assis2, State.rouladeAV):
                        jb.occupe_state(State.rouladeAV, temps)
                        return True
                if jb.infoDegatT > 2:
                    if ja.state == State.cou:
                        jb.occupe_state(State.rouladeAV, temps)
                        return True
                if jb.infoDegatF > 2:
                    if ja.state == State.front:
                        jb.occupe_state(State.rouladeAV, temps)
                        return True
            # pour alterner les attaques
            if jb.infoCoup == 0:
                jb.occupe_state(State.coupdepied, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 1:
                jb.occupe_state(State.debout, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 2:
                jb.occupe_state(State.araignee, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 3:
                jb.occupe_state(State.debout, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 4:
                jb.occupe_state(State.assis2, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 5:
                jb.occupe_state(State.genou, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup in (6, 7):
                jb.levier = jb.avance_levier()
                jb.infoCoup = 0
        elif distance <= 6:
            # pour autoriser les croisements
            if not demo and ja.state == State.saute:
                jb.occupe_state(State.rouladeAV, temps)
                return True
            if lvl == 3:
                if ja.state == State.devant:
                    jb.state = State.protegeD
                    jb.reftemps = temps
                    return True
            if lvl == 2:
                if ja.state == State.genou:
                    jb.occupe_state(State.saute, temps)
                    return True
            if lvl > 1:
                if jb.infoDegatG > 4:
                    if ja.state in (State.assis2, State.genou):
                        if jb.rtl:
                            jb.occupe_state(State.coupdepied, temps)
                        else:
                            jb.occupe_state(State.genou, temps)
                        return True
                    if lvl > 2:
                        if ja.state == State.araignee:
                            jb.occupe_state(State.araignee, temps)
                            return True
                if jb.infoDegatG > 2:
                    if ja.state == State.coupdepied:
                        jb.occupe_state(State.rouladeAV, temps)
                        return True
                    if jb.rtl:
                        if ja.state in (State.assis2, State.genou):
                            jb.occupe_state(State.rouladeAV, temps)
                            return True
                    else:
                        if ja.state in (State.assis2, State.coupdepied):
                            jb.occupe_state(State.genou, temps)
                            return True

            if jb.infoCoup == 0:
                jb.occupe_state(State.coupdepied, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 1:
                jb.occupe_state(State.coupdetete, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 2:
                jb.occupe_state(State.araignee, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 3:
                jb.occupe_state(State.debout, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 4:
                jb.occupe_state(State.assis2, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 5:
                jb.occupe_state(State.genou, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 6:
                jb.occupe_state(State.debout, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 7:
                jb.levier = jb.avance_levier()
                jb.infoCoup = 0
    elif lvl in (4, 5, 7):
        if distance >= 15:  # quand trop loin
            jb.occupe_state(State.rouladeAV, temps)
            return True
        if distance < 15:
            if lvl == 7:
                if ja.state == State.decapite:
                    jb.occupe_state(State.rouladeAV, temps)
                    return True
        if distance == 12 and ja.state == State.debout:
            jb.occupe_state(State.decapite, temps)
            return True
        if 9 < distance < 15:  # pour se rapprocher
            if ja.levier == ja.recule_levier():
                jb.state = State.debout
                return True
            jb.levier = jb.avance_levier()
        elif distance == 9:
            if ja.attente > 100:
                jb.occupe_state(State.decapite, temps)
                return True
            if demo:
                if jb.rtl:
                    if ja.attente > 25:
                        jb.occupe_state(State.decapite, temps)
                        return True
                else:
                    if ja.attente > 100:
                        jb.occupe_state(State.decapite, temps)
                        return True
            if ja.state == State.rouladeAR:
                jb.occupe_state(State.genou, temps)
                return True
            if lvl < 7:
                if ja.occupe:
                    jb.occupe_state(State.rouladeAV, temps)
                    return True
            if lvl == 7:
                if ja.occupe:
                    jb.levier = jb.avance_levier()
        elif 6 < distance < 9:  # distance de combat 1
            # pour autoriser les croisements
            if not demo and ja.state == State.rouladeAV:
                jb.occupe_state(State.saute, temps)
                return True
            # pour se rapprocher
            if ja.state == State.rouladeAR:
                jb.occupe_state(State.genou, temps)
                return True
            if ja.levier == ja.recule_levier():
                jb.occupe_state(State.araignee, temps)
                return True
            # plus l'IA est forte, plus il y des des coups imposs avant infocoupB ou infodegat
            if lvl == 5:
                if ja.state == State.front:
                    jb.state = State.protegeH
                    jb.reftemps = temps
                    return True
            # pour eviter les degats repetitifs
            if jb.infoDegatG > 4:
                if ja.state in (State.assis2, State.genou, State.araignee):
                    jb.occupe_state(State.araignee, temps)
                    return True
            if jb.infoDegatG > 2:
                if ja.state in (State.assis2, State.genou, State.araignee):
                    jb.occupe_state(State.rouladeAV, temps)
                    return True
            if jb.infoDegatT > 2:
                if ja.state == State.cou:
                    jb.occupe_state(State.genou, temps)
                    return True
            if jb.infoDegatF > 2:
                if lvl < 7:
                    if ja.state == State.front:
                        jb.occupe_state(State.rouladeAV, temps)
                        return True
            # pour alterner les attaques
            if jb.infoCoup == 0:
                jb.occupe_state(State.devant, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 1:
                jb.occupe_state(State.front, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 2:
                jb.occupe_state(State.araignee, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 3:
                jb.occupe_state(State.araignee, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 4:
                jb.occupe_state(State.cou, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 5:
                jb.levier = jb.avance_levier()
                jb.infoCoup = 0
        elif distance <= 6:
            # pour autoriser les croisements
            if not demo and ja.state == State.saute:
                jb.occupe_state(State.rouladeAV, temps)
                return True
            if lvl > 4:
                if ja.state == State.devant:
                    jb.state = State.protegeD
                    jb.reftemps = temps
                    return True
            if 4 < lvl < 7:
                if ja.state == State.genou:
                    jb.occupe_state(State.saute, temps)
                    return True
            if jb.infoDegatG > 4:
                if ja.state in (State.assis2, State.genou, State.araignee):
                    jb.occupe_state(State.araignee, temps)
                    return True
            if jb.infoDegatG > 2:
                if ja.state in (State.assis2, State.genou, State.araignee,
                                State.coupdepied):
                    jb.occupe_state(State.rouladeAV, temps)
                    return True
            if jb.infoCoup == 0:
                jb.occupe_state(State.coupdepied, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 1:
                jb.occupe_state(State.coupdetete, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 2:
                jb.occupe_state(State.araignee, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 3:
                jb.occupe_state(State.genou, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 4:
                jb.occupe_state(State.genou, temps)
                jb.infoCoup += 1
                return True
            if jb.infoCoup == 5:
                jb.levier = jb.avance_levier()
                jb.infoCoup = 0
    return False
