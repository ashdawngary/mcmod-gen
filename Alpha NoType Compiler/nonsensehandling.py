#####################
# literaly preprocess the code for the mistakes and stuff that we can quick fix.
#####################

def rmvGarbage(line):
    return line.lstrip()


def removeWord(line):
    i = line.find(" ")
    line = line[i + 1:]
    line.lstrip()
    return line

def removeSpaces(line):
    line = line.rstrip()
    line = line.lstrip()
    return line
def intersects(a,b):
    q = a
    v = b
    for i in q:
        if i in v:
            return True
    return False
def exactParameters(line):
    start = line.find("(")
    end = line.rfind(")")
    line = line[start + 1:end]
    return line
def exactString(line):
    start = line.find("\"")
    end = line.rfind("\"")
    line = line[start + 1:end]
    return line

def getFunctionName(line):
    return line[:line.find("(")]

def cleanComments(fline):
    if '//' in fline:
        return fline[:fline.find('//')]
    else:
        return fline
def cleanFront(fline):
    if len(fline) == 0:
        return fline
    if fline[0] != ' ' or not ' ' in fline:
        return fline

    startix = 0
    while startix < len(fline):
        if (fline[startix] != ' '):
            return fline[startix:]
        startix += 1
    # we should never reach here logic but whatever
    return fline
