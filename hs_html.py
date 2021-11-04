#!/usr/bin/python3
# ------------------------------
# datei: hs_html.py
# autor: Helmut Sigl
# datum: 04/11/2021
# ------------------------------

# Imports

from hs_logbase import Logbase

# Definitions

class Basic_element:

	def __init__(self, p_content = ''):
		self.__content = ''
		if p_content != '':
			self.set(p_content)

	def set(self, p_content):
		if isinstance(p_content, str):
			self.__content = p_content

	def put(self):
		print(self.__content)

class Advanced_element:
	
	def __init__(self, p_content = ''):
		self.__all_elements = []
		if p_content != '':
			self.add(p_content)

	def add(self, p_element):
		if isinstance(p_element, str):
			t = Basic_element(p_element)
			self.add(t)
		elif isinstance(p_element, Basic_element):
			self.__all_elements.append(p_element)
		elif isinstance(p_element, Advanced_element):
			self.__all_elements.append(p_element)

	def put(self):
		if self.__all_elements != []:
			for i in self.__all_elements:
				i.put()

class Webpage(Advanced_element, Logbase):

	def __init__(self, p_title = 'unbenannt', p_css = ''):
		Advanced_element.__init__(self)
		Logbase.__init__(self)
		self.__title = ''
		self.__all_css = []
		self.set_title(p_title)
		self.add_css(p_css)

	def set_title(self, p_title):
		if isinstance(p_title, str):
			self.__title = p_title

	def add_css(self, p_file):
		if isinstance(p_file, str) and p_file != '':
			self.__all_css.append(p_file)

	def put(self):
		print(self.__put_pagehead())
		Advanced_element.put(self)
		print(self.__put_pageend())

	def __put_pagehead(self):
		ret = 'Content-Type: text/html\n\n'
		ret += '<!DOCTYPE html>\n'
		ret += '<html lang="de">\n'
		ret += '\t<head>\n'
		if self.__all_css != []:
			for i in self.__all_css:
				ret += '\t\t<link rel="stylesheet" href="%s">\n' %(i)
		ret += '\t\t<meta charset="utf-8" />\n'
		ret += '\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
		ret += '\t\t<title>%s</title>\n' %(self.__title)
		ret += '\t</head>\n'
		ret += '\t<body>\n'
		return ret

	def __put_pageend(self):
		ret = '\n\t</body>\n'
		ret += '</html>\n'
		return ret

class Divclass(Advanced_element):
	
	def __init__(self, p_klasse = ''):
		Advanced_element.__init__(self)
		if isinstance(p_klasse, str):
			self.__klasse = p_klasse

	def put(self):
		if self.__klasse != '':
			print ('<div class="%s">' %(self.__klasse))
			Advanced_element.put(self)
			print ('</div>\t<!-- Ende der Klasse *** %s -->' %(self.__klasse))
		else:
			print ('<div>')
			Advanced_element.put(self)
			print ('</div>')

class Webhelper:

	def __init__(self):
		# Definition Abkürzungen und Konstanten
		self.cr = self.br(1)
		self.lf = self.br(2)
		self.new = 0
		self.old = 1
		self.thin = 0
		self.thick = 1

	# Gibt die angegebene Menge <br>-Tags zurück, Default ist 1.
	def br(self, p_anzahl = 1):
		ret = ''
		for x in range(p_anzahl):
			ret += '<br>'
		return ret

	# Gibt einen Link zurück. Dieser Link kann in einem neuen Tab oder im
	# alten Tab geöffnet werden.
	def link(self, p_new, p_wohin, p_text):
		if p_new == self.new: 
			ret = '<a href="%s" target="_blank">%s</a>' %(p_wohin, p_text)
		else:
			ret = '<a href="%s">%s</a>' %(p_wohin, p_text)
		return ret

	# Gibt den übergebenen Text als Überschrift (h1..h6) zurück,
	# Default = h1.
	def hx(self, p_text, p_wert = 1):
		if p_wert not in range(1,7): p_wert = 1
		return '<h%i>%s</h%i>' %(p_wert, p_text, p_wert)

	# Gibt eine horizontale Linie zurück.
	# Diese kann "thin" oder "thick" sein,
	# Default ist "thin".
	def hr(self, p_thickness = 0):
		if p_thickness == self.thin:
			ret = '<hr size="1">'
		else: 
			ret = '<hr>'
		return ret

	# Gibt die angegebene Menge erzwungener Leerzeichen zurück,
	# Default ist 1.
	def lz(p_anzahl = 1):
		ret = ''
		for x in range(p_anzahl):
			ret += '&nbsp;'
		return ret

	# Gibt einen Text mit wählbarer Länge zurück. Default ist 10 Zeichen.
	def lp(self, p_anzahl = 10):
		leprum = """Pellentesque habitant morbi tristique senectus et netus et 
		malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat 
		vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet 
		quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat 
		eleifend leo. Quisque sit amet est et sapien ullamcorper pharetra. 
		Vestibulum erat wisi, condimentum sed, commodo vitae, ornare sit amet, 
		wisi. Aenean fermentum, elit eget tincidunt condimentum, eros ipsum 
		rutrum orci, sagittis tempus lacus enim ac dui. Donec non enim in turpis 
		pulvinar facilisis. Ut felis. Praesent dapibus, neque id cursus faucibus, 
		tortor neque egestas augue, eu vulputate magna eros eu erat. Aliquam erat 
		volutpat. Nam dui mi, tincidunt quis, accumsan porttitor, facilisis 
		luctus, metus wisi. Aenean fermentum, elit eget tincidunt condimentum, 
		eros ipsum Aenean fermentum, elit eget tincidunt condimentum, non enim 
		rutrum orci, sagittis tempus lacus enim ac dui. Donec non enim in turpis 
		pulvinar facilisis. Ut felis. Praesent dapibus, neque id cursus faucibus, 
		tortor neque egestas augue, eu vulputate magna eros eu erat. Aliquam erat 
		volutpat. Nam dui mi, tincidunt quis, accumsan porttitor, facilisis 
		luctus, metus"""
		if p_anzahl > 1221: p_anzahl = 1221
		ret = leprum[0:p_anzahl]
		return ret

	# Gibt eine Tabelle zurück. Folgende Parameter werden verarbeitet:
	# 1. Allgemeine Tabellenüberschrift (Caption) als String: 'bla'
	# 2. Die Spaltenüberschriften als einzelnes Tupel: ('bla', 'blub')
	# 3. Die Daten als Liste von Tupel: ('bla1', 'blub1'), ('bla2', 'blub2')
	# Sollte nur eine Zeile ausgegeben werden gilt folgendes: ('bla', 'blub'),
	# Das gilt auch wenn die Tupel im Script zusammengesetzt werden!
	# Die letzten vier Parameter bestimmen den Rand für Caption, Tabelle, Spaltenüberschrift
	# und Zellen. Standardmäßig wird die Tabelle mit Rändern aber freier Caption erstellt.
	# Benötigt folgende css-Definition als Beispiel:
	# -----------------------------------------------------------
	# caption.mitrand, table.mitrand, th.mitrand, td.mitrand {
	#	border: 2px solid #a1dbd0;
	# }
	# -----------------------------------------------------------
	def tabelle(self, p_caption, p_zellenbeschreibung, p_daten, p_rc = 0, p_rt = 0, p_rth = 1, p_rtd = 1):
		if p_rc == 0: c = '<caption>'
		else: c = '<caption class="mitrand">'
		if p_rt == 0: t = '<table>'
		else: t = '<table class="mitrand">'
		if p_rth == 0: th = '<th>'
		else: th = '<th class="mitrand">'
		if p_rtd == 0: td = '<td>'
		else: td = '<td class="mitrand">'
		res = '\n<!-- ********* Beginn der Tabelle ********* -->\n'
		res += t
		if p_caption != '': res += '\n%s%s</caption>' %(c, p_caption)
		if len(p_zellenbeschreibung) > 0:
			res += '\n<tr>'
			for x in p_zellenbeschreibung:
				res += '\n%s%s</th>' %(th, x)
			res += '\n</tr>'
		for x in p_daten:
			res += '\n<tr>'
			for y in x:
				res += '\n%s%s</td>' %(td, y)
			res += '\n</tr>'
		res += '\n</table>'
		res += '\n<!-- ********** Ende der Tabelle ********** -->\n'
		return res

