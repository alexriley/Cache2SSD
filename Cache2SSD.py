#/bin/python3
'''
Cache2SSD.py
Written by Alex Riley <alex@riley.cc>
Created 21 February 2015
Last Modified 21 February 2015

'''
from os.path import isdir, exists

import sys, os, shutil

#Globals:
errors = []
SourcesArgList = {'-s','-src','-source'}
DestinationArgList = {'-d','-dest','-destination'}
SourceDirectory = ''
DestinationDirectory = ''
ConfigFileName = '.Cache2SSD.config'
ConfigFile = open(ConfigFileName, "a+")
    
def PromptSourceDirectory():
    return input("Where would you like to cache from? (e.g. 'Your steam folder'/steamapps/common)\n->")
def PromptDestDirectory():
    return input("Where to cache this to? (Select any directory on the SSD which you have read/write permissions for)\n->")

def ReadConfigFile():
    #Returns tuple if 
    ConfigFile.seek(0,0) # go to the beginning of the file
    line=ConfigFile.readline()
    SourceDirectory = ''
    DestinationDirectory = ''
    #Parse file:
    while line:
        if line[0] != '#': #for comments
            if "SOURCE=" in line:
                if SourceDirectory != '':
                    print("Bad Config file, multiple Sources specified. Config file Ignored")
                    return ('','')
                SourceDirectory = line.replace("SOURCE=","").replace("\n","")
            elif "DESTINATION=" in line:
                if DestinationDirectory != '':
                    print("Bad Config file, multiple Sources specified. Config file Ignored")
                    return ('','')
                DestinationDirectory = line.replace("DESTINATION=","").replace("\n","")
        line = ConfigFile.readline()
    #Check values:
    if SourceDirectory != '' or DestinationDirectory != '':
        for x in {SourceDirectory, DestinationDirectory}:
            if x != '' and not exists(x):
                print("Directory %s in config file does not exist, Config file ignored" % (x))
                return ('','')
    ConfigFile.close()
    return (SourceDirectory,DestinationDirectory)
        
                
        
        
def cache(Source, Destination):
    #Copy the directory from source to destination
    if exists(Destination):
        print("ERROR: %s already exists." % Destination)
        return False

    try:
        shutil.move(Source,Destination)
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
    
    ShellSymLink = "ln -s 'DESTINATIONPATH' 'SOURCEPATH'"
    ShellSymLink = ShellSymLink.replace("DESTINATIONPATH", Destination)
    ShellSymLink = ShellSymLink.replace("SOURCEPATH", Source)
    
    print("Shell command:\n%s" % (ShellSymLink)) #TESTING
    
    os.popen(ShellSymLink)
    return True

def uncache(Source, Destination):
    #TODO
    '''
    Source is a symlink to Destination
    
    Pseudocode:
    Check that Source is a symlink. Return false if not
    
    Otherwise:
    Remove source symlink
    Move Destination to Source
    Delete Destination
    return true
    '''  
    if not os.path.islink(Source):
        return False
    
    RemoveSymLinkCommand = "rm -f 'SOURCE'" # NOTE: this removes the symlink, it doesn't delete any files
    RemoveSymLinkCommand = RemoveSymLinkCommand.replace("SOURCE", Source)
    os.popen(RemoveSymLinkCommand)
    
    if(exists(Source)):
        print("%s Should have been moved, but wasn't",Source)
        return False
    
    try:
        shutil.move(Destination, Source)
    except OSError as why:
        errors.extend(str(why))
    if errors:
        print("Directory not copied\nERRORS:")
        for x in errors:
            print("%s", x)
        return False
    
    return True
    
def main():
    (SourceDirectory,DestinationDirectory) = ReadConfigFile()
    # If there are arguments, parse them for commands:
    if len(sys.argv) > 1:
        for x in range(1,len(sys.argv)-1):
            if sys.argv[x] in SourcesArgList and SourceDirectory == '':
                SourceDirectory = sys.argv[x+1]
            if sys.argv[x] in DestinationArgList and DestinationDirectory == '':
                DestinationDirectory = sys.argv[x+1]
                
    # If prompt for directories if not specified in arguments
    if SourceDirectory == '': SourceDirectory = PromptSourceDirectory()
    if DestinationDirectory == '': DestinationDirectory = PromptDestDirectory()

    print("Source %s\nDestination: %s" % (SourceDirectory,DestinationDirectory)) #TESTING
    for directory in {SourceDirectory, DestinationDirectory}:  
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
    if not (DestinationDirectory.endswith('/')):
        DestinationDirectory += '/'
    SourceChoice = -1
    dirs = os.listdir(SourceDirectory)
    dirs.sort()
    if(len(dirs) == 0):
        print("Source directory %s is empty, exiting" % (SourceDirectory))
        return
    #Display list of choices
    # Note: Starting the count at 1 for the user, adjusting the users input accordingly
    # (If user selects '7' from the list shown, it's actually dirs[6])
    for x in range(len(dirs)):
        print("%i: %s" % (x+1,dirs[x])) 
    SourceChoice = int(input("What would you like to cache? ->")) -1
    if SourceChoice <= 0 or SourceChoice >= len(dirs):
        print("%i is not a valid choice" % (SourceChoice+1))
        return
    SourcePath = SourceDirectory+dirs[SourceChoice]
    DestinationPath = DestinationDirectory+dirs[SourceChoice]

    if cache(SourcePath,DestinationPath):
        input("COMPLETE %s is now cached. Press enter to exit." % (SourcePath))
    else :
        input("Not cached. Press enter to exit")
    
    
    
    

if __name__ == "__main__":
    main()