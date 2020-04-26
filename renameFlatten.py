# -*- coding: utf-8 -*-
# for Python3 (needs Unicode)

"""
TODO:
 - Needs relative dir in final naming
 - Needs to consider empty folders
 - Also, test linux platfrom 
 - also check if it is considering filename length cap (win/linux) 
        Windows can't exceed MAX_PATH value (259 characters for files, 248 for folders).
"""

import os, shutil, sys, time

def splitPath(p):
    """Returns a list of folder names in path to p
    """
    a,b = os.path.split(p)
    return (splitPath(a) if len(a) and len(b) else []) + [b]

def safeprint(s):
    """This is needed to prevent the Windows console from choking on Unicode characters in paths.
    """
    try:
        print(s)
    except UnicodeEncodeError:
        if sys.version_info >= (3,):
            print(s.encode('utf8').decode(sys.stdout.encoding))
        else:
            print(s.encode('utf8'))

def flatten(dirInpt, doit):
    """Flattens a directory by moving all nested files up to the dirInpt and renaming uniquely based on the original path.
    Converts all occurances of "SEP" to "REPL" in names (this allows un-flatting later, but at the cost of the replacement).
    
    If doit is True, does action; otherwise just simulates.
    
    """
    
    SEP  = "__"
    REPL = "?"

    folderCount = 0
    fileCount = 0
    

    outLog1=[]
    outLog2=[]
    ## reused code, for deleting the abs folder 
    # 
    sp = splitPath(dirInpt)
    np = ""
    for element in sp[1:]:
        e2 = element.replace(SEP, REPL)
        np += e2 + SEP
    dirInptnewName = np 
    #
    
    if not doit:
        print("Simulating:")

    for path, dirs, files in os.walk(dirInpt, topdown=False): 

    
        if path != dirInpt: # this needed?
                     


            for f in files:
                #
                sp = splitPath(path)
                np = ""

                for element in sp[1:]:
                    e2 = element.replace(SEP, REPL)
                    np += e2 + SEP
                f2 = f.replace(SEP, REPL)
                newNameAbs = np + f2
                #
                
                
                newNameRel=newNameAbs.replace(dirInptnewName, "")

                outLog1.append("Moved:       "+ dirInpt+"__"+newNameRel )
                # todo: break if newNameRel exceeds the win size
                if doit:
                    shutil.move(os.path.join(path, f), os.path.join(dirInpt, newNameRel))
                fileCount += 1

            # regex on path but dirInpt
            #
            newpath=path.replace(dirInpt,'').replace('\\',"\\\\")
            outLog2.append("Dir removed: "+dirInpt+newpath)




            if doit:
                os.rmdir(path)
            folderCount += 1

    print 
    for line in  outLog2 +outLog1:
        safeprint(line)

    if doit:
        print("Done.")        
    else:
        print("Test case complete.")


    print("Moved files:", fileCount)
    print("Removed folders:", folderCount)
    input("Press Enter to continue...")

if __name__ == "__main__":
    print("Please input the folder that needs flattening. When confident on action add keyword 'DOIT'.")
    print("Or press Enter to exit...")
    print("")
    sysargv=input()
    sysargv=sysargv.split(" ")  

    print(sysargv)
    if len(sysargv) < 1:
        print("Flattens all files in a path recursively, moving them all to the")
        print("dirInpt folder, renaming based on the path to the original folder.")
        print("Removes all now-empty subfolders of the given path.")
        print("")
        print("Syntax: flatten [path] [DOIT]")
        print("")
        print("The DOIT parameter makes flatten do the action; without it the action is only simualted.")
        print("Examples:")
        print("  flatten //machine/path/foo          Simulates flattening all contents of the given path")
        print("  flatten //machine/path/bar DOIT     Actually flattens given path")
        input("Press Enter to continue...")
    else:
        if len(sysargv) == 2 and sysargv[1] == "DOIT":
            flatten(sysargv[0], True)
        else:
            flatten(sysargv[0], False)
