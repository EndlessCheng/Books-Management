# -*- coding: UTF-8 -*-

import Tkinter
import MySQLdb

class LoginUI(object):

	def __init__(self):
		self.top = Tkinter.Tk()
		
		#TODO: add hint label
		
		self.managerName = Tkinter.StringVar(self.top)
		self.managerNameEntry = Tkinter.Entry(self.top, width = 20, textvariable = self.managerName)
		self.managerNameEntry.pack()
		
		self.password = Tkinter.StringVar(self.top)
		self.passwordEntry = Tkinter.Entry(self.top, width = 20, show = '*', textvariable = self.password)
		self.passwordEntry.bind('<Return>', self.connectMySQL)
		self.passwordEntry.pack()
		
		self.quitButton = Tkinter.Button(self.top, text = 'EXIT', command = self.top.quit)
		self.quitButton.pack()
	
	def connectMySQL(self, ev = None):
		try:
			manager = MySQLdb.connect(user = self.managerName.get(), passwd = self.password.get())
			
			#TODO: 结束当前界面
			#TODO: 建立新的界面
			
			manager.query('create database book_db')
		except MySQLdb.OperationalError, err:
			print 'wrong username or password!'
			#TODO: add label to show username or password error
			
def init():
	loginUI = LoginUI()
	Tkinter.mainloop()
		
if __name__ == '__main__':
	init()
