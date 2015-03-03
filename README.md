Cache2SSD

What it does: copies folder from a slower HDD to a faster HDD and back easily. I mainly wrote this for my own uses, I have a 60GB SSD which I would like to copy games to while playing and then copy back when no longer in use. I hope you may find it useful.

I took the idea from a program called 'Steam Mover', which I used for the same purpose when I used Windows (available at http://www.traynier.com/software/steammover).

This will probably work on Mac OS X with few revisions. I haven't tested it on a Mac, so I have no means of confirming this.

Command line arguments: (Optional, if no directories are specified, the user will be prompted)

{python3 Cache2SSD.py} {'-s','-src','-source'} {Source Folder} {'-c','-cache'} {Cache Folder}

Or, set Source and cache folders in a file called '.Cache2SSD.config' in the same directory as Cache2SSD.py with 2 lines as follows:
'

SOURCE=/BiggerDrive/Steam/steamapps/common/

CACHE=/SSDcache/

'

If directories are specified in command line arguments and in a file, the command line arguments are used.


My usage case:
I have a 60GB SSD and a 1TB HDD for my files. I keep my steam library on the HDD and move the games which I play to the SSD.

Notes:
Run the script in python3 - not python2. Ubuntu uses python2 for python *.py by default.
Do not use this for anything important which you haven't backed up. While I've tested this and it works reliably for me, things may go wrong.
Use absolute locations for Source and Cache directories (E.g. if Cache2SSD is in your home directory, use CACHE=/home/user/SSDCache/ and not CACHE=SSDCache/)

TODO:
GUI, probably in tkinter

Test for free space when copying files

Save a config set within the script

License: GPLv2.
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