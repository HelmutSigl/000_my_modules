#!/usr/bin/python3
# ------------------------------
# datei: hs_baseclasses.py
# autor: Helmut Sigl
# datum: 06/11/2021
# ------------------------------

# Imports

# Definitions

class Basic_html_element:

	def __init__(self, p_content = ''):
		self.__content = ''
		if p_content != '':
			self.set(p_content)

	def set(self, p_content):
		if isinstance(p_content, str):
			self.__content = p_content

	def put(self):
		print(self.__content)

class Advanced_html_element:
	
	def __init__(self, p_element = ''):
		self.__all_elements = []
		if p_element != '':
			self.add(p_element)

	def add(self, p_element):
		if isinstance(p_element, str):
			t = Basic_html_element(p_element)
			self.add(t)
		elif isinstance(p_element, Basic_html_element):
			self.__all_elements.append(p_element)
		elif isinstance(p_element, Advanced_html_element):
			self.__all_elements.append(p_element)

	def put(self):
		if self.__all_elements != []:
			for i in self.__all_elements:
				i.put()

class Logbase:

    def __init__(self, p_log_obj):
        self.__lo = p_log_obj

    def set_lo(self, p_log_obj):
        self.__lo = p_log_obj
    
    def log(self, p_message):
        try: self.__lo.log(p_message)
        except: pass
