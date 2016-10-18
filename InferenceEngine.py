class KnowledgeBase:

    # uses the method described by Russell and Norvig to perform unification (p 328)  
    # this method differs from R&N's implementation in that we do not handle compound
    # expressions (functions), since none of our rules require it 
    # input: x is a variable, constant or list 
    # input: y is a variable, constant or list, or compound expression
    # input: theta, the substitution built up so far () 
    # function returns a substitution to make x and y identical   
    def unify(x, y, theta):
        # if there is no theta that can unify x and y, return false
        #if theta == False:
        #    return False
        # if x and y are the same, no need for a substitution    
        #elif x == y:
        #    return theta
        #elif(is_variable(x)):
        #    return unify_var(x, y, theta)
        #elif (is_variable(y)): 
        #    return unify_var(x, y, theta)
        #elif (is_compound(x) and is_compound(y)):
        #    return unify(x.args, y.args, unify(x.op, y,op, theta))
        #elif (is_list(x) and is_list(y)):
        #    return unify (x.rest, y.rest, unify(x.first, y.first, theta))
        #else:
            return False

    # helper function for unification, also inspired by Russell and Norvig implementation 
    # omitted the occur check bc it did not seem necessary for this application, and 
    # bc of complexity concerns     
    def unify_var(var, x, theta):
        #if var/val in theta:
        #    return unify(val, x, 0)
        #elif x/val in theta:
        #    return unify(var, val, theta) 
        #else:
        #    return add{var/x} to theta            

    # helper function for unification, also inspired by Russell and Norvig implementation 
    # omitted the occur check bc it did not seem necessary for this application, and 
    # bc of complexity concerns     
    def is_variable(x):
        #if var/val in theta:
         #   return unify(val, x, 0)
        #elif x/val in theta:
        #    return unify(var, val, theta) 
        #else:
        #    return add{var/x} to theta   