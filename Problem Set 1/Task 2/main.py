import csp

def charRange(a,z):
    return [chr(char) for char in range(ord(a),ord(z)+1)]

constraints = [
                "a==b+c+e+f", #c[0]=c1
                "d==e+f+21",
                "d**2==e*e*a+694",
                "e+f<a",
                "h*j+e*16==(g+i)**2-48", # c[4]=c5
                "a-c==(h-f)**2+4",
                "4*j==g**2+7",
                "2*m==k**2-25", # c[7]=c8
                "(n-o)**2==(j-f)*o*2",
                "n**2==m*j+100",
                "(l+n)**2+1875==g*(b+f)*(k+m+n+30)",
                "l*o==(a**2)*(k-g)",
                "l**3==m**2-(o*f*a)"
            ]
running = "yes"
while running == "yes":
    probType = input("What kind of problem do you want to run?\nEnter 'predefined' or 'custom':\n")
    if probType == "predefined":
        probChoice = "start"
        while probChoice != "A" and probChoice != "B" and probChoice != "C":
            probChoice = input("Which problem do you want to run?\nEnter 'A', 'B', or 'C'\n")
            if probChoice == "A":
                A = csp.problem(
                    variables = charRange("a","f"),
                    constraints = constraints[:4],
                    domains = {v:list(range(1,101)) for v in charRange("a","f")}
                )
                A.backtrackV3()
                another = input("Do you want to run another problem?\nEnter 'yes' or 'no':\n")
                if another == "yes":
                    break
                else:
                    exit()
            elif probChoice == "B":
                B = csp.problem(
                    variables = charRange("a","j"),
                    constraints = constraints[:7],
                    domains = {v:list(range(1,101)) for v in charRange("a","j")}
                )
                B.backtrackV3()
                another = input("Do you want to run another problem?\nEnter 'yes' or 'no':\n")
                if another == "yes":
                    break
                else:
                    exit()
            elif probChoice == "C":
                print("This one takes roughly a minute or so.")
                C = csp.problem(
                    variables = charRange("a","o"),
                    constraints = constraints[:13],
                    domains = {v:list(range(1,101)) for v in charRange("a","o")}
                )
                C.backtrackV3()
                running = input("Do you want to run another problem?\nIf so type 'yes', otherwise enter any character to exit:\n")
            else:
                probChoice = input("Invalid Choice. Try again.\nEnter 'A', 'B', or 'C'")
    elif probType == "custom":
        print("Enter your variables as single alphabetic characters.\nWhen done just hit enter.")
        vars = set()
        while True:
            newVar = input()
            if newVar == "": break
            else:
                while not newVar.isalpha() or len(newVar) != 1:
                    newVar = input("That last input either wasn't an alphabetic character or was more than one character. Please try again:\n")
                vars.add(newVar)

        print("Now enter the domains for each variable. Enter the min value and the max value:\n")
        domains = {}
        for var in sorted(list(vars)):
            print(f"For {var}:")
            min,max = input("\tmin = "), input("\tmax = ")
            domains[var] = list(range(int(min),int(max)+1))

        print("\nNow enter your constraints as python evaluable code (i.e. 1+2==3 ).\nPlease only input valid variables.\nWhen done just hit enter.\n")
        constraints = []
        okSymbols = set([">","<","=", "!"])
        while True:
            newConstraint = input()
            if newConstraint == "": break
            else:
                invalidChar = False # check for invalid chars
                for char in newConstraint: # look for invalid chars
                    if char.isalpha():
                        if char not in vars:
                            invalidChar = True
                            break
                if invalidChar:
                    print("Your constraint contained an invalid character. Please enter it again or hit enter to finish constraint input.")
                    continue
                editedConstraint = newConstraint
                for char in editedConstraint:
                    if char in vars:
                        editedConstraint = editedConstraint.replace(char,str(domains[char][0]))
                try:
                    eval(editedConstraint)
                except:
                    print("Your constraint was not a valid python evaluable. Please enter it again or hit enter to finish constraint input:\n")
                    continue
                constraints.append(newConstraint)

        print("Your problem is defined as follows:")
        print("Variables and domains")
        for var in vars:
            print(f"{var} has a domain of: [{domains[var][0]},{domains[var][len(domains[var])-1]}]")
        print("With constraints:")
        for constraint in constraints:
            print(constraint)
        correct = input("Is this correct? Enter 'yes' to continue to evaluation, otherwise press any character to problem input over.\n")
        if correct == 'yes':
            customProblem = csp.problem(
                variables = vars,
                constraints = constraints,
                domains = domains
            )
            customProblem.backtrackV3()

            another = input("Do you want to run another problem?\nIf so type 'yes', otherwise enter any character to exit:\n")
            if another == "yes":
                notDone = True
            else:
                notDone = False


