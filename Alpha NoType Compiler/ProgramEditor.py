import  nonsensehandling

def cross(set1,set2):
    newset = []
    for i in set1:
        for j in set2:
            newset.append(i+j)
    return newset;
charset = [chr(i) for i in range(ord('a'),ord('z'))]
diword = cross(charset,charset)
AVAILIBLE = cross(["#"],cross(diword,diword))

class ProgramEditor(object):
    """docstring for ProgramEditor."""

    def __init__(self, inputCode, flags = []):
        # code stuff
        self.lines = inputCode;
        self.functions = {}
        self.value = 0
        print self.lines
        while len(self.lines) > 0:
            nextLine = nonsensehandling.rmvGarbage(self.lines.pop(0))
            #print nextLine
            if nextLine[:4] == 'func' or nextLine[:3] == 'def':
                functionProtoType = nonsensehandling.removeWord(nextLine)
                if ("{" in functionProtoType):
                    functionProtoType = functionProtoType[:functionProtoType.find('{')] # snip it there.
                if (self.lines == []):
                    print "got an empty defintion??"
                    return # they forgot like alot xd
                functionBody = []
                counter = 1 if '{' in nextLine else 0
                if '{' in self.lines[0] and counter == 0:
                    counter = 1
                    self.lines[0] = self.lines[0][self.lines[0].find('{')+1:]
                    if len(self.lines[0].replace(' ','')) == 0:
                        self.lines.pop(0)

                while(len(self.lines) > 0):
                    nextLine = nonsensehandling.rmvGarbage(self.lines.pop(0))
                    #print "inf",nextLine,counter
                    if '{' in nextLine:
                        counter += 1
                    elif '}' in nextLine:
                        counter -= 1
                    if counter > 0 :
                        functionBody.append(nextLine)
                    if counter == 0:
                        break;
                if(counter != 0): # Failed to close the function
                    print "Failed to close a function.  Crashing"
                    return

                resultingFunction = LooseFunction(functionProtoType,functionBody)
                self.functions[resultingFunction.getName()] = resultingFunction
                self.value = min(resultingFunction.lint(),self.value)

        print("Function Reading done.")
        for func in self.functions.values():
            print func.getName(),func.parameters,func.returntype
    def interpret(self):
        return self.value
    def generateProgram(self):
        code = self.functions['main'].methodinvoke([], [], self.functions)
        return code
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
            print( "[W] %s is missing a return value (split it with -> )"%(prototype))
            splitcondition = ')'

        prototype,retpara = prototype.split(splitcondition)
        self.returntype = nonsensehandling.removeSpaces(retpara) # hopefully this is it

        if ')' in prototype:
            prototype = prototype[:prototype.index(')')]

        if '(' not in prototype:
            print("[-] %s is missing a openvalue"%(prototype))
            self.name = prototype
            return

        results = prototype.split('(')
        self.name = nonsensehandling.removeSpaces(results[0])
        self.parameters = filter(lambda x: len(x) > 0, map(lambda x: x.replace(" ",""),results[1].split(',')))

    def getName(self):
        return self.name



    def lint(self):
        '''
         tries to make sure that all functions invoked
         are actually listed as availibleFunctions with correct prototypes.
         '''
        queue = []
        pairing = {
            '{':'}',
            '[':']',
            '(':')'
        }
        reversePairing = {
            '}':'{',
            ']':'[',
            ')':'('
        }
        stackcopy= list(self.body)
        while(len(stackcopy) > 0):
            k = stackcopy.pop(0)
            #print "analyzing",k
            for char in k:
                if char in pairing.keys():
                    #print 'pushing: ', char
                    queue.append(char)
                elif char in pairing.values():
                    if len(queue) == 0:
                        self.announceError("Unpaired got a %s with no opening: %s"%(char,reversePairing[char]))
                        return -1
                    if pairing[queue.pop()] != char:
                        print "MisPaired"
                        return -1
        self.isLinted = True
        return len(queue) == 0
    def generateCoolName(self):
        return AVAILIBLE.pop(0)
    def extractOuterParameters(self,string):
        params = [""]
        clevel = 0
        string = list(string)
        while len(string) > 0:
            q  = string.pop(0)
            if q == '(':
                clevel += 1
            elif q == ')':
                clevel -= 1;
            elif q== ',' and clevel == 0:
                params.append("")
            else:
                params[-1] = params[-1] + q
        return params
    def announceError(self,message):
        print "****************************************"
        print "             ERROR(%s)                      "%(self.name)
        print message
        print "****************************************"
    def evaluateWithReturnPointer(self,line, rtnptr , cScopeVariables, freed, methodHandles): # marped
        #print "Interpretting line with return pointer: %s, variables: %s free variables: %s"%(rtnptr,cScopeVariables,freed)
        # returns a handle
        # k(a - q(b)) + c
        # litearly just translate this thing.
        tokens = [""]
        queue = list(line)
        cLevel = 0
        while len(queue) > 0:
            nextC = queue.pop(0)
            if nextC in "*-+/%" and cLevel == 0:
                tokens.append(nextC)
                tokens.append("")
            elif (nextC in ['<','>','=']) and cLevel == 0:
                if queue[0] == '=':
                    tokens.append(nextC+'=')
                    queue.pop(0)
                else:
                    tokens.append(nextC)
                tokens.append('')
            else:
                if nextC == 'a' and queue[:3] == ['n','d',' ']:
                    tokens.append('and')
                    tokens.append('')
                    queue = queue[3:]
                elif nextC == 'o' and queue[:2] == ['r',' ']:
                    tokens.append('or')
                    tokens.append('')
                    queue = queue[2:]
                elif nextC == '&' and queue[:1] == ['&']:
                    tokens.append('&&')
                    tokens.append('')
                    queue = queue[1:]
                elif nextC == '|' and queue[:1] == ['|']:
                    tokens.append('||')
                    tokens.append('')
                    queue = queue[1:]
                else:
                    if nextC == '(':
                        cLevel += 1
                    elif nextC == ')':
                        cLevel -= 1;
                    tokens[-1] = tokens[-1] + nextC

        #print "[>]Need to Evaluate", tokens
        tokens = map(lambda x: x.replace(" ","").replace("\t",""), tokens)
        toReliquish = [] # pointers to untrash when done
        codebefore = []
        aggregate = []
        for token in tokens:
            if token in "*-+/%":
                aggregate.append(token)
                continue
            if token in ["<", ">","<=",">=","==","&&","||"]:
                aggregate.append(token)
                continue
            if token == "and":
                aggregate.append("&&")
                continue
            if token == "or":
                aggregate.append('||')
                continue
            if '(' in token:
                newpointer = ""

                todo = self.extractOuterParameters(nonsensehandling.exactParameters(token))
                #print "params",todo
                parameters = []
                for todo_part in todo:
                    if todo_part[0] == '&': # we've got a pointer on the loose.
                        if not todo_part[1:] in cScopeVariables:
                            self.announceError("[-]invalid base for pointer : ",todopart[1:])
                        else:
                            newpointer = cScopeVariables[todo_part[1:]]
                    else:
                        if len(freed) == 0:
                            #print "[!]oops! we need another pointer.(function input pointer)"
                            newpointer = self.generateCoolName()
                        else:
                            newpointer = freed.pop(0)
                        #print "[*]obtained a pointer for method call ", nonsensehandling.getFunctionName(token), newpointer
                        toReliquish.append(newpointer)
                        v = self.evaluateWithReturnPointer(todo_part,newpointer,cScopeVariables,freed,methodHandles)
                        codebefore.extend(v)
                    parameters.append(newpointer)




                vpointer = ""
                if len(tokens) == 1:
                    vpointer = rtnptr # checkmate
                elif len(freed) == 0:
                    #print "[!]oops! we need another pointer.(function value pointer)"
                    vpointer = self.generateCoolName()
                    toReliquish.append(vpointer)
                else:
                    vpointer = freed.pop(0)
                    toReliquish.append(vpointer)

                targetinvoke = nonsensehandling.getFunctionName(token)
                #codebefore.append("compupte "+targetinvoke+"(%s)"%(','.join(parameters))+ " to contribute to "+ rtnptr+" via "+vpointer )
                if not targetinvoke in methodHandles:
                    self.announceError( '[-]Unable to find func: '+targetinvoke)


                executioncode = methodHandles[targetinvoke].methodinvoke(parameters,freed,methodHandles,returnHandle=vpointer)
                codebefore.extend(executioncode)
                aggregate.append(vpointer)
            elif token in cScopeVariables:
                #print "[*]Got a pre-exist reference to: %s"%(token)
                aggregate.append(cScopeVariables[token])
            else:
                try:
                    aggregate.append(str(int(token)))
                except:
                    self.announceError( "[-]error, no reference to: `%s`\n Line: `%s`\nCurrent Variables: %s"%(token,line,cScopeVariables))

        if (rtnptr != None):
            aggregate = [rtnptr+" ="] + aggregate #+ ["-- evaluating %s"%(line)]

            codebefore.append(' '.join(aggregate))
        freed.extend(toReliquish)
        return codebefore
    def matchParameters(self,inputParameters):
        scope = {}
        if len(self.parameters) != len(inputParameters):
            self.announceError( "[-][%s]Incorrect Parameter Matching (%s original but passed %s)"%(self.name,len(self.parameters),len(inputParameters)))
            return scope
        else:
            for i in self.parameters:
                scope[i] = inputParameters.pop(0)

        return scope
    def queryVariable(self,freed):
        if len(freed) == 0:
            return self.generateCoolName()
        else:
            return freed.pop()
    def queryBoolean(self,freed):
        return self.queryVariable(freed).replace('#','') # cast it back into a boolean/flag from int/counter

    def methodinvoke(self,parameters,free,methodHandles,returnHandle=False):
        currentScope = self.matchParameters(parameters)
        copycode = list(self.body)
        returnedHandle = self.queryBoolean(free)
        answer,throw = self.invoke(copycode,currentScope,free,methodHandles,returnHandle=returnHandle, returnedHandle = returnedHandle)
        #print currentScope,self.parameters
        for i in currentScope:
            if not i in self.parameters:
                free.append(currentScope[i])

        return answer
    def deIntersectFreeMemory(self,oldscope,newScope,freeStack):
        #compares oldscope to new scope, will relinquish variables if they arent used in the oldscope
        for variable in newScope.keys():
            if not variable in oldscope:
                v = newScope.pop(variable)
                if not v in oldscope.values():
                    freeStack.append(v)

    def handleNativeCode(self,line,code,currentScope):
        ''' returns code,copycode '''

        clevel = 1 if '{' in line else 0
        nativeCode =[]
        while (len(code) > 0 and clevel >= 0):
            popped = code.pop(0)
            if '{' in popped:
                clevel += 1;
            elif '}' in popped:
                clevel -= 1;
            if clevel != 0:
                revisedPopped = []
                tokens = popped.split('!')
                for q in tokens:
                    mp = q.replace(' ','')
                    if mp in currentScope:
                        revisedPopped.append(currentScope[mp])
                    else:
                        #self.announceError('couldnt find: '+mp)
                        revisedPopped.append(q)
                nativeCode.append(''.join(revisedPopped))
            else:
                break
        return nativeCode,code

    def handleIfStatement(self,evalExpression,code,currentScope,free,methodHandles,returnHandle=False,returnedHandle=False):
        scopecopy = dict(currentScope)
        toFree = []
        toWrite = []

        booleanCheckVar = self.queryBoolean(free)
        evalExpression = nonsensehandling.exactParameters(evalExpression)
        isReturnStatement = False
        prelimCheckCode = self.evaluateWithReturnPointer(evalExpression,booleanCheckVar,currentScope,free,methodHandles)

        clevel = 1 if '{' in evalExpression else 0
        toInvokeOnIf =[]
        while (len(code) > 0 and clevel >= 0):
            popped = code.pop(0)
            if '{' in popped:
                clevel += 1;
            elif '}' in popped:
                clevel -= 1;
            if clevel != 0:
                toInvokeOnIf.append(popped)
            else:
                break;

        ifBlock,potentialReturn = self.invoke(toInvokeOnIf,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
        isReturnStatement |= potentialReturn

        if len(code) == 0 or not 'else' in code[0]:
            return prelimcheckcode+['if(%s && !%s)'%(booleanCheckVar,returnedHandle)]+ifBlock+['endif'],code,isReturnStatement


        clevel = 1 if '{' in code.pop(0) else 0
        toInvokeOnElse =[]
        while (len(code) > 0 and clevel >= 0):
            popped = code.pop(0)
            if '{' in popped:
                clevel += 1;
            elif '}' in popped:
                clevel -= 1;
            if clevel != 0:
                toInvokeOnElse.append(popped)
            else:
                break

        elseBlock,potentialReturn = self.invoke(toInvokeOnElse,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
        isReturnStatement |= potentialReturn

        self.deIntersectFreeMemory(scopecopy,currentScope,free)

        return prelimcheckcode+['if(%s && !%s)'%(booleanCheckVar,returnedHandle)]+ifBlock+['else']+elseBlock+['endif'],code,isReturnStatement



    def handleForLoop(self,evalExpression,code,currentScope,free,methodHandles,returnHandle=False,returnedHandle = False):
        # eval expression is in the form for(onestatement;checkcase;iterate){
        ''' extremely beta rn '''
        scopecopy = dict(currentScope)
        toFree =[]
        toWrite = []
        orig = str(evalExpression)
        booleanCheckVar = self.queryBoolean(free)
        evalExpression = nonsensehandling.exactParameters(evalExpression)
        isReturnStatement = False

        line = ''
        expression = '1'
        iter = ''

        try:
            line,expression,iter = evalExpression.split(';')
        except:
            self.announceError('You do not have exactly 3 statements in your for expression\n%s'%(evalExpression))
        # establish it
        left,right = line.split("=")
        left = left.replace(" ","")
        iterval = self.queryVariable(free) if not left in currentScope else currentScope[left]
        currentScope[left] = iterval
        prelimcode = self.evaluateWithReturnPointer(right,iterval,currentScope,free,methodHandles)

        # implement the whole statement itself.\

        prelimCheckCode = self.evaluateWithReturnPointer(expression,booleanCheckVar,currentScope,free,methodHandles)
        ifstatement = "if(%s && !%s)"%(booleanCheckVar,returnedHandle)
        nextstuff = "do;"
        clevel = 1 if '{' in orig else 0
        toInvokeOn =[]
        while (len(code) > 0 and clevel >= 0):
            popped = code.pop(0)
            if '{' in popped:
                clevel += 1;
            elif '}' in popped:
                clevel -= 1;
            if clevel != 0:
                toInvokeOn.append(popped)
            else:
                break;
        beefWhile,potentialReturn = self.invoke(toInvokeOn,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
        isReturnStatement |= potentialReturn

        #ignore the return bc it litearly will make 0 impact.

        left,right = iter.split("=")
        left = left.replace(" ","")
        iterval = self.announceError("Cannot Create a new variable in incrementor portion\nof for loop.\n%s"%(evalExpression)) if not left in currentScope else currentScope[left]
        currentScope[left] = iterval
        incrementorcode = self.evaluateWithReturnPointer(right,iterval,currentScope,free,methodHandles)
        repeatCheckCode = self.evaluateWithReturnPointer(expression,booleanCheckVar,currentScope,free,methodHandles)


        self.deIntersectFreeMemory(scopecopy,currentScope,free)

        lastStuff = "while(%s && !%s);"%(booleanCheckVar,returnedHandle)

        return prelimcode+prelimCheckCode+[ifstatement,nextstuff]+beefWhile+incrementorcode+repeatCheckCode+[lastStuff,'endif;'],code,isReturnStatement


    def handleWhileLoop(self,evalExpression,code,currentScope,free,methodHandles,returnHandle=False,returnedHandle = False):
        if returnedHandle == False:
            print "Error! No Returned Handle for While Loop!"
        scopecopy = dict(currentScope)

        toFree =[]
        booleanCheckVar = self.queryBoolean(free)
        originalexp = str(evalExpression)
        evalExpression = nonsensehandling.exactParameters(evalExpression)
        isReturnStatement = False
        #  evaluateWithReturnPointer(self,line, rtnptr , cScopeVariables, freed, methodHandles)
        prelimCheckCode = self.evaluateWithReturnPointer(evalExpression,booleanCheckVar,currentScope,free,methodHandles)
        ifstatement = "if(%s && !%s)"%(booleanCheckVar,returnedHandle)
        nextstuff = "do;"
        clevel = 1 if '{' in originalexp else 0
        toInvokeOn =[]
        while (len(code) > 0 and clevel >= 0):
            popped = code.pop(0)
            if '{' in popped:
                clevel += 1;
            elif '}' in popped:
                clevel -= 1;
            if clevel != 0:
                toInvokeOn.append(popped)
        beefWhile,potentialReturn = self.invoke(toInvokeOn,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
        isReturnStatement |= potentialReturn
        repeatCheckCode = self.evaluateWithReturnPointer(evalExpression,booleanCheckVar,currentScope,free,methodHandles)

        lastStuff = "while(%s && !%s);"%(booleanCheckVar,returnedHandle)

        self.deIntersectFreeMemory(scopecopy,currentScope,free)

        # dont free that memory otherwise we wil have problemos bc counter / flag corruption

        return prelimCheckCode+[ifstatement,nextstuff]+beefWhile+repeatCheckCode + [lastStuff,'endif'] ,code,isReturnStatement

    def cout(self,expr,cScope,free,methodHandles):
        parts = expr.split('<<')
        precomputecode = []
        sections = []
        auxmem = []
        parts = filter(lambda x: len(x.replace(' ','')) > 0, parts)

        for sector in parts:
            if '\"' in sector: # treat it as a string
                sections.append(nonsensehandling.exactString(sector).replace('\"',""))
            else:
                sector = sector.replace(' ','')
                if sector.replace(' ','') in cScope:
                    sections.append('%'+cScope[sector.replace(' ','')]+"%")
                elif 'COLORS.' in sector[:7].upper():
                    RESULT = sector[7:].lower()
                    pairing = {
                        'black': '&0',
                        'dark_blue': '&1',
                        'dark_green': '&2',
                        'dark_aqua' : '&3',
                        'dark_red':   '&4',
                        'dark_purple': '&5',
                        'gold': '&6',
                        'gray': '&7',
                        'dark_gray': '&8',
                        'blue': '&9',
                        'green': '&a',
                        'aqua': '&b',
                        'red': '&c',
                        'light_purple':'&d',
                        'yellow': '&e',
                        'white': '&f',
                        'clear': '&r&f',
                        'reset': '&r'
                    }
                    if not RESULT in pairing:
                        self.announceError('Unknown color: %s\nChoose from: '%(sector[7:],pairing.keys()))
                    else:
                        sections.append(pairing[RESULT])
                else:

                    newvar = self.queryVariable(free)
                    #evaluateWithReturnPointer(self,line, rtnptr , cScopeVariables, freed, methodHandles):
                    precomputecode.extend(self.evaluateWithReturnPointer(sector,newvar,cScope,free,methodHandles))
                    sections.append('%'+str(newvar)+"%")
                    auxmem.append(newvar)
        free.extend(auxmem)
        return precomputecode + ['log(\"'+''.join(sections)+'\")']



    def invoke(self, copycode,currentScope,free, methodHandles,returnHandle=False, returnedHandle = False):

        '''
        @input:
        - parameters a list.
        - free variables a dictionary {int: [list of free integer names], boolean: [list of free boolean names]}

        @output:
        - some code amrite

        '''
        isReturn = False
        lastValueReturn = False
        toFree = []
        toWrite = []
        endifcount = 0
        while( len(copycode) > 0):
            line = nonsensehandling.cleanFront(copycode.pop(0))
            if line[:3] in ['if ','if(']: # if statement, handle it
                code,copycode,isReturn = self.handleIfStatement(line[3:],copycode,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
                toWrite.extend(code)
            elif line[:4] in ['for ','for(']: # for statement, handle it
                code,copycode,isReturn = self.handleForLoop(line,copycode,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
                toWrite.extend(code)

            elif line[:len('while')+1] in ['while ','while(']:
                code,copycode,isReturn = self.handleWhileLoop(line,copycode,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
                toWrite.extend(code)
            elif line[:len('return') + 1 ] == 'return ':
               if not returnHandle:
                   print "[?]Unable to return due to no return ptr"
                   isReturn = True
               else:
                   isReturn = True
                   result = self.evaluateWithReturnPointer(line[len('return '):],returnHandle,currentScope,free,methodHandles)
                   toWrite.extend(result)
               toWrite.append('SET('+returnedHandle+')')
            elif line[:len('cout')+1] == 'cout ':
                toWrite.extend(self.cout(line[len('cout')+1:], currentScope,free,methodHandles   ) )
            elif line[:len('native')+1] in ['native ','native{']:
                code,copycode = self.handleNativeCode(line,copycode,currentScope)
                toWrite.extend(code)

            else: # assignment based pointer.
                returnloc = None
                if '=' in line:
                    left,right = line.split("=")
                    left = left.replace(" ","")
                    if left in currentScope:
                        returnloc = currentScope[left]
                    elif len(free) > 0:
                        returnloc = free.pop(0)

                    else:
                        returnloc = self.generateCoolName()
                    currentScope[left] = returnloc
                    toWrite.extend(self.evaluateWithReturnPointer(right,returnloc,currentScope,free,methodHandles))
                else:
                    toWrite.extend(self.evaluateWithReturnPointer(line,None,currentScope,free,methodHandles))
            if isReturn and len(copycode) > 0:
                toWrite.append('if (!%s)'%(returnedHandle))
                endifcount += 1
                isReturn = not isReturn
        free.extend(toFree)
        toWrite.extend(['endif'] * endifcount)
        print toWrite
        return toWrite,isReturn


#p = LooseFunction("myfunction(a,b,c) -> int","")
#print '\n'.join(p.evaluateWithReturnPointer("fib(fib(n)-fib(1) + 1 * fib(15*fib(r)))+fib(n+v)-fib(n-x)", "&abc", {"x": '&a',"v": '&b','n': '&weirdpointer','r':'&rpointer'},  ['&freeex1','&freeval2'] ,[]))
