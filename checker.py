import glob
import ntpath

import re


def getFileNames(path):

    filenames=[]
    for filename in glob.glob(path + "*.deps", recursive=False):
        if "raw" not in filename:
            filenames.append(filename)
    return filenames


def getFileName(path, type="py"):
    """
    Strips down path so only file name is returned

    :param path: full path to file
    :param type: type of file,  by default- tmpl
    :return: file name
    """
    fileName = ntpath.basename(path)
    return re.sub('\.' + type + '$', '', fileName)


def getModulesWithProjects():
    dick = {}
    for name in getFileNames("/home/adelina/cern/analysis/"):
        shortFileName = getFileName(name)
        with open(name) as f:
            fileLines = f.readlines()
        for line in fileLines:
            if line in dick:
                dick[line] += [shortFileName[:-5]]
            else:
                dick[line] = [shortFileName[:-5]]
    del dick['Modules not supported in python3: \n']
    with open("/home/adelina/cern/conversions/results.deps", "w+") as f:
        for key, vlue in dick.items():
            f.write(key + ", ".join(vlue) + "\n" + "-" * 80 + "\n")

def getModulesOnly():
    dick = []
    for name in getFileNames("/home/adelina/cern/analysis/"):
        with open(name) as f:
            fileLines = f.readlines()
        for line in fileLines:
            line=line.replace("\n","")
            if line not in dick:
                dick.append(line)
    with open("/home/adelina/cern/conversions/modulesOnly.deps", "w+") as f:
        f.write("\n".join(dick))

def getNotSupportedStuff():
    li = []
    with open("/home/adelina/cern/conversions/modulesOnly.deps") as f:
        fileLines = f.readlines()
    for line in fileLines:
        if "not " in line.lower():
            li.append(line)

    dick = {}
    for name in getFileNames("/home/adelina/cern/analysis/"):
        shortFileName = getFileName(name)
        with open(name) as f:
            fileLines = f.readlines()
        for line in fileLines:
            line=line.replace("\n", "")
            if line in dick:
                dick[line] += [shortFileName[:-5]]
            else:
                dick[line] = [shortFileName[:-5]]
    del dick['Modules not supported in python3: ']
    results=[]
    for l in li:
        key=l.split()[0]
        results.append(l+"Used in projects: "+", ".join(dick[key]))

    with open("/home/adelina/cern/conversions/resultsFinal.deps", "w+") as f:
        f.write("\n".join(results))

if __name__=="__main__":
    # getModulesWithProjects()
    # getModulesOnly()
    getNotSupportedStuff()

