################################
# really cool compiler project #
################################
import os
import ProgramEditor



target_textfile = "testscript.txt"
outfile = "oc.txt"
if not os.path.exists(target_textfile):
    print("error could not find file: %s"%(target_textfile))
    exit(0)


CODE = ""
with open(target_textfile,"r") as fileHandle:
    CODE = fileHandle.read().replace('\r','').split("\n")
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
print "\nYour Code\n"
print '\n'.join(outwrite)

print("generated code. writing out to: %s"%(outfile))

#with open(outfile,'w') as writeHandle:
#    writeHandle.write(outwrite)
