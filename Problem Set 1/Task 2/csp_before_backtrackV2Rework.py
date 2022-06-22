import numpy as np
import math


class problem():
    variables = {}
    constraints = []
    domains = {}
    nva = 0

    orderOfAssignment = []

    def __init__(self, variables, constraints, domains):
        self.variables = {v: None for v in variables}
        self.constraints = constraints
        self.domains = domains

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
            print(self.variables)  #########################################################
            if self.goalTest("full"):
                return

            # select variable to assign
            variableToAssign = [*self.variables.keys()][currentVarIndexInVariablesKeys]
            for val in self.domains[variableToAssign]: # select value to assign
                originalVal = self.variables[variableToAssign]
                # push
                self.variables[variableToAssign] = val
                self.nva += 1
                if self.goalTest("part"):
                    naiveBacktrackRecurser(self,currentVarIndexInVariablesKeys+1)
                    if self.goalTest("full"):
                        return
            # pop
            self.variables[variableToAssign] = originalVal
            self.nva += 1
            return

        naiveBacktrackRecurser(self,0)
        solution = self.variables if self.goalTest("full") else "no solution exists"
        print(f"solution = {solution}\nfound in {self.nva} variable assignemnts")


    def naiveBacktrackTester(self): # this version is brute force - O(Π(d_i)) - the product of all the domains of the i variables
        # this solution works for simple problems, but takes too long for problem A
        def naiveBacktrackRecurserTester(self, varI):
            print(self.variables)  #########################################################
            if self.goalTest("full"):
                return

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

    def newDomains(self):
        '''
        1. search through each constraint to see if you can find any who have all variables assigned other than one
        2. if such a constraint is found, search through original domain narrow it down to those which comply with the constraint
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
                    # print(unassigned)
                    # print(constraint.replace(unassignedVar,str(i)))
                    if eval(constraintToEval.replace(unassignedVar,str(i))):
                        newDomain.append(i)
                if len(newDomain) > 0:
                    self.domains[unassignedVar] = newDomain


    def variableSelector(self):  ###################################### WORK ON 3 * and 4
        '''
        1. choose variable with smallest domain
        2. if there's a tie choose the unassigned variable with the most constraints
        3. if there is a tie * return the one whose constraints contain the fewest other unassigned variables
        4. if there is a tie return either of them (choose the first arbitrarily)
        '''

        '''1. choose variable with smallest domain'''
            # cycle through the list and use the length of the domain to determine the candidates for varToReturn based on the smallestDomainSize
        varToReturn, smallestDomainSize = None, None
        for var,domain in self.domains.items():
            if self.variables[var] is None:
                if varToReturn == None:
                    varToReturn, smallestDomainSize = var, len(domain)
                else:
                    if len(domain) < smallestDomainSize: # if there's only one smallestDomainSize then varToReturn will be a string
                        varToReturn, smallestDomainSize = var, len(domain)
                    elif len(domain) == smallestDomainSize: # if there is a tie for the smallest domain then varToReturn will be a list
                        varToReturn = list(varToReturn) + [var]
                # if varToReturn is a string then it has the smallest domain, so return it
        if isinstance(varToReturn,str): return varToReturn

        '''2. else varToReturn must be a list so there's a tie, so choose variable that is in the most constraints'''
        varsWithSmallestDomains = varToReturn
        varToReturn, mostConstraints = None, None
        for var in varsWithSmallestDomains:
            # count the constraints containing the var
            constraintCount = 0
            for constraint in self.constraints:
                if constraint.find(var) != -1: # then the constraint has the var
                    constraintCount += 1
            if mostConstraints is None:
                varToReturn, mostConstraints = var, constraintCount
            else:
                if constraintCount > mostConstraints: # if there's only one var with the mostConstraints then varToReturn will be a string
                    varToReturn, mostConstraints = var, constraintCount
                elif constraintCount == mostConstraints: # if there is a tie for the vars with the mostConstraints then varToReturn will be a list
                    varToReturn = list(varToReturn) + [var]
        # if varToReturn is a string then it has the smallest domain so return it
        if isinstance(varToReturn,str): return varToReturn

        '''3. else varToReturn must be a list so there's a tie, arbitrarily return the first in varToReturn'''
        return varToReturn[0]


    def backtrackV2(self): # this version w
        def backtrackV2Recurser(self, lastVar):
            print(self.variables)
            if self.goalTest("full"):
                return # innermost start of termination

            originalDomains = self.domains  ####################################################
            self.newDomains()  ########################################################
            print("Domain issues:")
            for key in self.domains:
                if len(self.domains[key])==1:
                    print(f"\t{key}:{self.domains[key]}")
            print()
            currentVar = self.variableSelector() ###################################################
            print("ASSIGNING",currentVar)
            originalVal = self.variables[currentVar]
            self.orderOfAssignment.append(currentVar)
            for val in self.domains[currentVar]:  # select value to assign
                self.variables[currentVar] = val  # push
                self.nva += 1
                if self.goalTest("part"):
                    backtrackV2Recurser(self, lastVar)
                    if self.goalTest("full"):
                        return # middle passing termination
                else:
                    print("partial goaltest failed, trying a new value or backtracking...\n")
                    print("Domain issues:")
                    for key in self.domains:
                        if len(self.domains[key]) == 1:
                            print(f"\t{key}:{self.domains[key]}")
            # pop
            self.variables[currentVar] = originalVal
            self.nva += 1
            self.domains = originalDomains ###########################################
            #self.orderOfAssignment.pop()
            return # outer passing of termination

        backtrackV2Recurser(self, 'a')
        solution = self.variables if self.goalTest("full") else "no solution exists"
        print(f"solution = {solution}\nfound in {self.nva} variable assignemnts")