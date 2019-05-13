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
