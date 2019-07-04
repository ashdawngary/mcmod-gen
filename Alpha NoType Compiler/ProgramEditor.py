import  nonsensehandling
import hashlib

def hash(s):
    return int(hashlib.sha1(s).hexdigest(), 16) % (10 ** 8)
def cross(set1,set2):
    newset = []
    for i in set1:
        for j in set2:
            newset.append(i+j)
    return newset;
charset = [chr(i) for i in range(ord('a'),ord('z'))]
diword = cross(charset,charset)
AVAILIBLE = cross(["#"],cross(diword,diword))
LOCALLIBRARIES = "C:\\users\\neelb\\Desktop\\mcmod-gen\\AlphaLib\\"
class ProgramEditor(object):
    """docstring for ProgramEditor."""

    def __init__(self, inputCode, flags = [],dRetF=lambda x:None):
        # code stuff
        self.lines = inputCode;
        self.functions = {}
        self.value = 0
        #print self.lines
        self.report = dRetF
        self.collectiveVariables = {} # variables from other libraries.
        self.isImported = set([])
        while len(self.lines) > 0:
            nextLine = nonsensehandling.rmvGarbage(self.lines.pop(0))
            #print nextLine
            if len(nextLine) == 0:
                continue
            elif nextLine[0] >= 'A' and nextLine[0] <= 'Z':
                #global variable
                collectiveVariables[nextLine.replace(' ','')] = AVAILIBLE.pop(0)
            elif nextLine[:5] == "using":
                # need to import a library
                # in the form using (libname,local/online,version) ex: 'using(hypixelcraft,local,*)'
                para = nonsensehandling.exactParameters(nextLine).split(",")
                target_textfile = LOCALLIBRARIES
                if para[2] == "*":
                    target_textfile = target_textfile+para[0]+"-latest.txt"
                else:
                    target_textfile = target_textfile+para[0]+"-v%s.txt"%(str(para[2]))
                print "[*]Looking for ",target_textfile
                with open(target_textfile,"r") as fileHandle:
                    CODE = fileHandle.read().replace('\r','').replace('\t','').split("\n")
                    CODE = map(nonsensehandling.cleanFront,CODE)
                    fileHandle.close()
                tempeditor = ProgramEditor(CODE)
                for qPro in tempeditor.functions:
                    if not qPro in tempeditor.isImported:
                        print "Importing Function: %s/%s"%(para[0],qPro)
                        self.functions[qPro] = tempeditor.functions[qPro]
                        self.isImported.add(qPro)
                for cVar in tempeditor.collectiveVariables:
                    print "Importing Variable: %s/%s"%(para[0],qPro)
                    self.collectiveVariables[cVar] = tempeditor.collectiveVariables[cVar]


            elif nextLine[:4] == 'func' or nextLine[:3] == 'def':
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

                resultingFunction = LooseFunction(functionProtoType,functionBody,self,debugStreamFunction=dRetF)
                self.functions[resultingFunction.getName()] = resultingFunction
                self.value = min(resultingFunction.lint(),self.value)

        #print("Function Reading done.")
        #for func in self.functions.values():
        #    print func.getName(),func.parameters,func.returntype
    def interpret(self):
        self.report({'name':'program-editor','retcode':self.value,'n-methods':len(self.functions.keys())})
        return self.value
    def generateProgram(self):
        code = self.functions['main'].methodinvoke([], [], self.functions)
        return code
class LooseFunction():
    """docstring for LooseFunction."""

    def __init__(self, prototype, fullWrite,programReference,debugStreamFunction=lambda x:None ):
        self.name = "unknown"
        self.parameters =[]
        self.returntype = "unknown"
        self.body = fullWrite
        self.isLinted = False
        self.programRef = programReference
        self.whiteListedStreams = ["if","else","for","eval","native","while","cout"]
        self.report= debugStreamFunction
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
        global AVAILIBLE
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

        line = nonsensehandling.cleanFront(line)
        self.report({'name':'eval-rptr','variables':cScopeVariables,'freedSize': len(freed),'numF':len(methodHandles.keys())})
        #print "\"%s\""%(line)
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
                if nextC == 'a' and queue[:3] == ['n','d',' '] and cLevel == 0:
                    tokens.append('and')
                    tokens.append('')
                    queue = queue[3:]
                elif nextC == 'o' and queue[:2] == ['r',' '] and cLevel == 0:
                    tokens.append('or')
                    tokens.append('')
                    queue = queue[2:]
                elif nextC == '&' and queue[:1] == ['&'] and cLevel == 0:
                    tokens.append('&&')
                    tokens.append('')
                    queue = queue[1:]
                elif nextC == '|' and queue[:1] == ['|'] and cLevel == 0:
                    tokens.append('||')
                    tokens.append('')
                    queue = queue[1:]
                elif nextC == '!' and queue[:1] == ['='] and cLevel == 0:
                    tokens.append('!=')
                    tokens.append('')
                    queue = queue[1:]
                else:
                    if nextC == '(':
                        cLevel += 1
                    elif nextC == ')':
                        cLevel -= 1;
                    tokens[-1] = tokens[-1] + nextC

        #print "[>]Need to Evaluate", tokens
        for i in range(0,len(tokens)):

            tokens[i] = tokens[i].replace("\t","")
            while('  ' in tokens[i]):
                tokens[i] = tokens[i].replace('  ',' ')
        while tokens[-1] == '':
            tokens.pop()
        toReliquish = [] # pointers to untrash when done
        codebefore = []
        aggregate = []
        for token in tokens:
            if token in "*-+/%":
                aggregate.append(token)
                continue
            if token in ["<", ">","<=",">=","==","&&","||","!="]:
                aggregate.append(token)
                continue
            if token == "and":
                aggregate.append("&&")
                continue
            if token == "or":
                aggregate.append('||')
                continue
            #print token,line
            if '(' in token:
                newpointer = ""

                todo = self.extractOuterParameters(nonsensehandling.exactParameters(token))
                #print "params",todo
                parameters = []


                for todo_part in todo:
                    if len(todo_part) == 0:
                        continue
                    elif todo_part[0] == '&' and not nonsensehandling.intersects("*+-/%",todo_part[1:]): # we've got a pointer on the loose.
                        if not todo_part[1:] in cScopeVariables:
                            self.announceError("[-]invalid base for pointer : "+str(todo_part[1:]))
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
                self.report({'name':'eval-tokencheck','params':list(parameters),'target-hash': hash(targetinvoke.replace(' ',''))})

                #codebefore.append("compupte "+targetinvoke+"(%s)"%(','.join(parameters))+ " to contribute to "+ rtnptr+" via "+vpointer )
                if targetinvoke.replace(' ','') != '':
                    targetinvoke = nonsensehandling.cleanFront(targetinvoke)
                    if not targetinvoke in methodHandles:
                        self.announceError( '[-]Unable to find func: '+targetinvoke)


                    executioncode = methodHandles[targetinvoke].methodinvoke(parameters,freed,methodHandles,returnHandle=vpointer)
                    codebefore.extend(executioncode)
                    aggregate.append(vpointer)
                else:
                    aggregate.append(parameters[0])

            elif '&' == token.replace(' ',"")[0]:
                tfrz = token.replace(' ',"")
                if not tfrz[1:] in cScopeVariables:
                    self.announceError("[-]invalid base for pointer : "+str(tfrz[1:]))
                else:
                    aggregate.append(cScopeVariables[tfrz[1:]])
            elif token.replace(' ',"") in cScopeVariables:
                #print "[*]Got a pre-exist reference to: %s"%(token)
                aggregate.append(cScopeVariables[token.replace(' ',"")])
            else:
                try:
                    aggregate.append(str(int(token.replace(' ',""))))
                except:
                    self.announceError( "[-]error, no reference to: `%s`\n Line: `%s`\nCurrent Variables: %s"%(token,line,cScopeVariables))

        if (len(aggregate) == 0 or (rtnptr != None and rtnptr != aggregate[-1])):
            aggregate = [rtnptr+" ="] + aggregate #+ ["-- evaluating %s"%(line)]

            codebefore.append(' '.join(aggregate))
        freed.extend(toReliquish)
        return codebefore
    def matchParameters(self,inputParameters):
        scope = dict(self.programRef.collectiveVariables)
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
        self.report({'name':'method-invoke','n-para':len(parameters),'hasReturnHandle':0 if returnHandle == False else 1})

        currentScope = self.matchParameters(parameters)
        copycode = list(self.body)
        returnedHandle = self.queryBoolean(free)


        answer,throw = self.invoke(copycode,currentScope,free,methodHandles,returnHandle=returnHandle, returnedHandle = returnedHandle)
        #print currentScope,self.parameters
        if(returnHandle in free):
            print "error!!!! return handle found in freed memory!"

        answer.append('UNSET(%s)'%(returnedHandle))
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
                    print "Freed: %s"%(v)
                    freeStack.append(v)

    def handleNativeCode(self,line,code,currentScope):
        ''' returns code,copycode '''
        self.report({'name':'native-parameters','codeToHandleAhead':code})
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
        self.report({'name':'native-return-parameters','nativeCode': nativeCode,'regularCode':code})

        return nativeCode,code

    def handleIfStatement(self,evalExpression,code,currentScope,free,methodHandles,returnHandle=False,returnedHandle=False):
        scopecopy = dict(currentScope)
        toFree = []
        toWrite = []
        original = evalExpression
        booleanCheckVar = self.queryBoolean(free)
        print "pre",evalExpression
        evalExpression = nonsensehandling.exactParameters(evalExpression)
        print evalExpression
        isReturnStatement = False
        prelimCheckCode = self.evaluateWithReturnPointer(evalExpression,booleanCheckVar,currentScope,free,methodHandles)

        clevel = 1 if '{' in original else 0
        toInvokeOnIf =[]
        while (len(code) > 0 and clevel >= 0):
            popped = code.pop(0)

            if '{' in popped:
                clevel += 1;
            elif '}' in popped:
                clevel -= 1;
            #print popped,clevel
            if clevel > 0:
                toInvokeOnIf.append(popped)
            else:
                break;
        print toInvokeOnIf
        ifBlock,potentialReturn = self.invoke(toInvokeOnIf,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
        isReturnStatement |= potentialReturn
        print potentialReturn,"ifblock result"
        #print "ifcheck",len(code),code[0]
        if len(code) == 0 or not 'else' in code[0]:
            return prelimCheckCode+['if(%s && !%s)'%(booleanCheckVar,returnedHandle)]+ifBlock+['endif;'],code,isReturnStatement


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
        #print "if statement", potentialReturn
        self.deIntersectFreeMemory(scopecopy,currentScope,free)

        return prelimCheckCode+['if(%s && !%s)'%(booleanCheckVar,returnedHandle)]+ifBlock+['else']+elseBlock+['endif;'],code,isReturnStatement



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
        print "for-toinvokeon",toInvokeOn
        beefWhile,potentialReturn = self.invoke(toInvokeOn,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
        isReturnStatement |= potentialReturn
        print "for loop potential", potentialReturn
        #ignore the return bc it litearly will make 0 impact.
        print "isReturnStatement",isReturnStatement
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
            else:
                break;
        beefWhile,potentialReturn = self.invoke(toInvokeOn,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
        isReturnStatement |= potentialReturn
        repeatCheckCode = self.evaluateWithReturnPointer(evalExpression,booleanCheckVar,currentScope,free,methodHandles)

        lastStuff = "while(%s && !%s);"%(booleanCheckVar,returnedHandle)

        self.deIntersectFreeMemory(scopecopy,currentScope,free)

        # dont free that memory otherwise we wil have problemos bc counter / flag corruption

        return prelimCheckCode+[ifstatement,nextstuff]+beefWhile+repeatCheckCode + [lastStuff,'endif;'] ,code,isReturnStatement

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
            if len(line) == 0:
                continue
            if line[:3] in ['if ','if(']: # if statement, handle it
                code,copycode,isReturn = self.handleIfStatement(line,copycode,currentScope,free,methodHandles,returnHandle=returnHandle,returnedHandle=returnedHandle)
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

            else: # assignment based pointer
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
            if isReturn:
                toWrite.append('if(!%s)'%(returnedHandle))
                endifcount += 1
                isReturn = not isReturn
        free.extend(toFree)
        toWrite.extend(['endif;'] * endifcount)
        #print endifcount > 0
        return toWrite,endifcount > 0


#p = LooseFunction("myfunction(a,b,c) -> int","")
#print '\n'.join(p.evaluateWithReturnPointer("fib(fib(n)-fib(1) + 1 * fib(15*fib(r)))+fib(n+v)-fib(n-x)", "&abc", {"x": '&a',"v": '&b','n': '&weirdpointer','r':'&rpointer'},  ['&freeex1','&freeval2'] ,[]))
