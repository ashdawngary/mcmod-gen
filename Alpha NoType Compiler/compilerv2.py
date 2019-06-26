################################
# really cool compiler project #
################################
import os
import ProgramEditor
import nonsensehandling


target_textfile = "sellscript.txt"#raw_input("File: ")
outfile = "C:\\Users\\neelb\\AppData\\Roaming\\.minecraft\\liteconfig\\common\\macros\\place.txt"
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
