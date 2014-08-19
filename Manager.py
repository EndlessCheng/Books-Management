# -*- coding: UTF-8 -*-

import Tkinter
import MySQLdb

class ManagerUI(object):
	
	def __init__(self, top_, manager_):
		
		self.top = top_
		self.manager = manager_
		
		# 弄个列表来管理？
		#注销、标签
		
		self.entryWidth = 40
		
		self.ISBN = Tkinter.StringVar(self.top)
		self.ISBNEntry = Tkinter.Entry(self.top, width = self.entryWidth, textvariable = self.ISBN)
		self.ISBNEntry.pack()
		
		self.bookname = Tkinter.StringVar(self.top)
		self.booknameEntry = Tkinter.Entry(self.top, width = self.entryWidth, textvariable = self.bookname)
		self.booknameEntry.pack()
		
		self.authorname = Tkinter.StringVar(self.top)
		self.authornameEntry = Tkinter.Entry(self.top, width = self.entryWidth, textvariable = self.authorname)
		self.authornameEntry.pack()
		
		self.publisher = Tkinter.StringVar(self.top)
		self.publisherEntry = Tkinter.Entry(self.top, width = self.entryWidth, textvariable = self.publisher)
		self.publisherEntry.pack()
		
		self.publishtime = Tkinter.StringVar(self.top)
		self.publishtimeEntry = Tkinter.Entry(self.top, width = self.entryWidth, textvariable = self.publishtime)
		self.publishtimeEntry.pack()
		
		self.price = Tkinter.StringVar(self.top)
		self.priceEntry = Tkinter.Entry(self.top, width = self.entryWidth, textvariable = self.price)
		self.priceEntry.pack()
		
		self.bfm = Tkinter.Frame(self.top)
		self.addBookButton = Tkinter.Button(self.bfm, text = 'Add', command = self.addBook)
		self.getBookButton = Tkinter.Button(self.bfm, text = 'Get', command = self.getBook)
		self.clearTableButton = Tkinter.Button(self.bfm, text = 'Clear', command = self.clearTable)
		
		self.addBookButton.pack(side = Tkinter.LEFT)
		self.getBookButton.pack(side = Tkinter.LEFT)
		self.clearTableButton.pack(side = Tkinter.LEFT)
		self.bfm.pack()
		
		self.quitButton = Tkinter.Button(self.top, text = 'EXIT', command = self.top.quit)
		self.quitButton.pack()
		
	def addBook(self, ev = None):
		#TODO: 防止 SQL 注入
		try:
			self.manager.query('insert into book values(%s,\'%s\',\'%s\',\'%s\',\'%s\',%s)' % \
			(self.ISBN.get(), \
			self.bookname.get().encode('utf8'), \
			self.authorname.get().encode('utf8'), \
			self.publisher.get().encode('utf8'), \
			self.publishtime.get(), \
			self.price.get()))
			self.manager.commit()
		except MySQLdb.IntegrityError, err:
			#TODO 已经存在此书
			print u'已经存在此书'
	
	def getBook(self, ev = None):
		#TODO: 防止 SQL 注入
		try:
			self.manager.query('select * from book where ISBN = ' + self.ISBN.get())
			res = self.manager.use_result().fetch_row(0)[0]
			self.bookname.set(res[1])
			self.authorname.set(res[2])
			self.publisher.set(res[3])
			self.publishtime.set(res[4])
			self.price.set(res[5])
		except IndexError, err:
			#TODO 未找到该书
			print u'未找到该书'
			
	def clearTable(self, ev = None):
		self.ISBN.set('')
		self.bookname.set('')
		self.authorname.set('')
		self.publisher.set('')
		self.publishtime.set('')
		self.price.set('')
		
def init(top = None, manager = None):
	managerUI = ManagerUI(top, manager)
	Tkinter.mainloop()

if __name__ == '__main__':
	init()