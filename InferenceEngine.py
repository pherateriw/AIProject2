class InferenceEngine:
    def __init__(self, kb):
        # theta is a dictionary of all substitutions where the variable is the key, values are the values 
        self.theta = {}        
        self.kb = kb
        self.removal_clauses = []
        self.clauses = ""

        # testing unification and resolution
        # self.test_unify(self.theta)
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
        # get predicate for Q
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
        # should not work bc predicates don't match, self.logger.infos false 
        # 1, 2. WORKING for both
        self.logger.info(self.preprocess_unify("KNOWS(John,x)", "FATHER(John,x)", theta))       
        self.logger.info(self.preprocess_unify("FATHER(John,x)","KNOWS(John,x)", theta))

        # predicates are the same, return empty theta
        # 3. WORKS    
        self.preprocess_unify("KNOWS(John,x)", "KNOWS(John,x)", theta)
        self.logger.info(self.theta)
        
        # should substitute x/John
        # 4. WORKS
        self.preprocess_unify("KNOWS(John)", "KNOWS(x)", theta)
        self.logger.info(self.theta)
        
        # x/John already in theta, should not re-add
        # 5. WORKS    
        self.preprocess_unify("KNOWS(x)", "KNOWS(John)", theta)        
        self.logger.info(self.theta)

        # should substitute y/John
        # 6. WORKS    
        self.preprocess_unify("KNOWS(y)", "KNOWS(John)", theta)        
        self.logger.info(self.theta)

        # should not add anything to theta
        # 7. WORKS    
        self.preprocess_unify("KNOWS(John)", "KNOWS(Richard)", theta)        
        self.logger.info(self.theta)
        
        # should substitute y/Richard
        # 8. WORKS    
        self.preprocess_unify("KNOWS(y)", "KNOWS(Richard)", theta)        
        self.logger.info(self.theta)        
        
        # should substitute x/Jane
        # 9. WORKS        
        self.preprocess_unify("KNOWS(John,x)", "KNOWS(John,Jane)", theta)                 
        self.logger.info(self.theta)         

        # should substitute x/Bill, y/John  
        # 10. WORKS    
        self.preprocess_unify("KNOWS(John,x)", "KNOWS(y,Bill)", theta)                 
        self.logger.info(self.theta)          
        
        # should fail, bc x cannot take on two values at same time
        # 11. WORKS
        self.preprocess_unify("KNOWS(x,John)", "KNOWS(x,Elizabeth)", theta)  
        self.logger.info(self.theta)          

    """" This implementation uses the method described by Russell and Norvig to perform resolution (p 255)  
    this method differs from R&N's implementation in that we are using FOL and not
    propositional logic.
    input: KB, the knowledge base, a sentence in FOL
    input: q, the query, a sentence in FOL
    input: clauses, set of clauses in FOL representation of KB and not q
    returns: the set of all possible clauses obtained by resolving KB and q"""
    def resolution(self, kb, q):
   
        # the set of clauses in FOL representation of KB and not q
        self.clauses = set(self.kb.clauses())
        
        # negate the query          
        negated_q = self.negate(q)         

        # add the negated query to the list of clauses
        self.clauses.add(negated_q)

        # the set of new clauses
        # when no new clauses can be added, KB does not entail q
        new = set()

        # loop until no new clauses can be added (which means KB does not entail q), or
        # two clauses yield the empty clause (which means KB entails q)
        while True:
            self.logger.info("clauses = {}".format(self.clauses))

            # variable to keep track of the length of clause list            
            clause_len = len(self.clauses)

            # make a list of all clauses (bc easier to deal with then set)
            clause_list = list(self.clauses)
            # make a list of all clause pairs            
            clause_pairs = []
            for i in range (0, clause_len):
                for j in range (i+1, clause_len):
                    clause_pairs.append([clause_list[i], clause_list[j]])

            pairs_len = len(clause_pairs)
            
            for pair_index in range (0, pairs_len):
                # get indices for two of the pairs in the list                
                val_index = 0
                ci = clause_pairs[pair_index][val_index] 
                val_index = val_index + 1
                cj = clause_pairs[pair_index][val_index] 
            
                #self.logger.info("ci = {}".format(ci))
                #self.logger.info("cj = {}".format(cj))

                # resolve returns the set of all possible clauses obtained by resolving ci and cj
                resolvents = set(self.resolve(ci, cj))
                #self.logger.info(self.resolve(ci, cj, clauses))
                self.logger.info("resolvents = {}".format(resolvents))
                self.logger.info("clauses = {}".format(self.clauses))
                self.logger.info(self.clauses)
                #self.logger.info(len(resolvents))

                # all we have left is the empty clause
                # resolution is finished
                # is None right here?
                if None in resolvents or self.clauses == None:
                    self.logger.info("clauses = {}".format(self.clauses))
                    return True

                # new becomes the union of new and resolvents
                # TODO: we might want union_update here, not totally sure I get the difference
                new = new.union(resolvents)
                #self.logger.info("new = {}".format(new))

            # checks if new is a subset of the clauses, if it is, keeps looping
            if self.clauses != None:
                if new.issubset(set(self.clauses)):
                    self.logger.info("clauses = {}".format(self.clauses))
                    return False

                self.clauses.union(new)
                self.logger.info(self.clauses)

            clause_pairs.clear()
            new.clear()

    """Return all clauses that can be obtained by resolving clauses ci and cj. Each pair
    that contans complementary literals is resolved to produce a new clause, which is added
    to the set if it is not alredy present.
    Remember: Horn clauses are going to be disjunctions
    note: a disjunction is true only if at least one of each pair that contains complementary literals
    is resolved to produce a new clause. New clauses are added to the new set in resolution.
    """
    def resolve(self, ci, cj):
        local_clauses = []
        local_clauses.clear()
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

        #self.logger.info("disjunct_list_i {}".format(disjunct_list_i))
        #self.logger.info("disjunct_list_j {}".format(disjunct_list_j))

        #self.logger.info("i size = {}".format(len(disjunct_list_i)))
        #self.logger.info("j size = {}".format(len(disjunct_list_j)))

        for i in disjunct_list_i:
            for j in disjunct_list_j:
                #self.logger.info("i = {}".format(i))
                #self.logger.info("j = {}".format(j))
                                
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
                
                #self.logger.info(i_bare)
                #self.logger.info(j_bare)

                self.preprocess_unify(i_bare, j_bare, self.theta)
                #self.logger.info(self.theta)

                # there is something in theta we unified, so we can try resolution
                if len(self.theta) > 0:
                    # see if we can resolve
                    # need to match on predicate i.e. B(x,y) and B(0,0)
                    i_bare_pred = i_bare.split('(')                    
                    j_bare_pred = j_bare.split('(')                        

                    #self.logger.info("i bare {} =".format(i_bare_pred))
                    #self.logger.info("j_bare {} =".format(j_bare_pred))

                    if i_bare_pred[0] == j_bare_pred[0]:
                        # i and j have the same predicate
                        self.logger.info("resolve i and j")

                        # resolve if we have !i == j or !j == i  
                        # have checked predicate is the same, and they have resolved, so 
                        if i[:1] == '!' and j[:1] != '!' or j[:1] == '!' and i[:1] != '!':
                            # substitute in theta for remaining clauses
                            disjunct_list_i = self.sub_values(disjunct_list_i, self.theta)
                            disjunct_list_j = self.sub_values(disjunct_list_j, self.theta)

                            self.logger.info("di = {}".format(disjunct_list_i))
                            self.logger.info("dj = {}".format(disjunct_list_j))

                            # if resolved, remove from disjuncts, clauses
                            # remove i and j from their respective lists
                            self.logger.info("ci = {}".format(ci))
                            self.logger.info("cj = {}".format(cj))

                            while i in disjunct_list_i:
                                self.logger.info("removing {}".format(i))
                                disjunct_list_i.remove(i)
                                if i in local_clauses:
                                    local_clauses.remove(i)

                            while j in disjunct_list_j:
                                self.logger.info("removing {}".format(j))
                                disjunct_list_j.remove(j)
                                if j in local_clauses:
                                    local_clauses.remove(j)


                            self.logger.info("di={}".format(disjunct_list_i))
                            self.logger.info("dj={}".format(disjunct_list_j))

                            # make the new list of disjuncts
                            updated_disjuncts = set()
                            for i in disjunct_list_i:
                                updated_disjuncts.add(i)

                            for j in disjunct_list_j:
                                updated_disjuncts.add(j)

                            updated_disjuncts = list(updated_disjuncts)

                            for a in updated_disjuncts:
                                local_clauses.append(a)

                            #self.logger.info("local clauses is now")
                            #self.logger.info(local_clauses)

                            # TODO: do this up to four
                            # remove the old disjunct and replace it with the new
                            if (self.clauses != None):
                                ci_index = list(self.clauses).index(ci) if ci in list(self.clauses) else -1
                                if ci_index != -1:
                                    self.logger.info("ci = {}".format(ci))
                                    if ' v ' in ci:
                                        
                                        if len(disjunct_list_i) == 1:
                                            #self.logger.info(self.clauses)
                                            self.clauses.discard(ci)
                                            self.logger.info("popped {}".format(ci_index))
                                            #self.logger.info(self.clauses)

                                            replacement_item = disjunct_list_i[0]
                                            self.clauses.add(replacement_item)
                                            #self.logger.info(self.clauses)
                                            # clear disjunct list
                                            disjunct_list_i.remove(ci_index)
                                            
                                        elif len(disjunct_list_i) == 2:
                                            self.clauses.discard(ci)
                                            disjunct_list_i.remove(ci)
                                
                                        elif len(disjunct_list_i) == 3:    
                                            # put back together
                                            if ci_index == 0:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[1]
                                                r2 = disjunct_list_i[2]
                                                self.clauses.add("{} v {}".format(r1, r2))  
                                            elif ci_index == 1:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[2]
                                                self.clauses.add("{} v {}".format(r1, r2))  
                                            elif ci_index == 2:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[1]
                                                self.clauses.add("{} v {}".format(r1, r2))                                                  
                                        elif len(disjunct_list_i) == 4:
                                            if ci_index == 0:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[1]
                                                r2 = disjunct_list_i[2]
                                                r3 = disjunct_list_i[3]                                                
                                                self.clauses.add("{} v {} v {}".format(r1, r2, r3))  
                                            elif ci_index == 1:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[1]
                                                r3 = disjunct_list_i[2]                                                
                                                self.clauses.add("{} v {} v {}".format(r1, r2, r3))  
                                            elif ci_index == 2:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[1]
                                                r3 = disjunct_list_i[3]                                                
                                                self.clauses.add("{} v {} v {}".format(r1, r2, r3)) 
                                            elif ci_index == 3:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[1]
                                                r3 = disjunct_list_i[2]                                                
                                                self.clauses.add("{} v {} v {}".format(r1, r2, r3)) 

                                        elif len(disjunct_list_i) == 5:
                                            if ci_index == 0:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[1]
                                                r2 = disjunct_list_i[2]
                                                r3 = disjunct_list_i[3] 
                                                r4 = disjunct_list_i[4]                                                 
                                                self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))                                          
                                            if ci_index == 1:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[2]
                                                r3 = disjunct_list_i[3] 
                                                r4 = disjunct_list_i[4]                                                 
                                                self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))                                         
                                            if ci_index == 2:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[1]
                                                r3 = disjunct_list_i[3] 
                                                r4 = disjunct_list_i[4]                                                 
                                                self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))
                                            if ci_index == 3:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[1]
                                                r3 = disjunct_list_i[2] 
                                                r4 = disjunct_list_i[4]                                                 
                                                self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))  
                                            if ci_index == 4:
                                                self.clauses.discard(ci)
                                                disjunct_list_i.remove(ci)
                                                r1 = disjunct_list_i[0]
                                                r2 = disjunct_list_i[1]
                                                r3 = disjunct_list_i[2] 
                                                r4 = disjunct_list_i[3]                                                 
                                                self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))  


                                if (self.clauses != None):
                                    cj_index = list(self.clauses).index(cj) if cj in list(self.clauses) else -1
                                    if cj_index != -1:
                                        #self.logger.info("cj = {}".format(ci))
                                        if ' v ' in cj:
                                            #TODO: handle more than one or
                                            if len(disjunct_list_j) == 1:
                                                #self.logger.info(self.clauses)
                                                self.clauses.discard(cj)
                                                self.logger.info("popped {}".format(cj_index))
                                                #self.logger.info(self.clauses)

                                                replacement_item = disjunct_list_j[0]
                                                self.clauses.add(replacement_item)
                                                #self.logger.info(self.clauses)
                                                # clear disjunct list
                                                disjunct_list_j.remove(cj_index)
                                            
                                            elif len(disjunct_list_j) == 2:
                                                self.clauses.discard(cj)
                                                disjunct_list_i.remove(cj)
                                
                                            elif len(disjunct_list_j) == 3:    
                                                # put back together
                                                if ci_index == 0:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[1]
                                                    r2 = disjunct_list_j[2]
                                                    self.clauses.add("{} v {}".format(r1, r2))  
                                                elif cj_index == 1:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[2]
                                                    self.clauses.add("{} v {}".format(r1, r2))  
                                                elif cj_index == 2:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[1]
                                                    self.clauses.add("{} v {}".format(r1, r2))                                                  
                                            elif len(disjunct_list_j) == 4:
                                                if cj_index == 0:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[1]
                                                    r2 = disjunct_list_j[2]
                                                    r3 = disjunct_list_j[3]                                                
                                                    self.clauses.add("{} v {} v {}".format(r1, r2, r3))  
                                                elif cj_index == 1:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[1]
                                                    r3 = disjunct_list_j[2]                                                
                                                    self.clauses.add("{} v {} v {}".format(r1, r2, r3))  
                                                elif cj_index == 2:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[1]
                                                    r3 = disjunct_list_j[3]                                                
                                                    self.clauses.add("{} v {} v {}".format(r1, r2, r3)) 
                                                elif cj_index == 3:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[1]
                                                    r3 = disjunct_list_j[2]                                                
                                                    self.clauses.add("{} v {} v {}".format(r1, r2, r3)) 

                                            elif len(disjunct_list_j) == 5:
                                                if cj_index == 0:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[1]
                                                    r2 = disjunct_list_j[2]
                                                    r3 = disjunct_list_j[3] 
                                                    r4 = disjunct_list_j[4]                                                 
                                                    self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))                                          
                                                if cj_index == 1:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[2]
                                                    r3 = disjunct_list_j[3] 
                                                    r4 = disjunct_list_j[4]                                                 
                                                    self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))                                         
                                                if cj_index == 2:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[1]
                                                    r3 = disjunct_list_j[3] 
                                                    r4 = disjunct_list_j[4]                                                 
                                                    self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))
                                                if cj_index == 3:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_j.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[1]
                                                    r3 = disjunct_list_j[2] 
                                                    r4 = disjunct_list_j[4]                                                 
                                                    self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))  
                                                if cj_index == 4:
                                                    self.clauses.discard(cj)
                                                    disjunct_list_i.remove(cj)
                                                    r1 = disjunct_list_j[0]
                                                    r2 = disjunct_list_j[1]
                                                    r3 = disjunct_list_j[2] 
                                                    r4 = disjunct_list_j[3]                                                 
                                                    self.clauses.add("{} v {} v {} v {}".format(r1, r2, r3, r4))  
            # after sub, remove those keys from theta, so we can try again
            self.theta.clear()
            return local_clauses

    # negate a clause
    def negate(self,q):
        # if clause already negated
        if '!' in q:
            split_q = q.split("!(")
            q = split_q[1]
            split_q = q.split(")")
            q = split_q[0]
            return "({})".format(q)   
        return "!({})".format(q)       
             
    # following resolution, subs in appropriate values from substitution string         
    def sub_values(self, disjunct_list, theta):      
        
        # uses key (corresponds to variable) to make appropriate subs in disjunct_list         
        for key in theta:
            key_variable = key
            #self.logger.info("key = {}".format(key_variable))

            for value in theta[key_variable]:
                value_of_key = value
                #self.logger.info("value = {}".format(value_of_key))
                # checks if there are values in the list before iterating
                num_items = len(disjunct_list)        

                if (num_items > 0):

                    # checks all the items in disjunct_list for possible substitution
                    for i in range(0,num_items):
                        # different cases where variable could be, after left paren, before right paren, or between two commas
                        if "({}+1,".format(key_variable) in disjunct_list:
                            sumV = value_of_key + 1                            
                            disjunct_list = disjunct_list.replace("{}".format(key_variable), "{}".format(sumV))
                        if "({}-1,".format(key_variable) in disjunct_list:
                            difV = value_of_key - 1                            
                            disjunct_list = disjunct_list.replace("{}".format(key_variable), "{}".format(difV))
                        if "({},".format(key_variable) in disjunct_list:
                            disjunct_list = disjunct_list.replace("{}".format(key_variable), "{}".format(value_of_key))
                        if ",{}+1)".format(key_variable) in disjunct_list:
                            sumV = value + 1                            
                            disjunct_list = disjunct_list.replace("{}".format(key_variable), "{}".format(sumV))                        
                        if ",{}-1)".format(key_variable) in disjunct_list:
                            difV = value - 1                            
                            disjunct_list = disjunct_list.replace("{}".format(key_variable), "{}".format(difV))               
                        if ",{})".format(key_variable) in disjunct_list:
                            disjunct_list = disjunct_list.replace("{}".format(key_variable), "{}".format(value_of_key))
        #self.logger.info("dl = {}".format(disjunct_list))
        return disjunct_list
                

    def test_resolution(self, kb):

        #q = "OLDER(Lulu,Fifi)"
        #self.resolution(kb, q)

        q = "B(0,0)"
        self.resolution(kb, q)

    # pass on to KnowledgeBase
    def tell(self, assertion, x, y):
        for a in assertion:
            if a != '_':
                self.kb.tell(a, x, y)

    # Ask for best choice for dude given choices/neighbors
    def ask(self, query, x, y):
        choices = self.get_neighbors(x, y)
        choice = self.best_choice(choices)
        return choice

    # get neighbors and their known_map char's
    def get_neighbors(self, x, y):
        neighbors = {'_': [], 'm': [], 'd': [], 's': [], 'w': [], 'p':[], 'o': []}
        try:
            if x > 0:
                neighbors.get(self.kb.known_map[x - 1][y]).append('^')
        except:
            if neighbors.get(self.kb.known_map[x - 1][y]) == '>' or neighbors.get(self.kb.known_map[x - 1][y]) == 'v' or neighbors.get(self.kb.known_map[x - 1][y]) == '<' or neighbors.get(self.kb.known_map[x - 1][y]) == '^' or neighbors.get(self.kb.known_map[x-1][y]) == '$':
                neighbors.get('s').append('^')
        try:
            if x < len(self.kb.known_map) - 1:
                neighbors.get(self.kb.known_map[x + 1][y]).append('v')
        except:
            if neighbors.get(self.kb.known_map[x + 1][y]) == '>' or neighbors.get(self.kb.known_map[x + 1][y]) == 'v' or neighbors.get(self.kb.known_map[x + 1][y]) == '<' or neighbors.get(self.kb.known_map[x + 1][y]) == '^' or neighbors.get(self.kb.known_map[x+1][y]) == '$':
                neighbors.get('s').append('v')
        try:
            if y > 0:
                neighbors.get(self.kb.known_map[x][y - 1]).append('<')
        except:
            if neighbors.get(self.kb.known_map[x][y-1]) == '>' or neighbors.get(self.kb.known_map[x][y-1]) == 'v' or neighbors.get(self.kb.known_map[x][y-1]) == '<' or neighbors.get(self.kb.known_map[x][y-1]) == '^' or neighbors.get(self.kb.known_map[x][y-1]) == '$':
                neighbors.get('s').append('<')
        try:
            if y < len(self.kb.known_map) - 1:
                neighbors.get(self.kb.known_map[x][y + 1]).append('>')
        except:
            if neighbors.get(self.kb.known_map[x][y+1]) == '>' or neighbors.get(self.kb.known_map[x][y+1]) == 'v' or neighbors.get(self.kb.known_map[x][y+1]) == '<' or neighbors.get(self.kb.known_map[x][y+1]) == '^' or neighbors.get(self.kb.known_map[x][y+1]) == '$':
                neighbors.get('s').append('>')

        return neighbors

    # Choose according to priorities:
    # unexplored
    # possible pit or possible wumpus
    # shoot a wumpus or travel previously explored cell
    def best_choice(self, choices):
        if len(choices.get('_')) > 0: # unexplored
            return choices.get('_')
        elif len(choices.get('m')) > 0 or len(choices.get('d')) > 0:  # potentially unsafe cells
            return list(choices.get('m') + choices.get('d'))
        elif len(choices.get('s')) > 0 and len(choices.get('w')) > 0:  # Random choice between safe space and kill wumpi
            rand = 0, 1
            import random
            rand = random.choice(rand)
            if rand == 0:
                return choices.get('s')
            else:
                l = []
                for c in choices.get('w'):
                    l.append('%sk' % c)
                return l
        elif len(choices.get('s')) > 0:  # previously travelled
            return choices.get('s')
        elif len(choices.get('w')) > 0:  # kill a wumpus
            l = []
            for c in choices.get('w'):
                l.append('%sk' % c)
            return l

        else:
            return ["Stuck"]
