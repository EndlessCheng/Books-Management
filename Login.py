# -*- coding: UTF-8 -*-

import Tkinter, MySQLdb, Manager

class LoginUI(object):

	def __init__(self):
		self.top = Tkinter.Tk()
		
		# TODO: add hint label
		
		self.managerName = Tkinter.StringVar(self.top)
		self.managerNameEntry = Tkinter.Entry(self.top, width = 20, textvariable = self.managerName)
		self.managerNameEntry.pack()
		
		self.password = Tkinter.StringVar(self.top)
		self.passwordEntry = Tkinter.Entry(self.top, width = 20, show = '*', textvariable = self.password)
		self.passwordEntry.bind('<Return>', self.connectMySQL)
		self.passwordEntry.pack()
		
		self.quitButton = Tkinter.Button(self.top, text = '退出', command = self.top.quit)
		self.quitButton.pack()
	
		###
		self.managerName.set('root')
		self.password.set('6682431')
		###
	
	def connectMySQL(self, ev = None):
		try:
			manager = MySQLdb.connect(host = 'localhost', user = self.managerName.get(), passwd = self.password.get(), db = 'book_management', charset = 'utf8')
			self.clear()
			Manager.init(self.top, manager)
			self.top.quit() # 别忘了加这句话，要不然 Manager 的 quitButton 要按两次
		except MySQLdb.OperationalError, err:
			print err[0] == 2003
			print type(err)
			# TODO: add label to show username or password error
			#print 'wrong username or password!'

	def clear(self, ev = None):
		self.managerNameEntry.pack_forget()
		self.passwordEntry.pack_forget()
		self.quitButton.pack_forget()
	
def init():
	loginUI = LoginUI()
	Tkinter.mainloop()
		
if __name__ == '__main__':
	init()
