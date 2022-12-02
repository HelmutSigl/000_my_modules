#!/usr/bin/python3
# ------------------------------
# datei: hs_files.py
# autor: Helmut Sigl
# datum: 06/11/2021
# ------------------------------

# Imports

import configparser
from datetime import datetime
from hs_baseclasses import Logbase

# Definitions

class Configfile(Logbase):

    def __init__(self, p_config_file, p_log_obj = ''):
        Logbase.__init__(self, p_log_obj)
        self.__cf = p_config_file
        self.__config = configparser.ConfigParser()
        self.__config.read(p_config_file)
        
    def get(self, p_section, p_key):
        try: 
            ret = self.__config[p_section][p_key]
            self.log('Konfigurationsfile: "' + self.__cf + '" : "' + p_section + '" / "' + p_key + '" lieferte: "' + ret + '"')
        except: 
            ret = ''
            self.log('Konfigurationsfile: "' + self.__cf + '" : "' + p_section + '" / "' + p_key + '" lieferte KEIN ERGEBNIS')
        return ret 

class Logfile:

    def __init__(self, p_log_file = ''):
        if p_log_file == '': self.__log_file = 'hs_log.log'
        else: self.__log_file = p_log_file

    def log(self, p_message):
        zeitstempel = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        strich = '--------------------------------------------------------------------'
        try:
            if p_message == 'clear': 
                datei = open(self.__log_file, 'w')
                datei.write(zeitstempel + ' : Neustart Logfile\r')
                datei.close()
                self.log('strich')
            else:
                datei = open(self.__log_file, 'a')
                if p_message == 'strich': datei.write(strich + '\r')
                elif p_message == 'leerzeile': datei.write('\r')
                else: datei.write(zeitstempel + ' : ' + p_message + '\r')
                datei.close()
        except: pass

