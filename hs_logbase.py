#!/usr/bin/python3
# ------------------------------
# datei: hs_logbase.py
# autor: Helmut Sigl
# datum: 03/11/2021
# ------------------------------

class Log_base:

    def __init__(self):
        self.lf = ''

    def set_log(self, p_logfile):
        self.lf = p_logfile
    
    def log(self, p_message):
        try: self.lf.put(p_message)
        except: pass
