from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
from tkinter.ttk import Notebook
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย V 1.0 by JOB')
GUI.geometry('600x800+500+50')

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
    expense = v_expense.get() 
    price = v_price.get()
    volume = v_volume.get()

    if expense == '':
        messagebox.showerror('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    if price == '':
        messagebox.showerror('Error','กรุณากรอกราคา')
        return
    if volume == '':
        volume = 1

    try:
        total = int(volume)*int(price)
        #print(' รายการ : {}, ราคา : {} บาท,'.format(expense,price))
        text = ('รายการ : {}\nราคา : {} บาท\nจำนวน : {} ชิ้น\nรวม : {} บาท'.format(expense,price,volume,total))
        v_result.set(text)
        v_expense.set('') 
        v_price.set('')
        v_volume.set('')

        with open('savedata.csv','a',encoding='utf8',newline=('')) as f:
            fw = csv.writer(f) 
            data = [days[today],dt,expense,price,volume,total]
            fw.writerow(data)  
        E1.focus()
        update_table()

    except: # Exception as e ดูว่าผิดพลาดเรื่องอะไร แล้วเก็บไว้ที่ e
        print('error')
        messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
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
read_csv()

L = ttk.Label(tap2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)
header = ['วัน','เวลา','รายการ','ค่าใช้จ่าย','จำนวน','ราคารวม']
resulttable = ttk.Treeview(tap2,columns=header,show='headings',height=20)
resulttable.pack()

# for i in range(len(header)):
    # resulttable.heading(header[i],text=header[i])

for h in header:
    resulttable.heading(h,text=h)

headerwidth = [70,120,150,80,80,80]

for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)

def update_table():
    resulttable.delete(*resulttable.get_children()) #get_children เป็นรหัสพิเศษ ส่วน * เป็นการคล้ายๆ forloop
    #วิธี forloop
    #for c in resulttable.get_children():
    #    resulttable.delete(c)
    data = read_csv()
    for i in data:
        resulttable.insert('','end',value=i)

update_table()

GUI.mainloop()
