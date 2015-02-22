#/bin/python3
'''
Cache2SSD.py
Written by Alex Riley <alex@riley.cc>
Created 21 February 2015
Last Modified 21 February 2015


'''
from os.path import isdir, exists

import sys, os, shutil, platform

#Globals:
errors = []
SourcesArgList = {'-s','-src','-source'}
CacheArgList = {'-c','-cache'}
SourceDirectory = ''
CacheDirectory = ''
ConfigFileName = '.Cache2SSD.config'
CachedFilesName= '.Cache2SSD.Cachedlist'
    
def PromptSourceDirectory():
    return input("Where would you like to cache from? (e.g. 'Your steam folder'/steamapps/common)\n->")
def PromptDestDirectory():
    return input("Where to cache this to? (Select any directory on the SSD which you have read/write permissions for)\n->")
def GetFilesList(SourceDir, CachedDir):
    #returns 2 lists of filenames: 
    SourceFilesList = os.listdir(SourceDir)
    SourceFilesList.sort()
    CachedFilesList = []
    if exists(CachedDir+CachedFilesName):
        CacheFile = open(CachedDir+CachedFilesName,'r')
        line = CacheFile.readline()
        while line:
            CachedFilesList.append(line.replace("\n",""))
            line = CacheFile.readline()
            CacheFile.close()
    
    #Files that have been cached will appear in both the SourceFileslist and the CachedFilesList
    #The following line removes all from SourceFilesList that are in CachedFilesList
    SourceFilesList = [x for x in SourceFilesList if x not in CachedFilesList] 
    return(SourceFilesList,CachedFilesList)
    
def ReadConfigFile():
    ConfigFile = open(ConfigFileName, "a+")
    #Returns tuple if 
    ConfigFile.seek(0,0) # go to the beginning of the file
    line=ConfigFile.readline()
    SourceDirectory = ''
    CacheDirectory = ''
    #Parse file:
    while line:
        if line[0] != '#': #for comments
            if "SOURCE=" in line:
                if SourceDirectory != '':
                    print("Bad Config file, multiple Sources specified. Config file Ignored")
                    ConfigFile.close()
                    return ('','')
                SourceDirectory = line.replace("SOURCE=","").replace("\n","")
            elif "CACHE=" in line:
                if CacheDirectory != '':
                    print("Bad Config file, multiple Sources specified. Config file Ignored")
                    ConfigFile.close()
                    return ('','')
                CacheDirectory = line.replace("CACHE=","").replace("\n","")
        line = ConfigFile.readline()
    if not (SourceDirectory.endswith('/')):
        SourceDirectory += '/'
    if not (CacheDirectory.endswith('/')):
        CacheDirectory += '/'
    #Check values:
    if SourceDirectory != '' or CacheDirectory != '':
        for x in {SourceDirectory, CacheDirectory}:
            if x != '' and not exists(x):
                print("Directory %s in config file does not exist. Config file ignored" % (x))
                return ('','')
    ConfigFile.close()
    return (SourceDirectory,CacheDirectory)
        
                
        
        
def cache(Source, Cache):
    FileName = Cache.replace(CacheDirectory,"")
    #Copy the directory from source to Cache    
    if exists(Cache):
        print("ERROR: %s already exists." % Cache)
        return False
    
    try:
        shutil.move(Source,Cache)
    except OSError as why:
        errors.extend(str(why))
    if errors:
        print("Directory not copied\nERRORS:")
        for x in errors:
            print("%s", x)
        return False
    
    #Create symbolic link
    if(exists(Source)):
        print("%s Should have been moved, but wasn't",Source)
        return False
    
    ShellSymLink = "ln -s 'CACHEPATH' 'SOURCEPATH'"
    ShellSymLink = ShellSymLink.replace("CACHEPATH", Cache)
    ShellSymLink = ShellSymLink.replace("SOURCEPATH", Source)
    
    print("Shell command:\n%s" % (ShellSymLink)) #TESTING
    
    os.popen(ShellSymLink)
    
    #Add this file to the list of cached files
    CacheFile = open(CacheDirectory+CachedFilesName,'a')
    CacheFile.write(FileName+'\n')
    CacheFile.close()
    
    return True

def uncache(Source, Cached):
    '''
    Source is a symlink to Cached
    
    Pseudocode:
    Check that Source is a symlink. Return false if not
    
    Otherwise:
    Remove source symlink
    Move Cached to Source
    Delete Cached
    Remove Cached from the Cached List file
    return true
    '''  
    CachedFileName = Cached.replace(CacheDirectory,"")
    if not os.path.islink(Source):
        return False
    
    RemoveSymLinkCommand = "rm -f 'SOURCE'" # NOTE: this removes the symlink, it doesn't delete any files
    RemoveSymLinkCommand = RemoveSymLinkCommand.replace("SOURCE", Source)
    os.popen(RemoveSymLinkCommand)
    os.wait() # popen() opens a child process which runs independently, without wait() if(exists(source)) may run before the symlink is removed 
    
    if(exists(Source)):
        print("%s Should have been moved, but wasn't" % Source)
        return False
    
    try:
        shutil.move(Cached, Source)
    except OSError as why:
        errors.extend(str(why))
    if errors:
        print("Directory not copied\nERRORS:")
        for x in errors:
            print("%s", x)
        return False
    #Update the cache list file
    #Get all lines from the file
    CacheFile = open(CacheDirectory+CachedFilesName, 'r')
    CacheFileLines = []
    line = CacheFile.readline()
    while line:
        CacheFileLines.append(line)
        line = CacheFile.readline()
    #Add back all lines except for the one just uncached
    CacheFile.close()
    CacheFile = open(CacheDirectory+CachedFilesName,'w')
    for line in CacheFileLines:
        if line.replace("\n","") != CachedFileName:
            CacheFile.write(line)
    CacheFile.close()
    

    return True
    
def main():
    global SourceDirectory
    global CacheDirectory
    
    if platform.system() != 'Linux':
        ans = raw_input("WARNING: Cache2SSD has only been tested on Linux. It may work on Mac OS X (as it is POSIX-compliant), but  won't work on Windows. Would you like to continue (yes/no)? \n->")
        if ans not in {'y','yes'}:
            return
    (SourceDirectory,CacheDirectory) = ReadConfigFile()
    # If there are arguments, parse them for commands:
    if len(sys.argv) > 1:
        for x in range(1,len(sys.argv)-1):
            if sys.argv[x] in SourcesArgList and SourceDirectory == '':
                SourceDirectory = sys.argv[x+1]
            if sys.argv[x] in CacheArgList and CacheDirectory == '':
                CacheDirectory = sys.argv[x+1]
                
    # If prompt for directories if not specified in arguments
    if SourceDirectory == '': SourceDirectory = PromptSourceDirectory()
    if CacheDirectory == '': CacheDirectory = PromptDestDirectory()

    print("Source %s\nCache: %s" % (SourceDirectory,CacheDirectory)) #TESTING
    for directory in {SourceDirectory, CacheDirectory}:  
        if exists(directory):
            if not isdir(directory): 
                print("ERROR: %s is not a directory" % (directory))
                return
        else:
            #TODO: Prompt user if they would like to create the directory
            print("ERROR: %s does not exist. Create it using mkdir or a file manager" % (directory))
            return 
        
    if not (SourceDirectory.endswith('/')):
        SourceDirectory += '/'
    if not (CacheDirectory.endswith('/')):
        CacheDirectory += '/'
    SourceFilesList = []
    CachedFilesList = []
    (SourceFilesList,CachedFilesList) = GetFilesList(SourceDirectory, CacheDirectory)
    if(len(SourceFilesList) == 0):
        print("Source directory %s is empty, exiting" % (SourceDirectory))
        return
    #Display list of choices
    # Note: Starting the count at 1 for the user, adjusting the users input accordingly
    # (If user selects '7' from the list shown, it's actually dirs[6])
    print("Uncached Directories (Enter number to cache):")
    for x in range(len(SourceFilesList)):
        print("%i: %s" % (x+1,SourceFilesList[x])) 
    print("Cached Directories (Enter number to uncache):")
    for x in range(len(CachedFilesList)):
        print("%i: %s" % (len(SourceFilesList)+x+1,CachedFilesList[x]))
    Choice = int(input("What would you like to do? ->")) -1
    if Choice < 0 or Choice > len(SourceFilesList)+len(CachedFilesList):
        print("%i is not a valid choice" % (Choice+1))
        return
    elif(Choice < len(SourceFilesList)): # If Choice is among cached
        SourcePath = SourceDirectory+SourceFilesList[Choice]
        CachePath = CacheDirectory+SourceFilesList[Choice]
        if cache(SourcePath,CachePath):
            input("COMPLETE %s is now cached. Press enter to exit." % (SourcePath))
        
        else :
            input("Not cached. Press enter to exit")
      
    elif(Choice >= len(SourceFilesList)): # If choice is to uncache
        Choice -= (len(SourceFilesList))
        SourcePath = SourceDirectory+CachedFilesList[Choice]
        CachePath = CacheDirectory+CachedFilesList[Choice]

        if uncache(SourcePath, CachePath):
            input("COMPLETE %s returned. Press enter to exit" % (CachePath))
        else:
            input("Not cached. Press enter to exit")
    return
    
    
    
    

if __name__ == "__main__":
    main()