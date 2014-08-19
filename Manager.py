# -*- coding: UTF-8 -*-

import Tkinter, MySQLdb, datetime
from tkintertable.TableModels import TableModel
from tkintertable.Tables import TableCanvas

class ManagerUI(object):
	
	def __init__(self, top_, manager_):
		
		self.top = top_
		self.manager = manager_
		
		self.initComponent()
		self.initTable()
		self.quitButton = Tkinter.Button(self.top, text = '退出', command = self.top.quit)
		self.quitButton.pack()
		
	def initComponent(self, ev = None):
		# 弄个列表来管理？
		# 注销、标签
	
		entryWidth = 40
		
		self.ISBN = Tkinter.StringVar(self.top)
		self.ISBNEntry = Tkinter.Entry(self.top, width = entryWidth, textvariable = self.ISBN)
		self.ISBNEntry.pack()
		
		self.bookname = Tkinter.StringVar(self.top)
		self.booknameEntry = Tkinter.Entry(self.top, width = entryWidth, textvariable = self.bookname)
		self.booknameEntry.pack()
		
		self.authorname = Tkinter.StringVar(self.top)
		self.authornameEntry = Tkinter.Entry(self.top, width = entryWidth, textvariable = self.authorname)
		self.authornameEntry.pack()
		
		self.publisher = Tkinter.StringVar(self.top)
		self.publisherEntry = Tkinter.Entry(self.top, width = entryWidth, textvariable = self.publisher)
		self.publisherEntry.pack()
		
		self.publishtime = Tkinter.StringVar(self.top)
		self.publishtimeEntry = Tkinter.Entry(self.top, width = entryWidth, textvariable = self.publishtime)
		self.publishtimeEntry.pack()
		
		self.price = Tkinter.StringVar(self.top)
		self.priceEntry = Tkinter.Entry(self.top, width = entryWidth, textvariable = self.price)
		self.priceEntry.pack()
		
		self.bfm = Tkinter.Frame(self.top)
		self.addBookButton = Tkinter.Button(self.bfm, text = '添加', command = self.addBook)
		# 可选TODO：撤销刚刚进行的操作
		self.getBookButton = Tkinter.Button(self.bfm, text = '获取', command = self.getBook)
		self.deleteButton = Tkinter.Button(self.bfm, text = '删除', command = self.deleteBook)
		self.clearTableButton = Tkinter.Button(self.bfm, text = '清空文本', command = self.clearTable)
		
		self.addBookButton.pack(side = Tkinter.LEFT)
		self.getBookButton.pack(side = Tkinter.LEFT)
		self.deleteButton.pack(side = Tkinter.LEFT)
		self.clearTableButton.pack(side = Tkinter.LEFT)
		self.bfm.pack()
	
	def initTable(self, ev = None):
		self.tableFrame = Tkinter.Frame(self.top)
		self.tableFrame.pack(expand = True, fill = Tkinter.BOTH) # 后期修改
		self.top.geometry('920x700+200+100')
		
		self.model = TableModel(rows = 0, columns = 0) # like HTML
		self.bookTable = TableCanvas(self.tableFrame, self.model, cellwidth=120, cellbackgr='#e3f698',
                        thefont=('Arial',12), rowheight=22, rowheaderwidth=30, rowselectedcolor='yellow', editable=False) # like CSS
						#改字体
		self.bookTable.createTableFrame()
		
		self.colnames = ('ISBN', 'bookname', 'authorname', 'publisher', 'publishtime', 'price')
		#TODO: 换成中文
		for name in self.colnames:
			self.bookTable.addColumn(name)
		self.bookTable.addRows(1)
		self.bookTable.autoResizeColumns()
		
	def addBook(self, ev = None):
		# TODO: 防止 SQL 注入
		try:
			self.manager.query('insert into book values(%s,\'%s\',\'%s\',\'%s\',\'%s\',%s)' %
			(self.ISBN.get(),
			self.bookname.get().encode('utf8'),
			self.authorname.get().encode('utf8'),
			self.publisher.get().encode('utf8'),
			self.publishtime.get(),
			self.price.get()))
			self.manager.commit()
		except MySQLdb.IntegrityError, err:
			# TODO 已经存在此书
			print u'已经存在此书'
	
	def getBook(self, ev = None):
		# TODO: 防止 SQL 注入
		try:
			self.model.deleteRows()
			self.bookTable.addRows(1)
			self.bookTable.redrawTable()
			
			self.manager.query('select * from book where ISBN = ' + self.ISBN.get())
			res = self.manager.use_result().fetch_row(0)[0]  #第一个0是
			
			for i in range(len(self.colnames)):
				if type(res[i]) == unicode:
					self.model.data[0][self.colnames[i]] = ('' + res[i]).encode('utf8')
				elif type(res[i]) == datetime.date:
					self.model.data[0][self.colnames[i]] = res[i].strftime('%Y-%m-%d') # 小写的 %y 是二位数的年份
				else: # long or float
					self.model.data[0][self.colnames[i]] = str(res[i])
			self.bookTable.autoResizeColumns()
			
		except IndexError, err:
			# TODO 未找到该书
			print u'未找到该书'
	
	def deleteBook(self, ev = None):
		# TODO: 防止 SQL 注入
		self.manager.query('delete from book where ISBN = ' + self.ISBN.get())
		self.manager.commit()
	
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