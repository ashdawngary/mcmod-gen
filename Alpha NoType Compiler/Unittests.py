import json
import nonsensehandling
import ProgramEditor

import os

OUTSTREAM = []
def onRecv(x):
    OUTSTREAM.append(x)


tests = [
['UnitTestSnippits/U1.txt','UnitTestSnippits/O1.json','UnitTestSnippits/C1.txt',False]
]
def compareOutStream(o1,o2):
    if len(o1) != len(o2):
        print "Produced 2 different sized streams, exit"
        return False
    for i in range(0,len(o1)):
        if (o1[i]['name'] != o2[i]['name']):
            print "error, different message types on %s"%(i)
            print o1,o2
            return False

        v = list(o1[i].keys())
        q = list(o2[i].keys())
        if v != q:
            print "error messages are of same type but different keys... on %s"%(i)
            print o1,o2
            return False

        for t in v:
            if type(o1[i][t]) == int:
                if (o1[i][t] != o2[i][t]):
                    print "Messages on index: %s dissagree on integer for header %s"%(i,t)
                    print o1,o2
                    return False
            if type(o1[i][t]) == list:
                if (len(o1[i][t]) != len(o2[i][t])):
                    print "Messages on index: %s dissagree on list sizes for header %s"%(i,t)
                    print o1,o2
                    return False
            elif type(o1[i][t]) == dict:
                if (len(o1[i][t].keys()) != len(o2[i][t].keys())):
                    print "Messages on index: %s dissagree on dict-key sizes for header %s"%(i,t)
                    print o1,o2
                    return False
    return True
def comparecode(a1,a2):
    count = lambda x,r:x.count(r)
    sanitychecks = ["endif;","while","do","if",""]
    for sc in sanitychecks:
        if (count(a1,sc) != count(a2,sc)):
            print "Count mismatch on %s"%(sc)
            return False
    return True

for unit_test in tests:
    target_textfile = unit_test[0]
    OUTSTREAM = []
    CODE = ""
    with open(target_textfile,"r") as fileHandle:
        CODE = fileHandle.read().replace('\r','').replace('\t','').split("\n")
        CODE = map(nonsensehandling.cleanFront,CODE)
        fileHandle.close()
    while('' in CODE):
        CODE.remove('')
    editor = ProgramEditor.ProgramEditor(CODE,dRetF=onRecv) # create a new program editor

    lint_scan = editor.interpret()
    outwrite = editor.generateProgram()
    if unit_test[3]:
        print "First time run, generating test case..."
        with open(unit_test[1],"w") as mk:
            mk.write('\n'.join(map(lambda x: json.dumps(x), OUTSTREAM)))
            mk.close()
        with open(unit_test[2],"w") as mk2:
            mk2.write('\n'.join(outwrite))
            mk2.close()
    else:
        answer_outstream = []
        with open(unit_test[1],"r") as mk:
            for obj in mk.read().split('\n'):
                answer_outstream.append(json.loads(obj))
            mk.close()
        answercode = ""
        with open(unit_test[2],"r") as mk2:
            answercode = mk2.read()
            mk2.close()
        if not (compareOutStream(OUTSTREAM,answer_outstream) and comparecode('\n'.join(outwrite),answercode)):
            print "Failed Case: Out Streams don't agree"
            for q in OUTSTREAM:
                print q
            print ""
            print '\n'.join(outwrite)
            exit(0)
print "All Cases Passed.(")
