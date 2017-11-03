import sys


class Formula:
    def __ne__(self, other):
        return not (self == other)

    def flatten(self):
        return self

    def getVariable(self, mapping):
        if self not in mapping:
            mapping[self] = freshVariable()
        return mapping[self]

##############################

class Variable(Formula):
    def __init__(self, x):
        self.x = x

    def __str__(self, parentheses = False):
        return str(self.x)

    def __hash__(self):
        return hash(self.x)

    def __eq__(self, other):
        if isinstance(other, Formula):
            return isinstance(other, Variable) and self.x == other.x
        else:
            return self.x == other

    def evaluate(self, values):
        return values[self.x]

    def simplify(self):
        return self

    def tseytin(self, mapping):
        return self

    def equiv(self, variable):
        return And(Or(variable, Not(self)), Or(Not(variable), self))

##############################

class Not(Formula):
    def __init__(self, x):
        self.x = makeFormula(x)

    def __str__(self, parentheses = False):
        return "~" + self.x.__str__(True)

    def __hash__(self):
        return hash(("~", self.x))

    def __eq__(self, other):
        return isinstance(other, Not) and self.x == other.x

    def evaluate(self, values):
        return not self.x.evaluate(values)

    def flatten(self):
        if isinstance(self.x, Not):
            return self.x.x
        else:
            return self

    def simplify(self):
        # pomoje more bit tale za negacijo notr
        if isinstance(self.x, Not):
            return self.x.x.simplify()
        elif isinstance(self.x, And):
            return Or(*(Not(y) for y in self.x.terms)).simplify()
        elif isinstance(self.x, Or):
            return And(*(Not(y) for y in self.x.terms)).simplify()
        else:
            return self.flatten().simplify()

    def tseytin(self, mapping):
        return Not(self.x.tseytin(mapping)).getVariable(mapping)

    def equiv(self, variable):
        return And(Or(variable, self.x), Or(Not(variable), self))


##############################

class Multi(Formula):
# tole je zdruzen razred za and in or, k mata podobne lastnosti
    def __init__(self, *args):
        # *args je poljubno število parametrov
        if len(args) == 1:
            args = args[0]
        self.terms = frozenset(makeFormula(x) for x in args)
        

    def __str__(self, parentheses = False):
        if len(self.terms) == 0:
            return self.empty
        elif len(self.terms) == 1:
            return next(iter(self.terms)).__str__(parentheses)
        out = self.connective.join(x.__str__(True) for x in self.terms)
        if parentheses:
            return "(%s)" % out
        else:
            return out

    def __hash__(self):
        return hash((self.connective, self.terms))

    def __eq__(self, other):
        return isinstance(other, self.getClass()) \
            and self.terms == other.terms

    def evaluate(self, values):
        return self.fun(x.evaluate(values) for x in self.terms)

    def flatten(self):
        this = self.getClass()
        terms = (x.flatten() for x in self.terms)
        out = this(*sum([list(x.terms) if isinstance(x, this)
                         else [x] for x in terms], []))
        if len(out.terms) == 1:
            return next(iter(out.terms))
        else:
            return out

    def simplify(self):
        terms = [x.simplify() for x in self.terms]
        const = self.getDualClass()
        if const in terms:
            return const
        if len(terms) == 1:
            return terms[0]
        return self.getClass()(*terms).flatten()

    def tseytin(self, mapping):
        return self.getClass()(*(x.tseytin(mapping)
                               for x in self.terms)).getVariable(mapping)
    


##############################



def poenostavi(formula, values):
    values2 = {}
    for k,v in values.items():
        if '-' in k:
            k = k.replace('-','')
            values2[k] = not v
        else:
            values2[k] = v

    values = values2
    #print("slovar")        
    #print(values)
    
    newFormula = []
    #find values
    if formula == []:
        return True, values
    for clause in formula:
        if not clause:
            # če je prazen
            return False, values
        newClause = []
        for term in clause:
            newTerm = term
            lit = term.replace("-", "")
            if lit in values:
                if "-" in term:
                    newTerm = not values[lit]
                else:
                    newTerm = values[lit]
            newClause.append(newTerm)
        newFormula.append(newClause)

    evaluatedFormula = []
    
    for clause in newFormula:
        # filter clause of falses
        newClause = []
        k = 0
        #newClause = [x for x in clause if x]
        #print(newClause)
        for x in clause:
            if x:
                newClause.append(x)
                if x == True:
                    k += 1
        
        #print(newClause)
        #print(evaluatedFormula)
        # print clause
        # clause is empty
        if not newClause:
            return False, values
##        else:
##            newClause = [x for x in newClause if x != True]
##            if not newClause:
##                newClause = True
        if k == 0:
            evaluatedFormula.append(newClause)
        #evaluatedFormula.append(newClause)
    return [x for x in evaluatedFormula if x != True], values

#print(poenostavi([["-a" , "b", "c"], ["w"], ["s", "-t"]], {"a":True, "w":False, "t":False}))
###########################
# dpll


def dpll(formula, vrednosti):
    # vrne novo formulo, kjer je vsem atomom pri
    nova_formula, nove_vrednosti= poenostavi(formula, vrednosti)
    #print(nova_formula)
    #print(nove_vrednosti)
    
    if nova_formula == []:
        return True, nove_vrednosti
    if nova_formula == False or nova_formula == True:
        return nova_formula, nove_vrednosti

    dolžine = []
    for clause in nova_formula:
        dolžine.append(len(clause))

    #print(dolžine)
        
    if 1 in dolžine:
        for clause in nova_formula:
            if len(clause) == 1:
                for x in clause:
                    if x in nove_vrednosti:
                        vr = nove_vrednosti[x]
                        #print('vr=nove_vre')
                        #print(vr)
                        if vr != True:
                            print('Napaka pri funkciji korak1')
                            break
                    nove_vrednosti[x] = True
        #print('konc zanke')
        #print(nova_formula)
        #print(nove_vrednosti)

        
        return dpll(nova_formula, nove_vrednosti)
    
    else:
        
        spr = nova_formula[0][0]
        nove_vrednosti[spr] = True
        #print(spr)
        #print(nove_vrednosti)
        #pomozne_vr = vrednosti.update({spr:True})
        nova_for, nove_vrednosti = poenostavi(nova_formula,nove_vrednosti)
        #print(nova_for)
        if nova_for == True:
            return nova_for, nove_vrednosti
        elif nova_for == False:
            nove_vrednosti = nove_vrednosti.update({spr:False})
            nova_for1 = poenostavi(formula,nove_vrednosti)
            #print( vrednosti)
            if nova_for1 == False:
                return False, print('ni rešitve')
            elif nova_for1 == True:
                return nova_for1, nove_vrednosti
            
            return dpll(nova_for1,nove_vrednosti)

        return dpll(nova_for,nove_vrednosti)




##############################

class And(Multi):
    empty = "T"
    connective = r" /\ "
    fun = all

    def getClass(self):
        return And

    def getDualClass(self):
        return Or

    def equiv(self, variable):
        return And(Or(variable, *(Not(x).flatten() for x in self.terms)),
                   *(Or(Not(variable), x) for x in self.terms))

##############################

class Or(Multi):
    empty = "F"
    connective = r" \/ "
    fun = any

    def getClass(self):
        return Or

    def getDualClass(self):
        return And

    def equiv(self, variable):
        return And(Or(Not(variable), *self.terms),
                   *(Or(variable, Not(x)) for x in self.terms))

##############################

T = And()
F = Or()

def makeFormula(x):
    if isinstance(x, Formula):
        return x
    else:
        return Variable(x)

##############################

counter = 0

def freshVariable():
    global counter
    counter += 1
    return Variable(("__", counter))

def tseytin(formula, mapping = None):
    if mapping is None:
        mapping = {}
    f = formula.tseytin(mapping)
    return And(f, *(k.equiv(v) for k, v in mapping.items())).flatten()

###############################

def main(argv):
    # argv = [vhodna.txt, izhodna.txt]
    # funkcija iz dimacs v cnf
    cnf = []
    vhodna = argv[0]   # o ali 1
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
            cnf.append(nov)
    f.close()

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
                        
            
###########################                
                
    
if __name__=='__main__':
    main(sys.argv[1:])






##Y:\_System\Desktop\projekt>python SATsolverdela.py test.txt k.txt





