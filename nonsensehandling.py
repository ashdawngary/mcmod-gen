#####################
# literaly preprocess the code for the mistakes and stuff that we can quick fix.
#####################

def rmvGarbage(line):
    line.lstrip("")
    return line

def removeWord(line):
    i = line.find(" ")
    line = line[i + 1:]
    line.lstrip()
    return line

def removeSpaces(line):
    line = line.rstrip()
    line = line.lstrip()
    return line

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
