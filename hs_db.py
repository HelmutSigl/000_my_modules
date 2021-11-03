#!/usr/bin/python3
# ------------------------------
# datei: hs_db.py
# autor: Helmut Sigl
# datum: 03/11/2021
# ------------------------------

# Imports

import sqlite3
import mysql.connector
from hs_config import Configuration
from hs_logbase import Logbase

# Definitions

class Database(Logbase):
	
	def __init__(self, p_config_file):
		Logbase.__init__()
		# Instanz von Konfiguration erzeugen
		self.__config = Configuration(p_config_file)
		# Status checken
		if self.__config.state():
			# Weiterverarbeitung wenn es geklappt hat
			self.__database_type()

	def get(self):
		# Datenbank zurückgeben
		return self.__db

	def __database_type(self):
			
		# Angefragten Datenbanktyp einlesen
		in_use = self.__config.get('database', 'in_use')
		# Weiterverarbeitung je nach Datenbanktyp
		if in_use == 'sqlite': self.__connect_sqlite()
		elif in_use == 'maria': self.__connect_maria()

	def __connect_sqlite(self):
		
		# Verbindungsdaten besorgen
		database = self.__config.get('sqlite', 'database')
		# Datenbank erzeugen
		self.__db = Sqlite_db(database)
		# Wenn Setup konfiguriert,
		# Daten besorgen und Setup ausführen
		if self.__config.get('sqlite', 'setup') == 'ja':
			set = self.__get_setup('sqlite')
			self.__db.exec(set)

	def __connect_maria(self):
		
		# Verbindungsdaten besorgen
		host = self.__config.get('maria', 'host')
		user = self.__config.get('maria', 'user')
		password = self.__config.get('maria', 'password')
		database = self.__config.get('maria', 'database')
		# Datenbank erzeugen
		self.__db = Maria_db(host, user, password, database)
		# Wenn Setup konfiguriert,
		# Daten besorgen und Setup ausführen
		if self.__config.get('maria', 'setup') == 'ja':
			set = self.__get_setup('maria')
			self.__db.exec(set)

	def __get_setup(self, p_type):

		# Wieviele Zeilen sind einzulesen
		setcount = int(self.__config.get(p_type, 'setcount'))
		# Einlesen in String
		set = ''
		for i in range(1,setcount+1):
			set = set + self.__config.get(p_type, 'set'+str(i)) + ' '
		# Zurückgeben des Strings
		return set

class Sqlite_db(Logbase):

	# Belegt die globalen Variablen, stellt Verbindung zur Datenbank her
	# und legt diese neu an falls sie nicht existiert
	def __init__(self, p_database):
		Logbase.__init__()
		self.__db = sqlite3.connect(p_database)
		self.__dbc = self.db.cursor()

	# Führt den übergebenen SQL-Befehl aus und liefert das
	# Ergebnis als eine Menge von Tupeln zurück
	def exec(self, p_sql):
		self.__dbc.execute(p_sql)
		ret = ()
		for x in self.__dbc:
			ret += x,
		return ret

	# Generiert einen "DESCRIBE-Befehl" für die übergebene Tabelle,
	# führt ihn aus und liefert das Ergebnis als eine Menge
	# von Tupeln zurück	
	def tableinfo(self, p_table):
		sql = 'pragma table_info ("%s")' % p_table
		return self.exec(sql)

	# Commited die gemachten Änderungen in der Datenbank
	def commit(self):
		self.__db.commit()

	# Schließt die Datenbank
	def close(self):
		self.__db.close()

class Maria_db(Sqlite_db):

	# Belegt die globalen Variablen und stellt Verbindung zur Datenbank her
	def __init__(self, p_host, p_user, p_password, p_database):
		self.__database = p_database
		self.__db = mysql.connector.connect(
			host=p_host,
			user=p_user,
			passwd=p_password,
			database=self.database)
		self.__dbc = self.__db.cursor()

	# Generiert einen "DESCRIBE-Befehl" für die übergebene Tabelle,
	# führt ihn aus und liefert das Ergebnis als eine Menge
	# von Tupeln zurück	
	def tableinfo(self, p_table):
		sql = 'describe %s' %(p_table)
		return self.exec(sql)

