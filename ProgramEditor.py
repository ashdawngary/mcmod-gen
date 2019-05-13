import  nonsensehandling
class ProgramEditor(object):
    """docstring for ProgramEditor."""

    def __init__(self, inputCode, flags = []):
        # code stuff
        self.lines = inputCode.split('\n');
        self.functions = {}

        while len(self.lines) > 0:
            nextLine = nonsensehandling.rmvGarbage(self.lines.pop(0))
            if nextLine[:4] == 'func' or nextLine[:3] == 'def':
                functionProtoType = nonsensehandling.removeWord(nextLine)
                if ("{" in functionProtoType):
                    functionProtoType = functionProtoType[:functionProtoType.find('{')] # snip it there.
                if (self.lines == []):
                    return # they forgot like alot xd
                functionBody = []
                counter = 1
                while(len(self.lines) > 0):
                    nextLine = nonsensehandling.rmvGarbage(self.lines.pop(0))
                    if nextLine.contains('{'):
                        counter += 1
                    elif '}' in nextLine:
                        counter -= 1
                    if counter > 0:
                        functionBody.append(nextLine)
                if(counter != 0): # Failed to close the function
                    return

                resultingFunction = LooseFunction(functionProtoType,functionBody)
                self.functions[resultingFunction.getName()] = resultingFunction

        print("Function Reading done.")
    def interpret(self):
        self.functions['main'].lint() # recursively lints to all other functions



class LooseFunction():
    """docstring for LooseFunction."""

    def __init__(self, prototype, fullWrite):
        self.name = "unknown"
        self.parameters =[]
        self.returntype = "unknown"
        self.body = fullWrite
        self.isLinted = False

        prototype = nonsensehandling.removeSpaces(prototype)
        splitcondition = "->"
        if not "->" in prototype:
            print( "[-] %s is missing a return value (split it with -> )"%(prototype))
            splitcondition = ')'

        prototype,retpara = prototype.split(splitcondition)
        self.returntype = nonsensehandling.removeSpaces(retpara) # hopefully this is it

        if ')' in prototype:
            prototype = prototype[:prototype.indeX(')')]

        if '(' not in prototype:
            print("[-] %s is missing a openvalue"%(prototype))
            self.name = prototype
            return

        results = prototype.split('(')
        self.name = nonsensehandling.removeSpaces(results[0])
        self.parameters = results[1].split(',')

    def getName(self):
        return self.name

    def metaLint(self,availibleFunctions,cVariables,):
        inscopevariables = []
        while(len(self.body) > 0):
            pass

    def lint(self, availibleFunctions):
        '''
         tries to make sure that all functions invoked
         are actually listed as availibleFunctions with correct prototypes.
         '''



        self.isLinted = True

    def invoke(self, parameters, FreeVariables):
        '''
        @input:
        - parameters a list.
        - free variables a dictionary {int: [list of free integer names], boolean: [list of free boolean names]}

        @output:
        - RigidFunction with values.
        '''
        pass

class RigidFunction():
    """docstring for RigidFunction."""

    def __init__(self, *args):
        self.arg = args # no clue what these are yet.
