#/bin/python3
'''
Cache2SSD.py
Originally written by Alex Riley <alex@riley.cc>
Created 21 February 2015
Last Modified 22 February 2015

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; (version 2) 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

from os.path import isdir, exists

import sys, os, shutil, platform, subprocess

class Cache2SSD:
    def __init__(self,SourceDirectory='',CacheDirectory=''):
        self.Source = SourceDirectory
        self.Cache = CacheDirectory
    
    errors = []
    ConfigFileName = '.Cache2SSD.config'
    #The cached file is used to keep track of which folders are being cached on a drive
    #The file consists of folder names, separated by newlines. It's stored in the cache directory
    CachedFilesName= '.Cache2SSD.Cachedlist' 
    def RunCLImode(self):
        # If prompt for directories if not specified in arguments
        if self.Source == '': self.Source = self.PromptSourceDirectory()
        if self.Cache == '': self.Cache = self.PromptCacheDirectory()
    
        print("Source %s\nCache: %s" % (self.Source,self.Cache))
        for directory in {self.Source, self.Cache}:  
            if exists(directory):
                if not isdir(directory): 
                    print("ERROR: %s is not a directory" % (directory))
                    return
            else:
                #TODO: Prompt user if they would like to create the directory
                print("ERROR: %s does not exist. Create it using mkdir or a file manager" % (directory))
                return 
            
        if not (self.Source.endswith('/')):
            self.Source += '/'
        if not (self.Cache.endswith('/')):
            self.Cache += '/'
        
        SourceFilesList = []
        CachedFilesList = []
        (SourceFilesList,CachedFilesList) = self.GetFilesList()
        if(len(SourceFilesList) == 0 and len(CachedFilesList) == 0):
            print("Source directory %s is empty, exiting" % (self.Source))
            return
        #Display list of choices
        # Note: Starting the count at 1 for the user, adjusting the users input accordingly
        
        #Choice = int(input("What would you like to do? ->")) -1
        Choice = self.PromptForChoice(SourceFilesList, CachedFilesList)
        if Choice < 0 or Choice > len(SourceFilesList)+len(CachedFilesList):
            print("%i is not a valid choice" % (Choice+1))
            return
        elif(Choice < len(SourceFilesList)): # If Choice is among cached
            SourcePath = self.Source+SourceFilesList[Choice]
            CachePath = self.Cache+SourceFilesList[Choice]
            if self.cache(SourcePath,CachePath):
                print("COMPLETE %s is now cached." % (SourcePath))
            
            else :
                print("ERROR: Not cached.")
          
        elif(Choice >= len(SourceFilesList)): # If choice is to uncache
            Choice -= (len(SourceFilesList))
            SourcePath = self.Source+CachedFilesList[Choice]
            CachePath = self.Cache+CachedFilesList[Choice]
    
            if self.uncache(SourcePath, CachePath):
                print("COMPLETE %s returned." % (CachePath))
            else:
                print("Not cached.")
    def SetSourceDirectory(self,SourceDirectory):
        self.Source = SourceDirectory
    def GetSourceDirectory(self): return self.Source
    
    def SetCacheDirectory(self,CacheDirectory):
        self.Cache = CacheDirectory
    def GetCacheDirectory(self,CacheDirectory): return self.Cache
        
    def PromptSourceDirectory(self):
        self.Source=input("Where would you like to cache from? (e.g. 'Your steam folder'/steamapps/common)\n->")
    def PromptCacheDirectory(self):
        self.Cache=input("Where to cache this to? (Select any directory on the SSD which you have read/write permissions for)\n->")
    def GetFilesList(self):
        #returns 2 lists of filenames
        SourceFilesList = os.listdir(self.Source)
        SourceFilesList.sort()
        CachedFilesOnDisk = os.listdir(self.Cache)
        CachedFilesList = []

        
        if exists(self.Cache+self.CachedFilesName):
            CacheFile = open(self.Cache+self.CachedFilesName,'r')
            line = CacheFile.readline()
            while line:
                CachedFilesList.append(line.replace("\n",""))
                line = CacheFile.readline()
            CacheFile.close()
        #List comprehensions:
        #CachedFilesList is all that are in the Source and Cache directory, and listed in the cache file
        CachedFilesList = [x for x in CachedFilesList if x in SourceFilesList and x in CachedFilesOnDisk]
        CachedFilesList.sort()
        #Files that have been cached will appear in both the SourceFileslist and the CachedFilesList
        #SourceFilesList is all items from SourceFilesList that are not in CachedFilesList
        SourceFilesList = [x for x in SourceFilesList if x not in CachedFilesList] 
        return(SourceFilesList,CachedFilesList)
         
    def ReadConfigFile(self):
        #Returns tuple of (Source, Cache), '' if one is not found
        ConfigFile = open(self.ConfigFileName, "a+")
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
        if SourceDirectory != '': self.SetSourceDirectory(SourceDirectory)
        if CacheDirectory != '': self.SetCacheDirectory(CacheDirectory)
        #return (SourceDirectory,CacheDirectory)
             
    def cache(self,Source,Cache):
        #Source is the folder in SourceDirectory which will be copied to Cache
        
        
        #FolderName = Cache.replace(CacheDirectory,"") #String of the folder user selected (e.g. Half-Life)
        
        #FolderName is Cache from 1 character after the last occurrence of '/' to the end:
        #e.g. if cache is /BigDrive/Half-Life, Folder name is Half-Life
        FolderName = Cache[Cache[0:len(Cache)-1].rindex("/")+1:]
        #Copy the directory from source to Cache    
        if exists(Cache):
            print("ERROR: %s already exists." % Cache)
            return False
        print("Copying %s, This make take a few minutes\n" % (FolderName))
        try:
            shutil.move(Source,Cache)
        except OSError as why:
            self.errors.extend(str(why))
        if self.errors:
            print("Directory not copied\nERRORS:")
            for x in self.errors:
                print("%s", x)
            return False
         
        #Create symbolic link
        if(exists(Source)):
            print("%s Should have been moved, but wasn't",Source)
            return False
         
        ShellSymLink = ["ln", "-s", Cache, Source]
         
        #print("Shell command:\n%s" % (ShellSymLink)) #TESTING
        subprocess.call(ShellSymLink)
         
        #Add this file to the list of cached files
        CacheFile = open(self.Cache+self.CachedFilesName,'a')
        CacheFile.write(FolderName+'\n')
        CacheFile.close()
         
        return True
     
    def uncache(self,Source, Cache):
        '''
        Source is a symlink to Cache
         
        Pseudocode:
        Check that Source is a symlink. Return false if not
         
        Otherwise:
        Remove source symlink
        Move Cache to Source
        Delete Cache
        Remove Cache from the Cache List file
        return true
        '''  
        #CachedFolderName = Cache.replace(CacheDirectory,"")
        #CachedFolderName is Cache from 1 character after the last occurrence of '/' to the end::
        #e.g. if cache is /BigDrive/Half-Life, Folder name is Half-Life
        CachedFolderName = Cache[Cache[0:len(Cache)-1].rindex("/")+1:]
        if not os.path.islink(Source):
            return False
         
        RemoveSymLinkCommand = ['rm', '-f', Source] # NOTE: this removes the symlink, it doesn't delete any files
                    
        subprocess.call(RemoveSymLinkCommand) #This should wait for the subprocess to complete before continuing
        if(exists(Source)):
            print("%s Should have been moved, but wasn't" % Source)
            return False
        print("Copying %s, This make take a few minutes\n" % (CachedFolderName))
        try:
            shutil.move(Cache, Source)
        except OSError as why:
            self.errors.extend(str(why))
        if self.errors:
            print("Directory not copied\nERRORS:")
            for x in self.errors:
                print("%s", x)
            return False
        #Update the cache list file
        #Get all lines from the file
        CacheFile = open(self.Cache+self.CachedFilesName, 'r')
        CacheFileLines = []
        line = CacheFile.readline()
        while line:
            CacheFileLines.append(line)
            line = CacheFile.readline()
        CacheFile.close()
        
        CacheFileLines.sort()
        #Add back all lines except for the one just uncached
        CacheFile = open(self.Cache+self.CachedFilesName,'w')
        for line in CacheFileLines:
            if line.replace("\n","") != CachedFolderName:
                CacheFile.write(line)
        CacheFile.close()
        
        return True
    def PromptForChoice(self,SourceFilesList,CachedFilesList):
        print("Source Directories (Enter number to cache):")
        if len(SourceFilesList) == 0: print("\tNone")
        for x in range(len(SourceFilesList)):
            print("%i: %s" % (x+1,SourceFilesList[x])) 
        print("Cached Directories (Enter number to uncache):")
        if(len(CachedFilesList) == 0): print("\tNone")
        for x in range(len(CachedFilesList)):
            print("%i: %s" % (len(SourceFilesList)+x+1,CachedFilesList[x]))
        Choice = int(input("What would you like to do? ->")) -1
        return Choice
    

def main():
    if platform.system() != 'Linux':
        ans = raw_input("WARNING: Cache2SSD has only been tested on Linux. It may work on Mac OS X (as it is POSIX-compliant), but won't work on Windows. Would you like to continue (yes/no)? \n->")
        if ans not in {'y','yes'}:
            return
    SSDCache = Cache2SSD()
    SSDCache.ReadConfigFile()
    (Source,Cache) = GetArguments()
    if Source != '': SSDCache.SetSourceDirectory(Source)
    if Cache != '': SSDCache.SetCacheDirectory(Cache)
    SSDCache.RunCLImode()
    return
    
def GetArguments():
    # If there are arguments, parse them for commands:
    SourcesArgList = ['-s','-src','-source']
    CacheArgList = ['-c','-cache']
    SourceDirectory = ''
    CacheDirectory= ''
    if len(sys.argv) > 1:
        for x in range(1,len(sys.argv)-1):
            if sys.argv[x] in SourcesArgList:
                SourceDirectory = sys.argv[x+1]
            if sys.argv[x] in CacheArgList:
                CacheDirectory = sys.argv[x+1]
    return (SourceDirectory,CacheDirectory)

if __name__ == "__main__":
    main()