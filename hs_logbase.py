#!/usr/bin/python3
# ------------------------------
# datei: hs_logbase.py
# autor: Helmut Sigl
# datum: 04/11/2021
# ------------------------------

# Imports

# Definitions

class Logbase:

    def __init__(self):
        self.__lf = ''

    def set_log(self, p_logfile):
        self.__lf = p_logfile
    
    def log(self, p_message):
        try: self.__lf.put(p_message)
        except: pass
