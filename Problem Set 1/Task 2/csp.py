import copy


class problem():
    variables = {}
    constraints = []
    domains = {}
    nva = 0

    orderOfAssignment = []
    recurseID = 1
    solutionCount = 0

    def __init__(self, variables, constraints, domains):
        self.variables = {v: None for v in variables}
        self.constraints = constraints
        self.domains = domains
        self.orderOfAssignment = []
        self.recurseID = 1
        self.solutionCount = 0

    def goalTest(self,type):
        # let's first evaluate all our constraints and store the evaluations in constraintEvaluations
        constraintEvaluations = []
        for constraint in self.constraints:  # for each constraint
            constraintToEval = constraint  # we don't want to alter the original constraint
            for char in constraintToEval:  # for each character in the constraint
                if char.isalpha():  # if the character is alphabetic
                    value = self.variables[char]  # get that variable's value
                    if value is None:
                        constraintToEval = "None"
                        break  # no need to continue parsing, move on to next constraint
                    else:  # replace it with its value
                        constraintToEval = constraintToEval.replace(char, str(self.variables[char]))
            # after all characters have been parsed evaluate the constraint and add it to constraintEvaluations
            constraintEvaluations.append(eval(constraintToEval))

        # now look through constraintEvaluations, counting all evaluations that were None
        partialPass = True  # if all non-None evaluations are true then partialPass is true
        noneCounter = 0
        for evaluation in constraintEvaluations:
            if evaluation is not None:
                partialPass = partialPass and evaluation
            else:
                noneCounter += 1
        # if partialPass is true and there were no None values then fullPass is true too!
        fullPass = partialPass and noneCounter == 0

        if type=="full": return fullPass
        elif type=="part": return partialPass
        else:
            print("Invalid keyword passed to goalTest. Exiting")
            exit(1)

    def naiveBacktrack(self): # this version is brute force - O(Π(d_i)) - the product of all the domains of the i variables
        def naiveBacktrackRecurser(self, currentVarIndexInVariablesKeys):
            if self.goalTest("full"):
                return
            else:
                # select variable to assign
                currentVar = [*self.variables.keys()][currentVarIndexInVariablesKeys]
                self.orderOfAssignment.append(currentVar)
                originalVal = self.variables[currentVar]
                for val in self.domains[currentVar]: # select value to assign
                    # push
                    self.variables[currentVar] = val
                    self.nva += 1
                    if self.goalTest("part"):
                        naiveBacktrackRecurser(self,currentVarIndexInVariablesKeys+1)
                        if self.goalTest("full"):
                            return
                # pop
                self.variables[currentVar] = originalVal
                self.nva += 1
                return

        naiveBacktrackRecurser(self,0)
        solution = self.variables if self.goalTest("full") else "no solution exists"
        print(f"solution = {solution}\nfound in {self.nva} variable assignemnts")
        print("order of assignments:", self.orderOfAssignment)

    def naiveBacktrackTester(self): # this version is brute force - O(Π(d_i)) - the product of all the domains of the i variables
        # this solution works for simple problems, but takes too long for problem A
        def naiveBacktrackRecurserTester(self, varI):
            print(self.variables)  #########################################################
            if self.goalTest("full"):
                return
            else:
                # select variable to assign
                variableToAssign = vars[varI]
                originalVal = self.variables[variableToAssign]
                for val in self.domains[variableToAssign]: # select value to assign
                    # push
                    self.variables[variableToAssign] = val
                    self.nva += 1
                    if self.goalTest("part"):
                        naiveBacktrackRecurserTester(self,varI+1)
                        if self.goalTest("full"):
                            return
                    # pop
                self.variables[variableToAssign] = originalVal
                self.nva += 1
                return
        vars = ['a','b','c']
        naiveBacktrackRecurserTester(self,0)
        solution = self.variables if self.goalTest("full") else "no solution exists"
        print(f"solution = {solution}\nfound in {self.nva} variable assignemnts")

    def variableSelector(self):
        '''
        1. choose variable with smallest domain
        2. if there's a tie choose the unassigned variable with the most constraints
        3. if there's a tie, arbitrarily return the first in varToReturn
        '''

        '''1. choose variable with smallest domain'''
        # cycle through the list and use the length of the domain to determine the candidates for varToReturn based on the smallestDomainSize
        varToReturn, smallestDomainSize = None, None
        for var, domain in self.domains.items():
            if self.variables[var] is None:
                if varToReturn is None:
                    varToReturn, smallestDomainSize = var, len(domain)
                else:
                    if len(domain) < smallestDomainSize:  # if there's only one smallestDomainSize then varToReturn
                        # will be a string
                        varToReturn, smallestDomainSize = var, len(domain)
                    elif len(
                            domain) == smallestDomainSize:  # if there is a tie for the smallest domain then varToReturn will be a list
                        varToReturn = list(varToReturn) + [var]
                # if varToReturn is a string then it has the smallest domain, so return it
        if isinstance(varToReturn, str) or varToReturn is None: return varToReturn ########################################################################## new for v4

        '''2. else varToReturn must be a list so there's a tie, so choose variable that is in the most constraints'''
        varsWithSmallestDomains = varToReturn
        varToReturn, mostConstraints = None, None
        for var in varsWithSmallestDomains:
            # count the constraints containing the var
            constraintCount = 0
            for constraint in self.constraints:
                if constraint.find(var) != -1:  # then the constraint has the var
                    constraintCount += 1

            # compare to earlier iterations to find best
            if mostConstraints is None:  # this must be the first iteration
                varToReturn, mostConstraints = var, constraintCount
            else:  # every iteration but the first
                if constraintCount > mostConstraints:  # if there's only one var with the mostConstraints then varToReturn will be a string
                    varToReturn, mostConstraints = var, constraintCount
                elif constraintCount == mostConstraints:  # if there is a tie for the vars with the mostConstraints then varToReturn will be a list
                    varToReturn = list(varToReturn) + [var]
        # if varToReturn is a string then it has the smallest domain so return it
        if isinstance(varToReturn, str): return varToReturn

        '''3. there's a tie, arbitrarily return the first in varToReturn'''
        return varToReturn[0]

    def backtrackV2(self):
        # this version uses a heuristic for choosing which variable to assign
        def backtrackV2Recurser(self):
            thisRecursion = self.recurseID
            if self.goalTest("full"):
                return # innermost start of termination
            else:
                currentVar = self.variableSelector() ################################################### New
                originalVal = self.variables[currentVar]
                self.orderOfAssignment.append(currentVar)
                for val in self.domains[currentVar]:  # select value to assign
                    self.variables[currentVar] = val  # push
                    self.nva += 1
                    if self.goalTest("part"):
                        self.recurseID += 1
                        backtrackV2Recurser(self)
                        if self.goalTest("full"):
                            return # middle passing termination
                # pop
                self.variables[currentVar] = originalVal
                self.nva += 1
                self.orderOfAssignment.pop()
                return # outer passing of termination

        backtrackV2Recurser(self)
        solution = self.variables if self.goalTest("full") else "no solution exists"
        print(f"solution = {solution}\nfound in {self.nva} variable assignemnts")
        print("order of assignments:", self.orderOfAssignment)

    def newDomains(self):
        '''
        1. search through each constraint to see if you can find any who have all variables assigned other than one
        2. if such a constraint is found, search through its original domain, narrow it down to those which comply with the constraint
        '''
        for constraint in self.constraints:
            # for this particular constraint get only relevant variables and their values
            relevantVariables = {c:self.variables[c] for c in constraint if c.isalpha()}
            # count how many values are None (i.e. still unassigned)
            unassigned = {key:val for key,val in relevantVariables.items() if val is None}
            if len(unassigned) == 1: # we found one!
                unassignedVar = list(unassigned.keys())[0] # get the unassigned variable
                #first we need to replace all the already assigned variables with their values
                constraintToEval = constraint
                for var in relevantVariables:
                    if var != unassignedVar:  # but leave unassigned as a variable
                        constraintToEval = constraintToEval.replace(var,str(self.variables[var]))

                newDomain = []
                # loop through old domain and see which values could fit
                for i in self.domains[unassignedVar]:
                    if eval(constraintToEval.replace(unassignedVar,str(i))):
                        newDomain.append(i)
                #if len(newDomain) > 0: #####################################################################added this to fix a bug, but it resulted in a different bug later on
                self.domains[unassignedVar] = newDomain

    def backtrackV3(self):
        # this version uses a heuristic for choosing which variable to assign and
        # as assignments are made it reduces the domain for relevant variables
        def backtrackV3Recurser(self):
            thisRecursion = self.recurseID
            #print(thisRecursion)
            if self.goalTest("full"):
                return # innermost start of termination
            else:
                originalDomains = copy.deepcopy(self.domains)  ################################################### New
                self.newDomains()  ################################################### New
                if len([len(domain) for domain in self.domains.values() if len(domain) == 0]) > 0: # if there are any domains whose length are 0 dead end detected
                    return
                currentVar = self.variableSelector()
                originalVal = self.variables[currentVar]
                self.orderOfAssignment.append(currentVar)
                for val in self.domains[currentVar]:  # select value to assign
                    self.variables[currentVar] = val  # push
                    self.nva += 1
                    if self.goalTest("part"):
                        self.recurseID += 1
                        backtrackV3Recurser(self) # this may change the domain
                        self.domains = copy.deepcopy(originalDomains) # pop the domain
                        if self.goalTest("full"):
                            return # middle passing termination
                # pop
                self.variables[currentVar] = originalVal
                self.nva += 1
                self.domains = copy.deepcopy(originalDomains) ################################################### New
                self.orderOfAssignment.pop()
                return # outer passing of termination

        backtrackV3Recurser(self)
        solution = self.variables if self.goalTest("full") else "no solution exists"
        print(f"solution = {solution}\nfound in {self.nva} variable assignemnts")
        print("order of assignments:", self.orderOfAssignment)

    def countSolutions(self): #this will get updated to use backtrackV4 eventually
        def countSolutionsWithModifiedBacktrackV3Recurser(self):
            thisRecursion = self.recurseID
            if self.goalTest("full"):
                self.solutionCount += 1
            else:
                originalDomains = copy.deepcopy(self.domains)
                self.newDomains()
                if len([len(domain) for domain in self.domains.values() if len(domain) == 0]) > 0: # if there are any domains whose length are 0 dead end detected
                    return
                currentVar = self.variableSelector()
                originalVal = self.variables[currentVar]
                self.orderOfAssignment.append(currentVar)
                for val in self.domains[currentVar]:  # select value to assign
                    self.variables[currentVar] = val  # push
                    self.nva += 1
                    if self.goalTest("part"):
                        self.recurseID += 1
                        countSolutionsWithModifiedBacktrackV3Recurser(self) # this will change domains which is why we need to "pop" the domain changes below
                        self.domains = copy.deepcopy(originalDomains) ################################################################################################################BUG FIX
                # pop
                self.variables[currentVar] = originalVal #the for loop 'changes' the variable for us so we only have to manually change it back to the original once, here
                self.nva += 1
                self.domains = copy.deepcopy(originalDomains)
                self.orderOfAssignment.pop()
                return  # outer passing of termination

        def countSolutionsWithModifiedBacktrackV4Recurser(self):
            thisRecursion = self.recurseID
            if self.goalTest("full"):
                self.solutionCount += 1
            else:
                originalDomains = copy.deepcopy(self.domains)
                self.newDomains()
                if len([len(domain) for domain in self.domains.values() if
                        len(domain) == 0]) > 0:  # if there are any domains whose length are 0 dead end detected
                    return
                currentVar = self.variableSelector()
                originalVal = self.variables[currentVar]
                self.orderOfAssignment.append(currentVar)
                orderedValuesToTry = self.leastConstrainingValuesFirst(currentVar)  ################################################### New
                for val in orderedValuesToTry:  # select value to assign
                    self.variables[currentVar] = val  # push
                    self.nva += 1
                    if self.goalTest("part"):
                        self.recurseID += 1
                        countSolutionsWithModifiedBacktrackV4Recurser(self)
                        self.domains = copy.deepcopy(originalDomains)
                # pop
                self.variables[currentVar] = originalVal
                self.nva += 1
                self.domains = copy.deepcopy(originalDomains)
                self.orderOfAssignment.pop()
                return  # outer passing of termination

        countSolutionsWithModifiedBacktrackV3Recurser(self)
        #countSolutionsWithModifiedBacktrackV4Recurser(self)
        return self.solutionCount

    def leastConstrainingValuesFirst(self, curVar):
        '''
        1. find all relevantConstraints involving curVar and the relevantVariables. relevantConstraints should be edited
            so that if a value has already been assigned to a variable earlier then that value is substituted in place
            of that variable here

        2. make a list of valuesToTry - this will be a list of tuples with the first value of each tuple being the
        proposed value for curVar and the second value is the numberOfSolutions to that value's constraint
        sub-problem. To do this we'll have to cycle through all possible values for curVar, forming sub problems,
        and count how many solutions exist to that sub-problem

        3. sort valuesToTry such that numberOfSolutions is ordered most to least, then strip numberOfSolutions
            and return valuesToTry
        '''

        ''' 1. let's make our subproblem template '''
        relevantConstraints = []
        relevantVariables = set() # we don't want duplicates
        for constraint in self.constraints:
            if constraint.find(curVar) != -1: # this constraint has curVar, so it's relevant
                editedConstraint = copy.deepcopy(constraint)
                #if a value has already been assigned for a variable therein, substitute that value in place of the variable
                for char in editedConstraint:
                    if char.isalpha() and self.variables[char] is not None and char != curVar:
                        editedConstraint = editedConstraint.replace(char,str(self.variables[char]))
                    elif char.isalpha() and char != curVar: # then it is unassigned (None) and therefore relevant to the subproblem tempalte
                        relevantVariables.add(char)
                relevantConstraints.append(editedConstraint)

        ''' 2. count solutions to each subproblem '''
        subProblemDomains = {var:domain for var,domain in self.domains.items() if var in relevantVariables}
        valuesToTry = []
        for val in self.domains[curVar]:
            self.nva += 1
            subProblemConstraints = [constraint.replace(curVar, str(val)) for constraint in relevantConstraints]
            subProblem = problem(
                variables = list(relevantVariables),
                constraints = subProblemConstraints,
                domains = copy.deepcopy(subProblemDomains)
            )
            subProblem.countSolutions()
            self.nva += subProblem.nva
            numberOfSolutions = subProblem.solutionCount
            if numberOfSolutions > 0: # we don't even want to try the value if there are no possible solutions for it
                valuesToTry.append( (val, numberOfSolutions) )

        ''' 3. sort valuesToTry such that numberOfSolutions is ordered most to least, then strip numberOfSolutions
            and return valuesToTry '''
        valuesToTry.sort(key=lambda tup:tup[1], reverse=True) # for each tuple, tup in the list, use tup[1] as the key and sort in reverse order (max to min)
        return [tup[0] for tup in valuesToTry] #return a list consisting of just the first elements

    def backtrackV4(self):
        # this version uses a heuristic for choosing which variable to assign and
        # as assignments are made it reduces the domain for relevant variables and
        # valueOrdering attempts forward checking to order the value assignment s.t. the Least Constraining Values are chosen first
        def backtrackV4Recurser(self):
            thisRecursion = self.recurseID
            if self.goalTest("full"):
                return # innermost start of termination
            else:
                originalDomains = copy.deepcopy(self.domains)
                self.newDomains()
                if len([len(domain) for domain in self.domains.values() if len(domain) == 0]) > 0: # if there are any domains whose length are 0 dead end detected !!!!!!!!!!!NEED TO ADD TO OTHER PLACES!!!!!!!!!!!!!!!!!
                    return
                currentVar = self.variableSelector()
                originalVal = self.variables[currentVar]
                self.orderOfAssignment.append(currentVar)
                orderedValuesToTry = self.leastConstrainingValuesFirst(currentVar) ################################################### New
                for val in orderedValuesToTry:  # select value to assign
                    self.variables[currentVar] = val  # push
                    self.nva += 1
                    if self.goalTest("part"):
                        self.recurseID += 1
                        backtrackV4Recurser(self)
                        self.domains = copy.deepcopy(originalDomains)
                        if self.goalTest("full"):
                            return # middle passing termination
                # pop
                self.variables[currentVar] = originalVal
                self.nva += 1
                self.domains = copy.deepcopy(originalDomains)
                self.orderOfAssignment.pop()
                return # outer passing of termination

        backtrackV4Recurser(self)
        solution = self.variables if self.goalTest("full") else "no solution exists"
        print(f"solution = {solution}\nfound in {self.nva} variable assignemnts")
        print("order of assignments:", self.orderOfAssignment)
