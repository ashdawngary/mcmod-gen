################################
# really cool compiler project #
################################
import os
import ProgramEditor
import nonsensehandling


target_textfile = "GenericSugarCaneScript.txt"#raw_input("File: ")
outfile = "C:\\Users\\neelb\\AppData\\Roaming\\.minecraft\\liteconfig\\common\\macros\\cqmplexBeta.txt"


def compileFile(target_textfile,outfile):
    if not os.path.exists(target_textfile):
        print("error could not find file: %s"%(target_textfile))
        exit(0)


    CODE = ""
    with open(target_textfile,"r") as fileHandle:
        CODE = fileHandle.read().replace('\r','').replace('\t','').split("\n")
        CODE = map(nonsensehandling.cleanFront,CODE)
        fileHandle.close()

    while('' in CODE):
        CODE.remove('')

    # loaded all the code

    editor = ProgramEditor.ProgramEditor(CODE) # create a new program editor

    lint_scan = editor.interpret()

    if lint_scan != 0:
        print("Error your program crashed because %s oops i guess ur done"%(lint_scan))
        exit(0)



    outwrite = editor.generateProgram()
    #print "\nYour Code\n"
    #print '\n'.join(outwrite)

    print("generated code. writing out to: %s"%(outfile))

    with open(outfile,'w') as writeHandle:
        writeHandle.write('\n'.join(outwrite))


instructions = []
with open("intent.txt","r") as mk:
    instructions = mk.read().split("\n")

base_dir = ""
input_dir = ""
for step in instructions:
    parts = step.split(" ")
    if len(parts) < 2:
        continue
    if parts[0] == ":setTargetOutput":
        base_dir = ''.join(parts[1:])[1:-1]
    elif parts[0] == ":setLocalLibrary":
        #print "set LocalLibraries to", parts[1][1:-1]
        ProgramEditor.LOCALLIBRARIES = ''.join(parts[1:])[1:-1]
    elif parts[0] == ":setTargetInput":
        input_dir = ' '.join(parts[1:])[1:-1]
    elif parts[0] == ":compile":
        cFile = input_dir + parts[1][1:-1]
        target = base_dir+parts[2][1:-1]
        print "[:compile] %s --> %s"%(cFile,target)
        compileFile(cFile,target)
