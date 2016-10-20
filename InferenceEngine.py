# TODO: MAKE THETA FOR EACH PREDICATE?
import KnowledgeBase

class InferenceEngine:
    def __init__(self, kb):
        # theta is a dictionary of all substitutions where the variable is the key, values are the values 
        self.theta = {}        
        self.kb = kb
        
        # testing unification and resolution
        #self.test_unify(self.theta)
        self.test_resolution(self.kb)

    # preprocesses sentences to check that the predicates match, and to get the relevant arguments
    def preprocess_unify(self, P, Q, theta):
        # the sentences P and Q will always be in the same form, so we can make some assumptions here
        # first, the predicate will always proceed a left paren
        # second, the indices will always be in form x,y and this could hold variables or constants
                
        # first, deal with sentence P           
        # get predicate for P
        split_string = P.split('(')
        predicateP = split_string[0]
        # get arguments for P (will determine if they are variables or constants later)
        split_string = split_string[1].split(')')    
        argsP = split_string[0]

        # now, deal with sentence Q
        # get 
        split_string = Q.split('(')
        predicateQ = split_string[0]
        # get indices for P (will determine if they are variables or constants later)
        split_string = split_string[1].split(')')    
        argsQ = split_string[0]        
        
        if predicateP != predicateQ:
            return False
        else:
            self.unify(argsP, argsQ, theta)
    
    """ reminder: unification takes two atomic sentences P and Q and returns a substitution that 
    makes P and Q identical. This implementation uses the method described by Russell 
    and Norvig to perform unification (p 328). This method differs from R&N's implementation 
    in that we do not handle compound expressions (functions), since none of our rules require it. 
    input: x is a variable, constant or list 
    input: y is a variable, constant or list, or compound expression
    input: theta, the substitution built up so far ()"""   
    def unify(self, P, Q, theta):               
        # if there is no theta that can unify x and y, return false
        if self.theta is None:
            return None            
        # if x and y are the same, no self.need for a substitution    
        elif P == Q:         
            return self.theta
        elif self.is_variable(P):
            return self.unify_var(P, Q, self.theta)
        elif self.is_variable(Q): 
            return self.unify_var(Q, P, self.theta)
        elif self.is_list(P) and self.is_list(Q):                
                split_stringP = ""                
                split_stringQ = ""                
                p_first = ""                
                p_rest = ""
                q_first = ""
                q_rest = ""
                
                split_stringP = P.split(',')
                p_first = split_stringP[0]
                p_rest = split_stringP[1]
                
                split_stringQ = Q.split(',')
                q_first = split_stringQ[0]
                q_rest = split_stringQ[1]     
                
                return self.unify(p_rest, q_rest, self.unify(p_first, q_first, self.theta))
        else:        
            return False

    # note: we have specified that a single variable will be one lowercase character a-z (although not v)
    def is_variable(self, X):     
        if len(X) == 1:
            if (X.islower()):            
                if (X != 'v'):
                    return True
        else:
            return False

    # note: assumes that all variables in a list are of form x,y
    def is_list(self, X):               
        if ',' in X:        
            return True
        else:
            return False

    # helper function for unification, also inspired by Russell and Norvig implementation 
    # note: omitted the occur check bc it did not seem necessary for this application, and 
    # bc of complexity concerns    
    def unify_var(self, var, x, theta):       
    
        # there is already an entry in theta for this var
        if var in self.theta:            
            # the case where x needs to be added to theta 
            
            if (x not in theta[var]):                
                theta[var].append(x)
                return self.unify(var, x, theta)
            else:
                # takes care of case where x already in theta
                for value in self.theta[var]:
                    return(self.unify(value, x, theta))              
        else:
            # adds the var/value combination to theta
            key = var
            value = x            
            
            self.theta.setdefault(key,[])
            self.theta[var].append(value)
                                   
            return self.theta 
                  
    def test_unify(self, theta):
        # should not work bc predicates don't match, prints false 
        # 1, 2. WORKING for both
        print(self.preprocess_unify("KNOWS(John,x)", "FATHER(John,x)", theta))       
        print(self.preprocess_unify("FATHER(John,x)","KNOWS(John,x)", theta))

        # predicates are the same, return empty theta
        # 3. WORKS    
        self.preprocess_unify("KNOWS(John,x)", "KNOWS(John,x)", theta)
        print(self.theta)
        
        # should substitute x/John
        # 4. WORKS
        self.preprocess_unify("KNOWS(John)", "KNOWS(x)", theta)
        print(self.theta)
        
        # x/John already in theta, should not re-add
        # 5. WORKS    
        self.preprocess_unify("KNOWS(x)", "KNOWS(John)", theta)        
        print(self.theta)

        # should substitute y/John
        # 6. WORKS    
        self.preprocess_unify("KNOWS(y)", "KNOWS(John)", theta)        
        print(self.theta)

        # should not add anything to theta
        # 7. WORKS    
        self.preprocess_unify("KNOWS(John)", "KNOWS(Richard)", theta)        
        print(self.theta)
        
        # should substitute y/Richard
        # 8. WORKS    
        self.preprocess_unify("KNOWS(y)", "KNOWS(Richard)", theta)        
        print(self.theta)        
        
        # should substitute x/Jane
        # 9. WORKS        
        self.preprocess_unify("KNOWS(John,x)", "KNOWS(John,Jane)", theta)                 
        print(self.theta)         

        # should substitute x/Bill, y/John  
        # 10. WORKS    
        self.preprocess_unify("KNOWS(John,x)", "KNOWS(y,Bill)", theta)                 
        print(self.theta)          
        
        # should fail, bc x cannot take on two values at same time
        # 11. WORKS
        self.preprocess_unify("KNOWS(x,John)", "KNOWS(x,Elizabeth)", theta)  
        print(self.theta)          

    # TO DO: GET SUBSTITUTION DIALED
    def substitute(self, theta):
        print("Not yet implemented")  

    """" This implementation uses the method described by Russell and Norvig to perform resolution (p 255)  
    this method differs from R&N's implementation in that we are using FOL and not
    propositional logic.
    input: KB, the knowledge base, a sentence in FOL
    input: q, the query, a sentence in FOL
    input: clauses, set of clauses in FOL representation of KB and not q
    returns: the set of all possible clauses obtained by resolving KB and q"""
    def resolution(self, kb, q):
        print("in resolution") 

        # TODO: parse clauses somewhere in here        
        # the set of clauses in FOL representation of KB and not q
        clauses = set(self.kb.clauses())
        
        # negate the query          
        negated_q = self.negate(q) 
        print(negated_q)        
        
        
        # add the negated query to the list of clauses
        clauses.add(negated_q)
        
        print(clauses)
        
        # the set of new clauses
        # when no new clauses can be added, KB does not entail q
        new = set()

        # loop until no new clauses can be added (which means KB does not entail q), or
        # two clauses yield the empty clause (which means KB entails q)
        while True:
            # variable to keep track of the length of clause list            
            clause_len = len(clauses)
            # make a list of all clause pairs                    
          
        #clause_pairs = [(clauses[i], clauses[j]) for i in range(clause_len) for j in range(i+1, clause_len)]
        
        
            #print(clause_pairs)            
            
        #    for (ci, cj) in pairs:
        #        resolvents = pl_resolve(ci, cj)
        #        if FALSE in resolvents: 
        #            return True
        #        new.union_update(set(resolvents))
        #    if new.issubset(set(clauses)): return False

        #    for c in new:
       #         if c not in clauses: clauses.append(c)        
        
            c1 = ""
            c2 = ""
            False 
            
            #print(clauses)
            self.resolve(c1, c2)               

    # DO UNIFICATION, but where? look at other algo in book        
    def resolve(self, c1, c2):
        print("in resolve")
        """Return all clauses that can be obtained by resolving clauses ci and cj.
        >>> pl_resolve(to_cnf(A|B|C), to_cnf(~B|~C|F))
        [(A | C | ~C | F), (A | B | ~B | F)]
        """
        #clauses = []
        #or di in disjuncts(ci):
        #    for dj in disjuncts(cj):
        #        if di == ~dj or ~di == dj:
        #            dnew = unique(removeall(di, disjuncts(ci)) + removeall(dj, disjuncts(cj)))
        #        clauses.append(NaryExpr('|', *dnew))
    #return clauses
        
    def negate(self,q):
        print("negate")
        return "!{}".format(q)       
        
    # Do we need?     
    def universal_instantiation(self, theta):
        print("Not yet implemented") 

    # Do we need?          
    def existential_instantiation(self, theta):
        print("Not yet implemented")  
        
    def test_resolution(self, kb):
        q = "BREEZE(0,0)"
        self.resolution(kb, q)