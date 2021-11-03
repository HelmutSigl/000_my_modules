#!/usr/bin/python3
# ------------------------------
# datei: hs_db.py
# autor: Helmut Sigl
# datum: 02/11/2021
# ------------------------------

# Imports

import sqlite3
import mysql.connector
from hs_config import Configuration

# Definitions

class Database:
	
	def __init__(self, p_config_file):
		
		# Instanz von Konfiguration erzeugen
		self.config = Configuration(p_config_file)
		# Status checken
		if self.config.state():
			# Weiterverarbeitung wenn es geklappt hat
			self.__database_type()

	def get(self):
		# Datenbank zurückgeben
		return self.db

	def __database_type(self):
			
		# Angefragten Datenbanktyp einlesen
		in_use = self.config.get('database', 'in_use')
		# Weiterverarbeitung je nach Datenbanktyp
		if in_use == 'sqlite': self.__connect_sqlite()
		elif in_use == 'maria': self.__connect_maria()

	def __connect_sqlite(self):
		
		# Verbindungsdaten besorgen
		database = self.config.get('sqlite', 'database')
		# Datenbank erzeugen
		self.db = Sqlite_db(database)
		# Wenn Setup konfiguriert,
		# Daten besorgen und Setup ausführen
		if self.config.get('sqlite', 'setup') == 'ja':
			set = self.__get_setup('sqlite')
			self.db.exec(set)

	def __connect_maria(self):
		
		# Verbindungsdaten besorgen
		host = self.config.get('maria', 'host')
		user = self.config.get('maria', 'user')
		password = self.config.get('maria', 'password')
		database = self.config.get('maria', 'database')
		# Datenbank erzeugen
		self.db = Maria_db(host, user, password, database)
		# Wenn Setup konfiguriert,
		# Daten besorgen und Setup ausführen
		if self.config.get('maria', 'setup') == 'ja':
			set = self.__get_setup('maria')
			self.db.exec(set)

	def __get_setup(self, p_type):

		# Wieviele Zeilen sind einzulesen
		setcount = int(self.config.get(p_type, 'setcount'))
		# Einlesen in String
		set = ''
		for i in range(1,setcount+1):
			set = set + self.config.get(p_type, 'set'+str(i)) + ' '
		# Zurückgeben des Strings
		return set

class Sqlite_db:

	# Belegt die globalen Variablen, stellt Verbindung zur Datenbank her
	# und legt diese neu an falls sie nicht existiert
	def __init__(self, p_database):
		self.db = sqlite3.connect(p_database)
		self.dbc = self.db.cursor()

	# Führt den übergebenen SQL-Befehl aus und liefert das
	# Ergebnis als eine Menge von Tupeln zurück
	def exec(self, p_sql):
		self.dbc.execute(p_sql)
		ret = ()
		for x in self.dbc:
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
		self.db.commit()

	# Schließt die Datenbank
	def close(self):
		self.db.close()

class Maria_db(Sqlite_db):

	# Belegt die globalen Variablen und stellt Verbindung zur Datenbank her
	def __init__(self, p_host, p_user, p_password, p_database):
		self.database = p_database
		self.db = mysql.connector.connect(
			host=p_host,
			user=p_user,
			passwd=p_password,
			database=self.database)
		self.dbc = self.db.cursor()

	# Generiert einen "DESCRIBE-Befehl" für die übergebene Tabelle,
	# führt ihn aus und liefert das Ergebnis als eine Menge
	# von Tupeln zurück	
	def tableinfo(self, p_table):
		sql = 'describe %s' %(p_table)
		return self.exec(sql)

