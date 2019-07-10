#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'turbogears==1.1.3','console_scripts','tg-admin'
__requires__ = 'turbogears==1.1.3'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('turbogears==1.1.3', 'console_scripts', 'tg-admin')()
)
