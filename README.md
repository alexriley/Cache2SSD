Cache2SSD

License: GPLv2. Please see LICENSE for the terms.

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

What it does: Easily copy a folder to a faster drive. By using symbolic links, it appears that the folder hasn't moved to any program that accesses it. When you need that space back, run Cache2SSD again to copy it back and remove the symbolic link.

This will probably work on Mac OS X with few revisions. I haven't tested in on a Mac, so I have no means of confirming this.

Command line arguments: (Optional, if no directories are specified, the user will be prompted)
{python3 Cache2SSD.py} {'-s','-src','-source'} {Source Folder} {'-c','-cache'} {Cache Folder}

Or, set Source and cache folders in a file called '.Cache2SSD.config' in the same directory as Cache2SSD.py with 2 lines as follows:
'
SOURCE=/BiggerDrive/Steam/steamapps/common/
CACHE=/SSDcache/
'

If directories are specified in command line arguments and a config file, the command line arguments are used.


My usage case:
I have a 60GB SSD and a 1TB HDD for my files. I keep my steam library on the HDD and cache the games which I play to the SSD.

Notes:
Run the script in python3 - not python2. Ubuntu uses python2 for python *.py by default.
Do not use this for anything important which you haven't backed up. While I've tested this and it works reliably for me, things may go wrong.

TODO:
GUI, probably in tkinter
Test for free space when copying files
Save a config set within the script