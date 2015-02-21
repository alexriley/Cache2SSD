#/bin/python3

from os.path import isdir, exists

import sys, os, shutil
def PromptSourceDirectory():
    return input("Where would you like to cache from? (e.g. 'Your steam folder'/steamapps/common)\n->")
def PromptDestDirectory():
    return input("Where to cache this to? (Select any directory on the SSD which you have write permissions for)\n->")
def cache(Source, Destination):
    #TODO
    return

def uncache(Source, Destination):
    #TODO
    return
    
def main():
    SourcesArgList = {'-src','-s','-source'}
    DestinationArgList = {'-d','-dest','-destination'}
    SourceDirectory = ''
    DestinationDirectory = ''
    errors = []
    if len(sys.argv) > 1:
        for x in range(1,len(sys.argv)-1):
            if sys.argv[x] in SourcesArgList:
                SourceDirectory = sys.argv[x+1]
            if sys.argv[x] in DestinationArgList:
                DestinationDirectory = sys.argv[x+1]
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
    if SourceDirectory != '':
        print("dirs length: %i" % (len(dirs)))
        for x in range(len(dirs)):
            print("%i: %s" % (x+1,dirs[x])) 
        SourceChoice = int(input("What would you like to cache? ->")) -1
        if SourceChoice <= 0 or SourceChoice >= len(dirs):
            print("%i is not a valid choice" % (SourceChoice+1))
            return
    SourcePath = SourceDirectory+dirs[SourceChoice]
    DestinationPath = DestinationDirectory+dirs[SourceChoice]
    if exists(DestinationPath):
        print("ERROR: %s already exists." % DestinationPath)
        return
    
    print("Copying %s to %s" % (SourcePath,DestinationPath))
    
    #Copy the directory from source to destination
    try:
        shutil.move(SourcePath,DestinationPath)
    except OSError as why:
        errors.extend(str(why))
    if errors:
        print("Directory not copied\nERRORS:")
        for x in errors:
            print("%s", x)
        return
    
    #Create symbolic link
    if(exists(SourcePath)):
        print("%s Should have been moved, but wasn't",SourcePath)
        return
    
    ShellSymLink = "ln -s DESTINATIONPATH SOURCEPATH"
    ShellSymLink = ShellSymLink.replace("DESTINATIONPATH", DestinationPath)
    ShellSymLink = ShellSymLink.replace("SOURCEPATH", SourcePath)
    
    print("Shell command:\n%s" % (ShellSymLink)) #TESTING
    
    os.popen(ShellSymLink)
    input("COMPLETE %s is now cached. Press enter to exit." % (SourcePath))
    
    
    
    
    

if __name__ == "__main__":
    main()