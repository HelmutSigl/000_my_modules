#!/usr/bin/python3
# ------------------------------
# datei: hs_config.py
# autor: Helmut Sigl
# datum: 03/11/2021
# ------------------------------

# Imports

import configparser
from hs_logbase import Logbase

# Definitions

class Configuration(Logbase):

    def __init__(self, p_config_file):
        Logbase.__init__(self)
		# Instanz von Konfiguration erzeugen
        self.__config = configparser.ConfigParser()
		# Konfiguration einlesen
        try: 
            self.__config.read(p_config_file)
            self.__status = True
        except: self.__status = False

    def state(self):
        return self.__status
    
    def get(self, p_section, p_key):
        try: ret = self.__config[p_section][p_key]
        except: ret = ''
        return ret 


