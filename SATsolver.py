import sys
#from boolean import *
from collections import OrderedDict

##############################


def poenostavi(formula, vrednosti):
    # funkcija poenostavi poenostavi formulo in vanj vstavi
    # podane vrednosti

    # zgeneriramo slovar, da nimamo negacije spremenljivk,
    # ampak le posamezne spremenljivke
    vrednosti2 = dict()
    for k,v in vrednosti.items():
        if '-' in k:
            k = k.replace('-','')
            vrednosti2[k] = not v
        else:
            vrednosti2[k] = v

    vrednosti = vrednosti2
    #print("slovar")        
    #print(vrednosti)

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
        
        #print(evaluatedFormula)
        # če je clause prazen
        if not novClause:
            return False, vrednosti
        if k == 0:
            evaluatedFormula.append(novClause)
    return [x for x in evaluatedFormula if x != True], vrednosti


##############################
## DPLL:

pomozne = OrderedDict(dict())
def dpll(formula, vrednosti):
    # na dani formuli izvedemo dpll algoritem
    nova_formula, nove_vrednosti= poenostavi(formula, vrednosti)
##    print('dpll:')
##    print(nova_formula)
##    print(nove_vrednosti)
##    print('pomozne')
##    print(pomozne)
    
    if nova_formula == []:
        return True, nove_vrednosti
    
    elif nova_formula == True:
        return nova_formula, nove_vrednosti
    
## pomoje more bit tale elif zravn:
    elif nova_formula == [[]]:
        return False, nove_vrednosti
        
    elif nova_formula == False:
        if not pomozne:
            return False, print('ni rešitve')
        zadnji_dodan = next(reversed(pomozne))
        vr_zadnjega = not pomozne[zadnji_dodan][0]
        zadnja_formula = pomozne[zadnji_dodan][1]
        zadnje_vrednosti = pomozne[zadnji_dodan][2]
        zadnje_vrednosti[zadnji_dodan] = vr_zadnjega
        del pomozne[zadnji_dodan]
        return dpll(zadnja_formula, zadnje_vrednosti)

    dolžine = []
    for clause in nova_formula:
        dolžine.append(len(clause))

        
    if 1 in dolžine:
        for clause in nova_formula:
            if len(clause) == 1:
                for x in clause:
                    nov = x.replace('-','')
                    if nov in nove_vrednosti:
                        if '-' in x:
                            vr = not nove_vrednosti[nov]
                        else:
                            vr = nove_vrednosti[nov]

##                        print('vr=nove_vre')
##                        print(nove_vrednosti)
    
                    else:
                        nove_vrednosti[x] = True
##        print('konc zanke')
##        print(nova_formula)
##        print(nove_vrednosti)

        return dpll(nova_formula, nove_vrednosti)
    
    
    else:
        # izberemo prvo spremenljivko
        spr = nova_formula[0][0]
##        print(str(spr))
        nove_vrednosti[spr] = True

        pomozne[spr] = (True,nova_formula,nove_vrednosti)
##        print('slovar pomozne')
##        print(pomozne)
        nova_for, nove_vrednosti = poenostavi(nova_formula,nove_vrednosti)
##        print(nova_for)
##        print('nove_vrednosti')
##        print(nove_vrednosti)
        if nova_for == True:
            return nova_for, nove_vrednosti
        elif nova_for == False:
            nove_vrednosti = nove_vrednosti.update({spr:False})
            nova_for1, nove_vrednosti1 = poenostavi(formula,nove_vrednosti)
##            print('prvi elif v else:')
##            print(nove_vrednosti1)
##            print(nova_for1)
            if nova_for1 == False:
                return False, print('ni rešitve')
            elif nova_for1 == True:
                return nova_for1, nove_vrednosti1
            
            return dpll(nova_for1,nove_vrednosti1)

        return dpll(nova_for,nove_vrednosti)


##############################
    

def main(argv):
    # argv = [vhodna.txt, izhodna.txt]
    # funkcija main iz dimacs formata spremeni formulo v cnf format
    # in zapiše rešitev v ustrezni obliki na izhodno datoteko
    cnf = []
    vhodna = argv[0]   # 0 ali 1
    izhodna = argv[1]   # 1 ali 2
    with open(vhodna,'r') as f:
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

##    print('main funkcija: spremeni v cnf')
##    print(cnf)
    
    vr = dict()
    formula, vrednosti = dpll(cnf,vr)
    with open(izhodna, 'w') as g:
        if formula == True:
            mn = set()
            for k,v in vrednosti.items():
                if v == True:
                    mn.add(k)
                else:
                    mn.add('-'+k)
            mn = ' '.join(mn)    
            print(str(mn),file=g)
        else:
            print('0',file=g)   
    g.close()
                        
            
##############################                

## ko bo vse perfektno to odkomentiramo
    
##if __name__=='__main__':
##    main(sys.argv[1:])
##




## ukaz v ukazni vrstici:
##Y:\_System\Desktop\projekt>python SATsolverdela.py test.txt k.txt

## PRIMERI, ki delajo:
# main(['4_9_NE.txt','l.txt'])
# main(['4_8.txt','l.txt'])
# main(['50_80.txt','l.txt'])
# main(['sudoku_easy.txt','l.txt'])
# main(['sudoku_hard.txt','l.txt'])
# main(['sudoku_mini.txt','l.txt'])
# main(['300_883.txt','l.txt'])

## PRIMERI z napako: RecursionError: maximum recursion depth exceeded in comparison
# main(['64_254.txt','l.txt'])
# main(['100_160_NE.txt','l.txt'])
# main(['600_1841.txt','l.txt'])
# main(['600_2237.txt','l.txt'])
# main(['1318_3668.txt','l.txt'])





