#!/usr/bin/env python
from collections import defaultdict
from clang.cindex import *
import argparse
import glob

class myNewThing:
    def __init__(this,ignoreCase = False, verbose = False):
        this.funcDefinitions = defaultdict(list)
        this.funcCalls = defaultdict(list)
        this.funcImpls = defaultdict(list)
        this.missingFiles = defaultdict(list)
        this.missplaced = defaultdict(list)

        this.ignoreCase = ignoreCase
        this.verbose = verbose

    def addDef(this,funcDef):
        this.add(this.funcDefinitions[funcDef.spelling,funcDef.type.spelling],funcDef)

    def addCall(this,funcDef):
        this.add(this.funcCalls[funcDef.spelling,funcDef.type.spelling],funcDef)

    def addImpl(this,funcDef):
        this.add(this.funcImpls[funcDef.spelling,funcDef.type.spelling],funcDef)

    def add(this,filelist,funcDef):
        filename = str(funcDef.location.file).lower() if this.ignoreCase else str(funcDef.location.file).lower()
        filelist.append(filename
                + " " + str(funcDef.location.line))

    def printAll(this):
        this.printFuncDefns()
        this.printFuncCalls()
        this.printFuncImpls()

    def printFuncDefns(this):
        print(" ==== funcDefs ==== ")
        this.printDict(this.funcDefinitions)

    def printFuncCalls(this):
        print(" ==== funcCalls ==== ")
        this.printDict(this.funcCalls)

    def printFuncImpls(this):
        print(" ==== funcImpls ==== ")
        this.printDict(this.funcImpls)

    def printDict(this,dictionary):
        for keyFunc,valFunc in dictionary.keys():
            li = dictionary[keyFunc,valFunc]
            print (keyFunc,valFunc,li)

    def printMissing(this):
        print(" === Missing Files === ")
        for keyMiss,funcList in this.missingFiles.items():
            print( "-",keyMiss,funcList)
        print()

    def printMissplaced(this):
        print(" === Missplaced Files === ")
        for keyMiss,funcList in this.missplaced.items():
            print( "-",keyMiss,funcList)
        print()

    def findMatching(this):
        if this.verbose:
            print(" === Start matching === ")
        for keyFunc,valFunc in this.funcDefinitions.keys():
            for keyCall,valCall in this.funcImpls.keys():
                if keyFunc == keyCall and valFunc == valCall:
                    liDefNoExt = [ os.path.splitext(x)[0] for x in this.funcDefinitions[keyCall,valCall]]
                    liImplNoExt = [ os.path.splitext(x)[0] for x in this.funcImpls[keyCall,valCall]]
                    liCallNoExt = [ os.path.splitext(x)[0] for x in this.funcCalls[keyCall,valCall]]
                    for impl in liImplNoExt:
                        if impl not in liDefNoExt:#and impl in liCallNoExt:
                            fileEx = "(exists)"
                            if not os.path.isfile(impl+".h"):
                                fileEx = "(missing)"
                                this.missingFiles[impl+".h"].append((keyFunc,valCall))
                            else:
                                this.missplaced[impl+".h"].append((keyFunc,valCall))
                            if this.verbose:
                                print(keyFunc, valCall , "not defined in",impl+".h" , fileEx)

def find_funcs_and_calls(tu):
    """ Retrieve lists of function declarations and call expressions in a translation unit
    """
    filename = tu.cursor.spelling

    calls = []
    funcs = []
    defs = []
    for c in tu.cursor.walk_preorder():
        p = False
        if c.location.file is None:
            pass
        elif c.location.file.name != filename:
            pass
        elif c.kind == CursorKind.CALL_EXPR:
            calls.append(c)
            p = True
        elif c.kind == CursorKind.FUNCTION_DECL:
            if c.is_definition():
                defs.append(c)
            else:
                funcs.append(c)
            p = True
        #if p:
           # print(c.kind,c.displayname, c.is_definition())
           # print()
    return funcs, calls, defs


def run(args,files):
    CC =  '-x c++ --std=c++11'.split()
    calls = []
    defs = []

    nT = myNewThing(args.ignoreCase,args.verbose)

    for iterNumber,curFile in enumerate(files):
        if args.verbose:
            print(curFile,iterNumber)
        idx = Index.create()
        tu = idx.parse(curFile, args=CC)
        funcs, calls, defs = find_funcs_and_calls(tu)
        for f in funcs:
            nT.addDef(f)
        for fCall in calls:
            nT.addCall(fCall)
        for d in defs:
            nT.addImpl(d)

    if args.verbose:
        nT.printAll()
    nT.findMatching()
    nT.printMissing()
    nT.printMissplaced()

def setupArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-C", "--ignoreCase",action="store_true")
    return parser

def globList(fileWildcardList):

    files = []
    for x in fileWildcardList:
        files.extend(glob.glob(x))
    return files


import os.path
def parseArguments(parser):
    args, files = parser.parse_known_args()
    for f in files:
        if not os.path.isfile(f):
            return args,[]

    if args.verbose:
        print(files)
        print(args)
    return args,files

def main():
    parser = setupArgs()
    args,files = parseArguments(parser);
    run(args,files);
main()
