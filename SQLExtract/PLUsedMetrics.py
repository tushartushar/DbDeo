import os

def writeFile(fileName, text):
    with open(fileName, "a", errors='ignore') as f:
        f.write(text + "\n")

def readFileContents(fileName):
    if(os.path.exists(fileName)):
        with open(fileName, "r+", errors='ignore') as f:
            return f.read()
    return ""

def countLOC(file):
    if(os.path.exists(file)):
        with open(file, "r+", errors='ignore') as f:
            return len(f.readlines())
    return 0


def computePLusedMetrics(sourceRoot, dir, resultFile):
    java = 0
    cs = 0
    c = 0
    cxx = 0
    py =0
    vb =0
    php = 0
    jsx = 0
    pl =0
    mm =0
    rb =0
    aspx =0
    htmx=0
    sql=0
    pkb = 0
    fileCount = 0
    totalLOC =0
    for root, dirs, files in os.walk(os.path.join(sourceRoot, dir)):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            if os.path.exists(os.path.join(root,file)):
                isProgram = False
                fileCount += 1
                if file.endswith(".java"):
                    java += 1
                    isProgram = True
                if file.endswith(".cs"):
                    cs +=1
                    isProgram = True
                if file.endswith(".c"):
                    c +=1
                    isProgram = True
                if file.endswith(".cpp") or file.endswith(".chh"):
                    cxx +=1
                    isProgram = True
                if file.endswith(".py"):
                    py +=1
                    isProgram = True
                if file.endswith(".vb"):
                    vb +=1
                    isProgram = True
                if file.endswith(".php"):
                    php +=1
                    isProgram = True
                if file.endswith(".js") or file.endswith(".jsp"):
                    jsx +=1
                    isProgram = True
                if file.endswith(".pl"):
                    pl +=1
                    isProgram = True
                if file.endswith(".mm"):
                    mm +=1
                    isProgram = True
                if file.endswith(".rb"):
                    rb +=1
                    isProgram = True
                if file.endswith(".asp") or file.endswith(".aspx"):
                    aspx +=1
                    isProgram = True
                if file.endswith(".htm") or file.endswith(".html"):
                    htmx +=1
                    isProgram = True
                if file.endswith(".sql"):
                    sql +=1
                    isProgram = True
                if file.endswith(".pkb"):
                    pkb +=1
                    isProgram = True
                if isProgram:
                    totalLOC += countLOC(os.path.join(root, file))
    writeFile(resultFile, dir + "," + str(fileCount) + "," + str(java) + "," + str(cs) + "," + str(c) + "," + str(cxx)
              + "," + str(py) + "," +
    str(vb) + "," + str(php) + "," + str(jsx) + "," + str(pl) + "," + str(mm) + "," + str(rb) + "," + str(aspx)
    + "," + str(htmx) + "," + str(sql) + "," + str(pkb) + "," + str(totalLOC))


