#!/usr/bin/python3
# ------------------------------
# datei: hs_config.py
# autor: Helmut Sigl
# datum: 27/10/2021
# ------------------------------

# Imports

import configparser

# Definitions

class Configuration:

    def __init__(self, p_config_file):

		# Instanz von Konfiguration erzeugen
        self.config = configparser.ConfigParser()
		# Konfiguration einlesen
        try: 
            self.config.read(p_config_file)
            self.__status = True
        except: self.__status = False

    def state(self):
        return self.__status
    
    def get(self, p_section, p_key):
        try: ret = self.config[p_section][p_key]
        except: ret = ''
        return ret 


