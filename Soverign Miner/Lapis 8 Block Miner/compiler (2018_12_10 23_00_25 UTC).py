def analyzewhitespace(lne):
    c = list(lne)
    streak = 0
    tabs_count = 0
    for i in range(0,len(c)):
        if c[i] == " ":
            streak += 1
        if streak  == 4:
            tabs_count += 1
            streak = 0
        if c[i] == "\t":
            tabs_count += 1
            streak = 0
    return tabs_count

def counttabs(lne):
    c = 0
    while lne[c] == " " or lne[c] == "\t":
        c += 1
    if c== 0:
        return 0,0
    else:
        return analyzewhitespace(lne[:c]),c




    
def force_compile(filename,fle = False,tabtype = '\t'):
    
    repo = {}
    print "[*]Force Compiling %s"%(filename)
    types = []
    try:
        with open(filename,"r") as k:
            types = k.readlines()
            k.close()
    except:
        return False
    #return types
    print "[*]Formatting lines to Tab/Line Format"
    lines = []
    for line in types:
        #tabs = line.count("\t")
        tabs,splitidx = counttabs(line)
        line = line[tabs:]
        lines.append([tabs,line])
    print "[*]Looking for program-insert-flags"
    newprog = []
    for idx in range(0,len(lines)):
        if lines[idx][1][:2] == "%%":
            print "[*]: Line %s: %s requires code insertation!"%(idx,lines[idx][1][:-1])
            filename = lines[idx][1][2:]
            filename = filename.split("%%")[0]
            if not filename in repo.keys():
                print "[!]: Need to Force-Compile %s from directory"%(filename)
                c = force_compile(filename,tabtype = tabtype)
                if c == False:
                    print "[-] ERROR: Unable to Force-Compile %s"%(filename)
                repo[filename] = c
            data = repo[filename]
            base_tabs = lines[idx][0]
            for synthline in data.split("\n"):
                #nlt = data.count("\t")
                nlt,splitidx = counttabs(data)
                synthline = synthline[splitidx:]
                newprog.append([base_tabs + nlt,synthline+"\n"])
        else:
            newprog.append(lines[idx])
    print "[*]Writing Macro-Text"
    newprogram = ""
    for line in newprog:
        newprogram += (tabtype*line[0])+ line[1]
    print "[+]Macro-Text Created!"
    if fle == False:
        return newprogram
    elif type(fle) != str:
        print "[-] Outfile not valid format."
    else:
        with open(fle,"w") as k:
            k.write(newprogram)
            k.close()
