# TODO: MAKE THETA FOR EACH PREDICATE?
import KnowledgeBase

class InferenceEngine:
    def __init__(self, kb):
        # theta is a dictionary of all substitutions where the variable is the key, values are the values 
        self.theta = {}        
        self.kb = kb
        
        # testing unification and resolution
        #self.test_unify(self.theta)
        # self.test_resolution(self.kb)

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
   
        # the set of clauses in FOL representation of KB and not q
        clauses = set(self.kb.clauses())
        
        # negate the query          
        negated_q = self.negate(q)         
        
        # the flag for resolution looping        
        loop_flag = True        
        
        # add the negated query to the list of clauses
        clauses.add(negated_q)

        # for testing
        print(clauses)         
         

        # loop until no new clauses can be added (which means KB does not entail q), or
        # two clauses yield the empty clause (which means KB entails q)
        while loop_flag:
            # variable to keep track of the length of clause list            
            clause_len = len(clauses)

            # make a list of all clauses (bc easier to deal with then set)                
            clause_list = list(clauses)
            # make a list of all clause pairs            
            clause_pairs = []
            for i in range (0, clause_len):
                for j in range (i+1, clause_len):
                    clause_pairs.append([clause_list[i], clause_list[j]])
            
            # the set of new clauses
            # when no new clauses can be added, KB does not entail q
            new = set()
    
                
            
            
            # for testing
            print(clause_pairs)            
            print(len(clause_pairs)) 
            pairs_len = len(clause_pairs)
            
            
            print(clause_pairs[0])            
            print(clause_pairs[0][0])
            print(clause_pairs[0][1])  

            for pair_index in range (0, pairs_len - 1):
                # get indices for two of the pairs in the list                
                val_index = 0
                ci = clause_pairs[pair_index][val_index] 
                val_index = val_index + 1
                cj = clause_pairs[pair_index][val_index] 
            
                # resolve returns the set of all possible clauses obtained by resolving ci and cj            
                resolvents = self.resolve(ci, cj)
                
                
        #        if FALSE in resolvents: 
        #            return True
        #        new.union_update(set(resolvents))
        #    if new.issubset(set(clauses)): return False

        #    for c in new:
       #         if c not in clauses: clauses.append(c)        
        
            loop_flag = False 
            
            #print(clauses)           
 
        """Return all clauses that can be obtained by resolving clauses ci and cj. Each pair
        that contans complementary literals is resolved to produce a new clause, which is added
        to the set if it is not alredy present. 
        Remember: Horn clauses are going to be disjunctions
        note: a disjunction is true only if at least one of each pair that contains complementary literals
        is resolved to produce a new clause. New clauses are added to the new set in resolution. 
        """
    def resolve(self, ci, cj):
        clauses = []
        disjunct_list_i = []
        disjunct_list_j = []        
        
        # slice up disjuncts in ci, store in disjuncts_i
        if 'v' in ci:          
            # we have a disjunct, split on the "v" to get the constituent parts
            # extra space is tdict2 = dict1.copy()o handle the whitespace around or
            disjunct_list_i = ci.split(" v ")
        else:
            # just a normal term
            disjunct_list_i.append(ci)
        

        # slice up disjuncts in cj, store in disjuncts_j
        if 'v' in cj:          
            # we have a disjunct, split on the "v" to get the constituent parts
            disjunct_list_j = cj.split(" v ")
        else:
            disjunct_list_j.append(cj)

        
        for i in disjunct_list_i:
            for j in disjunct_list_j:
                print("i = {}".format(i))
                print("j = {}".format(j))                
                                
                # before the preprocessing step, remove !() from both i and j (temporarily)  
                if '!' in i:
                    i_strip = i.split("!(")
                    # slice off that last paren
                    i_bare = i_strip[1][:-1]                    
                else:
                    i_bare = i
                
                if '!' in j:
                    j_strip = j.split("!(")
                    # slice off that last paren
                    j_bare = j_strip[1][:-1]                                
                else:
                    j_bare = j
                
                self.preprocess_unify(i_bare, j_bare, self.theta)

                print(self.theta)
                # TODO: get so is working for multiple theta, of different sizes                
                # there is something in theta we unified, so we can try resolution
                if len(self.theta) > 1:
                    # see if we can resolve
                    # need to match on predicate i.e. B(x,y) and B(0,0)
                    i_bare_pred = i_bare.split('(')                    
                    j_bare_pred = j_bare.split('(')                        
                                    
                    if i_bare_pred[0] == j_bare_pred[0]:
                        # i and j have the same predicate
                        print("resolve")   
                        # resolve if we have !i == j or !j == i  
                        # have checked predicate is the same, and they have resolved, so 
                        if (i[:1] == '!' and j[:1] != '!') or (j[:1] == '!' and i[:1] != '!'):   
                            # if resolved, remove from disjuncts
                            # remove i and j from their respective lists
                            while i in disjunct_list_i:
                                disjunct_list_i.remove(i)
                            
                            while j in disjunct_list_j:
                                disjunct_list_j.remove(j)     
                   
                            # substitute in theta for remaining clauses
                            disjunct_list_i = self.sub_values(disjunct_list_i, self.theta)
                            disjunct_list_j = self.sub_values(disjunct_list_j, self.theta)                                
                                                   
                            print(disjunct_list_i) 
                            print(disjunct_list_j)                                
                            # after sub, remove those keys from theta, so we can try again

                

                


                
                # update clauses in light of these changes
                



                      
        #            dnew = unique(removeall(di, disjuncts(ci)) + removeall(dj, disjuncts(cj)))
        #        clauses.append(NaryExpr('|', *dnew))
        return clauses
        
    def negate(self,q):
        return "!({})".format(q)       
             
    # following resolution, subs in appropriate values from substitution string         
    def sub_values(self, disjunct_list, theta):      
        
        # uses key (corresponds to variable) to make appropriate subs in disjunct_list         
        for key in theta:
            key_variable = key
            
            for value in theta[key_variable]:
                value_of_key = value
            
                # checks if there are values in the list before iterating
                num_items = len(disjunct_list)        
                if (num_items > 0):
                    # checks all the items in disjunct_list for possible substitution
                    for i in range(0,num_items):
                        # three different cases where variable could be, after left paren, before right paren, or between two commas
                        if ("({},".format(key_variable) in disjunct_list[i]) or (",{},".format(key) in disjunct_list[i]) or (",{})".format(key) in disjunct_list[i]):
                            disjunct_list[i] = disjunct_list[i].replace("{}".format(key_variable), "{}".format(value_of_key))   
                          
        return disjunct_list
                
                
                
    def test_resolution(self, kb):
        q = "B(0,0)"
        self.resolution(kb, q)

    def tell(self, key, assertion, x, y):
        self.kb.tell(key, assertion, x, y)

    def ask(self, query, x, y):
        possibles = ['^', '>', 'v', '<', 's^', 's>', 'sv', 's<'] # move these directions or shoot these directions
        choices = self.get_neighbors(x, y)
        choice = self.best_choice(choices)
        return choice

    def get_neighbors(self, x, y):
        neighbors = {'_': [], 'm':[], 'd': [], 's': [], 'w':[], 'p':[], 'o':[]}
        if x > 0:
            neighbors.get(self.kb.known_map[x - 1][y]).append('^')
        if x < len(self.kb.known_map) - 1:
            neighbors.get(self.kb.known_map[x + 1][y]).append('v')
        if y > 0:
            neighbors.get(self.kb.known_map[x][y - 1]).append('<')
        if y < len(self.kb.known_map) - 1:
            neighbors.get(self.kb.known_map[x][y + 1]).append('>')
        return neighbors

    def best_choice(self, choices):
        if len(choices.get('_')) > 0: #unexplored
            return choices.get('_')
        elif len(choices.get('m')) > 0 or len(choices.get('d')) > 0: #potentials
            return list(choices.get('m') + choices.get('d'))
        elif len(choices.get('s')) > 0 and len(choices.get('w')) > 0: #Random choice between safe space and kill wumpi
            rand = 0, 1
            import random
            rand = random.choice(rand)
            if rand == 0:
                return choices.get('s')
            else:
                return choices.get('w')
        elif len(choices.get('s')) > 0:
            return choices.get('s')
        elif len(choices.get('w')) > 0:
            l = []
            for c in choices.get('w'):
                l.append('k%s' % c)
            return l

        else:
            return ["Stuck"]