import sys
from collections import OrderedDict


##############################


def poenostavi(formula, vrednosti):
    # funkcija poenostavi formulo in vanjo vstavi
    # podane vrednosti

    # zgeneriramo slovar, da nimamo negacije spremenljivk,
    # ampak le posamezne spremenljivke
    vrednosti2 = dict()
    for k, v in vrednosti.items():
        if '-' in k:
            k = k.replace('-', '')
            vrednosti2[k] = not v
        else:
            vrednosti2[k] = v

    vrednosti = vrednosti2

    # vstavimo vrednosti v formulo
    novaFormula = []
    if formula == []:
        return True, vrednosti

    for clause in formula:
        if not clause:
            # če je prazen seznam
            return False, vrednosti
        novClause = []
        for term in clause:
            novTerm = term
            lit = term.replace("-", "")
            if lit in vrednosti:
                if "-" in term:
                    novTerm = not vrednosti[lit]
                else:
                    novTerm = vrednosti[lit]
            novClause.append(novTerm)
        novaFormula.append(novClause)

    # formulo z vrednostmi poenostavimo
    evaluatedFormula = []
    for clause in novaFormula:
        novClause = []
        k = 0
        for x in clause:
            if x:
                novClause.append(x)
                if x == True:
                    k += 1


        # če je clause prazen
        if not novClause:
            return False, vrednosti
        if k == 0:
            evaluatedFormula.append(novClause)
    return [x for x in evaluatedFormula if x != True], vrednosti


##############################
## DPLL:

def dpll(formula, vrednosti):
    pomozne = OrderedDict(dict())
    while True:
        # na dani formuli izvedemo dpll algoritem
        nova_formula, nove_vrednosti = poenostavi(formula, vrednosti)


        weDone = False

        if nova_formula == True or nova_formula == []:
            return True, nove_vrednosti


        elif nova_formula == False or nova_formula == [[]]:
            if not pomozne:
                return False, print('ni rešitve')
            zadnji_dodan = next(reversed(pomozne))
            while pomozne[zadnji_dodan][3]:
                del pomozne[zadnji_dodan]
                if not pomozne:
                    return False, print('ni rešitve')
            
                zadnji_dodan = next(reversed(pomozne))
            vr_zadnjega = not pomozne[zadnji_dodan][0]
            zadnja_formula = pomozne[zadnji_dodan][1]
            zadnje_vrednosti = pomozne[zadnji_dodan][2]
            zadnje_vrednosti[zadnji_dodan] = vr_zadnjega
            pomozne[zadnji_dodan] = (vr_zadnjega, zadnja_formula, zadnje_vrednosti, True)
            formula, vrednosti = zadnja_formula, zadnje_vrednosti
            weDone = True
        
                
        if not weDone:
            dolžine = []
            for clause in nova_formula:
                dolžine.append(len(clause))

            if 1 in dolžine:
                for clause in nova_formula:
                    if len(clause) == 1:
                        for x in clause:
                            nov = x.replace('-', '')
                            if nov in nove_vrednosti:
                                if '-' in x:
                                    vr = False
                                else:
                                    vr = True

                                if vr!= nove_vrednosti[nov]:
                                    if not pomozne:
                                        return False, print('ni rešitve')
                                    zadnji_dodan = next(reversed(pomozne))
                                    while pomozne[zadnji_dodan][3]:
                                        del pomozne[zadnji_dodan]
                                        if not pomozne:
                                            return False, print('ni rešitve')
                                        zadnji_dodan = next(reversed(pomozne))
                
                                    vr_zadnjega = not pomozne[zadnji_dodan][0]
                                    zadnja_formula = pomozne[zadnji_dodan][1]
                                    zadnje_vrednosti = pomozne[zadnji_dodan][2]
                                    zadnje_vrednosti[zadnji_dodan] = vr_zadnjega
                                    pomozne[zadnji_dodan] = (vr_zadnjega, zadnja_formula, zadnje_vrednosti, True)
                                    formula, vrednosti = zadnja_formula, zadnje_vrednosti
                                    weDone = True
         



                            else:
                                nove_vrednosti[x] = True

                if not weDone:
                    formula, vrednosti = nova_formula, nove_vrednosti

            else:  # izberemo prvo spremenljivko
                spr = nova_formula[0][0]
                nove_vrednosti[spr] = True
                pomozne[spr] = (True, nova_formula, nove_vrednosti,False)

                # poenostavljena formula z vrednostjo True za spr
                nova_for, nove_vred = poenostavi(nova_formula, nove_vrednosti)

                if nova_for == True:
                    return nova_for, nove_vred
                
                elif nova_for == False:
                    nove_vrednosti[spr] = False
                    pomozne[spr] = (False, nova_formula, nove_vrednosti, True)
                    nova_for1, nove_vrednosti1 = poenostavi(nova_formula, nove_vrednosti)
    
                    if nova_for1 == False:
                        while pomozne[spr][3]:
                            del pomozne[spr]
                            if not pomozne:
                                return False, print('ni rešitve')
                            spr = next(reversed(pomozne))
                        zadnji_dodan = spr
                        vr_zadnjega = not pomozne[zadnji_dodan][0]
                        zadnja_formula = pomozne[zadnji_dodan][1]
                        zadnje_vrednosti = pomozne[zadnji_dodan][2]
                        zadnje_vrednosti[zadnji_dodan] = vr_zadnjega
                        pomozne[zadnji_dodan] = (vr_zadnjega, zadnja_formula, zadnje_vrednosti, True)

                        formula, vrednosti = zadnja_formula, zadnje_vrednosti
                        weDone = True
                    elif nova_for1 == True:
                        return nova_for1, nove_vrednosti1
                    if not weDone:
                        formula, vrednosti = nova_for1, nove_vrednosti1
                        weDone = True
                if not weDone:
                    formula, vrednosti = nova_for, nove_vred  


##############################

                    
def main(argv):
    # argv = [vhodna.txt, izhodna.txt]
    # funkcija main iz dimacs formata spremeni formulo v cnf format
    # in zapiše rešitev v ustrezni obliki na izhodno datoteko
    cnf = []
    vhodna = argv[0]  
    izhodna = argv[1]  
    with open(vhodna, 'r') as f:
        for vrstica in f:
            vrstica = vrstica.strip()
            if 'c' in vrstica:
                continue
            elif 'p' in vrstica:
                sez = vrstica.split()
                st_spr = sez[2]
                st_stavkov = sez[3]
            nov = vrstica.strip('0').split()
            if nov == []:
                continue
            else:
                cnf.append(nov)
    f.close()

 
    vr = dict()
    formula, vrednosti = dpll(cnf, vr)
    with open(izhodna, 'w') as g:
        if formula == True:
            mn = set()
            for k, v in vrednosti.items():
                if v == True:
                    mn.add(k)
                else:
                    mn.add('-' + k)
            mn = ' '.join(mn)
            print(str(mn), file=g)
        else:
            print('0', file=g)
    g.close()

##############################



if __name__=='__main__':
    main(sys.argv[1:])
    

