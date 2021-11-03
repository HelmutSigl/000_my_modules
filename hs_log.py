#!/usr/bin/python3
# ------------------------------
# datei: hs_log.py
# autor: Helmut Sigl
# datum: 03/11/2021
# ------------------------------

# Imports

from datetime import datetime
from hs_config import Configuration

# Definitions

class Logfile:

    def __init__(self, p_config_file = 'hs_log.log'):
        
        self.__logfile = Configuration(p_config_file).get('logging', 'logfile')
        if self.__logfile == '': self.logfile = p_config_file

    def put(self, p_message):
        
        zeitstempel = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        strich = '--------------------------------------------------------------------'
        datei = open(self.__logfile, 'a')
        if p_message == 'strich': datei.write(strich + '\r')
        elif p_message == 'leerzeile': datei.write('\r')
        else: datei.write(zeitstempel + ' : ' + p_message + '\r')
        datei.close()


