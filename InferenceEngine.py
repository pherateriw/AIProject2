import re

class InferenceEngine:
    def __init__(self):
        # theta is a dictionary of all substitutions where the variable is the key, values are the values 
        self.theta = {}        
    
    
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
    
    # reminder: unification takes two atomic sentences P and Q and returns a substitution that makes
    # P and Q identical.
    # This implementation uses the method described by Russell and Norvig to perform unification (p 328)  
    # this method differs from R&N's implementation in that we do not handle compound
    # expressions (functions), since none of our rules require it. 
    # input: x is a variable, constant or list 
    # input: y is a variable, constant or list, or compound expression
    # input: theta, the substitution built up so far () 
    # function returns a substitution to make x and y identical   
    def unify(self, P, Q, theta):               
            
        # if there is no theta that can unify x and y, return false
        if self.theta == False:
            return False             
        # if x and y are the same, no self.need for a substitution    
        elif P == Q:
            print("No need to unify {} and {}".format(P, Q))           
            return self.theta
        elif self.is_variable(P):   
            return self.unify_var(P, Q, theta)
        elif self.is_variable(Q):            
            return self.unify_var(Q, P, theta)
        #elif (is_list(x) and is_list(y)):
        #    return unify (x.rest, y.rest, unify(x.first, y.first, theta))
        else:        
            return False

    # note: we have specified that a single variable will be one lowercase character a-z
    def is_variable(self, X):
        pattern = re.compile("[a-z]")
        
        if (pattern.match(X)):         
            print("in is variable")
            return True
        else:
            return False

    # helper function for unification, also inspired by Russell and Norvig implementation 
    # omitted the occur check bc it did not seem necessary for this application, and 
    # bc of complexity concerns    
    def unify_var(self, var, x, theta):  

        if var in self.theta:
            print("{} in theta".format(var))
            for val in self.theta[var]:
                if (var in self.theta) and (val in self.theta[var]):
                    return self.unify(val,x,theta)
                # probably not right
                elif(x in self.theta) and (val in self.theta[x]):
                    print("in second if")
                    return self.unify(var,val,theta)
                else:
                    # PROBABLY NOT RIGHT
                    return self.theta[var].append(x)                     
        else:
            print("{} not in theta".format(var))
            # add var, x to theta
            self.theta.setdefault(var,[])
            self.theta[var].append(x)
            
            print(self.theta)            
            
            return self.theta 
       