#!/usr/bin/python3
# ------------------------------
# datei: hs_database.py
# autor: Helmut Sigl
# datum: 06/11/2021
# ------------------------------

# Imports

import sqlite3
import mysql.connector
from hs_baseclasses import Logbase
from hs_files import Configfile

# Definitions

class Database(Logbase):
	
	def __init__(self, p_config_file, p_log_obj = ''):
		Logbase.__init__(self, p_log_obj)
		self.__config = Configfile(p_config_file, self.lo)
		self.__db = ''
		self.__database_type()

	def get(self):
		return self.__db

	def __database_type(self):
		in_use = self.__config.get('database', 'in_use')
		if in_use == 'sqlite': self.__connect_sqlite()
		elif in_use == 'maria': self.__connect_maria()
		else: self.log('Database: Kann "in_use" nicht verarbeiten, keine Datenbank verbunden')

	def __connect_sqlite(self):
		database = self.__config.get('sqlite', 'database')
		if database != '':
			try:
				self.__db = Sqlite_db(database, self.lo)
				self.log('Database: Sqlite_db - Datenbank wurde verbunden')
			except: 
				self.__db = ''
				self.log('Database: Sqlite_db - Datenbank wurde NICHT verbunden, Exception')
		else:
			self.log('Database: Sqlite_db - Datenbank wurde NICHT verbunden, Parameterfehler')
		# Setup usw. noch zu überarbeiten, existiert Datenbank überhaupt usw.
		if self.__db != '' and self.__config.get('sqlite', 'setup') == 'ja':
			set = self.__get_setup('sqlite')
			self.__db.exec(set)

	def __connect_maria(self):
		host = self.__config.get('maria', 'host')
		user = self.__config.get('maria', 'user')
		password = self.__config.get('maria', 'password')
		database = self.__config.get('maria', 'database')
		if host != '' and user != '' and password != '' and database != '':
			try:
				self.__db = Maria_db(host, user, password, database, self.lo)
				self.log('Database: Maria_db - Datenbank wurde verbunden')
			except: 
				self.__db = ''
				self.log('Database: Maria_db - Datenbank wurde NICHT verbunden, Exception')
		else:
			self.log('Database: Maria_db - Datenbank wurde NICHT verbunden, Parameterfehler')
		# Setup usw. noch zu überarbeiten, existiert Datenbank überhaupt usw.
		if self.__db != '' and self.__config.get('maria', 'setup') == 'ja':
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
	def __init__(self, p_database, p_log_obj = ''):
		Logbase.__init__(self, p_log_obj)
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
	def __init__(self, p_host, p_user, p_password, p_database, p_log_obj = ''):
		Logbase.__init__(self, p_log_obj)
		self.db = mysql.connector.connect(
			host=p_host,
			user=p_user,
			passwd=p_password,
			database=p_database)
		self.dbc = self.db.cursor()

	# Generiert einen "DESCRIBE-Befehl" für die übergebene Tabelle,
	# führt ihn aus und liefert das Ergebnis als eine Menge
	# von Tupeln zurück	
	def tableinfo(self, p_table):
		sql = 'describe %s' %(p_table)
		return self.exec(sql)

