from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
from tkinter.ttk import Notebook
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย V 1.0 by JOB')
#GUI.geometry('750x800+500+50')
w = 750
h = 800
ws = GUI.winfo_screenwidth()
hs = GUI.winfo_screenheight()

x = (ws/2)-(w/2)
y = (hs/2)-(h/2)

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')


#---------------------------MENU--------------------------- from tkinter import *
menubar = Menu(GUI)
GUI.config(menu=menubar)

#file menu
filemenu = Menu(menubar,tearoff=0) #tearoff=0 ปิดตัวขีดๆ ลองลบออกละกัน
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')

#helpmenu
def About():
	messagebox.showinfo('เกี่ยวกับเรา','สวัสดีครับ นี่คือโปรแกรมที่พัฒนาโดยจ๊อบ')
helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)

#donatemenu
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
#-------------------------------------------------------------------------------

Alltap = Notebook(GUI)
#tap1 = Frame(Alltap, width=200, height=600)   fix size
#tap2 = Frame(Alltap, width=200, height=600)

tap1 = Frame(Alltap)
tap2 = Frame(Alltap)

icon_tap1 = PhotoImage(file='Addlist.png').subsample(5)
icon_tap2 = PhotoImage(file='List.png').subsample(6)

Alltap.add(tap1, text=f'{"Add Expense":^{20}}', image=icon_tap1, compound='top') #^{20} มีตัวทั้งหมด20 แต่อยู่ตรงกลาง <{20}ชิดซ้าย >{20}ชิดขวา
Alltap.add(tap2, text=f'{"Expense List":^{20}}', image=icon_tap2, compound='top')
Alltap.pack(fill=BOTH,expand=1) #มาจาก star ขยายให้เต็มทั้งสองแนว ยัง งงๆอยู่เหมือนกัน 5555

#----------------------- TAB1 --------------------------

FONT1=(None,20) 
F1 = Frame(tap1)
F1.pack()
#F1.place(x=100,y=20)

days = {'Mon':'จันทร์',
		'Tue':'อังคาร',
		'Wed':'พุธ',
		'Thu':'พฤหัส',
		'Fri':'ศุกร์',
		'Sat':'เสาร์',
		'Sun':'อาทิตย์'}

def Save(event=None):
	today = datetime.now().strftime('%a')
	#print(today)
	dt = datetime.now().strftime('%Y-%m-%d %H:%M')
	transid = datetime.now().strftime('%Y%m%d%H%M%f')
	expense = v_expense.get()

	########## Check Data input ############
	if expense == '':
		messagebox.showerror('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return
	else:
		try:
			price = float(v_price.get())
		except:
			messagebox.showerror('Error','กรุณากรอกราคา')

		try:
			volume = int(v_volume.get())
		except:
			volume = 1
	########################################
	
	#if price == '':
	#	messagebox.showerror('Error','กรุณากรอกราคา')
	#	return
	#if volume == '':
	#	volume = 1

	try:
		total = volume*price
		#print(' รายการ : {}, ราคา : {} บาท,'.format(expense,price))
		text = ('รายการ : {}\nราคา : {} บาท\nจำนวน : {} ชิ้น\nรวม : {} บาท'.format(expense,price,volume,total))
		v_result.set(text)
		v_expense.set('') 
		v_price.set('')
		v_volume.set('')

		with open('savedata.csv','a',encoding='utf8',newline=('')) as f:
			fw = csv.writer(f) 
			data = [transid,days[today],dt,expense,price,volume,total]
			fw.writerow(data)  
		E1.focus()
		update_table()

	except: # Exception as e ดูว่าผิดพลาดเรื่องอะไร แล้วเก็บไว้ที่ e
		#print('error')
		#messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_expense.set('') 
		v_price.set('')
		v_volume.set('')

GUI.bind('<Return>',Save)

mainicon = PhotoImage(file='Book.png').subsample(6)

bookpic = ttk.Label(F1, image=mainicon)
bookpic.pack(pady=20)

L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1) 
L.pack()
v_expense = StringVar() 
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()

L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1)
L.pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1)
L.pack()
v_volume = StringVar()
E3 = ttk.Entry(F1,textvariable=v_volume,font=FONT1)
E3.pack()

saveimage = PhotoImage(file='Save.png').subsample(8)
B1 = ttk.Button(F1,text='Save',image=saveimage,compound='left',command=Save)
B1.pack(ipadx=30,ipady=10,pady=10)

v_result = StringVar()
v_result.set('--------ผลลัพธ์-------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)
#savepic = ttk.Label(B1, image=saveimage)
#savepic.pack(pady=5)

#---------------------- TAB2 -------------------------

def read_csv():
	with open('savedata.csv',newline='',encoding='utf8') as f:
		fr = csv.reader(f)
		data = list(fr)
	return data
		# print(data)
		# for a,b,c,d,e,f in data:
		#    print(a)

L = ttk.Label(tap2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)
header = ['ID','วัน','เวลา','รายการ','ค่าใช้จ่าย','จำนวน','ราคารวม']
resulttable = ttk.Treeview(tap2,columns=header,show='headings',height=20)
resulttable.pack()

# for i in range(len(header)):
	# resulttable.heading(header[i],text=header[i])

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [120,70,120,150,80,80,80]

for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w)

alltransaction = {}

def updateCSV():
	with open('savedata.csv','w',newline='',encoding='utf8') as f: #'w' is replace 'a' is append(stack writer)
		fw = csv.writer(f)
		#prepare data to write (convert dictionary to list)
		data = list(alltransaction.values())
		fw.writerows(data)

def update_table():
	resulttable.delete(*resulttable.get_children()) #get_children เป็นรหัสพิเศษ ส่วน * เป็นการคล้ายๆ forloop
	#วิธี forloop
	#for c in resulttable.get_children():
	#    resulttable.delete(c)
	try:
		data = read_csv()
		for i in data:
			#create dictionary for find data in csv
			#print(i, 'loop', alltransaction)
			alltransaction[i[0]] = i 
			resulttable.insert('','0',value=i) #0 is beginpoint, 'end' is insert at the end point
		#print(alltransaction)
	except:
		print('No File')

def deleterecord(event=None):
	#print('Delete')
	if messagebox.askyesno('Delete Record','Do you want to remove?') == True:
		try:
			select = resulttable.selection()
			data = resulttable.item(select)
			data = data['values']
			deleteid = data[0]
			#print('alltransaction is',alltransaction)
			del alltransaction[str(deleteid)]
			#print(alltransaction)
			updateCSV()
			update_table()
		except:
			messagebox.showerror('Error','Please select your record.')
		

GUI.bind('<Delete>',deleterecord)


BDelete = ttk.Button(tap2,text='Delete',command=deleterecord)
BDelete.place(x=100,y=550)

######################### Rightclick Menu Tab2 ###########################
def Editrecord():
	POPUP = Toplevel() #same as Tk()
	POPUP.title('Edit')
	w = 500
	h = 400
	ws = GUI.winfo_screenwidth()
	hs = GUI.winfo_screenheight()

	x = (ws/2)-(w/2)
	y = (hs/2)-(h/2)

	POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

	def Edit():
		#print(data)
		data[3] = v_expense.get()
		data[4] = float(v_price.get())
		data[5] = int(v_volume.get())
		data[6] = data[4]*data[5]
		#print(alltransaction)
		alltransaction[str(editid)] = data
		#print(alltransaction)
		updateCSV()
		update_table()
		POPUP.destroy()


	select = resulttable.selection()
	data = resulttable.item(select)
	data = data['values']
	editid = data[0]
	#print(data)

	L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1) 
	L.pack()
	v_expense = StringVar() 
	v_expense.set(data[3])
	E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
	E1.pack()

	L = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1)
	L.pack()
	v_price = StringVar()
	v_price.set(data[4])
	E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
	E2.pack()

	L = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=FONT1)
	L.pack()
	v_volume = StringVar()
	v_volume.set(data[5])
	E3 = ttk.Entry(POPUP,textvariable=v_volume,font=FONT1)
	E3.pack()

	saveimage = PhotoImage(file='Save.png').subsample(8)
	B1 = ttk.Button(POPUP,text='Save',image=saveimage,compound='left',command=Edit)
	B1.pack(ipadx=30,ipady=10,pady=10)

	POPUP.mainloop()


rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=Editrecord)
rightclick.add_command(label='Delete',command=deleterecord)

def menupopup(event=None):
	#print(event.x_root, event.y_root) is a location where you right click
	rightclick.post(event.x_root, event.y_root) #show pop-up when you rightclick


resulttable.bind('<Button-3>',menupopup)
##########################################################################

update_table()

GUI.mainloop()
